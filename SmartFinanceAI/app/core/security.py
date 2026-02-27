"""
API Security - Service-to-Service Authentication

SmartFinanceBE authenticates users via JWT.
SmartFinanceBE calls SmartFinanceAI with X-API-Key header.
AI service trusts the user_id passed by the backend.
"""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the service-to-service API key."""
    if not api_key or api_key != settings.AI_SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key
