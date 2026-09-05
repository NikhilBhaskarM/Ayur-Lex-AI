import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Date, Integer, Float, Text, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base
from app.models.user import User


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    jurisdiction = Column(String(50), default="India", nullable=False)
    status = Column(String(50), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True)
    confidence = Column(String(20), nullable=True)
    confidence_score = Column(Float, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_type = Column(String(50), nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    formulation_data = Column(JSON, nullable=True)
    classification_result = Column(JSON, nullable=True)
    ip_assessment = Column(JSON, nullable=True)
    abs_assessment = Column(JSON, nullable=True)
    regulatory_pathway = Column(JSON, nullable=True)
    confidence = Column(String(20), nullable=True)
    status = Column(String(50), default="completed", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    authority = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    country = Column(String(50), nullable=True)
    authority_level = Column(Integer, nullable=False)
    crawl_frequency = Column(String(50), default="weekly", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_crawled = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    country = Column(String(50), nullable=True)
    statute = Column(String(255), nullable=True)
    status = Column(String(50), default="current", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    topics = Column(JSON, default=[], nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    effective_date = Column(Date, nullable=True)
    gazette_notification_number = Column(String(100), nullable=True)
    content_hash = Column(String(64), nullable=False)
    raw_content = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    version_status = Column(String(50), default="current", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_version_id = Column(UUID(as_uuid=True), ForeignKey("document_versions.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    section = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    article = Column(String(100), nullable=True)
    qdrant_point_id = Column(UUID(as_uuid=True), nullable=True)
    embedding_model = Column(String(100), nullable=False)
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class LegalProvision(Base):
    __tablename__ = "legal_provisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    provision_type = Column(String(50), nullable=False)
    provision_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    amended_by = Column(String(255), nullable=True)
    effective_from = Column(Date, nullable=True)


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    documents_processed = Column(Integer, default=0, nullable=False)
    chunks_created = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("ingestion_jobs.id", ondelete="CASCADE"), nullable=False)
    level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


__all__ = [
    "User",
    "Conversation",
    "Message",
    "Assessment",
    "Source",
    "Document",
    "DocumentVersion",
    "DocumentChunk",
    "LegalProvision",
    "IngestionJob",
    "IngestionLog",
]
