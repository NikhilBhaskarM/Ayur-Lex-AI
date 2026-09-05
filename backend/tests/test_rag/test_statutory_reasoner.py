import pytest
from app.rag.statutory_reasoner import StatutoryReasoner
from app.rag.retriever import RetrievedChunk

@pytest.fixture
def reasoner():
    return StatutoryReasoner()

@pytest.fixture
def sample_chunks():
    return [
        RetrievedChunk(
            chunk_id="patents-act-3p",
            content="Section 3(p) of The Patents Act, 1970 excludes traditional knowledge from patentability.",
            score=0.9,
            metadata={"source_title": "The Patents Act, 1970", "section": "Section 3(p)", "statute": "The Patents Act, 1970"}
        ),
        RetrievedChunk(
            chunk_id="patents-act-3e",
            content="Section 3(e) excludes mere admixtures unless synergy is proven.",
            score=0.85,
            metadata={"source_title": "The Patents Act, 1970", "section": "Section 3(e)", "statute": "The Patents Act, 1970"}
        ),
        RetrievedChunk(
            chunk_id="dc-act-classical-3a",
            content="Section 3(a) defines classical ASU drugs manufactured under Form 25-D without clinical trials.",
            score=0.88,
            metadata={"source_title": "The Drugs and Cosmetics Act, 1940", "section": "Section 3(a)", "statute": "Drugs and Cosmetics Act, 1940"}
        ),
        RetrievedChunk(
            chunk_id="trademarks-ayurveda-names",
            content="Classical medicine names like Triphala are publici juris under Section 9.",
            score=0.82,
            metadata={"source_title": "Trade Marks Act, 1999", "section": "Section 9", "statute": "Trade Marks Act, 1999"}
        ),
        RetrievedChunk(
            chunk_id="bd-act-sec-6",
            content="Section 6 mandates prior approval from NBA before patent grant on Form III.",
            score=0.86,
            metadata={"source_title": "The Biological Diversity Act, 2002", "section": "Section 6", "statute": "Biological Diversity Act, 2002"}
        )
    ]

def test_section_3p_direct_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("What is Section 3(p) of the Patents Act?", sample_chunks)
    assert "Section 3(p)" in ans
    assert "strictly unpatentable" in ans
    assert "[patents-act-3p]" in ans

def test_clinical_trials_direct_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("Do I need clinical trials to manufacture classical Ayurvedic medicine?", sample_chunks)
    assert "No, clinical trials are NOT required" in ans
    assert "Section 3(a)" in ans
    assert "Form 25-D" in ans
    assert "[dc-act-classical-3a]" in ans

def test_trademark_triphala_direct_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("Can I register a trademark for Triphala?", sample_chunks)
    assert "No, you cannot register an exclusive trademark" in ans
    assert "Section 9" in ans
    assert "publici juris" in ans
    assert "Cadila" in ans

def test_form_iii_direct_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("What is Form III of the National Biodiversity Authority?", sample_chunks)
    assert "NBA Form III" in ans
    assert "Section 6(1)" in ans
    assert "Rs. 10,000" in ans
    assert "[bd-act-sec-6]" in ans

def test_section_7_exemptions_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("What are the exemptions under the 2023 Biodiversity Amendment Act?", sample_chunks)
    assert "Section 7" in ans
    assert "Codified Traditional Knowledge" in ans
    assert "Cultivated Medicinal Plants" in ans
    assert "Registered AYUSH Practitioners" in ans
    assert "[bd-act-sec-7-2023]" in ans

def test_section_3e_synergy_answer(reasoner, sample_chunks):
    ans = reasoner.synthesize("How do I prove synergism under Section 3(e)?", sample_chunks)
    assert "Section 3(e)" in ans
    assert "mere admixture" in ans
    assert "Combination Index" in ans
    assert "[patents-act-3e]" in ans

def test_dynamic_irac_fallback(reasoner, sample_chunks):
    ans = reasoner.synthesize("What are the laboratory quality inspection standards?", sample_chunks)
    assert "Statutory Analysis" in ans
    assert "Core Legal Position" in ans
    assert "Actionable Compliance Steps" in ans
