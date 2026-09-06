"""
Ayurvedic IPR & Regulatory AI Assistant — Core Configuration Re-export
Provides backward-compatible and standard modular imports for settings and environment validation.
"""

from app.config import (
    settings,
    Settings,
    AppEnvironment,
    LLMProvider,
    EmbeddingProvider,
    RerankerProvider,
    validate_environment,
    mask_secret,
)

__all__ = [
    "settings",
    "Settings",
    "AppEnvironment",
    "LLMProvider",
    "EmbeddingProvider",
    "RerankerProvider",
    "validate_environment",
    "mask_secret",
]
