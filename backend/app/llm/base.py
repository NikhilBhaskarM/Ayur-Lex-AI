from abc import ABC, abstractmethod
from typing import Any

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict], temperature: float | None = None, max_tokens: int | None = None) -> str:
        pass

    @abstractmethod
    async def generate_structured(self, messages: list[dict], response_schema: type, temperature: float | None = None, max_tokens: int | None = None) -> Any:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
