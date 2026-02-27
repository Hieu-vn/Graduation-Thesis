from datetime import datetime

from pydantic import BaseModel


class HoldingOut(BaseModel):
    id: str
    accountId: str
    symbol: str
    name: str
    quantity: float
    averageCost: float
    currentPrice: float
    currency: str
    updatedAt: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "account_id"):
            data = {
                "id": obj.id,
                "accountId": obj.account_id,
                "symbol": obj.symbol,
                "name": obj.name,
                "quantity": obj.quantity,
                "averageCost": obj.average_cost,
                "currentPrice": obj.current_price,
                "currency": obj.currency,
                "updatedAt": obj.updated_at,
            }
            return cls(**data)
        return super().model_validate(obj, **kwargs)


class PortfolioOut(BaseModel):
    totalValue: float
    totalCost: float
    totalGain: float
    totalGainPercent: float
    holdings: list[HoldingOut]
