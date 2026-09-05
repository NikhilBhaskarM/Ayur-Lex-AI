from dataclasses import dataclass

@dataclass
class ConfidenceResult:
    level: str
    score: float
    factors: dict[str, float]

class ConfidenceScorer:
    def calculate_confidence(self, retrieval_scores: list[float], citation_coverage: float, source_authority_levels: list, source_freshness: float, num_sources: int) -> ConfidenceResult:
        # Multi-signal composite confidence scoring
        
        # 1. Retrieval Relevance (0.3)
        if retrieval_scores:
            max_s = max(retrieval_scores)
            avg_s = sum(retrieval_scores) / len(retrieval_scores)
            if 0 < max_s < 0.2:  # RRF score range (1/61 ~ 0.016)
                norm_retrieval = min(max_s / 0.016, 1.0)
            else:
                norm_retrieval = min(avg_s, 1.0)
        else:
            norm_retrieval = 0.0
        
        # 2. Citation Coverage (0.25)
        # Already normalized 0-1
        
        # 3. Source Authority (0.2)
        # Authority levels: 1=highest (legislation), 6=lowest (commentary)
        # Also handles string labels for backward compatibility
        auth_score = 0.0
        if source_authority_levels:
            numeric_levels = []
            for level in source_authority_levels:
                if isinstance(level, (int, float)):
                    numeric_levels.append(level)
                elif level == "Primary":
                    numeric_levels.append(1)
                elif level == "Secondary":
                    numeric_levels.append(3)
                else:
                    numeric_levels.append(5)
            if numeric_levels:
                best_level = min(numeric_levels)
                # Map 1-6 to 1.0-0.3 score
                auth_score = max(0.3, 1.0 - (best_level - 1) * 0.14)
            
        # 4. Source Freshness (0.15)
        # 0-1 score provided
        
        # 5. Corroboration (0.1)
        corroboration = min(num_sources / 3.0, 1.0) # Max score if 3+ sources
        
        final_score = (
            norm_retrieval * 0.3 +
            citation_coverage * 0.25 +
            auth_score * 0.2 +
            source_freshness * 0.15 +
            corroboration * 0.1
        )
        
        if final_score >= 0.75:
            level = "HIGH"
        elif final_score >= 0.5:
            level = "MEDIUM"
        else:
            level = "LOW"
            
        return ConfidenceResult(
            level=level,
            score=final_score,
            factors={
                "retrieval_relevance": norm_retrieval,
                "citation_coverage": citation_coverage,
                "source_authority": auth_score,
                "source_freshness": source_freshness,
                "corroboration": corroboration
            }
        )
