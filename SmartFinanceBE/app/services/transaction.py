from typing import List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCreate,
    TransactionFilter,
    TransactionOut,
    TransactionUpdate,
)


def get_transactions(
    db: Session, user_id: str, filters: TransactionFilter
) -> Tuple[List[Transaction], int]:
    query = (
        db.query(Transaction)
        .join(Account, Transaction.account_id == Account.id)
        .filter(Account.user_id == user_id)
    )

    if filters.accountId:
        query = query.filter(Transaction.account_id == filters.accountId)
    if filters.categoryId:
        query = query.filter(Transaction.category_id == filters.categoryId)
    if filters.type:
        query = query.filter(Transaction.type == filters.type)
    if filters.startDate:
        query = query.filter(Transaction.date >= filters.startDate)
    if filters.endDate:
        query = query.filter(Transaction.date <= filters.endDate)
    if filters.minAmount is not None:
        query = query.filter(Transaction.amount >= filters.minAmount)
    if filters.maxAmount is not None:
        query = query.filter(Transaction.amount <= filters.maxAmount)
    if filters.search:
        query = query.filter(Transaction.description.ilike(f"%{filters.search}%"))

    total = query.count()
    offset = (filters.page - 1) * filters.limit
    transactions = query.order_by(Transaction.date.desc()).offset(offset).limit(filters.limit).all()
    return transactions, total


def get_transaction(db: Session, transaction_id: str, user_id: str) -> Optional[Transaction]:
    return (
        db.query(Transaction)
        .join(Account, Transaction.account_id == Account.id)
        .filter(Transaction.id == transaction_id, Account.user_id == user_id)
        .first()
    )


def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
    transaction = Transaction(
        account_id=data.accountId,
        category_id=data.categoryId,
        type=data.type,
        amount=data.amount,
        currency=data.currency,
        description=data.description,
        date=data.date,
        notes=data.notes,
        tags=data.tags,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def update_transaction(db: Session, transaction: Transaction, data: TransactionUpdate) -> Transaction:
    update_data = data.model_dump(exclude_none=True)
    field_map = {
        "accountId": "account_id",
        "categoryId": "category_id",
    }
    for field, value in update_data.items():
        db_field = field_map.get(field, field)
        setattr(transaction, db_field, value)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction) -> None:
    db.delete(transaction)
    db.commit()


def serialize_transaction(t: Transaction) -> TransactionOut:
    return TransactionOut(
        id=t.id,
        accountId=t.account_id,
        categoryId=t.category_id,
        type=t.type,
        amount=t.amount,
        currency=t.currency,
        description=t.description,
        date=t.date,
        notes=t.notes,
        tags=t.tags,
        createdAt=t.created_at,
        updatedAt=t.updated_at,
    )
