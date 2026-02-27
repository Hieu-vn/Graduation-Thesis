"""
LLM Service - Ollama Wrapper via LangChain

Handles:
- Connection to local Ollama instance
- Text generation with conversation history
- Health check for Ollama availability
"""
import logging
from typing import List, Optional, Tuple

import httpx
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.core.config import settings

logger = logging.getLogger(__name__)

# Singleton LLM instance
_llm: Optional[ChatOllama] = None


def get_llm() -> ChatOllama:
    """Get or initialize the Ollama LLM instance (singleton)."""
    global _llm
    if _llm is None:
        logger.info(f"Initializing Ollama LLM: {settings.OLLAMA_MODEL} at {settings.OLLAMA_BASE_URL}")
        _llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.3,
            num_predict=2048,
        )
        logger.info("Ollama LLM initialized")
    return _llm


def generate_response(
    system_prompt: str,
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
) -> str:
    """
    Generate a response using Ollama LLM.

    Args:
        system_prompt: System prompt defining AI behavior
        user_message: Current user message
        conversation_history: List of {"role": "user"|"assistant", "content": "..."} dicts

    Returns:
        Generated response text
    """
    llm = get_llm()

    messages = [SystemMessage(content=system_prompt)]

    # Add conversation history
    if conversation_history:
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # Add the current message
    messages.append(HumanMessage(content=user_message))

    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
        raise RuntimeError(f"Không thể tạo phản hồi từ AI: {str(e)}")


async def check_ollama_status() -> dict:
    """Check if Ollama is running and the model is available."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check Ollama is running
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code != 200:
                return {"status": "error", "message": "Ollama không phản hồi"}

            data = resp.json()
            models = [m["name"] for m in data.get("models", [])]

            model_available = any(
                settings.OLLAMA_MODEL in m for m in models
            )

            return {
                "status": "ok" if model_available else "model_missing",
                "ollama_running": True,
                "model": settings.OLLAMA_MODEL,
                "model_available": model_available,
                "available_models": models,
            }
    except httpx.ConnectError:
        return {
            "status": "error",
            "ollama_running": False,
            "message": f"Không thể kết nối Ollama tại {settings.OLLAMA_BASE_URL}",
        }
    except Exception as e:
        return {
            "status": "error",
            "ollama_running": False,
            "message": str(e),
        }
