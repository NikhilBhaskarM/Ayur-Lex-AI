from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime
from app.schemas.chat import ConfidenceResponse

class AssessmentListResponse(BaseModel):
    id: UUID
    assessment_type: str
    jurisdiction: Optional[str] = None
    confidence: Optional[dict] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssessmentResponse(BaseModel):
    id: UUID
    assessment_type: str
    jurisdiction: Optional[str] = None
    formulation_data: dict[str, Any]
    classification_result: Optional[dict[str, Any]] = None
    ip_assessment: Optional[dict[str, Any]] = None
    abs_assessment: Optional[dict[str, Any]] = None
    sources_used: Optional[List[dict[str, Any]]] = None
    confidence: Optional[dict[str, Any]] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
