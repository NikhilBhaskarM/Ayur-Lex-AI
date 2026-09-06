import re
import structlog
from typing import Optional, Dict, Tuple
import httpx
from app.config import settings

logger = structlog.get_logger(__name__)

# Curated Ayurvedic & IPR Multilingual Terminology Lexicon
AYURVEDA_IPR_DICTIONARY = {
    # Herbs & Classical Formulations (Devanagari -> English)
    "हल्दी": "Turmeric / Curcuma longa / Haridra",
    "हरिद्रा": "Haridra / Curcuma longa / Turmeric",
    "नीम": "Neem / Azadirachta indica / Nimba",
    "निम्ब": "Nimba / Azadirachta indica / Neem",
    "अश्वगंधा": "Ashwagandha / Withania somnifera",
    "हयगंधा": "Hayagandha / Withania somnifera",
    "त्रिफला": "Triphala classical formulation (Amalaki, Bibhitaki, Haritaki)",
    "च्यवनप्राश": "Chyawanprash classical formulation",
    "गुग्गुलु": "Guggulu / Commiphora mukul / Guggulipid",
    "तुलसी": "Tulsi / Ocimum sanctum / Holy Basil",
    "ब्राह्मी": "Brahmi / Bacopa monnieri / Medhya Rasayana",
    "मंडूकपर्णी": "Mandukaparni / Centella asiatica",
    "गिलोय": "Giloy / Guduchi / Tinospora cordifolia",
    "गुडूची": "Guduchi / Tinospora cordifolia / Amrita",
    "शतावरी": "Shatavari / Asparagus racemosus",
    "अर्जुन": "Arjuna / Terminalia arjuna",
    "आमलकी": "Amalaki / Emblica officinalis / Amla",
    "आंवला": "Amla / Emblica officinalis / Amalaki",
    "शुंठी": "Shunthi / Zingiber officinale / Dry Ginger",
    "अदरक": "Ginger / Zingiber officinale / Ardraka",
    "पिप्पली": "Pippali / Piper longum / Long Pepper",
    "मरिच": "Maricha / Piper nigrum / Black Pepper",

    # Kannada Herbs (Kannada Script -> English)
    "ಅರಿಶಿನ": "Turmeric / Haridra / Curcuma longa",
    "ಬೇವು": "Neem / Nimba / Azadirachta indica",
    "ಅಶ್ವಗಂಧ": "Ashwagandha / Withania somnifera",
    "ತ್ರಿಫಲ": "Triphala classical formulation",
    "ತುಳಸಿ": "Tulsi / Ocimum sanctum",
    "ನೆಲ್ಲಿಕಾಯಿ": "Amla / Amalaki / Emblica officinalis",

    # Legal & IPR Terms
    "पेटेंट": "Patent / The Patents Act, 1970",
    "ट्रेडमार्क": "Trademark / Trade Marks Act, 1999",
    "भौगोलिक उपदर्शन": "Geographical Indication (GI)",
    "पारंपरिक ज्ञान": "Traditional Knowledge / TKDL / Section 3(p)",
    "जैव विविधता": "Biological Diversity Act, 2002 / NBA",
    "राष्ट्रीय जैव विविधता प्राधिकरण": "National Biodiversity Authority (NBA)",
    "लाभ साझाकरण": "Access and Benefit Sharing (ABS)",
    "पूर्व कला": "Prior Art / Section 3(p)",
    "घाव भरना": "Wound healing / Vranaropana",
    "सूजन": "Anti-inflammatory / Shothahara",
    "रोग प्रतिरोधक": "Immunomodulatory / Rasayana",
    "पाचन": "Digestive / Deepana Pachana",

    # Kannada Legal Terms
    "ಪೇಟೆಂಟ್": "Patent / The Patents Act, 1970",
    "ಸಾಂಪ್ರದಾಯಿಕ ಜ್ಞಾನ": "Traditional Knowledge / TKDL",
    "ಜೈವಿಕ ವೈವಿಧ್ಯತೆ": "Biological Diversity Act",
}

# English to Hindi Legal Phrase Templates for localized response synthesis
EN_TO_HI_TEMPLATES = [
    (r"This information is for informational purposes only and does not constitute legal advice\.",
     "यह जानकारी केवल सूचनात्मक उद्देश्यों के लिए है और यह कानूनी सलाह नहीं है।"),
    (r"Section 3\(p\) of The Patents Act, 1970 bars the patenting of traditional knowledge\.",
     "भारतीय पेटेंट अधिनियम, 1970 की धारा 3(p) पारंपरिक ज्ञान के पेटेंट पर रोक लगाती है।"),
    (r"Classical Ayurvedic formulations cannot be patented\.",
     "शास्त्रीय आयुर्वेदिक योगों (Classical Formulations) का पेटेंट नहीं कराया जा सकता है।"),
    (r"Novelty and inventive step with synergistic efficacy \(Section 3\(e\)\) are required\.",
     "पेटेंट के लिए नवीनता और सहक्रियात्मक प्रभाव (धारा 3(e)) का वैज्ञानिक प्रमाण अनिवार्य है।"),
    (r"Approval from the National Biodiversity Authority \(NBA\) is mandatory\.",
     "राष्ट्रीय जैव विविधता प्राधिकरण (NBA) से पूर्व अनुमति प्राप्त करना अनिवार्य है।"),
]

class BhashiniService:
    def __init__(self):
        self.api_key = getattr(settings, "BHASHINI_API_KEY", None)
        self.user_id = getattr(settings, "BHASHINI_USER_ID", None)
        self.pipeline_url = getattr(
            settings, "BHASHINI_PIPELINE_URL", "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
        )

    def detect_language(self, text: str) -> str:
        """Detect language code based on Unicode character block analysis."""
        if not text:
            return "en"

        devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
        kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', text))
        tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', text))
        total_len = max(len(text.replace(" ", "")), 1)

        if devanagari_count / total_len > 0.15:
            return "hi"
        elif kannada_count / total_len > 0.15:
            return "kn"
        elif tamil_count / total_len > 0.15:
            return "ta"
        return "en"

    def expand_multilingual_query(self, query: str, detected_lang: Optional[str] = None) -> Tuple[str, list[str]]:
        """Expand regional script queries with statutory and botanical English equivalents."""
        lang = detected_lang or self.detect_language(query)
        expanded_tokens = []

        # Scan for vernacular Ayurvedic & legal terms in the query
        for term, expansion in AYURVEDA_IPR_DICTIONARY.items():
            if term in query:
                expanded_tokens.append(expansion)

        if lang != "en":
            # Add general context anchors for Indian legal RAG
            if any(k in query for k in ["पेटेंट", "पೇಟೆಂಟ್", "patent"]):
                expanded_tokens.append("Patents Act 1970 Section 3(p) Section 3(e) prior art")
            if any(k in query for k in ["जैव", "बायो", "ಜೈವಿಕ", "abs"]):
                expanded_tokens.append("Biological Diversity Act NBA Form I Form III ABS")

        if expanded_tokens:
            combined_query = f"{query} {' '.join(expanded_tokens)}"
            logger.info("Bilingual query expanded", original=query, lang=lang, expanded=combined_query)
            return combined_query, expanded_tokens

        return query, []

    async def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Tuple[str, str]:
        """Translate text using Bhashini ULCA API if credentials exist, otherwise using domain fallback."""
        if not text or source_lang.lower() == target_lang.lower():
            return text, "identical"

        # Attempt Bhashini ULCA Pipeline if keys are present
        if self.api_key and self.user_id:
            try:
                translated = await self._call_bhashini_pipeline(text, source_lang, target_lang)
                if translated:
                    return translated, "bhashini"
            except Exception as e:
                logger.warning("Bhashini API call failed, falling back to local lexicon", error=str(e))

        # Fallback: Intelligent domain-specific legal localization
        translated = self._fallback_translate(text, source_lang, target_lang)
        return translated, "ayurvedic_lexicon"

    async def _call_bhashini_pipeline(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Send inference request to Bhashini Dhruva NMT pipeline."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "userID": self.user_id,
        }
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang.lower(),
                            "targetLanguage": target_lang.lower(),
                        }
                    }
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            }
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(self.pipeline_url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                pipeline_response = data.get("pipelineResponse", [])
                if pipeline_response and len(pipeline_response) > 0:
                    output = pipeline_response[0].get("output", [])
                    if output and len(output) > 0:
                        return output[0].get("target")
        return None

    def _fallback_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Domain-specific dictionary and pattern replacement for legal & Ayurvedic texts."""
        result = text

        if target_lang.lower() in ("hi", "hindi"):
            # Apply template translations
            for pattern, replacement in EN_TO_HI_TEMPLATES:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

            # Replace individual key terms
            replace_map = {
                "patent": "पेटेंट (Patent)",
                "patents": "पेटेंट (Patents)",
                "trademark": "ट्रेडमार्क (Trademark)",
                "traditional knowledge": "पारंपरिक ज्ञान (Traditional Knowledge)",
                "prior art": "पूर्व कला (Prior Art)",
                "turmeric": "हल्दी (Turmeric)",
                "neem": "नीम (Neem)",
                "ashwagandha": "अश्वगंधा (Ashwagandha)",
                "wound healing": "घाव भरना (Vranaropana)",
                "biological diversity": "जैव विविधता (Biological Diversity)",
                "synergism": "सहक्रियाशीलता (Synergism)",
            }
            for en_term, hi_term in replace_map.items():
                result = re.sub(rf"\b{en_term}\b", hi_term, result, flags=re.IGNORECASE)

        elif target_lang.lower() in ("en", "english") and source_lang.lower() in ("hi", "kn", "sa"):
            for vernacular_term, en_expansion in AYURVEDA_IPR_DICTIONARY.items():
                if vernacular_term in result:
                    result = result.replace(vernacular_term, en_expansion)

        return result
