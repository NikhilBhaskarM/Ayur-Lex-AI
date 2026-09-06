import os
import hashlib
from dataclasses import dataclass
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class ParsedDocument:
    title: str
    content: str
    metadata: dict
    content_hash: str

class DocumentParser:
    async def parse_pdf(self, file_path: str) -> ParsedDocument:
        """Parse PDF document using PyMuPDF (fitz) page-by-page."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at {file_path}")

        logger.info("Parsing PDF document", file_path=file_path)
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            
            pages_text = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text("text")
                if page_text.strip():
                    pages_text.append(f"--- Page {page_num + 1} ---\n{page_text.strip()}")
            
            content = "\n\n".join(pages_text)
            
            # Extract PDF metadata
            doc_meta = doc.metadata or {}
            title = doc_meta.get("title") or os.path.splitext(os.path.basename(file_path))[0]
            metadata = {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "page_count": len(doc),
                "author": doc_meta.get("author", ""),
                "subject": doc_meta.get("subject", ""),
                "keywords": doc_meta.get("keywords", ""),
            }
            doc.close()

            if not content.strip():
                content = f"[Empty or Scanned PDF with no selectable text: {os.path.basename(file_path)}]"

            return ParsedDocument(
                title=title,
                content=content,
                metadata=metadata,
                content_hash=self._calculate_hash(content)
            )
        except Exception as e:
            logger.error("Failed to parse PDF with PyMuPDF", file_path=file_path, error=str(e))
            raise ValueError(f"Error parsing PDF document: {e}")

    async def parse_html(self, url: str) -> ParsedDocument:
        """Parse HTML from URL or raw HTML using trafilatura and BeautifulSoup."""
        logger.info("Parsing HTML content", url=url)
        content = ""
        title = "HTML Document"
        
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                resp = await client.get(url, headers={"User-Agent": "AyurvedaIPR-Bot/1.0"})
                html_text = resp.text
        except Exception as e:
            logger.warning("Failed to fetch HTML via HTTP", url=url, error=str(e))
            html_text = ""

        if html_text:
            try:
                import trafilatura
                extracted = trafilatura.extract(html_text, include_links=True, output_format="txt")
                if extracted:
                    content = extracted
                
                # Extract title
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_text, "html.parser")
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()
            except Exception as e:
                logger.warning("Trafilatura extraction failed, falling back to BeautifulSoup", error=str(e))
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                content = soup.get_text(separator="\n").strip()
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()

        if not content:
            content = f"[HTML Document from {url}]"

        return ParsedDocument(
            title=title,
            content=content,
            metadata={"url": url},
            content_hash=self._calculate_hash(content)
        )

    async def parse_text(self, content: str, title: str = "Text Document", metadata: Optional[dict] = None) -> ParsedDocument:
        """Parse plain text content."""
        return ParsedDocument(
            title=title,
            content=content,
            metadata=metadata or {},
            content_hash=self._calculate_hash(content)
        )

    async def parse_markdown(self, content: str, title: str = "Markdown Document", url: Optional[str] = None, metadata: Optional[dict] = None) -> ParsedDocument:
        """Parse markdown content (e.g. from Crawl4AI)."""
        meta = metadata or {}
        if url:
            meta["url"] = url
        return ParsedDocument(
            title=title,
            content=content,
            metadata=meta,
            content_hash=self._calculate_hash(content)
        )

    def _calculate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
