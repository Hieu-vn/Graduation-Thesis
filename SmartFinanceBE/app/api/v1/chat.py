"""
Chat API Endpoints

POST /api/chat              - Send a message, get AI response
GET  /api/chat/sessions     - List all chat sessions
GET  /api/chat/sessions/:id - Get session history
DELETE /api/chat/sessions/:id - Delete a session
GET  /api/chat/health       - Check Ollama status
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatHistoryOut,
    ChatRequest,
    ChatResponse,
    ChatSessionOut,
)
from app.services import chat as chat_service
from app.services.ai.llm import check_ollama_status

router = APIRouter()


@router.post("", response_model=ChatResponse)
def send_message(
    body: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Send a message to the AI chatbot and receive a response."""
    try:
        result = chat_service.process_chat(
            db=db,
            user_id=current_user.id,
            message=body.message,
            session_id=body.session_id,
        )
        return ChatResponse(**result)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xử lý chat: {str(e)}",
        )


@router.get("/sessions", response_model=list[ChatSessionOut])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all chat sessions for the current user."""
    sessions = chat_service.get_chat_sessions(db, current_user.id)
    return [ChatSessionOut(**s) for s in sessions]


@router.get("/sessions/{session_id}", response_model=list[ChatHistoryOut])
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the full message history of a chat session."""
    messages = chat_service.get_session_history(db, current_user.id, session_id)
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phiên hội thoại không tồn tại",
        )
    return [ChatHistoryOut.model_validate(m) for m in messages]


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a chat session and all its messages."""
    count = chat_service.delete_session(db, current_user.id, session_id)
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phiên hội thoại không tồn tại",
        )
    return {"message": f"Đã xóa {count} tin nhắn", "deleted_count": count}


@router.get("/health")
async def ai_health():
    """Check the health status of the AI service (Ollama)."""
    status_info = await check_ollama_status()
    return status_info
