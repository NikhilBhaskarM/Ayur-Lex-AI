"""
Ayur-Lex-AI — Adaptive Multi-Tier Heterogeneous Execution Router

Non-destructively intercepts incoming queries before processing and triages them
into three distinct execution tiers:
- TIER 1 ("simple"): Conversational / Trivial / Definitional
  * Bypasses vector search and agent debate. Sub-second direct generation via Llama 3.1 8B / GPT-4o-mini.
- TIER 2 ("statutory"): Direct Statutory & Regulatory Lookups
  * Calls existing hybrid retriever (Qdrant + BM25) and reranker, generating an authoritative
    IRAC statutory response backed by statutory_reasoner.py using DeepSeek-R1 / Qwen-2.5-7B / GPT-4o.
- TIER 3 ("debate"): Complex Formulations & Full Patentability Analysis
  * Triggers the Multi-Agent Adversarial Debate Engine (debate_engine.py) streamed over WebSocket.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import re
import structlog

logger = structlog.get_logger(__name__)

DOMAIN_PERSONA = "Ayur-Lex-AI: Specialized Indian Patent Law & Ayurvedic IPR Engine"

DOMAIN_SYSTEM_PROMPT = """You are Ayur-Lex-AI: Specialized Indian Patent Law & Ayurvedic IPR Engine.

MANDATORY DOMAIN FRAMING DIRECTIVE:
Every query, including basic definitions (e.g., "what is a patent", "what is prior art", "what is an invention"), MUST NEVER receive a generic textbook or non-Indian legal reply. EVERY response MUST be strictly contextualized through the Indian legal and Ayurvedic patenting framework, explicitly analyzing:
1. Indian Patents Act, 1970 statutory exclusions:
   - Section 3(p): Traditional Knowledge Digital Library (TKDL) exclusion of classical Ayurvedic knowledge and duplication of traditional properties documented in ancient treatises (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya).
   - Section 3(e): Mere admixture bar vs demonstrable supra-additive synergism (empirical Combination Index CI < 1.0 or isobolographic analysis).
   - Section 3(d): Enhanced therapeutic efficacy requirement (Novartis AG v. Union of India standard) for modified or incremental formulations.
2. Biological Diversity Act, 2002:
   - Mandatory Section 6 prior approval on Form III from the National Biodiversity Authority (NBA) prior to applying for or sealing patents based on Indian biological resources.
3. High-Value Patentability Thresholds:
   - Standardized extraction fractions (supercritical CO2, solvent extraction matrices), novel non-classical stoichiometric ratios, and synergistic bio-enhancement (pharmacokinetic AUC increases).
"""

CONTEXT_FORCING_INSTRUCTION = """[MANDATORY DOMAIN CONSTRAINT]: You are Ayur-Lex-AI: Specialized Indian Patent Law & Ayurvedic IPR Engine. Do NOT provide a generic textbook legal definition. You MUST contextualize your entire response strictly through Indian Patent Law (The Patents Act, 1970) and Ayurvedic/biological innovations, explicitly analyzing:
1. §3(p) TKDL traditional knowledge bar
2. §3(e) mere admixture vs synergistic combinations (CI < 1.0)
3. §3(d) enhanced therapeutic efficacy (Novartis standard)
4. Biological Diversity Act, 2002 mandatory Form III NBA clearance under Section 6
5. High-value patentability requirements (standardized extraction fractions, synergistic bio-enhancement)
"""


@dataclass
class TierClassification:
    tier: str  # "simple" | "statutory" | "debate"
    model_name: str
    rationale: str
    confidence: float
    statutory_risk_prediction: Dict[str, str] = field(default_factory=dict)
    recommended_action: str = "direct_response"


class AdaptiveRouter:
    """Non-destructive query triage router classifying queries into 3 execution tiers
    with strict domain persona framing."""

    @staticmethod
    def get_domain_persona() -> str:
        return DOMAIN_PERSONA

    @staticmethod
    def get_domain_system_prompt() -> str:
        return DOMAIN_SYSTEM_PROMPT

    @staticmethod
    def apply_domain_context(query: str, tier: str = "simple") -> str:
        """Prepend context-forcing instructions to prevent generic textbook legal replies."""
        return f"{CONTEXT_FORCING_INSTRUCTION}\nUser Query: {query}"

    # Keywords indicative of Tier 1 (Simple definitions, greetings, conversational Ayush facts)
    TIER_1_PATTERNS = [
        r"\b(hi|hello|hey|greetings|good morning|good evening)\b",
        r"\bwhat is (section 3\(?[a-z]\)?|section \d+|tkdl|ayush|ipr|patents?|trademark|copyright|prior art|an invention)\b",
        r"\bwho is (the controller|charaka|sushruta)\b",
        r"\b(can|does) (turmeric|curcumin|neem|tulsi|ginger|amla) (cure|treat|help with)\b",
        r"\bmeaning of (section 3\(?[a-z]\)?|ayurveda|traditional knowledge|prior art)\b",
        r"\bexplain (section 3\(?[a-z]\)?|tkdl|prior art)\b",
        r"\btell me about (tkdl|traditional knowledge)\b",
    ]

    # Keywords indicative of Tier 3 (Formulations, synergy, patentability, extraction, ratios)
    TIER_3_PATTERNS = [
        r"\b(synerg|synergistic|synergism|combination index|ci\s*[<:=]|chou[\s-]talalay)\b",
        r"\b(patentability|can i patent|patentable|is this formulation patentable)\b",
        r"\b(extract|supercritical|solvent fraction|bioavailability|novel ratio|formulation of)\b",
        r"\b(withania|curcuma|piper nigrum|piperine|triphala|polyherbal|composition comprising)\b",
        r"\bsection 3\(?e\)?\b",
        r"\bsection 3\(?p\)?\s*(and|vs|versus)?\s*section 3\(?e\)?\b",
        r"\b(novartis standard|enhanced therapeutic efficacy|mere admixture)\b",
        r"\b(biological diversity act|nba form (iii|1|3)|section 6 bda)\b",
    ]

    # Keywords indicative of Tier 2 (Specific statutes, rules, forms, penalties, gazettes)
    TIER_2_PATTERNS = [
        r"\bsection \d+\b",
        r"\brule \d+[a-z]?\b",
        r"\bform \d+[a-z]?\b",
        r"\b(drugs and cosmetics act|rule 158-?b|form 25-?e|ayush license)\b",
        r"\b(penalty|penalties|punishment|fine|offence|offense) under\b",
        r"\b(ayurveda aahara|fssai regulation|gazette)\b",
        r"\b(bda|biological diversity act|nba approval procedure|state biodiversity board)\b",
        r"\b(first examination report|fer timeline|ipab precedent)\b",
    ]

    def classify_query(self, query: str) -> TierClassification:
        """Triage an incoming legal or technical query into Tier 1, Tier 2, or Tier 3."""
        q_lower = query.lower().strip()

        # 1. Evaluate Tier 3 first: Complex formulations, synergy claims, patent debate candidates
        for pattern in self.TIER_3_PATTERNS:
            if re.search(pattern, q_lower):
                # Calculate preliminary risk indicators
                sec_3p = "High" if any(h in q_lower for h in ["turmeric", "curcumin", "ashwagandha", "neem", "triphala", "traditional"]) else "Medium"
                sec_3e = "Synergistic (CI < 1.0)" if "synerg" in q_lower or "ci" in q_lower else "Admixture Bar"
                bda_risk = "Approval Required" if any(k in q_lower for k in ["bda", "biodiversity", "herb", "extract", "patent"]) else "Exempt"

                logger.info("AdaptiveRouter triaged query to TIER 3 (Debate)", query=query[:50])
                return TierClassification(
                    tier="debate",
                    model_name="Claude 3.5 Sonnet / GPT-4o Multi-Agent Debate",
                    rationale="Complex formulation requiring adversarial novelty defense under §3(e) and statutory IRAC adjudication.",
                    confidence=0.96,
                    statutory_risk_prediction={
                        "sec_3p": sec_3p,
                        "sec_3e": sec_3e,
                        "bda_form3": bda_risk
                    },
                    recommended_action="launch_3d_chamber"
                )

        # 2. Evaluate Tier 1: Conversational / Trivial / Definitional (e.g. 'What is Section 3(p)?')
        for pattern in self.TIER_1_PATTERNS:
            if re.search(pattern, q_lower):
                logger.info("AdaptiveRouter triaged query to TIER 1 (Simple)", query=query[:50])
                return TierClassification(
                    tier="simple",
                    model_name="Llama 3.1 8B (via Ollama) / GPT-4o-mini",
                    rationale="Conversational or definitional inquiry; answered immediately with sub-second direct generation.",
                    confidence=0.98,
                    statutory_risk_prediction={
                        "sec_3p": "Cleared",
                        "sec_3e": "Admixture Bar",
                        "bda_form3": "Exempt"
                    },
                    recommended_action="fast_direct_generation"
                )

        # 3. Evaluate Tier 2: Specific statutory and regulatory lookups
        for pattern in self.TIER_2_PATTERNS:
            if re.search(pattern, q_lower):
                logger.info("AdaptiveRouter triaged query to TIER 2 (Statutory)", query=query[:50])
                return TierClassification(
                    tier="statutory",
                    model_name="DeepSeek-R1 / Qwen-2.5-7B (Statutory Reasoner)",
                    rationale="Specific legislative or regulatory query routed through Qdrant/BM25 retrieval and deterministic statutory reasoner.",
                    confidence=0.94,
                    statutory_risk_prediction={
                        "sec_3p": "Medium",
                        "sec_3e": "Admixture Bar",
                        "bda_form3": "Approval Required"
                    },
                    recommended_action="hybrid_retrieval_and_statutory_synthesis"
                )

        # Default fallback: If query has more than 15 words and mentions botanical or patent terms -> Tier 2
        if len(q_lower.split()) > 15 and any(w in q_lower for w in ["patent", "license", "formulation", "herb", "ingredient", "claim"]):
            return TierClassification(
                tier="statutory",
                model_name="DeepSeek-R1 / Qwen-2.5-7B (Statutory Reasoner)",
                rationale="Multi-clause inquiry requiring legislative retrieval and statutory synthesis.",
                confidence=0.88,
                statutory_risk_prediction={
                    "sec_3p": "Medium",
                    "sec_3e": "Admixture Bar",
                    "bda_form3": "Approval Required"
                },
                recommended_action="hybrid_retrieval_and_statutory_synthesis"
            )

        # Otherwise Tier 1
        return TierClassification(
            tier="simple",
            model_name="Llama 3.1 8B / GPT-4o-mini",
            rationale="General knowledge query processed via fast-tier generation.",
            confidence=0.90,
            statutory_risk_prediction={
                "sec_3p": "Cleared",
                "sec_3e": "Admixture Bar",
                "bda_form3": "Exempt"
            },
            recommended_action="fast_direct_generation"
        )
