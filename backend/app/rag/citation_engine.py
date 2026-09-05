import re
from dataclasses import dataclass
from typing import Optional
from app.rag.retriever import RetrievedChunk

@dataclass
class Citation:
    chunk_id: str
    source_title: str
    authority: str
    section: Optional[str] = None
    rule: Optional[str] = None
    article: Optional[str] = None
    version_date: Optional[str] = None
    official_url: Optional[str] = None
    retrieved_at: Optional[str] = None
    relevant_passage: Optional[str] = None

from app.rag.statutory_knowledge import STATUTORY_CORPUS

class CitationEngine:
    def extract_citations(self, response: str, chunks: list[RetrievedChunk]) -> list[Citation]:
        citations = []
        chunk_map = {c.chunk_id: c for c in chunks}
        statutory_map = {d["id"]: d for d in STATUTORY_CORPUS}
        
        # Find all brackets like [some_id]
        pattern = r'\[([a-zA-Z0-9_-]+)\]'
        matches = re.finditer(pattern, response)
        
        seen = set()
        for match in matches:
            cid = match.group(1)
            if cid in seen:
                continue
            if cid in chunk_map:
                seen.add(cid)
                chunk = chunk_map[cid]
                meta = chunk.metadata
                citations.append(Citation(
                    chunk_id=cid,
                    source_title=meta.get("source_title") or meta.get("source_name") or meta.get("statute") or "Primary Statute",
                    authority=meta.get("authority", "Statutory Authority"),
                    section=meta.get("section"),
                    rule=meta.get("rule"),
                    article=meta.get("article"),
                    version_date=meta.get("version_date"),
                    official_url=meta.get("source_url") or meta.get("portal_url") or meta.get("url"),
                    retrieved_at=meta.get("retrieved_at"),
                    relevant_passage=chunk.content[:240] + "..." if len(chunk.content) > 240 else chunk.content
                ))
            elif cid in statutory_map:
                seen.add(cid)
                doc = statutory_map[cid]
                meta = doc.get("metadata", {})
                citations.append(Citation(
                    chunk_id=cid,
                    source_title=meta.get("source_title") or meta.get("source_name") or meta.get("statute") or "Primary Statute",
                    authority=meta.get("authority", "Statutory Authority"),
                    section=meta.get("section"),
                    rule=meta.get("rule"),
                    article=meta.get("article"),
                    version_date=meta.get("version_date"),
                    official_url=meta.get("source_url") or meta.get("portal_url") or meta.get("url"),
                    retrieved_at=meta.get("retrieved_at"),
                    relevant_passage=doc["content"][:240] + "..." if len(doc["content"]) > 240 else doc["content"]
                ))
                
        return citations
