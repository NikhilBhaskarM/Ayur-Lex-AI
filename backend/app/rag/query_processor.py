from dataclasses import dataclass, field
from typing import Optional, List
import asyncio
from app.services.bhashini_service import BhashiniService

@dataclass
class ProcessedQuery:
    original_query: str
    jurisdiction: str | None
    detected_language: str = "en"
    search_query: str = ""
    topics: List[str] = field(default_factory=list)
    ip_types: List[str] = field(default_factory=list)
    intent: str = "informational"
    requires_clarification: bool = False
    clarification_questions: List[str] = field(default_factory=list)

class QueryProcessor:
    def __init__(self):
        self.bhashini = BhashiniService()

    async def process_query(self, query: str, jurisdiction: str | None = None) -> ProcessedQuery:
        # 1. Multilingual language detection and query expansion
        detected_lang = self.bhashini.detect_language(query)
        search_query, expansions = self.bhashini.expand_multilingual_query(query, detected_lang)
        
        query_lower = search_query.lower()

        # 2. Jurisdiction Detection
        detected_jurisdiction = jurisdiction
        if not detected_jurisdiction:
            if "india" in query_lower or "indian" in query_lower:
                detected_jurisdiction = "India"
            elif "international" in query_lower or "wipo" in query_lower:
                detected_jurisdiction = "International"

        # 3. IP Types Classification
        ip_types = []
        ip_map = {
            "patent": "Patent",
            "पेटेंट": "Patent",
            "trademark": "Trademark",
            "ट्रेडमार्क": "Trademark",
            "gi ": "Geographical Indication",
            "geographical indication": "Geographical Indication",
            "copyright": "Copyright",
            "design": "Design",
            "trade secret": "Trade Secret",
            "pvp": "Plant Variety Protection",
            "plant variety": "Plant Variety Protection"
        }
        for kw, ip_type in ip_map.items():
            if kw in query_lower:
                ip_types.append(ip_type)

        # 4. Topics Classification
        topics = []
        topic_map = {
            "abs": "ABS",
            "access and benefit": "ABS",
            "जैव विविधता": "ABS",
            "tk": "Traditional Knowledge",
            "traditional knowledge": "Traditional Knowledge",
            "पारंपरिक ज्ञान": "Traditional Knowledge",
            "ayush": "AYUSH",
            "food": "Food",
            "cosmetic": "Cosmetic",
            "advertising": "Advertising"
        }
        for kw, topic in topic_map.items():
            if kw in query_lower:
                topics.append(topic)

        return ProcessedQuery(
            original_query=query,
            jurisdiction=detected_jurisdiction,
            detected_language=detected_lang,
            search_query=search_query,
            topics=list(set(topics)),
            ip_types=list(set(ip_types))
        )
