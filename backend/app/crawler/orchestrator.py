import asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.models import Source, IngestionJob, IngestionLog
from app.crawler.crawler import Crawl4AICrawler
from app.crawler.change_detector import ChangeDetector
from app.ingestion.pipeline import IngestionPipeline
from app.config import settings

logger = structlog.get_logger(__name__)

class CrawlOrchestrator:
    def __init__(self):
        self.crawler = Crawl4AICrawler()
        self.change_detector = ChangeDetector()
        self.pipeline = IngestionPipeline()

    async def run_crawl_job(self, db: AsyncSession, source_id: uuid.UUID, force_reindex: bool = False) -> IngestionJob:
        source_result = await db.execute(select(Source).where(Source.id == source_id))
        source = source_result.scalar_one_or_none()
        
        if not source:
            raise ValueError(f"Source {source_id} not found")
        if not source.is_active:
            raise ValueError(f"Source {source_id} is inactive")
            
        job = IngestionJob(
            id=uuid.uuid4(),
            source_id=source_id,
            status='running',
            job_type='crawl',
            documents_found=0,
            documents_processed=0,
            documents_failed=0,
            chunks_created=0,
            errors=[],
            started_at=datetime.now(timezone.utc)
        )
        db.add(job)
        
        initial_log = IngestionLog(
            id=uuid.uuid4(),
            job_id=job.id,
            level='info',
            message=f'Starting crawl for source: {source.name}',
            created_at=datetime.now(timezone.utc)
        )
        db.add(initial_log)
        await db.commit()
        
        try:
            semaphore = asyncio.Semaphore(getattr(settings, "CRAWLER_MAX_CONCURRENT", 3))
            crawl_results = await self.crawler.crawl_source(source, semaphore)
            
            for result in crawl_results:
                if not result.success:
                    logger.error("Crawl failed for URL", url=result.url, error=result.error)
                    job.documents_failed += 1
                    err_log = IngestionLog(
                        id=uuid.uuid4(),
                        job_id=job.id,
                        level='error',
                        message=f'Crawl failed for {result.url}: {result.error}',
                        created_at=datetime.now(timezone.utc)
                    )
                    db.add(err_log)
                    continue
                    
                job.documents_found += 1
                
                change_result = await self.change_detector.detect_changes(db, source_id, result.url, result.content_hash)
                
                if not change_result.has_changed and not force_reindex:
                    logger.info("Unchanged content, skipping", url=result.url)
                    continue
                    
                metadata = {
                    "source_name": source.name,
                    "authority": source.authority,
                    "jurisdiction": source.jurisdiction,
                    "country": source.country,
                }
                
                ingestion_result = await self.pipeline.ingest_document(
                    db=db,
                    source_id=source_id,
                    url=result.url,
                    title=result.title,
                    content=result.markdown_content,
                    metadata=metadata
                )
                
                job.documents_processed += 1
                job.chunks_created += ingestion_result.chunks_created
                
                success_log = IngestionLog(
                    id=uuid.uuid4(),
                    job_id=job.id,
                    document_id=ingestion_result.document_id,
                    level='info',
                    message=f'Successfully ingested {result.url}',
                    created_at=datetime.now(timezone.utc)
                )
                db.add(success_log)
                
            source.last_crawled = datetime.now(timezone.utc)
            job.status = 'completed'
            job.completed_at = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.exception("Crawl job failed", source_id=str(source_id), error=str(e))
            job.status = 'failed'
            job.completed_at = datetime.now(timezone.utc)
            job.errors = [{"error": str(e)}]
            
            fail_log = IngestionLog(
                id=uuid.uuid4(),
                job_id=job.id,
                level='error',
                message=f'Job failed: {str(e)}',
                created_at=datetime.now(timezone.utc)
            )
            db.add(fail_log)
            
        finally:
            await db.commit()
            
        return job

    async def run_crawl_all(self, db: AsyncSession, force_reindex: bool = False) -> list[IngestionJob]:
        sources_result = await db.execute(select(Source).where(Source.is_active == True))
        sources = sources_result.scalars().all()
        
        jobs = []
        for source in sources:
            job = await self.run_crawl_job(db, source.id, force_reindex)
            jobs.append(job)
            
        return jobs
