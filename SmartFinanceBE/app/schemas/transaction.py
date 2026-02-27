from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

TransactionType = Literal["income", "expense", "transfer"]


class TransactionCreate(BaseModel):
    accountId: str
    categoryId: Optional[str] = None
    type: TransactionType
    amount: float
    currency: str = "VND"
    description: str
    date: date
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class TransactionUpdate(BaseModel):
    accountId: Optional[str] = None
    categoryId: Optional[str] = None
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class TransactionOut(BaseModel):
    id: str
    accountId: str
    categoryId: Optional[str] = None
    type: str
    amount: float
    currency: str
    description: str
    date: date
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "account_id"):
            data = {
                "id": obj.id,
                "accountId": obj.account_id,
                "categoryId": obj.category_id,
                "type": obj.type,
                "amount": obj.amount,
                "currency": obj.currency,
                "description": obj.description,
                "date": obj.date,
                "notes": obj.notes,
                "tags": obj.tags,
                "createdAt": obj.created_at,
                "updatedAt": obj.updated_at,
            }
            return cls(**data)
        return super().model_validate(obj, **kwargs)


class TransactionFilter(BaseModel):
    accountId: Optional[str] = None
    categoryId: Optional[str] = None
    type: Optional[TransactionType] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    minAmount: Optional[float] = None
    maxAmount: Optional[float] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20
