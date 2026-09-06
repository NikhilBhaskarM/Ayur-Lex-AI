from dataclasses import dataclass
from typing import Any
from app.embeddings.factory import get_embedding_provider
from app.rag.vector_search import VectorStore, SearchResult
from app.rag.keyword_search import KeywordSearcher

@dataclass
class RetrievedChunk:
    chunk_id: str
    content: str
    score: float
    metadata: dict[str, Any]

class HybridRetriever:
    def __init__(self, vector_store: VectorStore, keyword_searcher: KeywordSearcher):
        self.vector_store = vector_store
        self.keyword_searcher = keyword_searcher
        self.embedding_provider = get_embedding_provider()
        self.k = 60 # RRF constant

    def _compute_rrf(self, vector_results: list[SearchResult], keyword_results: list[SearchResult]) -> list[RetrievedChunk]:
        scores = {}
        chunks = {}
        
        for rank, res in enumerate(vector_results):
            if res.id not in scores:
                scores[res.id] = 0.0
                chunks[res.id] = res
            scores[res.id] += 1.0 / (self.k + rank + 1)
            
        for rank, res in enumerate(keyword_results):
            if res.id not in scores:
                scores[res.id] = 0.0
                chunks[res.id] = res
            scores[res.id] += 1.0 / (self.k + rank + 1)
            
        # Sort by RRF score
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        
        return [
            RetrievedChunk(
                chunk_id=chunks[chunk_id].id,
                content=chunks[chunk_id].content,
                score=scores[chunk_id],
                metadata=chunks[chunk_id].metadata
            )
            for chunk_id in sorted_ids
        ]

    async def retrieve(self, query: str, jurisdiction: str | None, filters: dict | None, top_k: int = 20) -> list[RetrievedChunk]:
        effective_filters = filters or {}
        if jurisdiction:
            effective_filters["jurisdiction"] = jurisdiction
        
        query_vector = await self.embedding_provider.embed_query(query)
        
        # Parallel search
        vector_results = await self.vector_store.search(query_vector, effective_filters, limit=top_k)
        
        # Keyword search on corpus
        keyword_results = self.keyword_searcher.search(query, limit=top_k * 2)
        
        # Filter keyword results matching jurisdiction if specified
        filtered_keyword = []
        for r in keyword_results:
            match = True
            if jurisdiction and r.metadata.get("jurisdiction"):
                if r.metadata.get("jurisdiction").lower() != jurisdiction.lower():
                    match = False
            if match:
                filtered_keyword.append(r)
        
        if not filtered_keyword:
            filtered_keyword = keyword_results
        
        return self._compute_rrf(vector_results, filtered_keyword[:top_k])
