"""
Retrieval Service - MySQL Structured Queries + Chroma Semantic Search

Handles:
- Structured queries for financial summaries (spending, income, budgets, balances)
- Semantic search for transaction descriptions
- Data formatting for LLM context
"""
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.services.ai.embeddings import semantic_search as chroma_search

logger = logging.getLogger(__name__)


def get_spending_summary(
    db: Session, user_id: str, start_date: date, end_date: date
) -> Dict[str, Any]:
    """Get spending summary grouped by category for a date range."""
    results = (
        db.query(
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count"),
        )
        .join(Account, Transaction.account_id == Account.id)
        .outerjoin(Category, Transaction.category_id == Category.id)
        .filter(
            Account.user_id == user_id,
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    categories = []
    total_spending = 0
    for row in results:
        cat_name = row.category_name or "Chưa phân loại"
        amount = float(row.total)
        total_spending += amount
        categories.append({
            "category": cat_name,
            "amount": amount,
            "count": int(row.count),
        })

    return {
        "total_spending": total_spending,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "categories": categories,
        "transaction_count": sum(c["count"] for c in categories),
    }


def get_income_summary(
    db: Session, user_id: str, start_date: date, end_date: date
) -> Dict[str, Any]:
    """Get income summary grouped by category for a date range."""
    results = (
        db.query(
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count"),
        )
        .join(Account, Transaction.account_id == Account.id)
        .outerjoin(Category, Transaction.category_id == Category.id)
        .filter(
            Account.user_id == user_id,
            Transaction.type == "income",
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    categories = []
    total_income = 0
    for row in results:
        cat_name = row.category_name or "Chưa phân loại"
        amount = float(row.total)
        total_income += amount
        categories.append({
            "category": cat_name,
            "amount": amount,
            "count": int(row.count),
        })

    return {
        "total_income": total_income,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "categories": categories,
    }


def get_budget_status(
    db: Session, user_id: str, month: int, year: int
) -> List[Dict[str, Any]]:
    """Get budget vs actual spending for a given month."""
    budgets = (
        db.query(Budget, Category.name.label("category_name"))
        .join(Category, Budget.category_id == Category.id)
        .filter(
            Budget.user_id == user_id,
            Budget.month == month,
            Budget.year == year,
        )
        .all()
    )

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    result = []
    for budget, cat_name in budgets:
        actual = (
            db.query(func.sum(Transaction.amount))
            .join(Account, Transaction.account_id == Account.id)
            .filter(
                Account.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.type == "expense",
                Transaction.date >= start_date,
                Transaction.date <= end_date,
            )
            .scalar()
        ) or 0

        result.append({
            "category": cat_name,
            "budget_amount": float(budget.amount),
            "actual_spending": float(actual),
            "remaining": float(budget.amount) - float(actual),
            "usage_percent": round(float(actual) / float(budget.amount) * 100, 1) if budget.amount > 0 else 0,
        })

    return result


def get_account_balances(db: Session, user_id: str) -> List[Dict[str, Any]]:
    """Get all account balances for a user."""
    accounts = (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .all()
    )

    return [
        {
            "name": acc.name,
            "type": acc.type,
            "balance": float(acc.balance),
            "currency": acc.currency,
        }
        for acc in accounts
    ]


def get_recent_transactions(
    db: Session, user_id: str, limit: int = 20
) -> List[Dict[str, Any]]:
    """Get the most recent transactions."""
    transactions = (
        db.query(Transaction, Category.name.label("category_name"))
        .join(Account, Transaction.account_id == Account.id)
        .outerjoin(Category, Transaction.category_id == Category.id)
        .filter(Account.user_id == user_id)
        .order_by(Transaction.date.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "description": t.description,
            "amount": float(t.amount),
            "type": t.type,
            "category": cat_name or "Chưa phân loại",
            "date": str(t.date),
            "currency": t.currency,
            "notes": t.notes,
        }
        for t, cat_name in transactions
    ]


def get_spending_comparison(
    db: Session, user_id: str, current_start: date, current_end: date,
    previous_start: date, previous_end: date
) -> Dict[str, Any]:
    """Compare spending between two periods."""
    current = get_spending_summary(db, user_id, current_start, current_end)
    previous = get_spending_summary(db, user_id, previous_start, previous_end)

    current_by_cat = {c["category"]: c["amount"] for c in current["categories"]}
    previous_by_cat = {c["category"]: c["amount"] for c in previous["categories"]}

    all_categories = set(current_by_cat.keys()) | set(previous_by_cat.keys())

    comparison = []
    for cat in all_categories:
        cur = current_by_cat.get(cat, 0)
        prev = previous_by_cat.get(cat, 0)
        change_pct = ((cur - prev) / prev * 100) if prev > 0 else (100 if cur > 0 else 0)
        comparison.append({
            "category": cat,
            "current_amount": cur,
            "previous_amount": prev,
            "change_amount": cur - prev,
            "change_percent": round(change_pct, 1),
        })

    comparison.sort(key=lambda x: abs(x["change_percent"]), reverse=True)

    total_change = current["total_spending"] - previous["total_spending"]
    total_change_pct = (
        (total_change / previous["total_spending"] * 100)
        if previous["total_spending"] > 0
        else 0
    )

    return {
        "current_period": {"start": str(current_start), "end": str(current_end), "total": current["total_spending"]},
        "previous_period": {"start": str(previous_start), "end": str(previous_end), "total": previous["total_spending"]},
        "total_change": total_change,
        "total_change_percent": round(total_change_pct, 1),
        "by_category": comparison,
    }


def retrieve_context(
    db: Session, user_id: str, intent: str, entities: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main retrieval function - fetches relevant financial data based on intent.

    Args:
        db: Database session
        user_id: User ID
        intent: One of 'lookup' (FR25), 'trend' (FR26), 'advice' (FR27)
        entities: Extracted entities (dates, categories, etc.)

    Returns:
        Dict of financial context data
    """
    today = date.today()
    start_date = entities.get("start_date", today.replace(day=1))
    end_date = entities.get("end_date", today)

    context = {}

    if intent == "lookup":
        # FR25: Basic information lookup
        context["spending"] = get_spending_summary(db, user_id, start_date, end_date)
        context["income"] = get_income_summary(db, user_id, start_date, end_date)
        context["balances"] = get_account_balances(db, user_id)
        context["recent_transactions"] = get_recent_transactions(db, user_id, limit=10)

    elif intent == "trend":
        # FR26: Trend analysis - compare current vs previous period
        delta = end_date - start_date
        previous_end = start_date - timedelta(days=1)
        previous_start = previous_end - delta

        context["comparison"] = get_spending_comparison(
            db, user_id, start_date, end_date, previous_start, previous_end
        )
        context["current_spending"] = get_spending_summary(db, user_id, start_date, end_date)

    elif intent == "advice":
        # FR27: Financial advice - comprehensive data
        context["spending"] = get_spending_summary(db, user_id, start_date, end_date)
        context["income"] = get_income_summary(db, user_id, start_date, end_date)
        context["balances"] = get_account_balances(db, user_id)
        context["budgets"] = get_budget_status(db, user_id, today.month, today.year)
        context["recent_transactions"] = get_recent_transactions(db, user_id, limit=30)

        # Also get previous month for comparison
        prev_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        prev_month_end = today.replace(day=1) - timedelta(days=1)
        context["previous_spending"] = get_spending_summary(
            db, user_id, prev_month_start, prev_month_end
        )

    else:
        # Default: general lookup
        context["spending"] = get_spending_summary(db, user_id, start_date, end_date)
        context["balances"] = get_account_balances(db, user_id)

    # Always include semantic search if there's a query
    query = entities.get("query", "")
    if query:
        context["semantic_matches"] = chroma_search(user_id, query, top_k=5)

    return context
