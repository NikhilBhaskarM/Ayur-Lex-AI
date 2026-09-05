from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.config import settings

def get_llm_provider() -> LLMProvider:
    provider_name = settings.LLM_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIProvider(provider_name="openai")
    elif provider_name == "ollama":
        base_url = settings.LLM_BASE_URL or "http://localhost:11434/v1"
        return OpenAIProvider(base_url=base_url, provider_name="ollama")
    elif provider_name == "lmstudio":
        base_url = settings.LLM_BASE_URL or "http://localhost:1234/v1"
        return OpenAIProvider(base_url=base_url, provider_name="lmstudio")
    else:
        # Default fallback
        return OpenAIProvider()
