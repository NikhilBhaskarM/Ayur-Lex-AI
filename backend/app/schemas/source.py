from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime

class SourceResponse(BaseModel):
    id: UUID
    name: str
    authority: Optional[str] = None
    source_type: str
    url: Optional[str] = None
    jurisdiction: Optional[str] = None
    country: Optional[str] = None
    authority_level: Optional[int] = None
    crawl_frequency: Optional[str] = None
    is_active: bool
    last_crawled: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentResponse(BaseModel):
    id: UUID
    title: str
    document_type: str
    jurisdiction: Optional[str] = None
    status: str
    language: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SourceDetailResponse(SourceResponse):
    documents: List[DocumentResponse]
    document_count: int

    model_config = ConfigDict(from_attributes=True)
