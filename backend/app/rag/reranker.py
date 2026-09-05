import asyncio
from abc import ABC, abstractmethod
from app.rag.retriever import RetrievedChunk
from app.config import settings

class Reranker(ABC):
    @abstractmethod
    async def rerank(self, query: str, documents: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        pass

class NoOpReranker(Reranker):
    async def rerank(self, query: str, documents: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        return documents[:top_k]

class LocalReranker(Reranker):
    def __init__(self):
        self._model = None
        self._lock = asyncio.Lock()
        
    async def _get_model(self):
        if self._model is None:
            async with self._lock:
                if self._model is None:
                    def load_model():
                        try:
                            from flashrank import Ranker
                            return Ranker(model_name=settings.RERANKER_MODEL or "ms-marco-MiniLM-L-12-v2")
                        except Exception:
                            return None
                    self._model = await asyncio.to_thread(load_model)
        return self._model

    def _rerank_sync(self, model, query: str, documents: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        if not documents:
            return []
            
        passages = [
            {"id": doc.chunk_id, "text": doc.content, "meta": doc.metadata}
            for doc in documents
        ]
        
        rerank_request = {
            "query": query,
            "passages": passages
        }
        
        results = model.rerank(rerank_request)
        
        reranked = []
        for rank, res in enumerate(results[:top_k]):
            # Find the original doc
            original_doc = next((d for d in documents if d.chunk_id == res["id"]), None)
            if original_doc:
                original_doc.score = res.get("score", 1.0 / (rank + 1))
                reranked.append(original_doc)
                
        return reranked

    async def rerank(self, query: str, documents: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        model = await self._get_model()
        if not model:
            # Fallback if not installed
            return documents[:top_k]
            
        return await asyncio.to_thread(self._rerank_sync, model, query, documents, top_k)

def get_reranker() -> Reranker:
    provider = settings.RERANKER_PROVIDER.lower() if settings.RERANKER_PROVIDER else "none"
    if provider == "local":
        return LocalReranker()
    # Cohere can be added later
    return NoOpReranker()
