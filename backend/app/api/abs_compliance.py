"""
Biological Diversity Act (BDA) & NBA Form Auto-Copilot Router
Automates Access and Benefit Sharing (ABS) compliance checks:
- Section 3(2) Foreign Entity / NRI / Foreign Shareholding vs. Section 7 Domestic Indian Entity.
- Auto-prefills structured JSON payloads for NBA Form III (Application for IPR on Biological Resources).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import structlog
from app.utils.taxonomy import lookup_herb

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["abs_compliance"])


class ABSCheckRequest(BaseModel):
    applicant_name: str = Field(..., description="Name of the applicant company or individual")
    applicant_type: str = Field(default="company", description="individual, company, university, llp")
    has_foreign_shareholding_or_directors: bool = Field(
        default=False,
        description="Whether the entity has ANY foreign equity, NRI shareholding, or non-Indian directors"
    )
    country_of_incorporation: Optional[str] = Field("India", description="Country where entity is registered")
    foreign_equity_percentage: Optional[float] = Field(0.0, description="Percentage of non-Indian shareholding")
    biological_resources: List[str] = Field(default=[], description="List of Indian biological resources/herbs used")
    geographical_source_state: Optional[str] = Field("India", description="Indian State of collection/sourcing")
    source_location_details: Optional[str] = Field(None, description="Forest, trader, farmer cooperative details")
    associated_traditional_knowledge: Optional[bool] = Field(True, description="Whether traditional/tribal knowledge was utilized")
    tk_holder_community: Optional[str] = Field(None, description="Specific tribal/local community if applicable")
    is_for_patent_filing: Optional[bool] = Field(True, description="Whether approval is sought for patent grant (Section 6)")
    patent_application_title: Optional[str] = Field(None, description="Title of proposed or pending patent application")


class ABSCheckResponse(BaseModel):
    applicant_classification: str
    governing_section: str
    approval_authority: str
    is_section_3_2_entity: bool
    mandatory_statutory_actions: List[str]
    benefit_sharing_obligation: str
    penal_provisions: str
    nba_form_iii_prefill: Dict[str, Any]
    compliance_status: str


@router.post("/abs-check", response_model=ABSCheckResponse)
async def check_abs_compliance(request: ABSCheckRequest):
    """
    Evaluates Section 3(2) vs Section 7 status under the Biological Diversity Act, 2002
    and produces a standardized, ready-to-file NBA Form III prefilled dataset.
    """
    try:
        # Determine if entity falls under Section 3(2)
        # Section 3(2) applies to:
        # a) Non-citizens of India
        # b) Citizens of India who are non-resident
        # c) Body corporate, association or organization incorporated/registered outside India
        # d) Body corporate registered in India having ANY non-Indian participation in share capital or management
        is_sec_3_2 = (
            request.has_foreign_shareholding_or_directors
            or (request.country_of_incorporation.lower() != "india")
            or (request.foreign_equity_percentage > 0.0)
        )

        # Standardize biological resources using taxonomy
        standardized_resources = []
        for herb in request.biological_resources:
            meta = lookup_herb(herb)
            if meta:
                standardized_resources.append({
                    "common_name": herb,
                    "botanical_name": meta["latin_binomial"],
                    "family": meta["family"],
                    "part_utilized": ", ".join(meta["parts_used"]),
                    "state_of_origin": request.geographical_source_state,
                    "is_normally_traded_commodity": False  # Section 40 exemption check
                })
            else:
                standardized_resources.append({
                    "common_name": herb,
                    "botanical_name": "Species Pending Identification",
                    "family": "Unspecified",
                    "part_utilized": "Whole plant / extract",
                    "state_of_origin": request.geographical_source_state,
                    "is_normally_traded_commodity": False
                })

        # Classification and regulatory determination
        if is_sec_3_2:
            classification = "Section 3(2) Non-Indian Entity / Foreign-Participated Enterprise"
            gov_section = "Biological Diversity Act, 2002 — Section 3(1), Section 3(2), Section 6 & Section 19"
            authority = "National Biodiversity Authority (NBA), Chennai"
            actions = [
                "MANDATORY PRIOR APPROVAL: Must obtain Form I approval from NBA BEFORE accessing any biological resource in India.",
                "MANDATORY FORM III APPROVAL: Must obtain Form III approval from NBA BEFORE applying for or sealing any patent in India or abroad.",
                "Execute formal ABS Agreement with NBA specifying upfront and annual benefit-sharing royalties.",
                "Submit proof of NBA filing to Indian Patent Office (CGPDTM) to avoid statutory abandonment under Section 10(4)(d)(ii)."
            ]
            benefit_sharing = (
                "Under the Guidelines on Access and Benefit Sharing (2014/2023), Section 3(2) commercial entities "
                "are subject to 0.1% to 0.5% of annual gross ex-factory sale price, or 3.0% to 5.0% of upfront patent licensing royalties."
            )
            penal = (
                "Section 55(1) BD Act: Imprisonment for a term which may extend to five years, or with fine which may "
                "extend to ten lakh rupees and damages, or both for accessing resources without prior approval."
            )
        else:
            classification = "Section 7 Domestic Indian Entity / Indian Citizen"
            gov_section = "Biological Diversity Act, 2002 — Section 7 & Section 6(1)"
            authority = f"State Biodiversity Board ({request.geographical_source_state} SBB) for commercial access + NBA (Form III) for Patent"
            actions = [
                "STATE BIODIVERSITY BOARD (SBB): Prior intimation on Form I to the State Biodiversity Board for commercial extraction.",
                "MANDATORY FORM III APPROVAL: Under Section 6(1), even 100% domestic Indian entities MUST obtain Form III approval from NBA before grant of any patent.",
                "Can apply for patent first, but approval MUST be obtained before the official sealing/grant of the patent.",
                "Maintain local Biodiversity Management Committee (BMC) sourcing records and Access permits."
            ]
            benefit_sharing = (
                "Section 7 domestic entities negotiating with State Biodiversity Boards typically contribute "
                "between 0.1% to 0.3% of annual sales turnover to the State Biodiversity Fund."
            )
            penal = (
                "Section 55(2) BD Act: Contravention of Section 7 or failure to secure Section 6 approval attracts "
                "penalties up to three years imprisonment or fine up to five lakh rupees or both."
            )

        # Auto-prefill Form III structure
        patent_title = request.patent_application_title or f"Synergistic Botanical Formulation containing {', '.join(request.biological_resources[:3])}"
        form_iii_data = {
            "form_name": "FORM III (See Rule 18 of Biological Diversity Rules, 2004)",
            "form_title": "Application for approval of the National Biodiversity Authority for applying for Intellectual Property Rights",
            "submission_date": datetime.now().strftime("%Y-%m-%d"),
            "section_1_applicant_profile": {
                "name": request.applicant_name,
                "applicant_type": request.applicant_type,
                "country_of_incorporation": request.country_of_incorporation,
                "is_section_3_2_entity": is_sec_3_2,
                "foreign_equity_percentage": request.foreign_equity_percentage,
                "registered_address": "Applicant Official Registered Office"
            },
            "section_2_invention_metadata": {
                "proposed_title_of_invention": patent_title,
                "patent_jurisdictions_sought": ["India (IPO)", "PCT International"] if is_sec_3_2 else ["India (IPO)"],
                "patent_office_application_number": "PENDING_PRE_GRANT_CLEARANCE",
                "brief_abstract": (
                    f"The invention relates to {patent_title} developed utilizing biological resources "
                    f"collected from {request.geographical_source_state}, India, exhibiting therapeutic and synergistic bioactivity."
                )
            },
            "section_3_biological_resources_schedule": standardized_resources,
            "section_4_geographical_sourcing": {
                "state": request.geographical_source_state,
                "district_taluk": request.source_location_details or "Procured from certified AYUSH cultivator / local APMC mandis",
                "biodiversity_management_committee": f"Local BMC, {request.geographical_source_state}",
                "traditional_knowledge_associated": request.associated_traditional_knowledge,
                "tk_provider": request.tk_holder_community or "Classical Ayurvedic Literature / TKDL Prior Art"
            },
            "section_5_benefit_sharing_proposal": {
                "proposed_mechanism": "Monetary royalty deposit into National Biodiversity Fund",
                "percentage_offered": "0.2% of annual gross ex-factory sales derived from patented claims",
                "non_monetary_commitments": "Technology transfer to local cultivators, local employment in raw herb collection"
            },
            "section_6_statutory_declaration": (
                "I/We hereby declare that all information furnished herein is true and correct to the best of our knowledge. "
                "I/We undertake to abide by the terms and conditions stipulated by the National Biodiversity Authority."
            )
        }

        return ABSCheckResponse(
            applicant_classification=classification,
            governing_section=gov_section,
            approval_authority=authority,
            is_section_3_2_entity=is_sec_3_2,
            mandatory_statutory_actions=actions,
            benefit_sharing_obligation=benefit_sharing,
            penal_provisions=penal,
            nba_form_iii_prefill=form_iii_data,
            compliance_status="ACTION_REQUIRED_PRIOR_TO_PATENT_GRANT"
        )

    except Exception as e:
        logger.exception("Error executing ABS compliance check", error=str(e))
        raise HTTPException(status_code=500, detail=f"ABS check failed: {str(e)}")
