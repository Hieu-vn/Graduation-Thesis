from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate
from app.schemas.common import ApiResponse
from app.services.account import (
    create_account,
    delete_account,
    get_account,
    get_accounts,
    serialize_account,
    update_account,
)

router = APIRouter()


@router.get("", response_model=ApiResponse[List[AccountOut]])
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    accounts = get_accounts(db, current_user.id)
    return ApiResponse(data=[serialize_account(a) for a in accounts])


@router.post("", response_model=ApiResponse[AccountOut], status_code=status.HTTP_201_CREATED)
def create(
    data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = create_account(db, current_user.id, data)
    return ApiResponse(data=serialize_account(account))


@router.get("/{account_id}", response_model=ApiResponse[AccountOut])
def get_one(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return ApiResponse(data=serialize_account(account))


@router.patch("/{account_id}", response_model=ApiResponse[AccountOut])
def update(
    account_id: str,
    data: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    account = update_account(db, account, data)
    return ApiResponse(data=serialize_account(account))


@router.delete("/{account_id}", response_model=ApiResponse[dict])
def delete(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    delete_account(db, account)
    return ApiResponse(data={"message": "Account deleted"})
