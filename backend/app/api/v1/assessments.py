from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.assessment import AssessmentListResponse, AssessmentResponse
from app.services.assessment_service import AssessmentService

router = APIRouter(tags=["assessments"])
assessment_service = AssessmentService()

@router.get("", response_model=List[AssessmentListResponse])
async def list_assessments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    assessments, _ = await assessment_service.get_user_assessments(db, current_user.id, page, page_size)
    return assessments

@router.get("/{id}", response_model=AssessmentResponse)
async def get_assessment(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    assessment = await assessment_service.get_assessment(db, current_user.id, id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
