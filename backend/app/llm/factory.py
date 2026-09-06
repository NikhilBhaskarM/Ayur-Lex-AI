from typing import Optional
from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.config import settings

def get_llm_provider(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> LLMProvider:
    provider_name = (provider or settings.LLM_PROVIDER).lower()
    
    if provider_name == "openai":
        url = base_url or "https://api.openai.com/v1"
        return OpenAIProvider(
            base_url=url,
            api_key=api_key or settings.LLM_API_KEY,
            model_name=model or "gpt-4o",
            provider_name="openai"
        )
    elif provider_name == "ollama":
        url = base_url or settings.LLM_BASE_URL or "http://localhost:11434/v1"
        return OpenAIProvider(
            base_url=url,
            api_key=api_key or "ollama",
            model_name=model or settings.LLM_MODEL or "llama3.1:8b",
            provider_name="ollama"
        )
    elif provider_name == "lmstudio":
        url = base_url or settings.LLM_BASE_URL or "http://localhost:1234/v1"
        return OpenAIProvider(
            base_url=url,
            api_key=api_key or "lmstudio",
            model_name=model or "local-model",
            provider_name="lmstudio"
        )
    else:
        # Default fallback
        return OpenAIProvider(
            base_url=base_url,
            api_key=api_key,
            model_name=model,
            provider_name=provider_name
        )
