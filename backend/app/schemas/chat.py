from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime
from app.schemas.common import Citation

class ConfidenceResponse(BaseModel):
    level: str
    score: float
    factors: dict[str, Any]

class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    jurisdiction: Optional[str] = None

class CitationResponse(BaseModel):
    source_title: str
    authority: Optional[str] = None
    section: Optional[str] = None
    rule: Optional[str] = None
    article: Optional[str] = None
    version_date: Optional[str] = None
    official_url: Optional[str] = None
    relevant_passage: Optional[str] = None

class ChatMessageResponse(BaseModel):
    conversation_id: UUID
    message_id: UUID
    answer: str
    citations: List[CitationResponse]
    confidence: ConfidenceResponse
    jurisdiction: str
    requires_clarification: bool
    clarification_questions: List[str]
    disclaimer: str

    model_config = ConfigDict(from_attributes=True)

class ConversationListResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    jurisdiction: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    message_count: int

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    citations: Optional[List[dict]] = None
    confidence_data: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConversationDetailResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    jurisdiction: Optional[str] = None
    status: str
    messages: List[MessageResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
