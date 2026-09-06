from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime

class ABSEvaluationRequest(BaseModel):
    involves_bio_resource: bool = True
    source_is_india: bool = True
    entity_type: str = "indian_entity"  # indian_citizen, indian_entity, foreign_or_nri
    purpose: str = "commercial"         # commercial, research, bio_survey
    is_cultivated: bool = False
    is_ayush_practitioner: bool = False
    is_codified_tk: bool = True
    applies_for_ipr: bool = False
    plant_names: Optional[List[str]] = []
    jurisdiction: Optional[str] = "India"

class ABSChecklistItem(BaseModel):
    question: str
    user_answer: str
    relevant_provision: str
    why_it_matters: str
    required_action: str
    authority: str
    confidence: str = "HIGH"
    needs_human_review: bool = False

class ABSEvaluationResponse(BaseModel):
    id: Optional[UUID] = None
    overall_status: str  # COMPLIANT_NO_APPROVAL_NEEDED, APPROVAL_REQUIRED_FROM_NBA, INTIMATION_TO_SBB_REQUIRED, EXEMPTION_APPLICABLE
    summary: str
    required_forms: List[str]
    benefit_sharing_applicable: bool
    estimated_benefit_sharing_rate: Optional[str] = None
    checklist: List[ABSChecklistItem]
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
