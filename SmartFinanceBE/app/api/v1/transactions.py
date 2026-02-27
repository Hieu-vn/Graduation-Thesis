import math
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.transaction import (
    TransactionCreate,
    TransactionFilter,
    TransactionOut,
    TransactionUpdate,
)
from app.services.transaction import (
    create_transaction,
    delete_transaction,
    get_transaction,
    get_transactions,
    serialize_transaction,
    update_transaction,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[TransactionOut])
def list_transactions(
    accountId: Optional[str] = Query(None),
    categoryId: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    startDate: Optional[date] = Query(None),
    endDate: Optional[date] = Query(None),
    minAmount: Optional[float] = Query(None),
    maxAmount: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filters = TransactionFilter(
        accountId=accountId,
        categoryId=categoryId,
        type=type,
        startDate=startDate,
        endDate=endDate,
        minAmount=minAmount,
        maxAmount=maxAmount,
        search=search,
        page=page,
        limit=limit,
    )
    transactions, total = get_transactions(db, current_user.id, filters)
    total_pages = math.ceil(total / limit) if limit > 0 else 1
    return PaginatedResponse(
        data=[serialize_transaction(t) for t in transactions],
        total=total,
        page=page,
        limit=limit,
        totalPages=total_pages,
    )


@router.post("", response_model=ApiResponse[TransactionOut], status_code=status.HTTP_201_CREATED)
def create(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = create_transaction(db, data)
    return ApiResponse(data=serialize_transaction(transaction))


@router.get("/{transaction_id}", response_model=ApiResponse[TransactionOut])
def get_one(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return ApiResponse(data=serialize_transaction(transaction))


@router.patch("/{transaction_id}", response_model=ApiResponse[TransactionOut])
def update(
    transaction_id: str,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    transaction = update_transaction(db, transaction, data)
    return ApiResponse(data=serialize_transaction(transaction))


@router.delete("/{transaction_id}", response_model=ApiResponse[dict])
def delete(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    delete_transaction(db, transaction)
    return ApiResponse(data={"message": "Transaction deleted"})
