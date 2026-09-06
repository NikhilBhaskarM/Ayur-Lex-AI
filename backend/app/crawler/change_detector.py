from dataclasses import dataclass
from typing import Optional
from uuid import UUID
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Document, DocumentVersion

logger = structlog.get_logger(__name__)

@dataclass
class ChangeResult:
    has_changed: bool
    change_type: str  # 'new', 'updated', 'unchanged'
    previous_hash: Optional[str] = None
    new_hash: str = ''
    previous_version_id: Optional[UUID] = None

class ChangeDetector:
    async def detect_changes(self, db: AsyncSession, source_id: UUID, url: str, new_content_hash: str) -> ChangeResult:
        logger.info("Detecting changes", source_id=str(source_id), url=url)
        
        query = (
            select(DocumentVersion)
            .join(Document, Document.id == DocumentVersion.document_id)
            .where(Document.source_id == source_id)
            .where(DocumentVersion.source_url == url)
            .order_by(DocumentVersion.version_number.desc())
            .limit(1)
        )
        
        result = await db.execute(query)
        latest_version = result.scalar_one_or_none()
        
        if not latest_version:
            logger.info("No existing version found, marking as new", url=url)
            return ChangeResult(
                has_changed=True,
                change_type='new',
                new_hash=new_content_hash
            )
            
        previous_hash = latest_version.content_hash
        previous_version_id = latest_version.id
        
        if previous_hash == new_content_hash:
            logger.info("Content unchanged", url=url, version_id=str(previous_version_id))
            return ChangeResult(
                has_changed=False,
                change_type='unchanged',
                previous_hash=previous_hash,
                new_hash=new_content_hash,
                previous_version_id=previous_version_id
            )
            
        logger.info("Content updated", url=url, previous_hash=previous_hash, new_hash=new_content_hash)
        return ChangeResult(
            has_changed=True,
            change_type='updated',
            previous_hash=previous_hash,
            new_hash=new_content_hash,
            previous_version_id=previous_version_id
        )
