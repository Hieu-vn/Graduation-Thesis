from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate


def get_accounts(db: Session, user_id: str) -> List[Account]:
    return db.query(Account).filter(Account.user_id == user_id).all()


def get_account(db: Session, account_id: str, user_id: str) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id, Account.user_id == user_id).first()


def create_account(db: Session, user_id: str, data: AccountCreate) -> Account:
    account = Account(
        user_id=user_id,
        name=data.name,
        type=data.type,
        balance=data.balance,
        currency=data.currency,
        institution=data.institution,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(db: Session, account: Account, data: AccountUpdate) -> Account:
    update_data = data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, account: Account) -> None:
    db.delete(account)
    db.commit()


def serialize_account(account: Account) -> AccountOut:
    return AccountOut(
        id=account.id,
        name=account.name,
        type=account.type,
        balance=account.balance,
        currency=account.currency,
        institution=account.institution,
        lastSyncedAt=account.last_synced_at,
        createdAt=account.created_at,
        updatedAt=account.updated_at,
    )
