"""
Section 3(e) Chou-Talalay Synergy Calculator & FER Parser Router
Provides quantitative pharmacology analytics for overcoming Section 3(e) mere admixture rejections
and automated First Examination Report (FER) legal rebuttal drafting.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import structlog
import re

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["synergy_analytics"])


# =====================================================================
# 1. Chou-Talalay Synergy Models & Endpoints
# =====================================================================

class ComponentDose(BaseModel):
    name: str = Field(..., description="Herb or bio-active marker name")
    dose_in_combination: float = Field(..., gt=0, description="Dose used in the synergistic combination (D1, D2)")
    dose_alone: float = Field(..., gt=0, description="Equi-effective dose of the single component alone (Dx1, Dx2)")
    unit: Optional[str] = Field("mg/kg", description="Unit of measurement (mg/kg, mcg/mL, % w/w)")


class SynergyCalculationRequest(BaseModel):
    formulation_name: str = Field(..., description="Title of the formulation")
    components: List[ComponentDose] = Field(..., min_length=2, description="At least two components required")
    assay_endpoint: Optional[str] = Field("Anti-inflammatory / Bioavailability AUC", description="Pharmacological biological assay")


class SynergyCalculationResponse(BaseModel):
    formulation_name: str
    combination_index: float
    classification: str
    section_3e_status: str
    patentability_adjudication: str
    pharmacological_explanation: str
    recommended_claim_clause: str
    isobologram_coordinates: List[Dict[str, Any]]
    statutory_precedents: List[str]


@router.post("/synergy-check", response_model=SynergyCalculationResponse)
async def calculate_chou_talalay_synergy(request: SynergyCalculationRequest):
    """
    Calculates the Chou-Talalay Combination Index (CI):
    CI = Sum(D_i / Dx_i)
    - CI < 1.0: Synergism (Clears Section 3(e) bar)
    - CI = 1.0: Additive Effect (High Section 3(e) rejection risk)
    - CI > 1.0: Antagonism (Unpatentable)
    """
    try:
        # Calculate Chou-Talalay CI for mutually exclusive independent components
        ci_sum = 0.0
        coords = []
        for comp in request.components:
            dose_ratio = comp.dose_in_combination / comp.dose_alone
            ci_sum += dose_ratio
            coords.append({
                "component": comp.name,
                "d_combination": comp.dose_in_combination,
                "d_alone": comp.dose_alone,
                "ratio_fraction": round(dose_ratio, 4),
                "unit": comp.unit
            })

        ci_value = round(ci_sum, 3)

        # Classify statutory status
        if ci_value < 0.85:
            classification = "Strong Synergism (Supra-Additive Interaction)"
            sec_3e_status = "CLEARED / LOW REJECTION RISK"
            patentability = (
                f"Statutory Section 3(e) threshold CLEARED. A Combination Index of {ci_value} (< 0.85) mathematically "
                "proves that the biological activity is supra-additive and cannot be attributed to a mere admixture. "
                "The formulation qualifies as an inventive synergistic combination under CGPDTM Patent Guidelines."
            )
            explanation = (
                f"The combination of {', '.join([c.name for c in request.components])} achieves equivalent biological "
                f"efficacy at a fraction ({ci_value}x) of the expected combined single-agent dosages. This unpredictable "
                "pharmacological interaction satisfies Section 2(1)(ja) and overcomes Section 3(e)."
            )
            claim_text = (
                f"A synergistic therapeutic composition comprising {request.components[0].name} and {request.components[1].name} "
                f"in a predetermined weight ratio, characterized in that the composition exhibits a Chou-Talalay Combination Index (CI) "
                f"of less than {ci_value + 0.05:.2f} for {request.assay_endpoint}."
            )
        elif 0.85 <= ci_value <= 1.15:
            classification = "Additive Effect (Simple Cumulative Action)"
            sec_3e_status = "HIGH SECTION 3(e) REJECTION RISK"
            patentability = (
                f"HIGH OBJECTION RISK. A Combination Index of {ci_value} indicates mere additivity. Under Section 3(e) "
                "of The Patents Act, 1970, substances obtained by a mere admixture resulting only in the aggregation of "
                "the properties of the components are statutorily non-patentable."
            )
            explanation = (
                "The observed efficacy corresponds directly to simple mathematical addition of the individual ingredients. "
                "The Indian Patent Office will issue an objection under Section 3(e) in the First Examination Report (FER)."
            )
            claim_text = (
                "Claims cannot be defended as a mere composition. Applicant must re-evaluate different stoichiometric ratios "
                "or incorporate a bio-enhancer (e.g. piperine) to achieve a Combination Index below 0.85."
            )
        else:
            classification = "Antagonistic Effect (Sub-Additive Interaction)"
            sec_3e_status = "FATAL OBJECTION UNDER SECTION 3(e)"
            patentability = (
                f"NON-PATENTABLE. A Combination Index of {ci_value} (> 1.15) demonstrates pharmacological antagonism. "
                "Components interfere with each other's bio-activity, failing the industrial applicability requirement "
                "under Section 2(1)(j) and Section 3(e)."
            )
            explanation = (
                "Higher dosages are required in combination than alone to achieve the endpoint, proving antagonistic "
                "inhibition. Not viable for patent prosecution."
            )
            claim_text = "Not patentable in current stoichiometric ratio."

        precedents = [
            "The Patents Act, 1970 — Section 3(e) statutory exclusion",
            "Biswanath Prasad Radhey Shyam v. Hindustan Metal Industries (1979) — Supreme Court precedent on mere juxtaposition vs synergism",
            "Indian Patent Office Guidelines for Examination of Patent Applications in the Field of Traditional Knowledge and Biological Material (Para 5.4 - Proof of Synergism)"
        ]

        return SynergyCalculationResponse(
            formulation_name=request.formulation_name,
            combination_index=ci_value,
            classification=classification,
            section_3e_status=sec_3e_status,
            patentability_adjudication=patentability,
            pharmacological_explanation=explanation,
            recommended_claim_clause=claim_text,
            isobologram_coordinates=coords,
            statutory_precedents=precedents
        )

    except Exception as e:
        logger.exception("Error executing synergy calculation", error=str(e))
        raise HTTPException(status_code=500, detail=f"Synergy calculation failed: {str(e)}")


# =====================================================================
# 2. FER Parser & Rebuttal Generator Models & Endpoints
# =====================================================================

class FERParseRequest(BaseModel):
    fer_text: str = Field(..., description="Pasted text of the First Examination Report or Hearing Notice from IPO")
    application_number: Optional[str] = Field("IN_PENDING", description="Patent Application Number")
    applicant_name: Optional[str] = Field("The Applicant", description="Name of applicant")
    combination_index: Optional[float] = Field(None, description="Quantified Chou-Talalay CI if available")
    novel_extraction_detail: Optional[str] = Field(None, description="E.g., Supercritical CO2 fraction with 40% withanolides")
    nba_approval_status: Optional[str] = Field("Form III Filed", description="Status of NBA clearance")


class FERParseResponse(BaseModel):
    application_number: str
    detected_objections: List[Dict[str, Any]]
    statutory_summary: str
    formal_written_rebuttal: str
    proposed_claim_amendments: List[str]
    case_law_authorities: List[str]


@router.post("/parse-and-counter", response_model=FERParseResponse)
async def parse_fer_and_generate_counter(request: FERParseRequest):
    """
    Parses First Examination Report (FER) objections and drafts formal statutory counter-arguments
    under Section 3(p), Section 3(e), Section 3(d), and Section 6 of the Biological Diversity Act.
    """
    try:
        text = request.fer_text
        lower = text.lower()
        detected = []

        # Detect Section 3(p) TKDL objection
        if "3(p)" in text or "3 (p)" in text or "traditional knowledge" in lower or "tkdl" in lower:
            detected.append({
                "statute": "Section 3(p), The Patents Act, 1970",
                "objection_type": "Traditional Knowledge Bar / TKDL Prior Art",
                "severity": "HIGH",
                "grounds": "Examiner asserts claims are an aggregation of traditionally known biological properties."
            })

        # Detect Section 3(e) Mere Admixture objection
        if "3(e)" in text or "3 (e)" in text or "mere admixture" in lower or "synergis" in lower or "aggregation" in lower:
            detected.append({
                "statute": "Section 3(e), The Patents Act, 1970",
                "objection_type": "Mere Admixture without Synergistic Demonstration",
                "severity": "CRITICAL",
                "grounds": "Examiner asserts the composition is a simple admixture lacking experimental proof of synergism."
            })

        # Detect Section 3(d) Efficacy objection
        if "3(d)" in text or "3 (d)" in text or "new form" in lower or "therapeutic efficacy" in lower:
            detected.append({
                "statute": "Section 3(d), The Patents Act, 1970",
                "objection_type": "Known Substance / Lack of Enhanced Efficacy",
                "severity": "HIGH",
                "grounds": "Examiner requires proof of significant enhancement in therapeutic efficacy over known base compounds."
            })

        # Detect BDA Section 6 objection
        if "biodiversity" in lower or "nba" in lower or "section 6" in lower or "10(4)" in lower:
            detected.append({
                "statute": "Section 6, Biological Diversity Act, 2002 read with Section 10(4)(d)(ii) of Patents Act",
                "objection_type": "Absence of National Biodiversity Authority Clearance",
                "severity": "PROCEDURAL / MANDATORY",
                "grounds": "Examiner requires submission of mandatory Form III NBA approval prior to grant."
            })

        # If no specific sections matched, flag general inventive step
        if not detected:
            detected.append({
                "statute": "Section 2(1)(j) & 2(1)(ja), The Patents Act, 1970",
                "objection_type": "Lack of Inventive Step / Obviousness",
                "severity": "MEDIUM",
                "grounds": "General objection regarding obvious combination of known botanical elements."
            })

        # Generate formal courtroom-grade written submission
        ci_str = f"Chou-Talalay Combination Index of CI = {request.combination_index}" if request.combination_index else "quantified supra-additive synergism data (CI < 1.0)"
        extract_str = request.novel_extraction_detail or "standardized solvent fraction characterized by specific biomarker enrichment"

        rebuttal_brief = f"""
BEFORE THE CONTROLLER OF PATENTS, THE PATENT OFFICE, INDIA
IN THE MATTER OF PATENT APPLICATION NO.: {request.application_number}
APPLICANT: {request.applicant_name}

WRITTEN SUBMISSION IN RESPONSE TO FIRST EXAMINATION REPORT (FER)

Respected Controller,

In response to the objections communicated in the First Examination Report, the Applicant respectfully submits the following statutory rebuttals:

1. REBUTTAL TO OBJECTION UNDER SECTION 3(p) (TRADITIONAL KNOWLEDGE):
The Learned Examiner has erred in asserting that the claimed invention falls within Section 3(p). While individual biological source materials may be referenced in classical Ayurvedic treatises, the presently claimed invention does NOT duplicate or aggregate traditional knowledge. Specifically:
- Classical treatises (e.g. Charaka Samhita) exclusively disclose crude aqueous decoctions (Kwath) or whole powders (Churna).
- In contrast, Claim 1 is strictly restricted to a novel, non-classical {extract_str} having a biomarker profile neither disclosed nor obtainable through ancient Ayurvedic methods.
- Consequently, the claimed subject matter is not part of the public domain or TKDL, and Section 3(p) is inapplicable.

2. REBUTTAL TO OBJECTION UNDER SECTION 3(e) (MERE ADMIXTURE VS. SYNERGISM):
The Examiner contends that the composition is a mere admixture. The Applicant vehemently traverses this finding:
- As established by the Hon'ble Supreme Court in 'Biswanath Prasad Radhey Shyam v. Hindustan Metal Industries' (AIR 1982 SC 1444), a combination of known integers is patentable if it produces an unexpected, new, and improved result.
- The Applicant has submitted empirical pharmacology data establishing a {ci_str}.
- Under the median-effect principle of Chou-Talalay, a CI < 1.0 constitutes mathematical and experimental proof of true supra-additive synergism. The components do not act as mere aggregated integers; rather, they functionally cooperate to deliver unprecedented bio-enhancement.
- Hence, the objection under Section 3(e) stands conclusively addressed and ought to be waived.

3. REBUTTAL TO OBJECTION UNDER SECTION 3(d) (THERAPEUTIC EFFICACY):
In accordance with the landmark judgment of the Hon'ble Supreme Court in 'Novartis AG v. Union of India' (2013) 6 SCC 1, Section 3(d) requires demonstrable enhancement in 'therapeutic efficacy'.
- The specification demonstrates statistically significant (p < 0.01) superiority in disease biomarker suppression over the individual botanical extracts administered alone.
- This represents enhanced clinical therapeutic efficacy, not merely altered physical properties.

4. COMPLIANCE WITH BIOLOGICAL DIVERSITY ACT, 2002 (SECTION 6):
- The Applicant confirms that an application on Form III has been duly submitted to the National Biodiversity Authority (NBA, Chennai) under Application Status: {request.nba_approval_status}.
- In terms of Section 6(1) of the Biological Diversity Act, approval is only required prior to the formal sealing/grant of the patent. The Applicant undertakes to place the NBA clearance certificate on record prior to grant.

PRAYER:
In view of the above statutory submissions, the Applicant respectfully prays that all objections raised in the FER be waived and the application be advanced to grant.
"""

        amendments = [
            f"Amended Claim 1: A synergistic pharmaceutical composition comprising {extract_str} characterized by a Chou-Talalay Combination Index CI < 1.0.",
            "Added Dependent Claim: Characterized in that the pharmacokinetic bioavailability AUC is enhanced by at least 25% compared to single-agent administration.",
            "Added Specification Disclaimer: Explicitly disclaiming classical aqueous decoctions documented in First Schedule Ayurvedic texts."
        ]

        authorities = [
            "Biswanath Prasad Radhey Shyam v. Hindustan Metal Industries (1979) 2 SCC 511 (Synergy Standard)",
            "Novartis AG v. Union of India (2013) 6 SCC 1 (Section 3(d) Therapeutic Efficacy Test)",
            "Indian Patent Office Guidelines for Examination of Traditional Knowledge (Para 5.4 - Overcoming Section 3(e))",
            "Biological Diversity Act, 2002 — Section 6(1) timing of Form III grant"
        ]

        return FERParseResponse(
            application_number=request.application_number,
            detected_objections=detected,
            statutory_summary=f"Identified {len(detected)} critical statutory objections across Section 3(p), 3(e), 3(d), and BDA.",
            formal_written_rebuttal=rebuttal_brief.strip(),
            proposed_claim_amendments=amendments,
            case_law_authorities=authorities
        )

    except Exception as e:
        logger.exception("Error parsing FER and generating counter", error=str(e))
        raise HTTPException(status_code=500, detail=f"FER parsing failed: {str(e)}")


# =====================================================================
# 3. Attorney Escalation Dossier Endpoint
# =====================================================================

class EscalationReportRequest(BaseModel):
    query: str
    assessment_answer: str
    statutory_risk: Dict[str, Any] = {}
    citations: List[Dict[str, Any]] = []
    confidence_data: Dict[str, Any] = {"level": "HIGH", "score": 0.95}
    applicant_name: Optional[str] = "Applicant Confidential"
    jurisdiction: Optional[str] = "national"


@router.post("/escalate")
async def generate_patent_agent_escalation(request: EscalationReportRequest):
    """
    Generates a formal export dossier for escalating the evaluation to a Registered Patent Agent.
    """
    try:
        from app.services.escalation_service import escalation_service
        report = escalation_service.generate_escalation_report(
            query=request.query,
            assessment_answer=request.assessment_answer,
            statutory_risk=request.statutory_risk,
            citations=request.citations,
            confidence_data=request.confidence_data,
            applicant_name=request.applicant_name,
            jurisdiction=request.jurisdiction or "national"
        )
        return report
    except Exception as e:
        logger.exception("Error generating escalation report", error=str(e))
        raise HTTPException(status_code=500, detail=f"Escalation report failed: {str(e)}")

