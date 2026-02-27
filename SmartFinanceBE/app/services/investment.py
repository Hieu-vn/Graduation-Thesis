from typing import List

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.holding import Holding
from app.schemas.holding import HoldingOut, PortfolioOut


def get_holdings(db: Session, user_id: str) -> List[Holding]:
    return (
        db.query(Holding)
        .join(Account, Holding.account_id == Account.id)
        .filter(Account.user_id == user_id)
        .all()
    )


def serialize_holding(h: Holding) -> HoldingOut:
    return HoldingOut(
        id=h.id,
        accountId=h.account_id,
        symbol=h.symbol,
        name=h.name,
        quantity=h.quantity,
        averageCost=h.average_cost,
        currentPrice=h.current_price,
        currency=h.currency,
        updatedAt=h.updated_at,
    )


def get_portfolio(db: Session, user_id: str) -> PortfolioOut:
    holdings = get_holdings(db, user_id)
    total_value = sum(h.quantity * h.current_price for h in holdings)
    total_cost = sum(h.quantity * h.average_cost for h in holdings)
    total_gain = total_value - total_cost
    total_gain_percent = (total_gain / total_cost * 100) if total_cost > 0 else 0.0

    return PortfolioOut(
        totalValue=total_value,
        totalCost=total_cost,
        totalGain=total_gain,
        totalGainPercent=round(total_gain_percent, 2),
        holdings=[serialize_holding(h) for h in holdings],
    )
