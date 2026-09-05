from openai import AsyncOpenAI
from app.embeddings.base import EmbeddingProvider
from app.config import settings

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self._model_name = settings.EMBEDDING_MODEL or "text-embedding-3-small"
        self._dimensions = settings.EMBEDDING_DIMENSIONS or 1536
        self.client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY
        )

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(
            input=texts,
            model=self._model_name,
            dimensions=self._dimensions if "3" in self._model_name else None
        )
        return [data.embedding for data in response.data]

    async def embed_query(self, query: str) -> list[float]:
        results = await self.embed_texts([query])
        return results[0]

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions
