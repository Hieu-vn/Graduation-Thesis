from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import PasswordChange, UserOut, UserUpdate
from app.services.user import change_password, update_user

router = APIRouter()


@router.get("/me", response_model=ApiResponse[UserOut])
def get_me(current_user: User = Depends(get_current_user)):
    return ApiResponse(data=UserOut.model_validate(current_user))


@router.patch("/me", response_model=ApiResponse[UserOut])
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = update_user(db, current_user, data)
    return ApiResponse(data=UserOut.model_validate(user))


@router.patch("/me/password", response_model=ApiResponse[dict])
def update_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = change_password(db, current_user, data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    return ApiResponse(data={"message": "Password updated successfully"})
