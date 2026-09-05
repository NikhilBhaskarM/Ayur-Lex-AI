import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import Assessment
import structlog
from typing import Any

logger = structlog.get_logger(__name__)

class AssessmentService:
    async def save_assessment(self, db: AsyncSession, user_id: uuid.UUID, assessment_type: str, data: dict[str, Any]) -> Assessment:
        assessment = Assessment(
            id=uuid.uuid4(),
            user_id=user_id,
            assessment_type=assessment_type,
            formulation_data=data.get("formulation_data", {}),
            jurisdiction=data.get("jurisdiction", "india"),
            status="completed"
        )
        db.add(assessment)
        await db.commit()
        await db.refresh(assessment)
        return assessment

    async def get_user_assessments(self, db: AsyncSession, user_id: uuid.UUID, page: int = 1, page_size: int = 10) -> tuple[list[Assessment], int]:
        stmt = select(Assessment).where(Assessment.user_id == user_id).order_by(desc(Assessment.created_at)).offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(stmt)
        assessments = result.scalars().all()
        
        # total count
        # In a real app we would do a separate count query
        total_stmt = select(Assessment).where(Assessment.user_id == user_id)
        total = len((await db.execute(total_stmt)).scalars().all())
        
        return list(assessments), total

    async def get_assessment(self, db: AsyncSession, user_id: uuid.UUID, assessment_id: uuid.UUID) -> Assessment | None:
        stmt = select(Assessment).where(Assessment.id == assessment_id, Assessment.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
