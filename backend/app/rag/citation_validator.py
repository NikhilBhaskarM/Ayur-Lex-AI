from dataclasses import dataclass
from app.rag.retriever import RetrievedChunk
from app.rag.citation_engine import Citation
from app.rag.statutory_knowledge import STATUTORY_CORPUS

@dataclass
class ValidationResult:
    validated_claims: list[str]
    unsupported_claims: list[str]
    overall_grounding_score: float

class CitationValidator:
    def validate_claims(self, response: str, chunks: list[RetrievedChunk], citations: list[Citation]) -> ValidationResult:
        # A simple heuristic validation
        # In a real system, an LLM would extract claims and verify them against the chunk content.
        # For this MVP, we perform a basic keyword overlap check between response sentences and cited chunks.
        
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        validated = []
        unsupported = []
        
        chunk_map = {c.chunk_id: c.content for c in chunks}
        statutory_map = {d["id"]: d["content"] for d in STATUTORY_CORPUS}
        
        for sentence in sentences:
            if not sentence:
                continue
                
            # Check if sentence has citations
            import re
            cited_ids = re.findall(r'\[([a-zA-Z0-9_-]+)\]', sentence)
            
            if cited_ids:
                # Check overlap
                words = set(sentence.lower().split())
                is_supported = False
                
                for cid in cited_ids:
                    content = chunk_map.get(cid) or statutory_map.get(cid)
                    if content:
                        chunk_words = set(content.lower().split())
                        # If more than 20% of significant words overlap
                        overlap = len(words.intersection(chunk_words))
                        if overlap > len(words) * 0.15:
                            is_supported = True
                            break
                            
                if is_supported:
                    validated.append(sentence)
                else:
                    unsupported.append(sentence)
            else:
                # No citation, we don't automatically flag as unsupported if it's general text, 
                # but for strict legal RAG, we might. Let's be lenient for transition sentences.
                pass
                
        total_claims = len(validated) + len(unsupported)
        score = len(validated) / total_claims if total_claims > 0 else 1.0
        
        return ValidationResult(
            validated_claims=validated,
            unsupported_claims=unsupported,
            overall_grounding_score=score
        )
