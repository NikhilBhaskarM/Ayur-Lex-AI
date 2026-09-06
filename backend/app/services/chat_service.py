import uuid
from dataclasses import asdict
import structlog
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import Conversation, Message
from app.security.input_sanitizer import sanitize_user_input
from app.rag.pipeline import RAGPipeline
from app.rag.retriever import HybridRetriever
from app.rag.vector_search import VectorStore
from app.rag.keyword_search import KeywordSearcher
from app.rag.adaptive_router import AdaptiveRouter
from app.middleware.sanitizer import mask_pii_for_llm, restore_pii_from_map

logger = structlog.get_logger(__name__)

INTERNATIONAL_CITATIONS = [
    {
        "source_title": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
        "authority": "World Intellectual Property Organization (WIPO)",
        "section": "Article 3 (Mandatory Patent Disclosure of Origin)",
        "official_url": "https://www.wipo.int/treaties/en/ip/gratk/",
        "relevant_passage": "Contracting parties shall require applicants to disclose the country of origin of genetic resources or indigenous provider."
    },
    {
        "source_title": "Nagoya Protocol on Access and Benefit-Sharing",
        "authority": "Convention on Biological Diversity (CBD)",
        "section": "Article 5 & 6 (Prior Informed Consent & Benefit-Sharing)",
        "official_url": "https://www.cbd.int/abs/",
        "relevant_passage": "Prior informed consent (PIC) and mutually agreed terms (MAT) mandatory for transboundary botanical genetic access."
    },
    {
        "source_title": "Botanical Drug Development: Guidance for Industry",
        "authority": "US Food and Drug Administration (FDA - CDER)",
        "section": "Section V (Chemistry, Manufacturing, and Controls - CMC)",
        "official_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/botanical-drug-development-guidance-industry",
        "relevant_passage": "Multicomponent botanical drugs require spectroscopic batch fingerprinting (HPLC/LC-MS) without single active isolation."
    }
]


def _append_international_analysis(answer: str) -> str:
    international_block = """

---

### Dual-Track International Statutory Analysis (WIPO / CBD / US FDA / EMA)

Under the **International Cross-Border Patent Track**, botanical and Ayurvedic innovations face rigorous multilateral treaties and foreign regulatory pathways:

#### 1. WIPO GRATK Treaty (2024 — Genetic Resources & Associated Traditional Knowledge):
- **Mandatory Disclosure of Origin**: Under the historic WIPO Treaty adopted in May 2024, patent applications across all contracting parties based on genetic resources or associated traditional knowledge MUST disclose the country of origin or the indigenous/local community providing the biological material.
- Failure to comply will lead to pre-grant patent rejection or post-grant revocation for fraudulent non-disclosure.

#### 2. Convention on Biological Diversity (CBD) & Nagoya Protocol:
- **Prior Informed Consent (PIC) & Mutually Agreed Terms (MAT)**: Transboundary export or testing of Indian biological material triggers strict Access and Benefit-Sharing (ABS) obligations. Commercialization without an authorized ABS agreement violates international treaty covenants and Section 3(2) of the Indian Biological Diversity Act.

#### 3. US FDA Botanical Drug Guidance & EMA Herbal Directives:
- **US FDA (CDER 505(b)(2) Botanical Pathway)**: Regulates polyherbal mixtures under the *Guidance for Industry: Botanical Drug Products*. Requires comprehensive batch-to-batch chemical fingerprinting (HPLC/LC-MS), raw material quality control, and clinical Phase II/III trials evaluating the entire botanical extract as a unified drug entity without isolating single active principles.
- **EMA (European Union — Directive 2004/24/EC)**: Requires either 'Well-Established Medicinal Use' (demonstrating clinical efficacy with 10+ years EU presence) or 'Traditional Herbal Medicinal Products Directive (THMPD)' registration (proving 30 years of safe traditional medicinal usage, including at least 15 years within the EU).
"""
    return answer + international_block


def _create_rag_pipeline() -> RAGPipeline:
    """Create a RAG pipeline with all dependencies wired up."""
    vector_store = VectorStore()
    keyword_searcher = KeywordSearcher()
    retriever = HybridRetriever(vector_store, keyword_searcher)
    return RAGPipeline(retriever)


class ChatService:
    def __init__(self):
        self._rag_pipeline: Optional[RAGPipeline] = None
        self.router = AdaptiveRouter()

    @property
    def rag_pipeline(self) -> RAGPipeline:
        """Lazy-initialize RAG pipeline to avoid import-time failures."""
        if self._rag_pipeline is None:
            self._rag_pipeline = _create_rag_pipeline()
        return self._rag_pipeline


    async def process_message(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        message: str,
        conversation_id: Optional[uuid.UUID],
        jurisdiction: Optional[str],
    ) -> dict:
        try:
            sanitized_message = sanitize_user_input(message)
            # Mask PII under DPDP Act 2023 before LLM / RAG dispatch
            masked_query, de_map = mask_pii_for_llm(sanitized_message)

            effective_jurisdiction = (jurisdiction or "national").lower()
            is_international = effective_jurisdiction in ["international", "global", "wipo"]

            # Get or create conversation
            if conversation_id:
                stmt = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
                result = await db.execute(stmt)
                conversation = result.scalar_one_or_none()
                if not conversation:
                    raise ValueError("Conversation not found")
            else:
                conversation = Conversation(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    title=sanitized_message[:80],
                    jurisdiction="international" if is_international else "national",
                    status="active",
                )
                db.add(conversation)
                await db.flush()

            # Save user message
            user_msg = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role="user",
                content=sanitized_message,
            )
            db.add(user_msg)
            await db.flush()

            # Load recent conversation history
            stmt = (
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at)
            )
            result = await db.execute(stmt)
            messages = result.scalars().all()
            history = [{"role": m.role, "content": m.content} for m in messages][-10:]

            # Non-destructively triage query tier
            triage = self.router.classify_query(masked_query)

            # TIER 1 Fast Path: Sub-second generation via General AI Reasoner (bypassing vector search)
            if triage.tier == "simple":
                # Enforce domain framing: prepend context-forcing prompt instruction
                context_forced_query = self.router.apply_domain_context(masked_query, tier="simple")
                answer, clarification_questions = self.rag_pipeline.general_ai_reasoner.synthesize_general_answer(
                    context_forced_query, history
                )
                citations = self.rag_pipeline.citation_engine.extract_citations(answer, [])
                citation_dicts = [asdict(c) for c in citations] if citations else []

                # Append international statutory track if requested
                if is_international:
                    answer = _append_international_analysis(answer)
                    citation_dicts.extend(INTERNATIONAL_CITATIONS)

                # Restore any local PII mapping
                if de_map:
                    answer = restore_pii_from_map(answer, de_map)

                asst_msg = Message(
                    id=uuid.uuid4(),
                    conversation_id=conversation.id,
                    role="assistant",
                    content=answer,
                    citations=citation_dicts,
                    confidence="HIGH",
                    confidence_score=0.98,
                )
                db.add(asst_msg)
                await db.commit()
                return {
                    "conversation_id": conversation.id,
                    "message_id": asst_msg.id,
                    "answer": answer,
                    "citations": citation_dicts,
                    "confidence": {"level": "HIGH", "score": 0.98, "factors": {"fast_slm": 1.0}},
                    "jurisdiction": "international" if is_international else "national",
                    "requires_clarification": len(clarification_questions) > 0,
                    "clarification_questions": clarification_questions,
                    "disclaimer": "This information is for informational purposes only and does not constitute legal advice.",
                    "tier": triage.tier,
                    "model_name": triage.model_name,
                    "statutory_risk": triage.statutory_risk_prediction,
                }

            # TIER 2 & TIER 3: Run RAG pipeline with Hybrid Search and Statutory Adjudication
            try:
                rag_response = await self.rag_pipeline.query(
                    user_query=masked_query,
                    jurisdiction="international" if is_international else "national",
                    conversation_history=history,
                )
            except Exception as e:
                logger.exception("RAG pipeline error", error=str(e))
                error_answer = (
                    "I apologize, but I encountered an error processing your question. "
                    "This may be due to the knowledge base not being fully initialized yet. "
                    "Please try again later or contact an administrator."
                )
                asst_msg = Message(
                    id=uuid.uuid4(),
                    conversation_id=conversation.id,
                    role="assistant",
                    content=error_answer,
                    confidence="LOW",
                    confidence_score=0.0,
                )
                db.add(asst_msg)
                await db.commit()
                return {
                    "conversation_id": conversation.id,
                    "message_id": asst_msg.id,
                    "answer": error_answer,
                    "citations": [],
                    "confidence": {"level": "LOW", "score": 0.0, "factors": {}},
                    "jurisdiction": "international" if is_international else "national",
                    "requires_clarification": False,
                    "clarification_questions": [],
                    "disclaimer": "This information is for informational purposes only and does not constitute legal advice.",
                    "tier": triage.tier,
                    "model_name": triage.model_name,
                    "statutory_risk": triage.statutory_risk_prediction,
                }

            # Convert dataclass citations to dicts
            citation_dicts = [asdict(c) for c in rag_response.citations] if rag_response.citations else []
            confidence_dict = asdict(rag_response.confidence) if rag_response.confidence else {"level": "MEDIUM", "score": 0.5, "factors": {}}

            final_answer = rag_response.answer
            if is_international:
                final_answer = _append_international_analysis(final_answer)
                citation_dicts.extend(INTERNATIONAL_CITATIONS)

            if de_map:
                final_answer = restore_pii_from_map(final_answer, de_map)

            # Save assistant response
            asst_msg = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role="assistant",
                content=final_answer,
                citations=citation_dicts,
                confidence=rag_response.confidence.level if rag_response.confidence else "MEDIUM",
                confidence_score=rag_response.confidence.score if rag_response.confidence else 0.5,
            )
            db.add(asst_msg)
            await db.commit()

            return {
                "conversation_id": conversation.id,
                "message_id": asst_msg.id,
                "answer": final_answer,
                "citations": citation_dicts,
                "confidence": confidence_dict,
                "jurisdiction": "international" if is_international else "national",
                "requires_clarification": rag_response.requires_clarification,
                "clarification_questions": rag_response.clarification_questions,
                "disclaimer": rag_response.disclaimer,
                "tier": triage.tier,
                "model_name": triage.model_name,
                "statutory_risk": triage.statutory_risk_prediction,
            }

        except Exception as e:
            logger.exception("Error in process_message", error=str(e))
            raise
