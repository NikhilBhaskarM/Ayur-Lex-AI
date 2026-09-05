import time
import json
from typing import Any
from openai import AsyncOpenAI
from app.llm.base import LLMProvider
from app.config import settings

class OpenAIProvider(LLMProvider):
    def __init__(self, base_url: str | None = None, api_key: str | None = None, model_name: str | None = None, provider_name: str = "openai"):
        self._provider_name = provider_name
        self._model_name = model_name or settings.LLM_MODEL
        self._last_offline_time = 0.0
        self.client = AsyncOpenAI(
            base_url=base_url or settings.LLM_BASE_URL,
            api_key=api_key or settings.LLM_API_KEY or "dummy_key",
            timeout=1.0,
            max_retries=0,
        )

    async def generate(self, messages: list[dict], temperature: float | None = None, max_tokens: int | None = None) -> str:
        if time.time() - self._last_offline_time < 15.0:
            raise ConnectionError("LLM server offline (cached check)")
        try:
            response = await self.client.chat.completions.create(
                model=self._model_name,
                messages=messages,
                temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
                max_tokens=max_tokens if max_tokens is not None else settings.LLM_MAX_TOKENS,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            self._last_offline_time = time.time()
            raise e

    async def generate_structured(self, messages: list[dict], response_schema: type, temperature: float | None = None, max_tokens: int | None = None) -> Any:
        # Assuming JSON mode is supported
        response = await self.client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
            max_tokens=max_tokens if max_tokens is not None else settings.LLM_MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content or "{}"
        try:
            return response_schema.model_validate_json(content)
        except Exception:
            # Fallback to json parsing and passing dict to model
            data = json.loads(content)
            return response_schema(**data)

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def provider_name(self) -> str:
        return self._provider_name
