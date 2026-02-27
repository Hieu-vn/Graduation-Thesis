from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "SmartFinanceBE"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 3001

    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/smart_finance"

    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:3001/api/auth/google/callback"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    FRONTEND_URL: str = "http://localhost:3000"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    # AI Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    AI_MAX_CONTEXT_TRANSACTIONS: int = 100
    AI_CONVERSATION_MEMORY_SIZE: int = 10

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
