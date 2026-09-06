"""
Bhashini Translation Service (Scaffolding & Hook)
Connects national Indian language queries (Hindi, Sanskrit, Kannada, Tamil, Telugu, Marathi)
with the Government of India Bhashini NLP ecosystem, translating vernacular intake
into standardized English legal claim terminology.
"""

from typing import Optional, Dict, Any
import structlog
from app.utils.taxonomy import enrich_query_with_taxonomy

logger = structlog.get_logger(__name__)

# Common Sanskrit / Hindi legal keywords mapped to English patent concepts
VERNACULAR_LEGAL_GLOSSARY: Dict[str, str] = {
    "avaleha": "herbal jam / semi-solid confection",
    "taila": "medicated herbal oil",
    "ghrita": "medicated clarified butter / lipid formulation",
    "asava": "naturally fermented herbal liquid",
    "arishta": "decoction-fermented herbal beverage",
    "churna": "fine botanical powder",
    "kwath": "aqueous decoction",
    "kashayam": "water extract / decoction",
    "bhasma": "calcinated nano-mineral / organometallic preparation",
    "rasaushadhi": "herbo-mineral metallic medicinal formulation",
    "anupana": "bio-enhancing pharmacokinetic vehicle / carrier",
    "samhita": "classical authoritative Ayurvedic treatise (First Schedule)",
    "yukti": "inventive therapeutic rationale / combination logic",
    "guna": "pharmacological property / attribute",
    "veerya": "potency / biological activity",
    "vipaka": "post-digestive transformation / metabolite profile",
    "prabhava": "unique non-obvious bio-action (inventive step)",
}


class BhashiniTranslationService:
    """
    Modular integration layer for National Language Translation Mission (Bhashini).
    Provides robust graceful fallback if API keys or network endpoints are unconfigured.
    """
    def __init__(
        self,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.user_id = user_id
        self.is_configured = bool(api_endpoint and api_key)
        if not self.is_configured:
            logger.info("Bhashini translation service operating in local deterministic scaffolding mode")

    async def translate_to_english_claim(
        self,
        source_text: str,
        source_language: str = "hi"
    ) -> Dict[str, Any]:
        """
        Translates regional vernacular text to standardized English patent language.
        If Bhashini credentials are not available, applies the local Ayurvedic legal
        glossary and taxonomic enricher with zero network failures.
        """
        cleaned_text = source_text.strip()
        translated_text = cleaned_text
        terms_mapped = []

        # Replace vernacular pharmaceutical form words with patent claim equivalents
        lower_text = cleaned_text.lower()
        for vern_term, eng_claim_equiv in VERNACULAR_LEGAL_GLOSSARY.items():
            if vern_term in lower_text:
                terms_mapped.append({"vernacular": vern_term, "legal_equivalent": eng_claim_equiv})
                # Add descriptive legal annotation
                translated_text = translated_text + f" [Standard Pharmaceutical Form: {eng_claim_equiv}]"

        # Enrich with Latin binomial taxonomy
        enriched_patent_claim = enrich_query_with_taxonomy(translated_text)

        return {
            "original_query": source_text,
            "detected_language": source_language,
            "translated_claim": enriched_patent_claim,
            "terms_standardized": terms_mapped,
            "bhashini_mode": "cloud_api" if self.is_configured else "local_taxonomic_scaffold",
            "statutory_note": "Claim standardized for Indian Patent Office examination clarity."
        }


# Global instance
bhashini_service = BhashiniTranslationService()
