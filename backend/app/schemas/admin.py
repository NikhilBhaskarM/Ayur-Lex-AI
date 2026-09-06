from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime

class IngestionJobResponse(BaseModel):
    id: UUID
    source_id: UUID
    source_name: Optional[str] = None
    status: str
    job_type: str
    documents_found: int
    documents_processed: int
    documents_failed: int
    chunks_created: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AdminStatsResponse(BaseModel):
    total_documents: int
    total_sources: int
    total_users: int
    total_conversations: int
    total_assessments: int
    active_ingestion_jobs: int
    recent_ingestion_jobs: List[IngestionJobResponse]

    model_config = ConfigDict(from_attributes=True)

class IngestRequest(BaseModel):
    source_id: UUID
    force_reindex: bool = False

class IngestionLogResponse(BaseModel):
    id: UUID
    job_id: UUID
    document_id: Optional[UUID] = None
    level: str
    message: str
    details: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CrawlJobDetailResponse(BaseModel):
    id: UUID
    source_id: UUID
    source_name: Optional[str] = None
    status: str
    job_type: str
    documents_found: int
    documents_processed: int
    documents_failed: int
    chunks_created: int
    errors: Optional[list] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    logs: List[IngestionLogResponse] = []

    model_config = ConfigDict(from_attributes=True)


class CrawlAllRequest(BaseModel):
    force_reindex: bool = False
