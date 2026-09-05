import pytest
from app.rag.confidence import ConfidenceScorer

def test_high_confidence_score():
    scorer = ConfidenceScorer()
    # High retrieval scores, 100% citation coverage, Level 1 authority, fresh, 3+ sources
    result = scorer.calculate_confidence(
        retrieval_scores=[0.92, 0.88, 0.85],
        citation_coverage=1.0,
        source_authority_levels=[1, 1, 2],
        source_freshness=1.0,
        num_sources=3
    )
    assert result.level == "HIGH"
    assert result.score >= 0.75
    assert result.factors["citation_coverage"] == 1.0

def test_medium_confidence_score():
    scorer = ConfidenceScorer()
    # Moderate retrieval, 60% citation coverage, Level 2 authority, 2 sources
    result = scorer.calculate_confidence(
        retrieval_scores=[0.65, 0.55],
        citation_coverage=0.6,
        source_authority_levels=[2, 3],
        source_freshness=0.8,
        num_sources=2
    )
    assert result.level == "MEDIUM"
    assert 0.5 <= result.score < 0.75

def test_low_confidence_score():
    scorer = ConfidenceScorer()
    # Weak retrieval, low citation coverage, Level 5 commentary
    result = scorer.calculate_confidence(
        retrieval_scores=[0.25],
        citation_coverage=0.2,
        source_authority_levels=[5],
        source_freshness=0.5,
        num_sources=1
    )
    assert result.level == "LOW"
    assert result.score < 0.5

def test_confidence_with_no_sources():
    scorer = ConfidenceScorer()
    result = scorer.calculate_confidence(
        retrieval_scores=[],
        citation_coverage=0.0,
        source_authority_levels=[],
        source_freshness=0.0,
        num_sources=0
    )
    assert result.level == "LOW"
    assert result.score == 0.0
