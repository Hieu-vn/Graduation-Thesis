from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    session_id: str
    intent: Optional[str] = None


class ChatHistoryOut(BaseModel):
    id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "created_at"):
            return cls(
                id=obj.id,
                role=obj.role,
                content=obj.content,
                created_at=obj.created_at,
            )
        return super().model_validate(obj, **kwargs)


class ChatSessionOut(BaseModel):
    session_id: str
    title: Optional[str] = None
    created_at: datetime
    message_count: int
