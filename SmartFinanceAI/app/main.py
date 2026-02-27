import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI Chatbot Service cho hệ thống quản lý tài chính SmartFinance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/ai")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.APP_NAME}


@app.on_event("startup")
async def startup_event():
    """Preload AI models on startup to avoid cold start."""
    logger = logging.getLogger(__name__)
    logger.info("SmartFinanceAI starting up...")

    try:
        from app.services.ai.embeddings import get_embedding_model
        logger.info("Preloading embedding model...")
        get_embedding_model()
        logger.info("Embedding model loaded ✅")
    except Exception as e:
        logger.warning(f"Failed to preload embedding model: {e}")

    logger.info(f"SmartFinanceAI ready on port {settings.PORT} 🚀")
