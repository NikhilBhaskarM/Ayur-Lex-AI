from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Source
from app.schemas.source import SourceResponse, SourceDetailResponse
from sqlalchemy import select

router = APIRouter(tags=["sources"])

@router.get("", response_model=List[SourceResponse])
async def list_sources(
    jurisdiction: Optional[str] = None,
    source_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Source)
    if jurisdiction:
        stmt = stmt.where(Source.jurisdiction == jurisdiction)
    if source_type:
        stmt = stmt.where(Source.source_type == source_type)
    if is_active is not None:
        stmt = stmt.where(Source.is_active == is_active)
        
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{id}", response_model=SourceDetailResponse)
async def get_source(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Source).where(Source.id == id)
    result = await db.execute(stmt)
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return {**source.__dict__, "documents": [], "document_count": 0}
