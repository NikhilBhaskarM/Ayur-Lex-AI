"""
Document Ingestion Pipeline

Orchestrates the full document ingestion process:
parse → hash → deduplicate → chunk → embed → store
"""

import uuid
import hashlib
from dataclasses import dataclass
from typing import Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.ingestion.parser import DocumentParser
from app.ingestion.chunker import TextChunker
from app.embeddings.factory import get_embedding_provider
from app.rag.vector_search import VectorStore
from app.models import Document, DocumentVersion, DocumentChunk, Source

logger = structlog.get_logger(__name__)


@dataclass
class IngestionResult:
    document_id: uuid.UUID
    version_id: uuid.UUID
    chunks_created: int
    is_update: bool
    content_hash: str


class IngestionPipeline:
    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = TextChunker()
        self._embedding_provider = None
        self._vector_store = None

    @property
    def embedding_provider(self):
        if self._embedding_provider is None:
            self._embedding_provider = get_embedding_provider()
        return self._embedding_provider

    @property
    def vector_store(self):
        if self._vector_store is None:
            self._vector_store = VectorStore()
        return self._vector_store

    async def ingest_document(
        self,
        db: AsyncSession,
        source_id: uuid.UUID,
        file_path: Optional[str] = None,
        url: Optional[str] = None,
        title: str = "Untitled",
        metadata: Optional[dict] = None,
    ) -> IngestionResult:
        """
        Ingest a document from file or URL into the knowledge base.

        Steps:
        1. Parse document (PDF/HTML/text)
        2. Calculate content hash
        3. Check for existing version with same hash (skip if unchanged)
        4. Create/update document and version in DB
        5. Chunk the content
        6. Generate embeddings for chunks
        7. Store chunks in PostgreSQL
        8. Upsert embeddings to Qdrant
        """
        metadata = metadata or {}
        logger.info(
            "Starting document ingestion",
            source_id=str(source_id),
            title=title,
            file_path=file_path,
            url=url,
        )

        # 1. Parse document
        if file_path and file_path.lower().endswith(".pdf"):
            parsed = await self.parser.parse_pdf(file_path)
        elif url:
            parsed = await self.parser.parse_html(url)
        elif file_path:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            parsed = await self.parser.parse_text(content)
        else:
            raise ValueError("Either file_path or url must be provided")

        if not parsed.content.strip():
            raise ValueError("Parsed document has no content")

        # 2. Content hash
        content_hash = hashlib.sha256(parsed.content.encode("utf-8")).hexdigest()

        # 3. Load source for metadata
        source_result = await db.execute(select(Source).where(Source.id == source_id))
        source = source_result.scalar_one_or_none()
        if not source:
            raise ValueError(f"Source {source_id} not found")

        # 4. Check for existing document with same title under this source
        existing_doc_result = await db.execute(
            select(Document).where(
                Document.source_id == source_id,
                Document.title == title,
            )
        )
        existing_doc = existing_doc_result.scalar_one_or_none()

        is_update = False

        if existing_doc:
            # Check if content has changed
            latest_version_result = await db.execute(
                select(DocumentVersion)
                .where(DocumentVersion.document_id == existing_doc.id)
                .order_by(DocumentVersion.version_number.desc())
                .limit(1)
            )
            latest_version = latest_version_result.scalar_one_or_none()

            if latest_version and latest_version.content_hash == content_hash:
                logger.info("Document unchanged, skipping", document_id=str(existing_doc.id))
                return IngestionResult(
                    document_id=existing_doc.id,
                    version_id=latest_version.id,
                    chunks_created=0,
                    is_update=False,
                    content_hash=content_hash,
                )

            # Archive the old version
            if latest_version:
                latest_version.version_status = "archived"
                is_update = True

            doc = existing_doc
            next_version_number = (latest_version.version_number + 1) if latest_version else 1
        else:
            # Create new document
            doc = Document(
                id=uuid.uuid4(),
                source_id=source_id,
                title=title,
                document_type=metadata.get("document_type", "legislation"),
                jurisdiction=source.jurisdiction,
                country=source.country,
                statute=metadata.get("statute"),
                status="current",
                language=metadata.get("language", "en"),
                metadata_=metadata,
                topics=metadata.get("topics", []),
            )
            db.add(doc)
            next_version_number = 1

        # 5. Create new version
        version = DocumentVersion(
            id=uuid.uuid4(),
            document_id=doc.id,
            version_number=next_version_number,
            content_hash=content_hash,
            raw_content=parsed.content,
            source_url=url or file_path,
            version_status="current",
        )
        db.add(version)
        await db.flush()

        # 6. Chunk the content
        chunks = self.chunker.chunk_text(
            text=parsed.content,
            chunk_size=512,
            chunk_overlap=50,
            metadata={
                "source_title": title,
                "authority": source.authority,
                "jurisdiction": source.jurisdiction,
                "country": source.country,
                "authority_level": source.authority_level,
                "source_url": url or file_path,
                "status": "current",
                **{k: v for k, v in metadata.items() if k in ("section", "rule", "article", "topics")},
            },
        )

        # 7. Generate embeddings
        chunk_texts = [c.content for c in chunks]
        embeddings = await self.embedding_provider.embed_texts(chunk_texts)

        # 8. Store chunks in PostgreSQL and Qdrant
        qdrant_points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = uuid.uuid4()

            # PostgreSQL chunk record
            db_chunk = DocumentChunk(
                id=chunk_id,
                document_version_id=version.id,
                document_id=doc.id,
                chunk_index=i,
                content=chunk.content,
                section=chunk.metadata.get("section"),
                rule=chunk.metadata.get("rule"),
                article=chunk.metadata.get("article"),
                metadata_=chunk.metadata,
                embedding_model=self.embedding_provider.model_name,
            )
            db.add(db_chunk)

            # Qdrant point
            qdrant_points.append({
                "id": str(chunk_id),
                "vector": embedding,
                "content": chunk.content,
                "metadata": {
                    "chunk_id": str(chunk_id),
                    "document_id": str(doc.id),
                    "source_title": title,
                    "authority": source.authority,
                    "jurisdiction": source.jurisdiction,
                    "country": source.country or "",
                    "authority_level": source.authority_level,
                    "source_url": url or file_path or "",
                    "status": "current",
                    "document_type": doc.document_type,
                    "section": chunk.metadata.get("section", ""),
                    "rule": chunk.metadata.get("rule", ""),
                    "article": chunk.metadata.get("article", ""),
                    "topics": metadata.get("topics", []),
                },
            })

        # Initialize and upsert to Qdrant
        await self.vector_store.initialize()
        if qdrant_points:
            await self.vector_store.upsert(qdrant_points)

        await db.commit()

        logger.info(
            "Document ingestion complete",
            document_id=str(doc.id),
            version_id=str(version.id),
            chunks_created=len(chunks),
            is_update=is_update,
        )

        return IngestionResult(
            document_id=doc.id,
            version_id=version.id,
            chunks_created=len(chunks),
            is_update=is_update,
            content_hash=content_hash,
        )
