from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import decode_token
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResendOtpRequest,
    UserOut,
    VerifyOtpRequest,
)
from app.schemas.common import ApiResponse
from app.services.auth import (
    authenticate_user,
    create_pending_registration,
    create_tokens,
    get_or_create_google_user,
    get_google_user_info,
    get_user_by_email,
    get_user_by_id,
    resend_otp,
    verify_otp_and_register,
)
from app.services.email import send_otp_email

router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


@router.post("/register")
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    pending = create_pending_registration(db, data)
    await send_otp_email(pending.email, pending.name, pending.otp_code)
    return ApiResponse(data=None, message="OTP sent to your email. Please verify to complete registration.")


@router.post("/verify-otp", response_model=ApiResponse[AuthResponse])
def verify_otp(data: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = verify_otp_and_register(db, data.email, data.otp)
    tokens = create_tokens(user.id)
    return ApiResponse(
        data=AuthResponse(user=UserOut.model_validate(user), token=tokens["access_token"])
    )


@router.post("/resend-otp")
async def resend_otp_endpoint(data: ResendOtpRequest, db: Session = Depends(get_db)):
    pending = resend_otp(db, data.email)
    await send_otp_email(pending.email, pending.name, pending.otp_code)
    return ApiResponse(data=None, message="New OTP sent to your email.")


@router.post("/login", response_model=ApiResponse[AuthResponse])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    tokens = create_tokens(user.id)
    return ApiResponse(
        data=AuthResponse(user=UserOut.model_validate(user), token=tokens["access_token"])
    )


@router.post("/refresh", response_model=ApiResponse[AuthResponse])
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    user_id = decode_token(data.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    tokens = create_tokens(user.id)
    return ApiResponse(
        data=AuthResponse(user=UserOut.model_validate(user), token=tokens["access_token"])
    )


@router.get("/google")
def google_login():
    """Redirect user to Google OAuth consent page."""
    params = urlencode({
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    })
    return RedirectResponse(url=f"{GOOGLE_AUTH_URL}?{params}")


@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    db: Session = Depends(get_db),
):
    """Handle Google OAuth callback, create JWT and redirect to FE."""
    google_data = await get_google_user_info(code)
    if not google_data or "id" not in google_data:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error=google_auth_failed"
        )
    user = get_or_create_google_user(db, google_data)
    tokens = create_tokens(user.id)
    token = tokens["access_token"]
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/auth/callback?token={token}"
    )
