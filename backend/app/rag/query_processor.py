from dataclasses import dataclass, field
import asyncio

@dataclass
class ProcessedQuery:
    original_query: str
    jurisdiction: str | None
    topics: list[str] = field(default_factory=list)
    ip_types: list[str] = field(default_factory=list)
    intent: str = "informational"
    requires_clarification: bool = False
    clarification_questions: list[str] = field(default_factory=list)

class QueryProcessor:
    async def process_query(self, query: str, jurisdiction: str | None = None) -> ProcessedQuery:
        # Run synchronous rules in thread if needed, but it's fast enough here.
        query_lower = query.lower()
        
        detected_jurisdiction = jurisdiction
        if not detected_jurisdiction:
            if "india" in query_lower or "indian" in query_lower:
                detected_jurisdiction = "India"
            elif "international" in query_lower or "wipo" in query_lower:
                detected_jurisdiction = "International"
                
        ip_types = []
        ip_map = {
            "patent": "Patent",
            "trademark": "Trademark",
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
                
        topics = []
        topic_map = {
            "abs": "ABS",
            "access and benefit": "ABS",
            "tk": "Traditional Knowledge",
            "traditional knowledge": "Traditional Knowledge",
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
            topics=list(set(topics)),
            ip_types=list(set(ip_types))
        )
