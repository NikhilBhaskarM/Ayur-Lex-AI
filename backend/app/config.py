"""
Ayurvedic IPR & Regulatory AI Assistant — Application Configuration

All settings are loaded from environment variables with sensible defaults
for local development.
"""

from enum import Enum
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LLMProvider(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    LMSTUDIO = "lmstudio"


class EmbeddingProvider(str, Enum):
    LOCAL = "local"
    OPENAI = "openai"


class RerankerProvider(str, Enum):
    LOCAL = "local"
    COHERE = "cohere"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    APP_NAME: str = "Ayurvedic IPR & Regulatory AI Assistant"
    APP_ENV: AppEnvironment = AppEnvironment.DEVELOPMENT
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://ayurveda:ayurveda_secret@localhost:5432/ayurveda_ipr"
    DATABASE_URL_SYNC: str = "postgresql://ayurveda:ayurveda_secret@localhost:5432/ayurveda_ipr"

    # --- Qdrant ---
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str = "ayurveda_legal"

    # --- Redis ---
    REDIS_URL: str = "redis://:ayurveda_redis_secret@localhost:6379/0"

    # --- LLM ---
    LLM_PROVIDER: LLMProvider = LLMProvider.OLLAMA
    LLM_BASE_URL: str = "http://localhost:11434/v1"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "llama3.1:8b"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 4096

    # --- Embeddings ---
    EMBEDDING_PROVIDER: EmbeddingProvider = EmbeddingProvider.LOCAL
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSIONS: int = 384

    # --- Reranker ---
    RERANKER_PROVIDER: RerankerProvider = RerankerProvider.LOCAL
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    COHERE_API_KEY: Optional[str] = None

    # --- Authentication ---
    SECRET_KEY: str = "change-this-to-a-random-secret-key-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 30

    # --- Crawler (Crawl4AI) ---
    CRAWLER_USER_AGENT: str = "AyurvedaIPR-Bot/1.0"
    CRAWLER_MAX_CONCURRENT: int = 3
    CRAWLER_RATE_LIMIT_SECONDS: int = 1
    CRAWLER_HEADLESS: bool = True
    CRAWLER_BROWSER_TYPE: str = "chromium"
    CRAWLER_PAGE_TIMEOUT: int = 30000
    CRAWLER_VERBOSE: bool = False
    CRAWLER_FOLLOW_INTERNAL_LINKS: bool = True
    CRAWLER_MAX_DEPTH: int = 2
    CRAWLER_MAX_PAGES_PER_SOURCE: int = 15

    # --- Multilingual ---
    BHASHINI_API_KEY: Optional[str] = None
    BHASHINI_USER_ID: Optional[str] = None

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == AppEnvironment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == AppEnvironment.PRODUCTION


settings = Settings()
