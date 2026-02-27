from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "SmartFinanceAI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 5000

    # Database (read-only access to SmartFinanceBE's MySQL)
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/smart_finance"

    # AI Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    AI_MAX_CONTEXT_TRANSACTIONS: int = 100
    AI_CONVERSATION_MEMORY_SIZE: int = 10

    # Service-to-Service Authentication
    AI_SERVICE_API_KEY: str = "smartfinance-ai-secret-key-change-in-production"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
