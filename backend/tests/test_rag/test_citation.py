import pytest
from app.rag.citation_engine import CitationEngine
from app.rag.retriever import RetrievedChunk

def test_citation_extraction_with_bracketed_refs():
    engine = CitationEngine()
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_1",
            content="Section 3(p) excludes traditional knowledge from patentability.",
            score=0.9,
            metadata={
                "source_title": "Patents Act, 1970",
                "authority": "Indian Patent Office",
                "section": "3(p)",
                "source_url": "https://ipindia.gov.in"
            }
        ),
        RetrievedChunk(
            chunk_id="chunk_2",
            content="Rule 158-B prescribes safety and efficacy requirements for ASU drugs.",
            score=0.85,
            metadata={
                "source_title": "Drugs and Cosmetics Rules, 1945",
                "authority": "Ministry of Ayush",
                "rule": "158-B",
                "source_url": "https://ayush.gov.in"
            }
        )
    ]
    
    response_text = (
        "In India, traditional formulations cannot be patented under Section 3(p) [chunk_1]. "
        "Furthermore, manufacturing licenses require compliance with ASU guidelines [chunk_2]."
    )
    
    citations = engine.extract_citations(response_text, chunks)
    assert len(citations) == 2
    assert citations[0].chunk_id == "chunk_1"
    assert citations[0].source_title == "Patents Act, 1970"
    assert citations[0].section == "3(p)"
    assert citations[1].chunk_id == "chunk_2"
    assert citations[1].rule == "158-B"

def test_citation_extraction_no_refs():
    engine = CitationEngine()
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_1",
            content="Classical Ayurveda is an ancient holistic medical system.",
            score=0.5,
            metadata={"source_title": "Ayurvedic General Background"}
        )
    ]
    response_text = "Ayurveda emphasizes balancing the doshas: Vata, Pitta, and Kapha."
    citations = engine.extract_citations(response_text, chunks)
    assert len(citations) == 0

def test_citation_metadata_mapping():
    engine = CitationEngine()
    chunks = [
        RetrievedChunk(
            chunk_id="bd_act_sec6",
            content="Section 6 requires NBA approval before applying for IPR.",
            score=0.95,
            metadata={
                "source_title": "Biological Diversity Act, 2002",
                "authority": "National Biodiversity Authority",
                "section": "6",
                "version_date": "2023-08-03",
                "source_url": "https://nbaindia.org"
            }
        )
    ]
    response_text = "Any IPR filed based on Indian biological resources requires NBA clearance [bd_act_sec6]."
    citations = engine.extract_citations(response_text, chunks)
    assert len(citations) == 1
    assert citations[0].authority == "National Biodiversity Authority"
    assert citations[0].official_url == "https://nbaindia.org"
    assert citations[0].version_date == "2023-08-03"
    assert "Section 6" in citations[0].relevant_passage
