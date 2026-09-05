import asyncio
import hashlib
import math
import structlog
from app.embeddings.base import EmbeddingProvider
from app.config import settings

logger = structlog.get_logger(__name__)

def _hash_vector(text: str, dim: int = 384) -> list[float]:
    vec = [0.0] * dim
    words = text.lower().split()
    if not words:
        return vec
    for word in words:
        h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h >> 8) & 1 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec

class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self):
        self._model_name = settings.EMBEDDING_MODEL or "all-MiniLM-L6-v2"
        self._dimensions = settings.EMBEDDING_DIMENSIONS or 384
        self._model = None
        self._fallback_mode = False
        self._lock = asyncio.Lock()

    async def _get_model(self):
        if self._model is None and not self._fallback_mode:
            async with self._lock:
                if self._model is None and not self._fallback_mode:
                    def load_model():
                        try:
                            from sentence_transformers import SentenceTransformer
                            return SentenceTransformer(self._model_name)
                        except Exception as e:
                            logger.info("sentence_transformers unavailable, using fast fallback embedding", reason=str(e))
                            return None
                    model = await asyncio.to_thread(load_model)
                    if model is not None:
                        self._model = model
                    else:
                        self._fallback_mode = True
        return self._model

    def _encode(self, texts: list[str]) -> list[list[float]]:
        if self._model is not None:
            embeddings = self._model.encode(texts)
            return embeddings.tolist()
        return [_hash_vector(t, self._dimensions) for t in texts]

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        await self._get_model()
        return await asyncio.to_thread(self._encode, texts)

    async def embed_query(self, query: str) -> list[float]:
        results = await self.embed_texts([query])
        return results[0]

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions
