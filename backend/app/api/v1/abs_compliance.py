from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.abs_compliance import ABSEvaluationRequest, ABSEvaluationResponse
from app.services.abs_compliance_service import ABSComplianceService

router = APIRouter(tags=["abs_compliance"])
abs_service = ABSComplianceService()

@router.post("/evaluate", response_model=ABSEvaluationResponse)
@router.post("", response_model=ABSEvaluationResponse)
async def evaluate_abs(
    request: ABSEvaluationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Evaluate Biological Diversity Act compliance, Section 3 vs Section 7, and NBA Form I-IV obligations."""
    return await abs_service.evaluate_abs(db=db, user_id=current_user.id, request=request)

@router.get("/{id}", response_model=ABSEvaluationResponse)
async def get_abs_assessment(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve details of a past ABS compliance assessment."""
    assessment = await abs_service.get_assessment(db=db, user_id=current_user.id, assessment_id=id)
    if not assessment:
        raise HTTPException(status_code=404, detail="ABS Assessment not found")
    return assessment
