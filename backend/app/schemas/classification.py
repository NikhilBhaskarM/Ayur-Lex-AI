from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.schemas.chat import ConfidenceResponse

class ClassificationRequest(BaseModel):
    formulation_name: str
    description: str
    ingredients: List[str]
    intended_use: str
    is_classical_text_based: Optional[bool] = None
    has_been_modified: Optional[bool] = None
    marketed_as: Optional[str] = None
    jurisdiction: str = 'india'
    biological_resources_involved: Optional[bool] = None

class ClassificationResponse(BaseModel):
    classification: str
    reasoning: str
    evidence: List[str]
    confidence: ConfidenceResponse
    missing_information: List[str]
    regulatory_implications: List[str]
    ip_implications: List[str]
    abs_implications: List[str]
    recommended_next_steps: List[str]
    disclaimer: str

    model_config = ConfigDict(from_attributes=True)
