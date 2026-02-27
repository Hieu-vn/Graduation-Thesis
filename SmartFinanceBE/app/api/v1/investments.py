from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.holding import HoldingOut, PortfolioOut
from app.services.investment import get_holdings, get_portfolio, serialize_holding

router = APIRouter()


@router.get("/portfolio", response_model=ApiResponse[PortfolioOut])
def portfolio(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = get_portfolio(db, current_user.id)
    return ApiResponse(data=result)


@router.get("/holdings", response_model=ApiResponse[List[HoldingOut]])
def holdings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    holdings_list = get_holdings(db, current_user.id)
    return ApiResponse(data=[serialize_holding(h) for h in holdings_list])
