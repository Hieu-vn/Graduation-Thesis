from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BudgetCreate(BaseModel):
    categoryId: str
    amount: float
    currency: str = "VND"
    month: int
    year: int


class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None


class BudgetOut(BaseModel):
    id: str
    categoryId: str
    categoryName: str
    amount: float
    spent: float
    currency: str
    month: int
    year: int
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}
