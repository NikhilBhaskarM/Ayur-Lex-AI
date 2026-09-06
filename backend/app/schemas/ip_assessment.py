from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime

class IPAssessmentRequest(BaseModel):
    asset_id: str
    formulation_name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = []
    synergy_evidence: Optional[str] = None
    biological_origin: Optional[str] = None
    jurisdiction: Optional[str] = "India"

class IPAssessmentResponse(BaseModel):
    id: Optional[UUID] = None
    asset_id: str
    title: str
    ip_type: str
    governing_act: str
    key_sections: str
    statutory_prerequisites: List[str]
    ayurvedic_specific_nuances: List[str]
    exclusion_risks: List[str]
    action_steps: List[str]
    rag_guidance: Optional[str] = None
    citations: Optional[List[dict]] = []
    confidence: Optional[dict] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
