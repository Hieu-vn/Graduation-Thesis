from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    email: str
    name: str

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    user: UserOut
    token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class GoogleCallbackRequest(BaseModel):
    code: str


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOtpRequest(BaseModel):
    email: EmailStr
