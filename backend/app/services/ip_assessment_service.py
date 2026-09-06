import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.models import Assessment
from app.schemas.ip_assessment import IPAssessmentRequest, IPAssessmentResponse

logger = structlog.get_logger(__name__)

IP_ROUTES_DATABASE = {
    "patent_formulation": {
        "title": "Patent Protection Assessment (The Patents Act, 1970)",
        "ip_type": "Patent",
        "governing_act": "The Patents Act, 1970 (as amended)",
        "key_sections": "Section 3(p), Section 3(d), Section 3(e), Section 10(4)(d)(ii)",
        "statutory_prerequisites": [
            "Novelty: Formulation/extraction process must not have been published anywhere globally or documented in TKDL/classical texts.",
            "Inventive Step: Non-obvious to a person skilled in Ayurvedic pharmacology (Dravyaguna Vigyana) and modern phytochemistry.",
            "Industrial Application: Capable of standardized industrial replication and batch-to-batch quality manufacture.",
            "Synergism Requirement (Section 3(e)): Combinations of known herbs MUST show experimental quantitative synergistic therapeutic effect (e.g., Combination Index CI < 1.0) over individual herbs.",
            "Enhanced Efficacy (Section 3(d)): New forms, isolated bioactive fractions, or modified extracts require comparative laboratory data demonstrating significantly superior therapeutic efficacy over crude extracts (Novartis AG v. Union of India standard)."
        ],
        "ayurvedic_specific_nuances": [
            "Section 3(p) bars patenting of traditional knowledge or mere aggregation of known properties of components.",
            "Mandatory biological origin disclosure under Section 10(4)(d)(ii) specifying source and geographical origin of raw herbs.",
            "Mandatory approval from the National Biodiversity Authority (NBA) under Section 6 of Biological Diversity Act before patent grant."
        ],
        "exclusion_risks": [
            "Statutory rejection under Section 3(p) if ingredients or their medicinal uses are cited in TKDL.",
            "Rejection under Section 3(e) as a 'mere admixture' if ingredients merely perform their known textbook actions.",
            "Pre-grant or post-grant opposition under Section 25 on grounds of traditional prior art anticipation."
        ],
        "action_steps": [
            "Conduct comprehensive TKDL and prior art search on InPASS (ipindia.gov.in) and WIPO Patentscope.",
            "Generate in vitro / in vivo synergism data with isobologram and Combination Index (CI) calculation.",
            "Draft patent specification with clear disclosure of biological material source and geographical origin.",
            "File Form III with the National Biodiversity Authority (NBA, Chennai) for IPR approval."
        ]
    },
    "trademark_brand": {
        "title": "Brand & Commercial Name Protection (The Trade Marks Act, 1999)",
        "ip_type": "Trademark",
        "governing_act": "The Trade Marks Act, 1999 & Trade Marks Rules, 2017",
        "key_sections": "Section 9 (Absolute Grounds for Refusal), Section 11 (Relative Grounds), Class 5 / Class 3 / Class 30",
        "statutory_prerequisites": [
            "Distinctiveness: Mark must be capable of distinguishing the Ayurvedic goods of one enterprise from those of others.",
            "Non-Descriptive: Must not consist exclusively of signs designating the kind, quality, quantity, or traditional medicinal purpose.",
            "Not a Generic Sanskrit Term: Common names of plants (e.g., 'Ashwagandha', 'Tulsi', 'Triphala') cannot be registered as monopolized trademarks for medicinal herbs."
        ],
        "ayurvedic_specific_nuances": [
            "Class 5 is the primary class for Ayurvedic medicinal preparations and pharmaceutical herbal remedies.",
            "Class 3 applies to Ayurvedic herbal cosmetics, herbal hair oils, and skincare preparations.",
            "Class 30 applies to Ayurvedic food supplements and Ayurveda Aahara wellness diet products.",
            "Prohibition under Section 9(1)(b) against monopolizing single Ayurvedic plant Sanskrit names or classical preparation types (e.g. Asava, Arishta, Churna)."
        ],
        "exclusion_risks": [
            "Refusal under Section 9(1)(b) for being purely descriptive of ingredients or health benefits.",
            "Opposition under Section 11 from existing registered marks in Class 5 or Class 3.",
            "Revocation under Section 57 if the mark becomes a generic customary term in the trade."
        ],
        "action_steps": [
            "Conduct public search on the Trade Marks Registry portal (ipindia.gov.in) across Classes 5, 3, and 30.",
            "Adopt a coined, arbitrary, or suggestive brand name rather than a descriptive herbal name.",
            "File Form TM-A with user affidavit and date of first commercial use documentation."
        ]
    },
    "classical_formulation": {
        "title": "Classical Formulation Protection (Non-Patentable TKDL Subject Matter)",
        "ip_type": "Traditional Knowledge / Defensive Protection",
        "governing_act": "The Patents Act, 1970 (Section 3(p)) & Drugs and Cosmetics Act, 1940",
        "key_sections": "Section 3(p) Patents Act; First Schedule to Drugs and Cosmetics Act",
        "statutory_prerequisites": [
            "Classical formulations published in authoritative texts listed in the First Schedule (Charaka Samhita, Sushruta Samhita, AFI, API) are public domain prior art.",
            "Cannot be monopolized by any single entity via patent rights."
        ],
        "ayurvedic_specific_nuances": [
            "Classical texts serve as defensive prior art codified in the Traditional Knowledge Digital Library (TKDL).",
            "Manufacturers must adhere to classical recipe ratios specified in the Ayurvedic Formulary of India (AFI).",
            "Protection strategy relies on trademark branding for proprietary trade dress and manufacturing quality marks."
        ],
        "exclusion_risks": [
            "Direct rejection under Section 3(p) of any patent application attempting to claim classical recipes (e.g., Triphala, Chyawanprash).",
            "Regulatory sanctions under Drugs and Cosmetics Act if classical recipes are adulterated or labeled incorrectly."
        ],
        "action_steps": [
            "Obtain classical Ayurvedic manufacturing license under Rule 153/154 of Drugs and Cosmetics Rules, 1945.",
            "Focus IP investment on distinctive trademark, proprietary logo, and trade dress packaging.",
            "Do not attempt patent filing for unmodified classical formulation recipes."
        ]
    },
    "geographical_indication": {
        "title": "Geographical Indication Protection (GI Act, 1999)",
        "ip_type": "Geographical Indication (GI)",
        "governing_act": "The Geographical Indications of Goods (Registration and Protection) Act, 1999",
        "key_sections": "Section 2(1)(e), Section 8, Section 11",
        "statutory_prerequisites": [
            "Geographical Link: Reputation, quality, or characteristics must be essentially attributable to geographic origin (e.g., soil, microclimate, traditional harvesting knowledge).",
            "Collective Association: Must be applied for by an association of persons, producers, or authorized organization representing collective grower interests."
        ],
        "ayurvedic_specific_nuances": [
            "Applies to regional Ayurvedic medicinal plants and heritage preparations (e.g., Nagauri Ashwagandha, Malabar Pepper, Navara Rice).",
            "GI confers collective public monopoly to regional growers; individual commercial companies cannot monopolize as private property."
        ],
        "exclusion_risks": [
            "Rejection if the geographic term has become generic across India.",
            "Individual commercial entity applications are not maintainable without producer collective standing."
        ],
        "action_steps": [
            "Form or partner with a registered association of regional Ayurvedic herbal cultivators.",
            "Collate historical, botanical, and agro-climatic evidence linking quality to geographic terrain.",
            "File GI Application with the Geographical Indications Registry in Chennai (ipindia.gov.in)."
        ]
    },
    "industrial_design": {
        "title": "Packaging & Applicator Design Protection (Designs Act, 2000)",
        "ip_type": "Industrial Design",
        "governing_act": "The Designs Act, 2000 & Designs Rules, 2001",
        "key_sections": "Section 4 (Prohibition of Registration), Section 5, Class 09 (Packaging/Containers)",
        "statutory_prerequisites": [
            "Absolute Novelty: Shape, configuration, pattern, or ornament must not have been published in India or abroad prior to filing date.",
            "Visual Appeal: Design must appeal to and be judged solely by the eye.",
            "Non-Functional: Does not protect functional mechanical mechanisms or medicinal compositions."
        ],
        "ayurvedic_specific_nuances": [
            "Protects unique aesthetic bottles, Ayurvedic dosage droppers, herbal inhalers, and copper/brass dispensing containers.",
            "Provides 10 years of initial design copyright protection, extendable by 5 years to 15 years total."
        ],
        "exclusion_risks": [
            "Rejection under Section 4 if the container shape is standard or previously published in product catalogues.",
            "Rejection if the shape is dictated solely by functional mechanical requirements."
        ],
        "action_steps": [
            "Prepare 7-angle professional orthographic line drawings or photographs of the empty container.",
            "File Form-1 design application with the Controller General of Patents, Designs and Trade Marks.",
            "Maintain strict commercial secrecy before the design application filing date."
        ]
    },
    "plant_variety": {
        "title": "Medicinal Plant Variety Protection (PPV&FR Act, 2001)",
        "ip_type": "Plant Variety Protection",
        "governing_act": "The Protection of Plant Varieties and Farmers' Rights Act, 2001",
        "key_sections": "Section 14, Section 15 (DUS Criteria)",
        "statutory_prerequisites": [
            "Distinctness: Clearly distinguishable by one or more essential characteristics from known varieties.",
            "Uniformity: Subject to variation from propagation, uniform in essential characteristics.",
            "Stability: Essential characteristics remain unchanged after repeated propagation."
        ],
        "ayurvedic_specific_nuances": [
            "Protects high-yield bioactive cultivars of Ayurvedic medicinal plants developed through institutional or farmer breeding.",
            "Farmers retain traditional rights to save, use, sow, resow, exchange, or sell farm produce seeds."
        ],
        "exclusion_risks": [
            "Rejection if the plant variety fails multi-season Distinctiveness, Uniformity and Stability (DUS) field trials."
        ],
        "action_steps": [
            "Complete multi-location DUS testing protocol with authorized ICAR / NBPGR institutes.",
            "File registration with the PPV&FR Authority in New Delhi."
        ]
    },
    "trade_secret": {
        "title": "Proprietary Manufacturing Know-How & Trade Secrets",
        "ip_type": "Trade Secret / Confidential Information",
        "governing_act": "Indian Contract Act, 1872 (Section 27) & Common Law of Breach of Confidence",
        "key_sections": "Common law protection; Section 27 Contract Act; NDAs",
        "statutory_prerequisites": [
            "Information must not be publicly known or readily accessible to competitors.",
            "Possesses commercial value because it is secret.",
            "Subject to reasonable measures under the circumstances to keep it confidential."
        ],
        "ayurvedic_specific_nuances": [
            "Used for proprietary extraction ratios, specialized purification (Shodhana) parameters, and equipment calibration.",
            "Cannot protect published active ingredients which must be disclosed on Ayurvedic medicine packaging under Rule 161."
        ],
        "exclusion_risks": [
            "Loss of all legal protection if a third party independently reverse-engineers the formulation.",
            "No monopoly against independent discovery."
        ],
        "action_steps": [
            "Implement Non-Disclosure Agreements (NDAs) and non-compete clauses with all laboratory and factory staff.",
            "Segment proprietary extraction steps so no single operator possesses end-to-end recipe parameters."
        ]
    }
}

class IPAssessmentService:
    async def evaluate_ip(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        request: IPAssessmentRequest
    ) -> IPAssessmentResponse:
        logger.info("Evaluating IP assessment", asset_id=request.asset_id, user_id=str(user_id))
        
        route = IP_ROUTES_DATABASE.get(request.asset_id, IP_ROUTES_DATABASE["patent_formulation"])
        
        # Build contextual guidance based on request inputs
        guidance_parts = [
            f"Asset Evaluation for '{request.formulation_name or 'Proposed Ayurvedic Asset'}' under {route['governing_act']}."
        ]
        
        if request.asset_id == "patent_formulation":
            if request.synergy_evidence:
                guidance_parts.append(
                    "Positive Factor: Synergistic experimental data indicated. Ensure combination index (CI < 1.0) "
                    "or isobologram graphs are incorporated in patent examples to withstand Section 3(e) scrutiny."
                )
            else:
                guidance_parts.append(
                    "Critical Gap: No quantitative synergistic data specified. Merely combining known Ayurvedic herbs "
                    "will result in Section 3(e) (mere admixture) and Section 3(p) (traditional knowledge) statutory objections."
                )
            if request.biological_origin:
                guidance_parts.append(
                    f"Biological Origin: Source from '{request.biological_origin}' requires mandatory Section 10(4) "
                    "disclosure and NBA approval under Section 6 of the Biological Diversity Act, 2002."
                )

        rag_guidance = " ".join(guidance_parts)
        
        citations = [
            {
                "source_title": route["governing_act"],
                "section": route["key_sections"],
                "official_url": "https://ipindia.gov.in"
            }
        ]
        
        confidence = {
            "level": "HIGH",
            "score": 0.95,
            "factors": {"statutory_rule_match": 1.0, "authority_level": 1}
        }
        
        # Persist to Assessment table
        assessment_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        
        assessment_record = Assessment(
            id=assessment_id,
            user_id=user_id,
            assessment_type="ip",
            jurisdiction=request.jurisdiction or "India",
            formulation_data=request.model_dump(),
            ip_assessment={
                "asset_id": request.asset_id,
                "title": route["title"],
                "ip_type": route["ip_type"],
                "governing_act": route["governing_act"],
                "key_sections": route["key_sections"],
                "rag_guidance": rag_guidance,
            },
            status="completed",
            created_at=now,
            updated_at=now
        )
        db.add(assessment_record)
        await db.commit()
        await db.refresh(assessment_record)
        
        return IPAssessmentResponse(
            id=assessment_id,
            asset_id=request.asset_id,
            title=route["title"],
            ip_type=route["ip_type"],
            governing_act=route["governing_act"],
            key_sections=route["key_sections"],
            statutory_prerequisites=route["statutory_prerequisites"],
            ayurvedic_specific_nuances=route["ayurvedic_specific_nuances"],
            exclusion_risks=route["exclusion_risks"],
            action_steps=route["action_steps"],
            rag_guidance=rag_guidance,
            citations=citations,
            confidence=confidence,
            created_at=now
        )

    async def get_assessment(self, db: AsyncSession, user_id: uuid.UUID, assessment_id: uuid.UUID) -> Optional[IPAssessmentResponse]:
        from sqlalchemy import select
        stmt = select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.user_id == user_id,
            Assessment.assessment_type == "ip"
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            return None
            
        ip_data = record.ip_assessment or {}
        asset_id = ip_data.get("asset_id", "patent_formulation")
        route = IP_ROUTES_DATABASE.get(asset_id, IP_ROUTES_DATABASE["patent_formulation"])
        
        return IPAssessmentResponse(
            id=record.id,
            asset_id=asset_id,
            title=ip_data.get("title", route["title"]),
            ip_type=ip_data.get("ip_type", route["ip_type"]),
            governing_act=ip_data.get("governing_act", route["governing_act"]),
            key_sections=ip_data.get("key_sections", route["key_sections"]),
            statutory_prerequisites=route["statutory_prerequisites"],
            ayurvedic_specific_nuances=route["ayurvedic_specific_nuances"],
            exclusion_risks=route["exclusion_risks"],
            action_steps=route["action_steps"],
            rag_guidance=ip_data.get("rag_guidance"),
            citations=[],
            confidence={"level": "HIGH", "score": 0.95},
            created_at=record.created_at
        )
