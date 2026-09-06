import asyncio
import os
import sys
import uuid
from sqlalchemy import select

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)

from app.database import init_db
from app.models.source import Source

sources_data = [
    {
        "name": "India Code — Digital Repository of Statutes & Rules",
        "authority": "Legislative Department, Ministry of Law and Justice",
        "source_type": "legislation",
        "url": "https://www.indiacode.nic.in",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly",
        "config": {"css_selector": "#content-area, .act-content, .main-content", "exclude_selectors": ["nav", "footer", ".breadcrumb", ".sidebar"]}
    },
    {
        "name": "IP India Public Databases (InPASS, Trade Marks, GI Registry)",
        "authority": "Office of the Controller General of Patents, Designs & Trade Marks (CGPDTM)",
        "source_type": "database",
        "url": "https://ipindia.gov.in",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".content-area, #main-content", "exclude_selectors": ["nav", "footer", ".header-top"]}
    },
    {
        "name": "National Biodiversity Authority (NBA / ABS Portal)",
        "authority": "National Biodiversity Authority (NBA)",
        "source_type": "legislation",
        "url": "https://nbaindia.org",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".main-content, #content", "exclude_selectors": ["nav", "footer", ".sidebar"]}
    },
    {
        "name": "Traditional Knowledge Digital Library (TKDL)",
        "authority": "CSIR & Ministry of Ayush",
        "source_type": "guideline",
        "url": "https://www.tkdl.res.in",
        "authority_level": 2,
        "jurisdiction": "India",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".content, #main", "exclude_selectors": ["nav", "footer"]}
    },
    {
        "name": "The Patents Act, 1970 (as amended)",
        "authority": "Office of the Controller General of Patents, Designs & Trade Marks",
        "source_type": "legislation",
        "url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly"
    },
    {
        "name": "The Drugs and Cosmetics Act, 1940 & Rules, 1945",
        "authority": "Ministry of Ayush / CDSCO",
        "source_type": "legislation",
        "url": "https://www.indiacode.nic.in",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly"
    },
    {
        "name": "The Biological Diversity Act, 2002 & Amendment Act, 2023",
        "authority": "National Biodiversity Authority (NBA)",
        "source_type": "legislation",
        "url": "https://nbaindia.org",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly"
    },
    {
        "name": "Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
        "authority": "Food Safety and Standards Authority of India (FSSAI)",
        "source_type": "regulation",
        "url": "https://fssai.gov.in",
        "authority_level": 2,
        "jurisdiction": "India",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".main-content, #content-area", "exclude_selectors": ["nav", "footer", ".sidebar"]}
    },
    {
        "name": "The Trade Marks Act, 1999",
        "authority": "Trade Marks Registry / CGPDTM",
        "source_type": "legislation",
        "url": "https://ipindia.gov.in",
        "authority_level": 1,
        "jurisdiction": "India",
        "crawl_frequency": "monthly"
    },
    {
        "name": "Ayurvedic Pharmacopoeia of India (API)",
        "authority": "Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H)",
        "source_type": "guideline",
        "url": "https://pcimh.gov.in",
        "authority_level": 2,
        "jurisdiction": "India",
        "crawl_frequency": "monthly"
    },
    {
        "name": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge",
        "authority": "World Intellectual Property Organization (WIPO)",
        "source_type": "treaty",
        "url": "https://www.wipo.int/tk/en/",
        "authority_level": 1,
        "jurisdiction": "International",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".main-content, article", "exclude_selectors": ["nav", "footer", ".sidebar", ".cookie-banner"]}
    },
    {
        "name": "Nagoya Protocol on Access to Genetic Resources and Benefit-Sharing",
        "authority": "Convention on Biological Diversity (CBD)",
        "source_type": "treaty",
        "url": "https://www.cbd.int/abs/",
        "authority_level": 1,
        "jurisdiction": "International",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".main-content, article", "exclude_selectors": ["nav", "footer", ".sidebar"]}
    },
    {
        "name": "EU Traditional Herbal Medicinal Products Directive (Directive 2004/24/EC)",
        "authority": "European Medicines Agency (EMA)",
        "source_type": "regulation",
        "url": "https://www.ema.europa.eu",
        "authority_level": 2,
        "jurisdiction": "International",
        "crawl_frequency": "monthly",
        "config": {"css_selector": ".main-content, article", "exclude_selectors": ["nav", "footer", ".sidebar", ".cookie-banner"]}
    }
]

async def seed_sources():
    await init_db()
    from app.database import async_session_maker
    async with async_session_maker() as session:
        try:
            for s in sources_data:
                # Check if source already exists
                existing = await session.execute(select(Source).where(Source.name == s["name"]))
                if existing.scalars().first():
                    continue

                source = Source(
                    id=uuid.uuid4(),
                    name=s["name"],
                    authority=s["authority"],
                    source_type=s["source_type"],
                    url=s["url"],
                    authority_level=s["authority_level"],
                    jurisdiction=s["jurisdiction"],
                    country=s.get("country", "IN"),
                    crawl_frequency=s["crawl_frequency"],
                    config=s.get("config"),
                    is_active=True
                )
                session.add(source)
            await session.commit()
            print("[SUCCESS] Successfully seeded authoritative legal sources into database!")
        except Exception as e:
            print(f"[ERROR] Error seeding sources: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_sources())
