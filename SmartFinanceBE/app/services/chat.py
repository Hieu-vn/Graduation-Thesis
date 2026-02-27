"""
Chat Service - Conversation management + RAG pipeline orchestration

Handles:
- Session management (create, list, get history, delete)
- Message persistence (save user + assistant messages)
- Coordinating the RAG pipeline for each user message
- Syncing transaction embeddings before querying
"""
import logging
import uuid
from typing import Dict, List, Optional, Tuple, Any

from sqlalchemy import func, distinct
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.account import Account
from app.models.chat_history import ChatHistory
from app.models.transaction import Transaction
from app.services.ai.embeddings import embed_transactions
from app.services.ai.pipeline import process_query

logger = logging.getLogger(__name__)


def _sync_embeddings(db: Session, user_id: str) -> None:
    """Sync user's transaction descriptions to Chroma (if needed)."""
    try:
        transactions = (
            db.query(Transaction)
            .join(Account, Transaction.account_id == Account.id)
            .filter(Account.user_id == user_id)
            .limit(settings.AI_MAX_CONTEXT_TRANSACTIONS)
            .all()
        )
        if transactions:
            embed_transactions(user_id, transactions)
    except Exception as e:
        logger.warning(f"Failed to sync embeddings for user {user_id}: {e}")


def _get_conversation_history(
    db: Session, user_id: str, session_id: str
) -> List[dict]:
    """Get conversation history for a session, limited to memory size."""
    messages = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id,
        )
        .order_by(ChatHistory.created_at.desc())
        .limit(settings.AI_CONVERSATION_MEMORY_SIZE * 2)  # user + assistant pairs
        .all()
    )

    # Reverse to chronological order
    messages.reverse()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def save_message(
    db: Session,
    user_id: str,
    session_id: str,
    role: str,
    content: str,
    metadata_json: Optional[dict] = None,
) -> ChatHistory:
    """Save a chat message to the database."""
    msg = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        role=role,
        content=content,
        metadata_json=metadata_json,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def process_chat(
    db: Session, user_id: str, message: str, session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main chat processing function.

    1. Create/reuse session
    2. Sync embeddings
    3. Get conversation history
    4. Save user message
    5. Run RAG pipeline
    6. Save assistant response
    7. Return result
    """
    # Create new session if needed
    if not session_id:
        session_id = str(uuid.uuid4())

    # Sync embeddings (background-ish, won't block if fails)
    _sync_embeddings(db, user_id)

    # Get conversation history for context
    history = _get_conversation_history(db, user_id, session_id)

    # Save user message
    save_message(db, user_id, session_id, "user", message)

    # Run RAG pipeline
    result = process_query(db, user_id, message, history)

    # Save assistant response
    save_message(
        db, user_id, session_id, "assistant", result["response"],
        metadata_json=result.get("metadata"),
    )

    return {
        "message": result["response"],
        "session_id": session_id,
        "intent": result.get("intent"),
    }


def get_chat_sessions(db: Session, user_id: str) -> List[dict]:
    """Get all chat sessions for a user."""
    sessions = (
        db.query(
            ChatHistory.session_id,
            func.min(ChatHistory.created_at).label("created_at"),
            func.count(ChatHistory.id).label("message_count"),
        )
        .filter(ChatHistory.user_id == user_id)
        .group_by(ChatHistory.session_id)
        .order_by(func.max(ChatHistory.created_at).desc())
        .all()
    )

    result = []
    for s in sessions:
        # Get the first user message as the session title
        first_msg = (
            db.query(ChatHistory.content)
            .filter(
                ChatHistory.session_id == s.session_id,
                ChatHistory.role == "user",
            )
            .order_by(ChatHistory.created_at.asc())
            .first()
        )

        title = first_msg.content[:80] if first_msg else "Cuộc trò chuyện mới"

        result.append({
            "session_id": s.session_id,
            "title": title,
            "created_at": s.created_at,
            "message_count": s.message_count,
        })

    return result


def get_session_history(
    db: Session, user_id: str, session_id: str
) -> List[ChatHistory]:
    """Get all messages in a session."""
    return (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id,
        )
        .order_by(ChatHistory.created_at.asc())
        .all()
    )


def delete_session(db: Session, user_id: str, session_id: str) -> int:
    """Delete all messages in a session. Returns count of deleted messages."""
    count = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id,
        )
        .delete()
    )
    db.commit()
    return count
