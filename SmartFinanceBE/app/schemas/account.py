from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

AccountType = Literal[
    "checking", "savings", "credit_card", "investment", "loan", "cash", "crypto", "other"
]


class AccountCreate(BaseModel):
    name: str
    type: AccountType
    balance: float = 0.0
    currency: str = "VND"
    institution: Optional[str] = None


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[float] = None
    currency: Optional[str] = None
    institution: Optional[str] = None


class AccountOut(BaseModel):
    id: str
    name: str
    type: str
    balance: float
    currency: str
    institution: Optional[str] = None
    lastSyncedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "__dict__"):
            data = {
                "id": obj.id,
                "name": obj.name,
                "type": obj.type,
                "balance": obj.balance,
                "currency": obj.currency,
                "institution": obj.institution,
                "lastSyncedAt": obj.last_synced_at,
                "createdAt": obj.created_at,
                "updatedAt": obj.updated_at,
            }
            return cls(**data)
        return super().model_validate(obj, **kwargs)
