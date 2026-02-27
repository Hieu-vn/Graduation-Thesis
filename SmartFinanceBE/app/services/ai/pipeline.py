"""
RAG Pipeline Orchestrator

Main entry point for the AI chatbot. Implements the 4-step RAG pipeline:
1. Query Understanding - Intent classification + entity extraction
2. Retrieval - Fetch relevant financial data
3. Context Assembly - Build prompt with context
4. Generation - Generate response via LLM
"""
import json
import logging
import re
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.services.ai.llm import generate_response
from app.services.ai.prompts import (
    INTENT_CLASSIFICATION_PROMPT,
    build_user_prompt,
    get_system_prompt,
)
from app.services.ai.retrieval import retrieve_context

logger = logging.getLogger(__name__)


def _parse_intent_response(response: str) -> Dict[str, Any]:
    """Parse the LLM's intent classification response."""
    # Try to extract JSON from the response
    # Remove markdown code fences if present
    cleaned = response.strip()
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
        intent = result.get("intent", "general")
        if intent not in ("lookup", "trend", "advice", "general"):
            intent = "general"

        entities = result.get("entities", {})
        return {"intent": intent, "entities": entities}
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse intent JSON: {response}")
        # Fallback: try to detect intent from keywords
        lower = response.lower()
        if "lookup" in lower:
            return {"intent": "lookup", "entities": {}}
        elif "trend" in lower:
            return {"intent": "trend", "entities": {}}
        elif "advice" in lower:
            return {"intent": "advice", "entities": {}}
        return {"intent": "general", "entities": {}}


def _resolve_dates(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve date strings from entities into date objects."""
    resolved = dict(entities)
    today = date.today()

    start_str = entities.get("start_date")
    end_str = entities.get("end_date")

    if start_str and start_str != "null":
        try:
            resolved["start_date"] = date.fromisoformat(start_str)
        except (ValueError, TypeError):
            resolved["start_date"] = today.replace(day=1)
    else:
        resolved["start_date"] = today.replace(day=1)

    if end_str and end_str != "null":
        try:
            resolved["end_date"] = date.fromisoformat(end_str)
        except (ValueError, TypeError):
            resolved["end_date"] = today
    else:
        resolved["end_date"] = today

    return resolved


def classify_intent(
    query: str,
    conversation_history: Optional[List[dict]] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    Step 1: Query Understanding
    Use LLM to classify the intent and extract entities from the user's query.

    Returns:
        Tuple of (intent, entities)
    """
    today_str = date.today().isoformat()
    prompt = INTENT_CLASSIFICATION_PROMPT.format(query=query, today=today_str)

    # Use a simpler system prompt for classification
    system = "Bạn là bộ phân loại câu hỏi. Chỉ trả về JSON, không giải thích gì thêm."

    response = generate_response(system, prompt)

    parsed = _parse_intent_response(response)
    intent = parsed["intent"]
    entities = _resolve_dates(parsed["entities"])
    entities["query"] = query

    logger.info(f"Classified intent: {intent}, entities: {entities}")
    return intent, entities


def process_query(
    db: Session,
    user_id: str,
    query: str,
    conversation_history: Optional[List[dict]] = None,
) -> Dict[str, Any]:
    """
    Main RAG pipeline - process a user query through all 4 steps.

    Args:
        db: Database session
        user_id: User ID
        query: User's natural language query
        conversation_history: Previous messages in the session

    Returns:
        Dict with 'response', 'intent', and 'metadata'
    """
    # Step 1: Query Understanding
    logger.info(f"Processing query for user {user_id}: {query}")
    intent, entities = classify_intent(query, conversation_history)

    # Step 2: Retrieval
    context = retrieve_context(db, user_id, intent, entities)

    # Step 3: Context Assembly
    system_prompt = get_system_prompt(intent)
    user_prompt = build_user_prompt(query, context)

    # Step 4: Generation
    response = generate_response(
        system_prompt,
        user_prompt,
        conversation_history=conversation_history,
    )

    return {
        "response": response,
        "intent": intent,
        "metadata": {
            "entities": {
                k: str(v) if isinstance(v, date) else v
                for k, v in entities.items()
            },
            "context_keys": list(context.keys()),
        },
    }
