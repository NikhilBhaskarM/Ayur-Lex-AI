import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import structlog

from app.models import HumanReview, User
from app.schemas.human_review import HumanReviewCreate, HumanReviewUpdate

logger = structlog.get_logger(__name__)

class HumanReviewService:
    async def create_review(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        request: HumanReviewCreate
    ) -> HumanReview:
        logger.info("Creating human review request", user_id=str(user_id), topic=request.topic)
        
        # Store topic in ai_assessment dictionary if provided
        ai_data = dict(request.ai_assessment or {})
        ai_data["topic"] = request.topic
        
        now = datetime.now(timezone.utc)
        review = HumanReview(
            id=uuid.uuid4(),
            assessment_id=request.assessment_id,
            user_id=user_id,
            status="new",
            user_question=request.user_question,
            ai_assessment=ai_data,
            facilitator_notes="",
            final_guidance="",
            priority=request.priority.lower(),
            created_at=now
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def list_reviews(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        role: str,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[HumanReview]:
        stmt = select(HumanReview)
        
        # Regular users only see their own requests; Facilitator and Admin see all
        if role.upper() not in ("ADMIN", "FACILITATOR"):
            stmt = stmt.where(HumanReview.user_id == user_id)
            
        if status:
            stmt = stmt.where(HumanReview.status == status)
            
        stmt = stmt.order_by(desc(HumanReview.created_at)).offset(offset).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_review(
        self,
        db: AsyncSession,
        review_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str
    ) -> Optional[HumanReview]:
        stmt = select(HumanReview).where(HumanReview.id == review_id)
        if role.upper() not in ("ADMIN", "FACILITATOR"):
            stmt = stmt.where(HumanReview.user_id == user_id)
            
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_review(
        self,
        db: AsyncSession,
        review_id: uuid.UUID,
        current_user: User,
        request: HumanReviewUpdate
    ) -> Optional[HumanReview]:
        review = await self.get_review(db, review_id, current_user.id, current_user.role)
        if not review:
            return None

        # Only facilitators and admins can update notes/guidance/status
        if current_user.role.upper() in ("ADMIN", "FACILITATOR"):
            if request.status:
                review.status = request.status
                if request.status == "completed":
                    review.completed_at = datetime.now(timezone.utc)
            if request.facilitator_notes is not None:
                review.facilitator_notes = request.facilitator_notes
            if request.final_guidance is not None:
                review.final_guidance = request.final_guidance
            if request.facilitator_id:
                review.facilitator_id = request.facilitator_id
                review.assigned_at = datetime.now(timezone.utc)
            elif not review.facilitator_id:
                review.facilitator_id = current_user.id
                review.assigned_at = datetime.now(timezone.utc)
        
        if request.priority:
            review.priority = request.priority.lower()

        await db.commit()
        await db.refresh(review)
        return review
