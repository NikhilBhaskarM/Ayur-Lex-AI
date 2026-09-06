from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.classification import ClassificationRequest, ClassificationResponse
from app.services.classification_service import ClassificationService
from app.services.assessment_service import AssessmentService

router = APIRouter(tags=["classification"])
classification_service = ClassificationService()
assessment_service = AssessmentService()

@router.post("", response_model=ClassificationResponse)
async def classify_formulation(
    request: ClassificationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await classification_service.classify_formulation(request)
    
    # Save as assessment
    await assessment_service.save_assessment(
        db=db,
        user_id=current_user.id,
        assessment_type="classification",
        data={"formulation_data": request.model_dump(), "jurisdiction": request.jurisdiction}
    )
    
    return result

@router.get("/{id}")
async def get_classification(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    assessment = await assessment_service.get_assessment(db, current_user.id, id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Classification not found")
    return assessment
