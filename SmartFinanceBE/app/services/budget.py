from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate


def get_budgets(
    db: Session, user_id: str, month: Optional[int] = None, year: Optional[int] = None
) -> List[BudgetOut]:
    query = db.query(Budget).filter(Budget.user_id == user_id)
    if month:
        query = query.filter(Budget.month == month)
    if year:
        query = query.filter(Budget.year == year)
    budgets = query.all()

    result = []
    for budget in budgets:
        spent = _get_spent_amount(db, user_id, budget.category_id, budget.month, budget.year)
        category = db.query(Category).filter(Category.id == budget.category_id).first()
        result.append(
            BudgetOut(
                id=budget.id,
                categoryId=budget.category_id,
                categoryName=category.name if category else "",
                amount=budget.amount,
                spent=spent,
                currency=budget.currency,
                month=budget.month,
                year=budget.year,
                createdAt=budget.created_at,
                updatedAt=budget.updated_at,
            )
        )
    return result


def _get_spent_amount(
    db: Session, user_id: str, category_id: str, month: int, year: int
) -> float:
    from datetime import date
    start = date(year, month, 1)
    import calendar
    last_day = calendar.monthrange(year, month)[1]
    end = date(year, month, last_day)

    result = (
        db.query(func.sum(Transaction.amount))
        .join(Account, Transaction.account_id == Account.id)
        .filter(
            Account.user_id == user_id,
            Transaction.category_id == category_id,
            Transaction.type == "expense",
            Transaction.date >= start,
            Transaction.date <= end,
        )
        .scalar()
    )
    return float(result or 0)


def get_budget(db: Session, budget_id: str, user_id: str) -> Optional[Budget]:
    return db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()


def create_budget(db: Session, user_id: str, data: BudgetCreate) -> Budget:
    budget = Budget(
        user_id=user_id,
        category_id=data.categoryId,
        amount=data.amount,
        currency=data.currency,
        month=data.month,
        year=data.year,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget: Budget, data: BudgetUpdate) -> Budget:
    if data.amount is not None:
        budget.amount = data.amount
    if data.currency is not None:
        budget.currency = data.currency
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget: Budget) -> None:
    db.delete(budget)
    db.commit()
