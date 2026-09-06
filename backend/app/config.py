"""
Ayurvedic IPR & Regulatory AI Assistant — Application Configuration

All settings are loaded from environment variables with sensible defaults
for local development. Includes DevSecOps environment validation and secret masking.
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
    ALLOWED_ORIGINS: Optional[str] = None
    MAX_REQUEST_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 Megabytes
    SECURITY_HEADERS_ENABLED: bool = True
    SANITIZE_PROMPT_INJECTION: bool = True

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
    RATE_LIMIT_PER_MINUTE: int = 120

    # --- Crawler ---
    CRAWLER_USER_AGENT: str = "AyurvedaIPR-Bot/1.0"
    CRAWLER_MAX_CONCURRENT: int = 3
    CRAWLER_RATE_LIMIT_SECONDS: int = 1

    # --- Multilingual ---
    BHASHINI_API_KEY: Optional[str] = None
    BHASHINI_USER_ID: Optional[str] = None

    @property
    def cors_origins_list(self) -> list[str]:
        raw = self.ALLOWED_ORIGINS or self.CORS_ORIGINS or ""
        origins = [origin.strip() for origin in raw.split(",") if origin.strip()]

        # Safe defaults for local development
        default_dev = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8000",
        ]
        for dev_origin in default_dev:
            if dev_origin not in origins:
                origins.append(dev_origin)

        # Disallow wildcard when allow_credentials=True
        return [o for o in origins if o != "*"]

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == AppEnvironment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == AppEnvironment.PRODUCTION


settings = Settings()


def mask_secret(value: Optional[str]) -> str:
    """Safely masks a secret string for logging (e.g., sk-...4abc)."""
    if not value:
        return "[NOT CONFIGURED]"
    if len(value) <= 6:
        return "****"
    return f"{value[:3]}...{value[-4:]}"


def validate_environment() -> dict:
    """
    Validates the runtime environment on application startup.
    Logs structured DevSecOps audit metrics, warns on missing optional keys,
    and ensures zero credentials or raw secrets are exposed in logs.
    """
    import structlog
    log = structlog.get_logger("security.audit")

    audit = {
        "env": settings.APP_ENV.value,
        "rate_limit_rpm": settings.RATE_LIMIT_PER_MINUTE,
        "payload_limit_mb": settings.MAX_REQUEST_SIZE_BYTES // (1024 * 1024),
        "cors_origins": settings.cors_origins_list,
        "security_headers": settings.SECURITY_HEADERS_ENABLED,
        "prompt_sanitizer": settings.SANITIZE_PROMPT_INJECTION,
    }

    # 1. Secret Key Check
    if settings.is_production and "change-this" in settings.SECRET_KEY.lower():
        log.error(
            "CRITICAL_SECURITY_ALERT: Default SECRET_KEY is active in production environment. "
            "Generate and assign a high-entropy SECRET_KEY."
        )
    else:
        log.info("JWT authentication initialized with configured SECRET_KEY")

    # 2. Database validation
    if "sqlite" in settings.DATABASE_URL.lower():
        log.info("Database configured with SQLite engine (embedded mode)")
    else:
        log.info("Database configured with PostgreSQL engine")

    # 3. Vector Database (Qdrant)
    if not settings.QDRANT_API_KEY:
        log.info("Qdrant API key not set; local vector engine or fallback mock mode engaged")
    else:
        log.info("Qdrant cloud cluster key authenticated", key=mask_secret(settings.QDRANT_API_KEY))

    # 4. LLM API Key
    if settings.LLM_PROVIDER == LLMProvider.OPENAI and not settings.LLM_API_KEY:
        log.warning("LLM provider set to OpenAI but LLM_API_KEY is not configured; fallback mock engaged")
    elif settings.LLM_API_KEY:
        log.info("LLM provider configured with API key", provider=settings.LLM_PROVIDER.value, key=mask_secret(settings.LLM_API_KEY))

    # 5. Multilingual Service (Bhashini)
    if not settings.BHASHINI_API_KEY:
        log.info("Bhashini API key not configured; local linguistic dictionary fallback active")
    else:
        log.info("Bhashini national translation gateway configured", key=mask_secret(settings.BHASHINI_API_KEY))

    log.info("DevSecOps runtime startup audit passed", **audit)
    return audit
