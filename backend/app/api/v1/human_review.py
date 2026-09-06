from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.human_review import (
    HumanReviewCreate, HumanReviewUpdate, HumanReviewResponse
)
from app.services.human_review_service import HumanReviewService

router = APIRouter(tags=["human_review"])
review_service = HumanReviewService()

def _format_review(r) -> HumanReviewResponse:
    topic = ""
    if r.ai_assessment and isinstance(r.ai_assessment, dict):
        topic = r.ai_assessment.get("topic", "")
    return HumanReviewResponse(
        id=r.id,
        assessment_id=r.assessment_id,
        user_id=r.user_id,
        facilitator_id=r.facilitator_id,
        status=r.status,
        topic=topic,
        user_question=r.user_question,
        ai_assessment=r.ai_assessment,
        facilitator_notes=r.facilitator_notes,
        final_guidance=r.final_guidance,
        priority=r.priority,
        assigned_at=r.assigned_at,
        completed_at=r.completed_at,
        created_at=r.created_at
    )

@router.post("", response_model=HumanReviewResponse)
async def create_human_review(
    request: HumanReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit an IPR or regulatory question for expert human facilitator review."""
    review = await review_service.create_review(db=db, user_id=current_user.id, request=request)
    return _format_review(review)

@router.get("", response_model=List[HumanReviewResponse])
async def list_human_reviews(
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List human review requests (users see their own; facilitators/admins see all)."""
    reviews = await review_service.list_reviews(
        db=db, user_id=current_user.id, role=current_user.role,
        status=status, limit=limit, offset=offset
    )
    return [_format_review(r) for r in reviews]

@router.get("/{id}", response_model=HumanReviewResponse)
async def get_human_review(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get details of a specific human review ticket."""
    review = await review_service.get_review(
        db=db, review_id=id, user_id=current_user.id, role=current_user.role
    )
    if not review:
        raise HTTPException(status_code=404, detail="Human review request not found")
    return _format_review(review)

@router.patch("/{id}", response_model=HumanReviewResponse)
async def update_human_review(
    id: UUID,
    request: HumanReviewUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update human review status, assign facilitator, or append regulatory guidance."""
    updated = await review_service.update_review(
        db=db, review_id=id, current_user=current_user, request=request
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Human review request not found or not permitted")
    return _format_review(updated)
