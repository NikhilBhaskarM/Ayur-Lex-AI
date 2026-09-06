import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.models import Assessment
from app.schemas.abs_compliance import (
    ABSEvaluationRequest, ABSChecklistItem, ABSEvaluationResponse
)

logger = structlog.get_logger(__name__)

class ABSComplianceService:
    async def evaluate_abs(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        request: ABSEvaluationRequest
    ) -> ABSEvaluationResponse:
        logger.info("Evaluating ABS compliance", entity_type=request.entity_type, user_id=str(user_id))
        
        checklist: List[ABSChecklistItem] = []
        required_forms: List[str] = []
        benefit_sharing_applicable = False
        benefit_sharing_rate = None
        needs_human_review = False
        
        # 1. Biological Resource Requirement (Section 2(c))
        checklist.append(ABSChecklistItem(
            question="Are Indian biological resources or associated traditional knowledge utilized?",
            user_answer="Yes" if request.involves_bio_resource and request.source_is_india else "No",
            relevant_provision="Section 2(c), Biological Diversity Act, 2002",
            why_it_matters="The BD Act applies strictly to biological resources occurring in and collected from India.",
            required_action="Verify taxonomic identification and geographical sourcing records." if request.involves_bio_resource else "No ABS compliance obligations if biological material is not involved.",
            authority="National Biodiversity Authority (NBA) / State Biodiversity Boards (SBB)",
            confidence="HIGH",
            needs_human_review=False
        ))

        if not (request.involves_bio_resource and request.source_is_india):
            overall_status = "COMPLIANT_NO_APPROVAL_NEEDED"
            summary = "No Indian biological resources or associated knowledge involved. Exempt from BD Act ABS provisions."
            return await self._persist_and_respond(db, user_id, request, overall_status, summary, [], False, None, checklist)

        # 2. Entity Status & Section 3 vs Section 7 Determination
        if request.entity_type == "foreign_or_nri":
            needs_human_review = True
            overall_status = "APPROVAL_REQUIRED_FROM_NBA"
            required_forms.append("NBA Form I (Access for Commercial Utilization or Research)")
            benefit_sharing_applicable = True
            benefit_sharing_rate = "0.1% to 0.5% of ex-factory gross sales or 3.0% to 5.0% of purchase price of bio-resource"
            checklist.append(ABSChecklistItem(
                question="Entity Categorization (Foreign individual, NRI, or Indian body corporate with non-Indian participation)",
                user_answer="Foreign / NRI / Non-Indian participation (Section 3(2))",
                relevant_provision="Section 3(1) & 3(2), Biological Diversity Act, 2002",
                why_it_matters="Mandatory statutory requirement to obtain PRIOR APPROVAL from NBA before accessing any Indian biological resource.",
                required_action="File Form I with NBA Chennai; execute Access and Benefit Sharing (ABS) Agreement prior to raw material procurement.",
                authority="National Biodiversity Authority (NBA, Chennai)",
                confidence="HIGH",
                needs_human_review=True
            ))
        else:
            # Domestic Indian Entity or Citizen
            if request.is_ayush_practitioner:
                overall_status = "EXEMPTION_APPLICABLE"
                checklist.append(ABSChecklistItem(
                    question="Ayush Practitioner Exemption (Section 7 Proviso & 2023 Amendment)",
                    user_answer="Registered Ayush Practitioner / Local Vaidya",
                    relevant_provision="Section 7 (Proviso) & Section 40, BD Act (as amended 2023)",
                    why_it_matters="Registered traditional practitioners of Ayush systems are statutorily exempt from prior intimation and benefit sharing.",
                    required_action="Maintain practitioner registration certificate and clinical dispensary records.",
                    authority="State Biodiversity Board (SBB)",
                    confidence="HIGH",
                    needs_human_review=False
                ))
            elif request.is_cultivated:
                overall_status = "INTIMATION_TO_SBB_REQUIRED"
                required_forms.append("State Biodiversity Board Form (Prior Intimation for Cultivated Produce)")
                checklist.append(ABSChecklistItem(
                    question="Cultivated Medicinal Plant Exemption (2023 Amendment Act)",
                    user_answer="Cultivated on private/contract farmland",
                    relevant_provision="Biological Diversity (Amendment) Act, 2023 (Cultivated Exemption)",
                    why_it_matters="Cultivated medicinal plants registered with local Biodiversity Management Committees (BMCs) are exempt from benefit sharing.",
                    required_action="Obtain Certificate of Cultivation from local BMC / Revenue Authority / State Agriculture Board.",
                    authority="State Biodiversity Board (SBB) / Local BMC",
                    confidence="HIGH",
                    needs_human_review=False
                ))
            else:
                overall_status = "INTIMATION_TO_SBB_REQUIRED"
                required_forms.append("State Biodiversity Board Prior Intimation Form")
                benefit_sharing_applicable = True
                benefit_sharing_rate = "0.1% to 0.5% of annual turnover under State ABS Regulations"
                checklist.append(ABSChecklistItem(
                    question="Domestic Indian Commercial Utilization (Section 7)",
                    user_answer="Domestic Entity sourcing wild-harvested bio-resources",
                    relevant_provision="Section 7, Biological Diversity Act, 2002",
                    why_it_matters="Indian commercial manufacturers accessing wild Indian biological resources must give PRIOR INTIMATION to the State Biodiversity Board.",
                    required_action="File prior intimation with the concerned State Biodiversity Board and deposit fair benefit sharing.",
                    authority="State Biodiversity Board (concerned State)",
                    confidence="HIGH",
                    needs_human_review=False
                ))

        # 3. IPR Filing Trigger (Section 6)
        if request.applies_for_ipr:
            required_forms.append("NBA Form III (Application for seeking prior approval for applying for IPR)")
            checklist.append(ABSChecklistItem(
                question="IPR / Patent Application on Biological Invention (Section 6)",
                user_answer="Applying for Patent or Plant Variety Protection",
                relevant_provision="Section 6, Biological Diversity Act, 2002",
                why_it_matters="Statutory bar prohibiting any applicant (Indian or foreign) from applying for patent rights inside or outside India based on research on Indian biological resources without prior approval from NBA.",
                required_action="File Form III with NBA Chennai before patent grant or immediately following provisional patent filing.",
                authority="National Biodiversity Authority (NBA, Chennai)",
                confidence="HIGH",
                needs_human_review=True
            ))

        # Summary computation
        summary = (
            f"ABS Evaluation Result: {overall_status}. "
            f"Entity is categorized as '{request.entity_type}' under the Biological Diversity Act. "
            f"Forms required: {', '.join(required_forms) if required_forms else 'None (Exempt)'}. "
            f"{'Benefit sharing is applicable.' if benefit_sharing_applicable else 'No benefit sharing required.'}"
        )

        return await self._persist_and_respond(
            db, user_id, request, overall_status, summary, required_forms,
            benefit_sharing_applicable, benefit_sharing_rate, checklist
        )

    async def _persist_and_respond(
        self, db: AsyncSession, user_id: uuid.UUID, request: ABSEvaluationRequest,
        overall_status: str, summary: str, required_forms: List[str],
        benefit_sharing_applicable: bool, benefit_sharing_rate: Optional[str],
        checklist: List[ABSChecklistItem]
    ) -> ABSEvaluationResponse:
        assessment_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        record = Assessment(
            id=assessment_id,
            user_id=user_id,
            assessment_type="abs",
            jurisdiction=request.jurisdiction or "India",
            formulation_data=request.model_dump(),
            abs_assessment={
                "overall_status": overall_status,
                "summary": summary,
                "required_forms": required_forms,
                "benefit_sharing_applicable": benefit_sharing_applicable,
                "benefit_sharing_rate": benefit_sharing_rate,
                "checklist": [item.model_dump() for item in checklist]
            },
            status="completed",
            created_at=now,
            updated_at=now
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)

        return ABSEvaluationResponse(
            id=assessment_id,
            overall_status=overall_status,
            summary=summary,
            required_forms=required_forms,
            benefit_sharing_applicable=benefit_sharing_applicable,
            estimated_benefit_sharing_rate=benefit_sharing_rate,
            checklist=checklist,
            created_at=now
        )

    async def get_assessment(self, db: AsyncSession, user_id: uuid.UUID, assessment_id: uuid.UUID) -> Optional[ABSEvaluationResponse]:
        from sqlalchemy import select
        stmt = select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.user_id == user_id,
            Assessment.assessment_type == "abs"
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            return None

        abs_data = record.abs_assessment or {}
        checklist_raw = abs_data.get("checklist", [])
        checklist = [ABSChecklistItem(**item) for item in checklist_raw]

        return ABSEvaluationResponse(
            id=record.id,
            overall_status=abs_data.get("overall_status", "COMPLIANT_NO_APPROVAL_NEEDED"),
            summary=abs_data.get("summary", ""),
            required_forms=abs_data.get("required_forms", []),
            benefit_sharing_applicable=abs_data.get("benefit_sharing_applicable", False),
            estimated_benefit_sharing_rate=abs_data.get("benefit_sharing_rate"),
            checklist=checklist,
            created_at=record.created_at
        )
