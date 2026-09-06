from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Any, Dict
from datetime import datetime

class HumanReviewCreate(BaseModel):
    topic: str
    user_question: str
    priority: str = "Normal"  # Normal, Urgent
    assessment_id: Optional[UUID] = None
    ai_assessment: Optional[Dict[str, Any]] = None

class HumanReviewUpdate(BaseModel):
    status: Optional[str] = None  # new, assigned, in_review, completed, needs_info
    facilitator_notes: Optional[str] = None
    final_guidance: Optional[str] = None
    priority: Optional[str] = None
    facilitator_id: Optional[UUID] = None

class HumanReviewResponse(BaseModel):
    id: UUID
    assessment_id: Optional[UUID] = None
    user_id: UUID
    facilitator_id: Optional[UUID] = None
    status: str
    topic: Optional[str] = None
    user_question: str
    ai_assessment: Optional[Dict[str, Any]] = None
    facilitator_notes: Optional[str] = None
    final_guidance: Optional[str] = None
    priority: str
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
