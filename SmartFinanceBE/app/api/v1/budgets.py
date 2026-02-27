from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate
from app.schemas.common import ApiResponse
from app.services.budget import (
    create_budget,
    delete_budget,
    get_budget,
    get_budgets,
    update_budget,
)

router = APIRouter()


@router.get("", response_model=ApiResponse[List[BudgetOut]])
def list_budgets(
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budgets = get_budgets(db, current_user.id, month, year)
    return ApiResponse(data=budgets)


@router.post("", response_model=ApiResponse[BudgetOut], status_code=status.HTTP_201_CREATED)
def create(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget_db = create_budget(db, current_user.id, data)
    budgets = get_budgets(db, current_user.id, data.month, data.year)
    created = next((b for b in budgets if b.id == budget_db.id), None)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create budget")
    return ApiResponse(data=created)


@router.patch("/{budget_id}", response_model=ApiResponse[BudgetOut])
def update(
    budget_id: str,
    data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = get_budget(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    updated = update_budget(db, budget, data)
    budgets = get_budgets(db, current_user.id, updated.month, updated.year)
    result = next((b for b in budgets if b.id == budget_id), None)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated budget")
    return ApiResponse(data=result)


@router.delete("/{budget_id}", response_model=ApiResponse[dict])
def delete(
    budget_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = get_budget(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    delete_budget(db, budget)
    return ApiResponse(data={"message": "Budget deleted"})
