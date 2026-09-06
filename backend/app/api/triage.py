"""
Dynamic Formulation & Regulatory Triage Wizard API Router
Classifies formulation intake into five distinct Indian regulatory & patent pathways:
1. Classical / Generic Medicine (First Schedule texts) -> Section 3(p) TKDL bar.
2. Patent or Proprietary (P&P) Medicine -> Section 3(e) mere admixture alert.
3. Phytopharmaceutical / New Drug (CDSCO Rule 122E) -> Section 6 BDA scrutiny.
4. Ayurveda Aahar (FSSAI 2022) -> Non-therapeutic restriction.
5. Ayurvedic Cosmetic (Schedule S) -> Carrier/vehicle novelty required.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import structlog
from app.utils.taxonomy import lookup_herb, generate_standardized_claim_terms

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["triage"])


class TriageClassificationRequest(BaseModel):
    formulation_name: str = Field(..., description="Name or working title of formulation")
    ingredients: List[str] = Field(default=[], description="List of botanical ingredients / extracts")
    indications: Optional[str] = Field(None, description="Intended therapeutic indication or usage")
    dosage_form: Optional[str] = Field(None, description="E.g., tablet, churna, nano-emulsion, oil")
    is_classical_text_based: Optional[bool] = Field(False, description="Whether derived from classical Ayurvedic texts")
    has_clinical_evidence: Optional[bool] = Field(False, description="Whether supported by clinical trial data")
    marketed_as: Optional[str] = Field("medicine", description="Target market category: medicine, food, cosmetic, phytopharma")
    extraction_technology: Optional[str] = Field(None, description="E.g. classical water decoction, supercritical CO2, standardized fraction")


class TriageClassificationResponse(BaseModel):
    formulation_name: str
    category: str
    statutory_hurdle: str
    governing_statutes: List[str]
    regulatory_requirements: List[str]
    patentability_assessment: str
    actionable_recommendations: List[str]
    statutory_risk_score: float
    taxonomic_breakdown: List[Dict[str, Any]]


# Classical First Schedule formulation references
CLASSICAL_KEYWORDS = [
    "triphala", "trikatu", "chyawanprash", "ashwagandharishta", "dashamoola",
    "sitopaladi", "talishadi", "brahmi ghrita", "mahayograj guggulu", "avipattikar",
    "hingwashtak", "chandraprabha", "amritarishta", "khadirarishta", "kumaryasava"
]


@router.post("/classify", response_model=TriageClassificationResponse)
async def classify_formulation_triage(request: TriageClassificationRequest):
    """
    Executes multi-parametric statutory & regulatory triage for Ayurvedic formulations.
    """
    try:
        f_name_lower = request.formulation_name.lower().strip()
        market_lower = (request.marketed_as or "medicine").lower().strip()
        indic_lower = (request.indications or "").lower().strip()
        extract_lower = (request.extraction_technology or "").lower().strip()

        # Build taxonomic data
        taxonomic_data = generate_standardized_claim_terms(request.ingredients)

        # -------------------------------------------------------------
        # 1. Ayurvedic Cosmetic (Schedule S / Cosmetics Rules 2020)
        # -------------------------------------------------------------
        if "cosmetic" in market_lower or any(kw in indic_lower for kw in ["skin whitening", "beautifying", "anti-aging cosmetic", "hair dye", "complexion"]):
            category = "Ayurvedic Cosmetic (Schedule S / Cosmetics Rules 2020)"
            hurdle = "Carrier / Vehicle Novelty Required (Therapeutic Claim Prohibition)"
            statutes = [
                "Drugs and Cosmetics Act, 1940 — Section 3(aaa)",
                "Cosmetics Rules, 2020",
                "Bureau of Indian Standards (BIS) Cosmetic Specifications",
                "The Patents Act, 1970 — Section 3(p) & Section 3(e)"
            ]
            reqs = [
                "Manufacturing license on Form COS-8 under Cosmetics Rules 2020.",
                "Strict prohibition against curative, therapeutic, or medicinal disease claims on packaging.",
                "Mandatory heavy metal (Lead < 20ppm, Arsenic < 2ppm, Mercury < 1ppm) testing compliance."
            ]
            assessment = (
                "Under Indian law, cosmetic preparations containing herbal extracts are not patentable "
                "merely for the biological properties of the herbs (barred under Section 3(p)). To establish "
                "patentability, claims must focus on a non-obvious cosmetic carrier matrix, novel surfactant/lipid "
                "delivery system, or synergistic skin-permeation vehicle."
            )
            recs = [
                "Draft patent claims directed to the cosmetic delivery vehicle rather than active herbal extracts.",
                "Ensure labeling does not use therapeutic terms like 'cure' or 'treat' to prevent misbranding under Section 17C.",
                "Register trademark in Class 3 (Cosmetics and Non-medicated preparations)."
            ]
            risk_score = 65.0

        # -------------------------------------------------------------
        # 2. Ayurveda Aahara (FSSAI Regulations 2022)
        # -------------------------------------------------------------
        elif "food" in market_lower or "aahar" in market_lower or "supplement" in market_lower:
            category = "Ayurveda Aahara (FSSAI Regulations 2022)"
            hurdle = "Non-Therapeutic Restriction (Prohibition of Disease Cure Claims)"
            statutes = [
                "Food Safety and Standards Act, 2006",
                "Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
                "The Patents Act, 1970 — Section 3(p) & 3(e)"
            ]
            reqs = [
                "FSSAI manufacturing license with mandatory Ayurveda Aahara logo on primary packaging.",
                "Ingredients must be exclusively sourced from Schedule A authoritative classical books.",
                "Strict prohibition against disease mitigation, cure, or therapeutic intervention claims."
            ]
            assessment = (
                "Ayurveda Aahara products are regulated strictly as dietary sustenance, not pharmaceuticals. "
                "Patentability is difficult under Section 3(e) unless a novel functional food matrix or stabilization "
                "process is claimed. Marketing with therapeutic claims will trigger regulatory seizure by FSSAI/AYUSH."
            )
            recs = [
                "Confine packaging claims to physiological maintenance, vitality (Rasayana), and nutritional balance.",
                "If claiming proprietary formulation, ensure excipients comply with permitted FSSAI additive lists.",
                "File process patent on food-matrix preservation/stabilization rather than therapeutic synergy."
            ]
            risk_score = 50.0

        # -------------------------------------------------------------
        # 3. Phytopharmaceutical / New Drug (CDSCO Rule 122E)
        # -------------------------------------------------------------
        elif "phytopharma" in market_lower or request.has_clinical_evidence or any(tech in extract_lower for tech in ["supercritical", "co2", "chromatographic", "purified fraction"]):
            category = "Phytopharmaceutical / New Drug (CDSCO Rule 122E)"
            hurdle = "Section 6 BDA Scrutiny & Mandatory Clinical Trial Phase Protocol"
            statutes = [
                "Drugs & Cosmetics Rules, 1945 — Rule 122E (Phytopharmaceutical Drugs)",
                "Biological Diversity Act, 2002 — Section 6 & Section 19 (Mandatory Form III)",
                "The Patents Act, 1970 — Section 2(1)(j), Section 3(d), Section 3(e)"
            ]
            reqs = [
                "Standardized fraction characterized by minimum 4 chemical/bioactive markers.",
                "Central Drugs Standard Control Organisation (CDSCO) Investigational New Drug (IND) clearance.",
                "Phase I to Phase III clinical safety and efficacy evaluation.",
                "Mandatory National Biodiversity Authority (NBA) approval prior to commercialization or patent grant."
            ]
            assessment = (
                "This pathway represents the highest-value IP asset class. Purified, standardized fractions "
                "with fingerprinting are exempt from traditional Section 3(p) TKDL bars because they are novel "
                "technical entities. However, mandatory Form III clearance from the NBA is non-negotiable under Section 6 of the BDA."
            )
            recs = [
                "File NBA Form III immediately prior to patent grant proceedings.",
                "Deposit voucher specimen and chromatogram fingerprints with approved repository.",
                "Submit dose-response pharmacokinetic data to overcome Section 3(d) therapeutic efficacy scrutiny."
            ]
            risk_score = 30.0

        # -------------------------------------------------------------
        # 4. Classical / Generic Medicine (First Schedule texts)
        # -------------------------------------------------------------
        elif request.is_classical_text_based or any(term in f_name_lower for term in CLASSICAL_KEYWORDS):
            category = "Classical / Generic Ayurvedic Medicine (First Schedule Texts)"
            hurdle = "Section 3(p) TKDL Bar (Traditional Knowledge Exclusion)"
            statutes = [
                "The Patents Act, 1970 — Section 3(p)",
                "Drugs and Cosmetics Act, 1940 — First Schedule Authoritative Texts",
                "Traditional Knowledge Digital Library (TKDL) Prior Art Database"
            ]
            reqs = [
                "Manufacturing must strictly adhere to the composition and method of preparation in the First Schedule text.",
                "AYUSH State Licensing Authority GMP license on Form 25D.",
                "No clinical trial required for classical manufacturing license."
            ]
            assessment = (
                "FATAL STATUTORY PATENT BAR: Inventions that reproduce or duplicate classical Ayurvedic texts "
                "(Charaka, Sushruta, Ashtanga Hridaya) belong to the public domain and are statutorily unpatentable "
                "under Section 3(p). CSIR-TKDL routinely revokes patents filed on classical formulations worldwide."
            )
            recs = [
                "Do NOT file a patent on the formulation composition itself (guaranteed Section 3(p) rejection).",
                "Rely on Trademark protection for distinct brand naming (Class 5).",
                "If novel delivery mechanism exists (e.g. liposomal, sublingual strip), claim only the novel delivery apparatus."
            ]
            risk_score = 95.0

        # -------------------------------------------------------------
        # 5. Patent or Proprietary (P&P) Medicine
        # -------------------------------------------------------------
        else:
            category = "Patent or Proprietary (P&P) Ayurvedic Medicine"
            hurdle = "Section 3(e) Mere Admixture Alert (Synergism Proof Required)"
            statutes = [
                "Drugs and Cosmetics Act, 1940 — Section 3(h)",
                "The Patents Act, 1970 — Section 3(e) & Section 3(p)",
                "Biological Diversity Act, 2002 — Section 6"
            ]
            reqs = [
                "Ayurvedic Drug License under Form 25D from State Licensing Authority.",
                "All botanical ingredients must be listed in authoritative books specified in the First Schedule.",
                "Safety and pilot efficacy documentation to support proprietary claim."
            ]
            assessment = (
                "Section 3(e) of the Indian Patents Act explicitly bars substances obtained by a mere admixture "
                "resulting only in aggregation of properties. Polyherbal blends are routinely rejected unless the "
                "specification demonstrates unexpected supra-additive synergistic bioactivity (e.g. Chou-Talalay CI < 1.0)."
            )
            recs = [
                "Conduct in-vitro or in-vivo combination index (CI) assays to establish quantifiable synergism.",
                "Specify unique non-classical botanical ratios with pharmacokinetic bio-availability enhancements (e.g. with piperine).",
                "File Form III with National Biodiversity Authority to ensure pre-grant compliance."
            ]
            risk_score = 75.0

        return TriageClassificationResponse(
            formulation_name=request.formulation_name,
            category=category,
            statutory_hurdle=hurdle,
            governing_statutes=statutes,
            regulatory_requirements=reqs,
            patentability_assessment=assessment,
            actionable_recommendations=recs,
            statutory_risk_score=risk_score,
            taxonomic_breakdown=taxonomic_data
        )

    except Exception as e:
        logger.exception("Error executing formulation triage", error=str(e))
        raise HTTPException(status_code=500, detail=f"Triage execution failed: {str(e)}")
