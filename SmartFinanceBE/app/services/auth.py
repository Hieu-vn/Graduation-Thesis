import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.otp_verification import OtpVerification
from app.models.user import User
from app.schemas.auth import RegisterRequest


def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=6))


def create_pending_registration(db: Session, data: RegisterRequest) -> OtpVerification:
    # Invalidate any existing pending OTPs for this email
    db.query(OtpVerification).filter(
        OtpVerification.email == data.email,
        OtpVerification.is_used == False,  # noqa: E712
    ).update({"is_used": True})

    hashed = get_password_hash(data.password)
    otp_code = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=2)

    pending = OtpVerification(
        email=data.email,
        name=data.name,
        hashed_password=hashed,
        otp_code=otp_code,
        expires_at=expires_at,
    )
    db.add(pending)
    db.commit()
    db.refresh(pending)
    return pending


def verify_otp_and_register(db: Session, email: str, otp: str) -> User:
    from fastapi import HTTPException, status

    pending = (
        db.query(OtpVerification)
        .filter(
            OtpVerification.email == email,
            OtpVerification.is_used == False,  # noqa: E712
        )
        .order_by(OtpVerification.created_at.desc())
        .first()
    )

    if not pending:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found")

    now = datetime.now(timezone.utc)
    expires_at = pending.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now > expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    if pending.otp_code != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    pending.is_used = True
    db.commit()

    user = User(email=pending.email, name=pending.name, hashed_password=pending.hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def resend_otp(db: Session, email: str) -> OtpVerification:
    from fastapi import HTTPException, status

    existing = (
        db.query(OtpVerification)
        .filter(
            OtpVerification.email == email,
            OtpVerification.is_used == False,  # noqa: E712
        )
        .first()
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending registration found for this email",
        )

    # Invalidate all old OTPs
    db.query(OtpVerification).filter(
        OtpVerification.email == email,
        OtpVerification.is_used == False,  # noqa: E712
    ).update({"is_used": True})

    otp_code = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=2)

    pending = OtpVerification(
        email=existing.email,
        name=existing.name,
        hashed_password=existing.hashed_password,
        otp_code=otp_code,
        expires_at=expires_at,
    )
    db.add(pending)
    db.commit()
    db.refresh(pending)
    return pending


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def register_user(db: Session, data: RegisterRequest) -> User:
    hashed = get_password_hash(data.password)
    user = User(email=data.email, name=data.name, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_tokens(user_id: str) -> dict:
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
    }


async def get_google_user_info(code: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return None

        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return user_resp.json()


def get_or_create_google_user(db: Session, google_data: dict) -> User:
    user = db.query(User).filter(User.google_id == google_data["id"]).first()
    if user:
        return user
    user = get_user_by_email(db, google_data["email"])
    if user:
        user.google_id = google_data["id"]
        db.commit()
        db.refresh(user)
        return user
    user = User(
        email=google_data["email"],
        name=google_data.get("name", google_data["email"]),
        google_id=google_data["id"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
