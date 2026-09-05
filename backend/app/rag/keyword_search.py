import os
import json
import sqlite3
import re
from rank_bm25 import BM25Okapi
from app.rag.vector_search import SearchResult
from app.rag.statutory_knowledge import STATUTORY_CORPUS

def load_combined_corpus() -> list[dict]:
    """Load both static statutory corpus and ingested chunks from the database."""
    docs = []
    seen_ids = set()

    for d in STATUTORY_CORPUS:
        meta = dict(d.get("metadata", {}))
        meta["source_title"] = meta.get("source_title") or meta.get("source_name") or meta.get("statute") or "Primary Statute"
        meta["portal_url"] = meta.get("portal_url") or meta.get("source_url") or meta.get("url")
        docs.append({"id": d["id"], "content": d["content"], "metadata": meta})
        seen_ids.add(d["id"])

    db_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ayurveda_ipr.db")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ayurveda_ipr.db")),
    ]
    for p in db_paths:
        if os.path.exists(p):
            try:
                con = sqlite3.connect(p)
                cur = con.cursor()
                cur.execute("SELECT id, content, section, rule, metadata_ FROM document_chunks")
                rows = cur.fetchall()
                for r in rows:
                    meta = {}
                    if r[4]:
                        try:
                            meta = json.loads(r[4]) if isinstance(r[4], str) else r[4]
                        except Exception:
                            pass
                    meta["section"] = r[2]
                    meta["rule"] = r[3]
                    meta["source_title"] = meta.get("source_title") or meta.get("source_name") or meta.get("statute") or "Primary Statute"
                    meta["portal_url"] = meta.get("portal_url") or meta.get("source_url") or meta.get("url")
                    cid = meta.get("chunk_tag", str(r[0]))
                    if cid not in seen_ids:
                        seen_ids.add(cid)
                        docs.append({
                            "id": cid,
                            "content": r[1],
                            "metadata": meta
                        })
                con.close()
                break
            except Exception:
                pass
    return docs

class KeywordSearcher:
    def __init__(self):
        self.bm25 = None
        self.documents = []
        # Pre-index all authoritative statutory corpus & database chunks
        self.index_documents(load_combined_corpus())

    def _tokenize(self, text: str) -> list[str]:
        return [t for t in re.split(r'\W+', text.lower()) if t]

    def index_documents(self, documents: list[dict]):
        self.documents = documents
        tokenized_corpus = []
        for doc in self.documents:
            # Combine content with section, statute, and source for rich keyword indexing
            meta = doc.get("metadata", {})
            extra_text = f"{meta.get('section', '')} {meta.get('statute', '')} {meta.get('source_title', '')} {meta.get('source_name', '')}"
            full_text = f"{doc['content']} {extra_text}"
            tokenized_corpus.append(self._tokenize(full_text))

        if tokenized_corpus:
            self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        if not self.bm25 or not self.documents:
            return []
            
        tokenized_query = self._tokenize(query)
        if not tokenized_query:
            return []

        doc_scores = list(self.bm25.get_scores(tokenized_query))
        q_lower = query.lower()

        # Add phrase bonus and metadata matching
        for idx, doc in enumerate(self.documents):
            content_lower = doc["content"].lower()
            meta = doc.get("metadata", {})
            section_lower = str(meta.get("section", "")).lower()
            statute_lower = str(meta.get("statute", "")).lower()

            # Section exact matches (e.g., 3(p), 3(e), 3(d), 158-b, form iii)
            for phrase in ["3(p)", "3(e)", "3(d)", "158-b", "form iii", "form i", "schedule t", "schedule e", "aahara", "tkdl", "cadila", "synerg"]:
                if phrase in q_lower and (phrase in section_lower or phrase in content_lower):
                    doc_scores[idx] += 3.5

            # Keyword containment
            matched_tokens = sum(1 for t in tokenized_query if t in content_lower or t in section_lower or t in statute_lower)
            if doc_scores[idx] == 0 and matched_tokens > 0:
                doc_scores[idx] = matched_tokens * 0.1

        scored_docs = list(zip(doc_scores, self.documents))
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, doc in scored_docs[:limit]:
            if score > 0:
                results.append(SearchResult(
                    id=doc["id"],
                    score=score,
                    content=doc["content"],
                    metadata=doc.get("metadata", {})
                ))
        return results
