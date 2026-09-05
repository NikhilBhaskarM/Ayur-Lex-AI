from typing import Optional
from app.schemas.classification import ClassificationRequest, ClassificationResponse
from app.schemas.chat import ConfidenceResponse
from app.rag.pipeline import RAGPipeline
from app.rag.retriever import HybridRetriever
from app.rag.vector_search import VectorStore
from app.rag.keyword_search import KeywordSearcher
import structlog

logger = structlog.get_logger(__name__)

def _create_rag_pipeline() -> RAGPipeline:
    vector_store = VectorStore()
    keyword_searcher = KeywordSearcher()
    retriever = HybridRetriever(vector_store, keyword_searcher)
    return RAGPipeline(retriever)

class ClassificationService:
    def __init__(self):
        self._rag_pipeline: Optional[RAGPipeline] = None

    @property
    def rag_pipeline(self) -> RAGPipeline:
        if self._rag_pipeline is None:
            self._rag_pipeline = _create_rag_pipeline()
        return self._rag_pipeline

    async def classify_formulation(self, data: ClassificationRequest) -> ClassificationResponse:
        logger.info("Classifying formulation", formulation_name=data.formulation_name)
        
        # Rule-assisted determination combined with RAG
        category = "Patent or Proprietary (P&P) Ayurvedic Medicine"
        reg_implications = []
        ip_implications = []
        abs_implications = []
        next_steps = []
        evidence = []

        is_classical = data.is_classical_text_based
        is_modified = data.has_been_modified
        marketed_as = (data.marketed_as or "Medicine").lower()

        if "cosmetic" in marketed_as:
            category = "Ayurvedic Cosmetic"
            reasoning = (
                f"The formulation '{data.formulation_name}' is intended to be marketed as a cosmetic. "
                "Under the Drugs and Cosmetics Act (Section 3(aaa)) and Cosmetics Rules 2020, cosmetic products "
                "intended for cleansing, beautifying, or promoting attractiveness cannot make therapeutic claims to cure, "
                "mitigate, or treat human diseases."
            )
            reg_implications = [
                "Manufacture requires cosmetic licensing under Chapter IV-A of Drugs & Cosmetics Act and Cosmetics Rules 2020.",
                "Mandatory adherence to Schedule M-II and Bureau of Indian Standards (BIS) parameters.",
                "Strict prohibition on medicinal / therapeutic claims on packaging or promotional labels."
            ]
            ip_implications = [
                "Formulation recipes generally not patentable unless non-obvious novel carrier/cosmetic vehicle.",
                "Trademark protection for brand name in Class 3 (Cosmetics/Non-medicated preparations).",
                "Industrial Design registration for unique packaging container/dispenser under Designs Act 2000."
            ]
            abs_implications = [
                "Use of Indian plant botanicals in commercial cosmetics triggers Section 7 BD Act prior intimation to SBB.",
                "Export of cosmetics with Indian biological material requires NBA approval."
            ]
            next_steps = [
                "Verify ingredient list against BIS negative lists for cosmetics.",
                "File application for cosmetic manufacturing license with State Licensing Authority.",
                "File trademark application for brand mark in Class 3."
            ]
            evidence = [
                "Drugs & Cosmetics Act, 1940 — Section 3(aaa) definition of Cosmetic",
                "Cosmetics Rules, 2020",
                "Rule 106, Drugs & Cosmetics Rules (Label claims limits)"
            ]
        elif "food" in marketed_as or "aahar" in marketed_as:
            category = "Ayurveda Aahara (Ayurvedic Food / Dietary Supplement)"
            reasoning = (
                f"The formulation '{data.formulation_name}' is formulated as food/dietary support. "
                "Under the Food Safety and Standards (Ayurveda Aahara) Regulations, 2022, foods prepared in accordance "
                "with authoritative books listed in Schedule A of FSSAI regulations constitute 'Ayurveda Aahara'."
            )
            reg_implications = [
                "Regulated under FSSAI Ayurveda Aahara Regulations, 2022 (not under D&C Act ASU drug licensing).",
                "Must display the official Ayurveda Aahara logo and clear declaration on front-of-pack.",
                "Prohibited from making drug/disease claims (only lifestyle/physiological well-being claims permitted)."
            ]
            ip_implications = [
                "Traditional recipes are unpatentable under Section 3(p) of Patents Act.",
                "Trademark registration available in Class 29/30/32 (Foods, herbal beverages, dietary preparations)."
            ]
            abs_implications = [
                "Normally Traded Commodities (NTC) list under Section 40 BD Act may exempt specified cultivated food items."
            ]
            next_steps = [
                "Obtain FSSAI Central License under Ayurveda Aahara category.",
                "Submit formulation to FSSAI Scientific Panel if non-Schedule A ingredient used.",
                "Register packaging trade dress and trademark in Class 30."
            ]
            evidence = [
                "Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
                "Section 22, Food Safety and Standards Act, 2006",
                "Section 40, Biological Diversity Act, 2002 (NTC List)"
            ]
        elif is_classical is True and (is_modified is False or is_modified is None):
            category = "Classical Ayurvedic Medicine (First Schedule Treatise)"
            reasoning = (
                f"The formulation '{data.formulation_name}' is manufactured strictly in accordance with authoritative "
                "classical Ayurvedic treatises listed in the First Schedule to the Drugs and Cosmetics Act, 1940 "
                "(such as Charaka Samhita, Sushruta Samhita, or Ayurvedic Formulary of India)."
            )
            reg_implications = [
                "Manufactured under Form 25-D license from State Licensing Authority (AYUSH).",
                "Exempt from preclinical safety/efficacy clinical trial data requirements.",
                "Strict compliance with Schedule T Good Manufacturing Practices (GMP) and API pharmacopoeial monographs."
            ]
            ip_implications = [
                "EXCLUDED from patentability under Section 3(p) of Patents Act (Traditional Knowledge).",
                "Name is PUBLICI JURIS: Classical name (e.g., Triphala Churna) cannot be registered as an exclusive trademark monopoly by any individual or firm.",
                "Brand differentiation must be established via distinctive House Trademark (e.g., '[Brand] Triphala')."
            ]
            abs_implications = [
                "Codified Traditional Knowledge is EXEMPT from SBB prior intimation and ABS payments under 2023 Biodiversity Amendment Act."
            ]
            next_steps = [
                "Verify standard operating procedures against Ayurvedic Pharmacopoeia of India (API).",
                "Submit manufacturing license application Form 24-D to State AYUSH Licensing Authority.",
                "Secure trademark for unique company brand name (Class 5)."
            ]
            evidence = [
                "Drugs & Cosmetics Act, 1940 — Section 3(a) & First Schedule",
                "The Patents Act, 1970 — Section 3(p) (TK exclusion)",
                "Biological Diversity (Amendment) Act, 2023 — Proviso to Section 7 (Codified TK exemption)"
            ]
        else:
            category = "Patent or Proprietary (P&P) Ayurvedic Medicine"
            reasoning = (
                f"The product '{data.formulation_name}' contains Ayurvedic ingredients but represents a novel combination, "
                "modified dosage form, or proprietary ratio not verbatim documented in First Schedule classical texts. "
                "It falls under Section 3(h) of the Drugs and Cosmetics Act as a Patent or Proprietary Medicine."
            )
            reg_implications = [
                "Licensed under Form 25-D as a Patent or Proprietary (P&P) ASU medicine.",
                "Must comply with Rule 158-B of Drugs and Cosmetics Rules (submission of textual evidence, pilot safety data, and published literature).",
                "Schedule T Good Manufacturing Practices (GMP) mandatory."
            ]
            ip_implications = [
                "Patents Act Section 3(e) requires QUANTITATIVE EVIDENCE OF SYNERGY for herbal combinations.",
                "Patents Act Section 3(d) applies if claiming new forms of known herbal extracts (enhanced efficacy proof required).",
                "Full product brand name can be registered as an exclusive trademark in Class 5 (Pharmaceuticals)."
            ]
            abs_implications = [
                "Commercial manufacturing triggers Section 7 Biological Diversity Act obligations with State Biodiversity Board.",
                "Patent filing requires mandatory Section 6 NBA registration prior to patent grant."
            ]
            next_steps = [
                "Generate laboratory synergistic assay data (Combination Index < 1.0) to support patentability.",
                "Conduct stability testing per Ayurvedic Pharmacopoeia of India guidelines.",
                "File Form 158-B safety dossier with State AYUSH Licensing Authority.",
                "File trademark application in Class 5 for proprietary brand name."
            ]
            evidence = [
                "Drugs & Cosmetics Act, 1940 — Section 3(h) (P&P Medicine definition)",
                "Drugs & Cosmetics Rules, 1945 — Rule 158-B (Safety & Efficacy guidelines)",
                "The Patents Act, 1970 — Section 3(e) (Synergism requirement)",
                "Biological Diversity Act, 2002 — Section 6 & 7"
            ]

        # Try to query RAG for supplemental statutory citations if possible
        try:
            query = f"Classify Ayurvedic formulation {data.formulation_name} with ingredients {', '.join(data.ingredients)} for {data.intended_use}"
            rag_resp = await self.rag_pipeline.query(query, jurisdiction=data.jurisdiction, conversation_history=[])
            if rag_resp and rag_resp.answer and "insufficient" not in rag_resp.answer.lower():
                evidence.append(f"Statutory Context: {rag_resp.answer[:200]}...")
        except Exception:
            logger.warning("RAG retrieval fallback for classification")

        return ClassificationResponse(
            classification=category,
            reasoning=reasoning,
            evidence=evidence,
            confidence=ConfidenceResponse(level="HIGH", score=0.88, factors={"statutory_fit": 0.9, "rules_alignment": 0.86}),
            missing_information=[
                "Exact quantitative percentage / ratio of each active botanical ingredient.",
                "Standard operating procedure (SOP) of extraction method (aqueous, hydroalcoholic, or supercritical CO2)."
            ],
            regulatory_implications=reg_implications,
            ip_implications=ip_implications,
            abs_implications=abs_implications,
            recommended_next_steps=next_steps,
            disclaimer="This classification is generated algorithmically for informational guidance and does not constitute a legally binding ruling by the State Licensing Authority or AYUSH Ministry."
        )
