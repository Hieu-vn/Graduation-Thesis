"""
AI Chat API Endpoints

All endpoints require X-API-Key header (service-to-service auth).
User authentication is handled by SmartFinanceBE, which passes user_id.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas import (
    ChatHistoryOut,
    ChatRequest,
    ChatResponse,
    ChatSessionOut,
    EmbeddingSyncRequest,
)
from app.services import chat as chat_service
from app.services.ai.llm import check_ollama_status
from app.services.ai.embeddings import embed_transactions
from app.models import Account, Transaction

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def send_message(
    body: ChatRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Process a chat message through the RAG pipeline."""
    try:
        result = chat_service.process_chat(
            db=db,
            user_id=body.user_id,
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


@router.get("/chat/sessions/{user_id}", response_model=list[ChatSessionOut])
def list_sessions(
    user_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get all chat sessions for a user."""
    sessions = chat_service.get_chat_sessions(db, user_id)
    return [ChatSessionOut(**s) for s in sessions]


@router.get("/chat/sessions/{user_id}/{session_id}", response_model=list[ChatHistoryOut])
def get_session(
    user_id: str,
    session_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Get the full message history of a chat session."""
    messages = chat_service.get_session_history(db, user_id, session_id)
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phiên hội thoại không tồn tại",
        )
    return [ChatHistoryOut.model_validate(m) for m in messages]


@router.delete("/chat/sessions/{user_id}/{session_id}")
def delete_session(
    user_id: str,
    session_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Delete a chat session and all its messages."""
    count = chat_service.delete_session(db, user_id, session_id)
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phiên hội thoại không tồn tại",
        )
    return {"message": f"Đã xóa {count} tin nhắn", "deleted_count": count}


@router.post("/embeddings/sync")
def sync_embeddings(
    body: EmbeddingSyncRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Manually sync transaction embeddings for a user."""
    from app.core.config import settings

    transactions = (
        db.query(Transaction)
        .join(Account, Transaction.account_id == Account.id)
        .filter(Account.user_id == body.user_id)
        .limit(settings.AI_MAX_CONTEXT_TRANSACTIONS)
        .all()
    )

    count = embed_transactions(body.user_id, transactions)
    return {"message": f"Đã đồng bộ {count} giao dịch", "count": count}


@router.get("/health")
async def ai_health():
    """Check the health status of the AI service."""
    ollama_status = await check_ollama_status()
    return {
        "service": "SmartFinanceAI",
        "status": "ok",
        "ollama": ollama_status,
    }
