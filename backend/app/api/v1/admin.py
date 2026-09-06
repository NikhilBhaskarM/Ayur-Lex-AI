"""Admin API endpoints for crawling, ingestion, and system management."""

import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List, Optional
from app.database import get_db, async_session_maker
from app.api.deps import require_role
from app.models import User, Source, Document, IngestionJob, IngestionLog
from app.schemas.admin import (
    AdminStatsResponse, IngestRequest, IngestionJobResponse,
    CrawlJobDetailResponse, IngestionLogResponse, CrawlAllRequest
)
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(tags=["admin"])


async def _run_crawl_job_background(source_id: UUID, force_reindex: bool = False):
    """Run a crawl job in the background with its own database session."""
    from app.crawler.orchestrator import CrawlOrchestrator
    orchestrator = CrawlOrchestrator()
    async with async_session_maker() as db:
        try:
            await orchestrator.run_crawl_job(db, source_id, force_reindex)
        except Exception as e:
            logger.error("Background crawl job failed", source_id=str(source_id), error=str(e))


async def _run_crawl_all_background(force_reindex: bool = False):
    """Run crawl for all active sources in the background."""
    from app.crawler.orchestrator import CrawlOrchestrator
    orchestrator = CrawlOrchestrator()
    async with async_session_maker() as db:
        try:
            await orchestrator.run_crawl_all(db, force_reindex)
        except Exception as e:
            logger.error("Background crawl-all job failed", error=str(e))


@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """Get system-wide statistics."""
    doc_count = (await db.execute(select(func.count(Document.id)))).scalar() or 0
    source_count = (await db.execute(select(func.count(Source.id)))).scalar() or 0
    user_count = (await db.execute(select(func.count(User.id)))).scalar() or 0

    from app.models import Conversation, Assessment
    conv_count = (await db.execute(select(func.count(Conversation.id)))).scalar() or 0
    assess_count = (await db.execute(select(func.count(Assessment.id)))).scalar() or 0

    active_jobs = (await db.execute(
        select(func.count(IngestionJob.id)).where(IngestionJob.status.in_(["pending", "running"]))
    )).scalar() or 0

    recent_jobs_result = await db.execute(
        select(IngestionJob)
        .order_by(IngestionJob.started_at.desc().nullslast())
        .limit(10)
    )
    recent_jobs = recent_jobs_result.scalars().all()

    job_responses = []
    for job in recent_jobs:
        source_result = await db.execute(select(Source.name).where(Source.id == job.source_id))
        source_name = source_result.scalar_one_or_none()
        job_responses.append(IngestionJobResponse(
            id=job.id,
            source_id=job.source_id,
            source_name=source_name,
            status=job.status,
            job_type=job.job_type,
            documents_found=job.documents_found or 0,
            documents_processed=job.documents_processed or 0,
            documents_failed=job.documents_failed or 0,
            chunks_created=job.chunks_created or 0,
            started_at=job.started_at,
            completed_at=job.completed_at,
        ))

    return AdminStatsResponse(
        total_documents=doc_count,
        total_sources=source_count,
        total_users=user_count,
        total_conversations=conv_count,
        total_assessments=assess_count,
        active_ingestion_jobs=active_jobs,
        recent_ingestion_jobs=job_responses
    )


@router.get("/users")
async def list_users(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """List all users."""
    result = await db.execute(select(User))
    return result.scalars().all()


@router.patch("/users/{id}")
async def update_user(
    id: UUID,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """Update a user (placeholder)."""
    return {}


@router.post("/ingest")
async def trigger_ingestion(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """Trigger a crawl + ingestion job for a specific source."""
    # Verify source exists
    source_result = await db.execute(select(Source).where(Source.id == request.source_id))
    source = source_result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    if not source.is_active:
        raise HTTPException(status_code=400, detail="Source is not active")

    # Launch background crawl
    background_tasks.add_task(_run_crawl_job_background, request.source_id, request.force_reindex)

    logger.info("Crawl job queued", source_id=str(request.source_id), source_name=source.name)
    return {
        "status": "queued",
        "source_id": str(request.source_id),
        "source_name": source.name,
        "message": f"Crawl job queued for '{source.name}'. Check /admin/ingestion-status for progress."
    }


@router.post("/crawl-all")
async def trigger_crawl_all(
    request: CrawlAllRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """Trigger crawl for all active sources."""
    active_count = (await db.execute(
        select(func.count(Source.id)).where(Source.is_active == True)
    )).scalar() or 0

    if active_count == 0:
        raise HTTPException(status_code=400, detail="No active sources found")

    background_tasks.add_task(_run_crawl_all_background, request.force_reindex)

    logger.info("Crawl-all job queued", active_sources=active_count)
    return {
        "status": "queued",
        "active_sources": active_count,
        "message": f"Crawl jobs queued for {active_count} active sources."
    }


@router.get("/ingestion-status", response_model=List[IngestionJobResponse])
async def list_ingestion_jobs(
    limit: int = 20,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """List recent ingestion/crawl jobs."""
    result = await db.execute(
        select(IngestionJob)
        .order_by(IngestionJob.started_at.desc().nullslast())
        .limit(limit)
    )
    jobs = result.scalars().all()

    responses = []
    for job in jobs:
        source_result = await db.execute(select(Source.name).where(Source.id == job.source_id))
        source_name = source_result.scalar_one_or_none()
        responses.append(IngestionJobResponse(
            id=job.id,
            source_id=job.source_id,
            source_name=source_name,
            status=job.status,
            job_type=job.job_type,
            documents_found=job.documents_found or 0,
            documents_processed=job.documents_processed or 0,
            documents_failed=job.documents_failed or 0,
            chunks_created=job.chunks_created or 0,
            started_at=job.started_at,
            completed_at=job.completed_at,
        ))

    return responses


@router.get("/ingestion-status/{job_id}", response_model=CrawlJobDetailResponse)
async def get_ingestion_job_detail(
    job_id: UUID,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed status of a specific ingestion/crawl job including logs."""
    job_result = await db.execute(select(IngestionJob).where(IngestionJob.id == job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Ingestion job not found")

    source_result = await db.execute(select(Source.name).where(Source.id == job.source_id))
    source_name = source_result.scalar_one_or_none()

    logs_result = await db.execute(
        select(IngestionLog)
        .where(IngestionLog.job_id == job_id)
        .order_by(IngestionLog.created_at.asc())
    )
    logs = logs_result.scalars().all()

    return CrawlJobDetailResponse(
        id=job.id,
        source_id=job.source_id,
        source_name=source_name,
        status=job.status,
        job_type=job.job_type,
        documents_found=job.documents_found or 0,
        documents_processed=job.documents_processed or 0,
        documents_failed=job.documents_failed or 0,
        chunks_created=job.chunks_created or 0,
        errors=job.errors,
        started_at=job.started_at,
        completed_at=job.completed_at,
        logs=[IngestionLogResponse(
            id=log.id,
            job_id=log.job_id,
            document_id=log.document_id,
            level=log.level,
            message=log.message,
            details=log.details,
            created_at=log.created_at,
        ) for log in logs]
    )


@router.get("/audit-logs")
async def list_audit_logs(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    """List audit logs (placeholder)."""
    return []
