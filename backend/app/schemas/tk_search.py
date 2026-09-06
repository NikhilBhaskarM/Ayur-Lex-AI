from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TKSearchRequest(BaseModel):
    query: str
    herb_name: Optional[str] = None
    therapeutic_claim: Optional[str] = None
    jurisdiction: Optional[str] = "India"
    top_k: int = 10

class ClassicalTreatiseCitation(BaseModel):
    treatise: str
    verse_or_chapter: Optional[str] = None
    indications: List[str]
    sanskrit_sloka: Optional[str] = None

class KnownPriorArtCase(BaseModel):
    patent_number: str
    patent_office: str
    applicant: str
    disputed_claims: str
    outcome: str
    key_prior_art_cited: str

class HerbPriorArtResult(BaseModel):
    herb_name: str
    sanskrit_name: str
    botanical_name: str
    family: str
    tkrc_class: str
    classical_treatises: List[ClassicalTreatiseCitation]
    famous_revocation_case: Optional[KnownPriorArtCase] = None
    section_3p_rejection_risk: str
    defensive_search_guidance: str

class TKSearchResponse(BaseModel):
    query: str
    matched_herbs: List[HerbPriorArtResult]
    rag_retrieved_provisions: List[Dict[str, Any]]
    total_matches: int
    defensive_advice: str

    model_config = ConfigDict(from_attributes=True)
