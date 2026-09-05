from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database import get_db
from app.api.deps import require_role
from app.models import User
from app.schemas.admin import AdminStatsResponse, IngestRequest
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(tags=["admin"])

@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    # Dummy implementation
    return AdminStatsResponse(
        total_documents=0,
        total_sources=0,
        total_users=0,
        total_conversations=0,
        total_assessments=0,
        active_ingestion_jobs=0,
        recent_ingestion_jobs=[]
    )

@router.get("/users")
async def list_users(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    return []

@router.patch("/users/{id}")
async def update_user(
    id: UUID,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    return {}

@router.post("/ingest")
async def trigger_ingestion(
    request: IngestRequest,
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    return {"status": "queued"}

@router.get("/ingestion-status")
async def list_ingestion_jobs(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    return []

@router.get("/audit-logs")
async def list_audit_logs(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db)
):
    return []
