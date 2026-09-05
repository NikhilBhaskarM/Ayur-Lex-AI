from dataclasses import dataclass
from typing import Any
import structlog
try:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False
    AsyncQdrantClient = None
    Distance = VectorParams = PointStruct = Filter = FieldCondition = MatchValue = MatchAny = None

from app.config import settings

logger = structlog.get_logger(__name__)

@dataclass
class SearchResult:
    id: str
    score: float
    content: str
    metadata: dict[str, Any]

class VectorStore:
    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION or "rag_collection"
        self.client = None
        if HAS_QDRANT:
            try:
                self.client = AsyncQdrantClient(
                    url=settings.QDRANT_URL or "http://localhost:6333",
                    api_key=settings.QDRANT_API_KEY
                )
            except Exception as e:
                logger.warning("Failed to create Qdrant client", error=str(e))

    async def initialize(self):
        if not self.client:
            return
        try:
            exists = await self.client.collection_exists(collection_name=self.collection_name)
            if not exists:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={"dense": VectorParams(size=settings.EMBEDDING_DIMENSIONS or 384, distance=Distance.COSINE)}
                )
                logger.info("Created Qdrant collection", collection_name=self.collection_name)
        except Exception as e:
            logger.error("Error initializing vector store", error=str(e))

    def _build_filter(self, filters: dict | None) -> Filter | None:
        if not filters:
            return None
        must = []
        for key, value in filters.items():
            if isinstance(value, list):
                must.append(FieldCondition(key=key, match=MatchAny(any=value)))
            else:
                must.append(FieldCondition(key=key, match=MatchValue(value=value)))
        return Filter(must=must) if must else None

    async def search(self, query_vector: list[float], filters: dict | None, limit: int = 20) -> list[SearchResult]:
        if not self.client:
            return []
        try:
            qdrant_filter = self._build_filter(filters)
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=("dense", query_vector),
                query_filter=qdrant_filter,
                limit=limit,
                with_payload=True
            )
            
            return [
                SearchResult(
                    id=str(r.id),
                    score=r.score,
                    content=r.payload.get("content", ""),
                    metadata=r.payload.get("metadata", {})
                )
                for r in results
            ]
        except Exception as e:
            logger.warning("Vector search offline fallback", error=str(e))
            return []

    async def upsert(self, points: list[dict]):
        # points should be dicts with id, vector, content, metadata
        qdrant_points = [
            PointStruct(
                id=p["id"],
                vector={"dense": p["vector"]},
                payload={"content": p["content"], "metadata": p.get("metadata", {})}
            )
            for p in points
        ]
        await self.client.upsert(
            collection_name=self.collection_name,
            points=qdrant_points
        )

    async def delete(self, ids: list[str]):
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids
        )
