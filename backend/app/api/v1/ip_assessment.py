from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.ip_assessment import IPAssessmentRequest, IPAssessmentResponse
from app.services.ip_assessment_service import IPAssessmentService

router = APIRouter(tags=["ip_assessment"])
ip_service = IPAssessmentService()

@router.post("/evaluate", response_model=IPAssessmentResponse)
@router.post("", response_model=IPAssessmentResponse)
async def evaluate_ip(
    request: IPAssessmentRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Evaluate IP protection route (Patent, Trademark, GI, Design, Trade Secret) for Ayurvedic assets."""
    return await ip_service.evaluate_ip(db=db, user_id=current_user.id, request=request)

@router.get("/{id}", response_model=IPAssessmentResponse)
async def get_ip_assessment(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve details of a past IP assessment."""
    assessment = await ip_service.get_assessment(db=db, user_id=current_user.id, assessment_id=id)
    if not assessment:
        raise HTTPException(status_code=404, detail="IP Assessment not found")
    return assessment
