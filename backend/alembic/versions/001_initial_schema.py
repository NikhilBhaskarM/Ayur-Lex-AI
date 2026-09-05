"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), default='USER', nullable=False),
        sa.Column('preferred_language', sa.String(10), default='en', nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Sources table
    op.create_table(
        'sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('authority', sa.String(255), nullable=False),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('jurisdiction', sa.String(50), nullable=False),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('authority_level', sa.Integer(), nullable=False),
        sa.Column('crawl_frequency', sa.String(50), default='weekly', nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('last_crawled', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Documents table
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('document_type', sa.String(50), nullable=False),
        sa.Column('jurisdiction', sa.String(50), nullable=False),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('statute', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), default='current', nullable=False),
        sa.Column('language', sa.String(10), default='en', nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('topics', sa.ARRAY(sa.String()), default=[], nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Document Versions table
    op.create_table(
        'document_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('effective_date', sa.Date(), nullable=True),
        sa.Column('gazette_notification_number', sa.String(100), nullable=True),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('raw_content', sa.Text(), nullable=False),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('version_status', sa.String(50), default='current', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Document Chunks table
    op.create_table(
        'document_chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_version_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('document_versions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('section', sa.String(100), nullable=True),
        sa.Column('rule', sa.String(100), nullable=True),
        sa.Column('article', sa.String(100), nullable=True),
        sa.Column('qdrant_point_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('embedding_model', sa.String(100), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Legal Provisions table
    op.create_table(
        'legal_provisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provision_type', sa.String(50), nullable=False),
        sa.Column('provision_number', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('amended_by', sa.String(255), nullable=True),
        sa.Column('effective_from', sa.Date(), nullable=True),
    )

    # Conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('jurisdiction', sa.String(50), default='India', nullable=False),
        sa.Column('status', sa.String(50), default='active', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('citations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.String(20), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('input_tokens', sa.Integer(), nullable=True),
        sa.Column('output_tokens', sa.Integer(), nullable=True),
        sa.Column('model_used', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Assessments table
    op.create_table(
        'assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_type', sa.String(50), nullable=False),
        sa.Column('jurisdiction', sa.String(50), nullable=False),
        sa.Column('formulation_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('classification_result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_assessment', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('abs_assessment', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('regulatory_pathway', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.String(20), nullable=True),
        sa.Column('status', sa.String(50), default='completed', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Ingestion Jobs table
    op.create_table(
        'ingestion_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(50), default='pending', nullable=False),
        sa.Column('documents_processed', sa.Integer(), default=0, nullable=False),
        sa.Column('chunks_created', sa.Integer(), default=0, nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Ingestion Logs table
    op.create_table(
        'ingestion_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ingestion_jobs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('level', sa.String(20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Human Review table
    op.create_table(
        'human_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.String(50), default='new', nullable=False),
        sa.Column('user_question', sa.Text(), nullable=False),
        sa.Column('ai_assessment', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('facilitator_notes', sa.Text(), nullable=True),
        sa.Column('final_guidance', sa.Text(), nullable=True),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('priority', sa.String(20), default='normal', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', sa.String(100), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('human_reviews')
    op.drop_table('ingestion_logs')
    op.drop_table('ingestion_jobs')
    op.drop_table('assessments')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('legal_provisions')
    op.drop_table('document_chunks')
    op.drop_table('document_versions')
    op.drop_table('documents')
    op.drop_table('sources')
    op.drop_table('users')
