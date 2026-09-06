import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse
import structlog
from app.config import settings

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

logger = structlog.get_logger(__name__)

@dataclass
class CrawlResult:
    url: str
    markdown_content: str
    content_hash: str  # SHA-256 of markdown_content
    title: str
    links: list[str] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None

class Crawl4AICrawler:
    def __init__(self):
        self.browser_config = BrowserConfig(
            headless=getattr(settings, "CRAWLER_HEADLESS", True),
            browser_type=getattr(settings, "CRAWLER_BROWSER_TYPE", "chromium"),
            user_agent=getattr(settings, "CRAWLER_USER_AGENT", "AyurvedaIPR-Bot/1.0"),
            verbose=getattr(settings, "CRAWLER_VERBOSE", False)
        )

    async def crawl_url(self, url: str, css_selector: str | None = None, exclude_selectors: list[str] | None = None, wait_for: str | None = None) -> CrawlResult:
        try:
            logger.info("Crawling URL", url=url)
            excluded_selector = ','.join(exclude_selectors) if exclude_selectors else None
            
            run_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                page_timeout=getattr(settings, "CRAWLER_PAGE_TIMEOUT", 30000),
                css_selector=css_selector,
                excluded_selector=excluded_selector,
                wait_for=wait_for
            )
            
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=url, config=run_config)
                
            if result.success:
                content = result.markdown_v2.raw_markdown if hasattr(result, 'markdown_v2') and result.markdown_v2 else result.markdown
                content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                title = result.metadata.get('title', url) if result.metadata else url
                
                links = [link.get('href') for link in result.links.get('internal', []) if link.get('href')]
                
                return CrawlResult(
                    url=url,
                    markdown_content=content,
                    content_hash=content_hash,
                    title=title,
                    links=links,
                    success=True
                )
            else:
                error_msg = result.error_message if hasattr(result, 'error_message') else "Unknown error"
                logger.error("Crawl failed", url=url, error=error_msg)
                return CrawlResult(
                    url=url,
                    markdown_content="",
                    content_hash="",
                    title="",
                    success=False,
                    error=error_msg
                )
                
        except Exception as e:
            logger.exception("Exception during crawl", url=url, error=str(e))
            return CrawlResult(
                url=url,
                markdown_content="",
                content_hash="",
                title="",
                success=False,
                error=str(e)
            )

    async def crawl_source(self, source, semaphore: asyncio.Semaphore | None = None) -> list[CrawlResult]:
        config = source.config or {}
        seed_urls = [source.url] + config.get('additional_urls', [])
        css_selector = config.get('css_selector')
        exclude_selectors = config.get('exclude_selectors')
        wait_for = config.get('wait_for')
        
        follow_internal = config.get('follow_internal_links', getattr(settings, "CRAWLER_FOLLOW_INTERNAL_LINKS", True))
        max_depth = config.get('max_depth', getattr(settings, "CRAWLER_MAX_DEPTH", 2))
        max_pages = config.get('max_pages', getattr(settings, "CRAWLER_MAX_PAGES_PER_SOURCE", 15))

        base_domain = urlparse(source.url).netloc

        queue = [(u, 0) for u in seed_urls]
        visited = set()
        results = []

        while queue and len(results) < max_pages:
            url, depth = queue.pop(0)

            # Strip fragments for deduplication
            clean_url = url.split('#')[0].rstrip('/')
            if clean_url in visited:
                continue
            visited.add(clean_url)

            if semaphore:
                async with semaphore:
                    res = await self.crawl_url(url, css_selector, exclude_selectors, wait_for)
            else:
                res = await self.crawl_url(url, css_selector, exclude_selectors, wait_for)

            results.append(res)

            # Follow internal links if enabled and within depth limit
            if follow_internal and res.success and depth < max_depth and len(results) + len(queue) < max_pages * 2:
                for link in res.links:
                    full_url = urljoin(url, link).split('#')[0].rstrip('/')
                    parsed_link = urlparse(full_url)
                    # Check same domain and valid scheme
                    if parsed_link.scheme in ("http", "https") and parsed_link.netloc == base_domain:
                        if full_url not in visited and not any(q[0] == full_url for q in queue):
                            queue.append((full_url, depth + 1))

            # Rate limiting
            await asyncio.sleep(getattr(settings, "CRAWLER_RATE_LIMIT_SECONDS", 1))

        logger.info(
            "Crawl source completed",
            source_name=source.name,
            pages_crawled=len(results),
            visited_count=len(visited)
        )
        return results
