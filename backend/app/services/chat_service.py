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

logger = structlog.get_logger(__name__)


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
                    jurisdiction=jurisdiction or "india",
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
            triage = self.router.classify_query(sanitized_message)

            # TIER 1 Fast Path: Sub-second generation via General AI Reasoner (bypassing vector search)
            if triage.tier == "simple":
                # Enforce domain framing: prepend context-forcing prompt instruction
                context_forced_query = self.router.apply_domain_context(sanitized_message, tier="simple")
                answer, clarification_questions = self.rag_pipeline.general_ai_reasoner.synthesize_general_answer(
                    context_forced_query, history
                )
                citations = self.rag_pipeline.citation_engine.extract_citations(answer, [])
                citation_dicts = [asdict(c) for c in citations] if citations else []
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
                    "jurisdiction": jurisdiction or conversation.jurisdiction or "india",
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
                    user_query=sanitized_message,
                    jurisdiction=jurisdiction or conversation.jurisdiction,
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
                    "jurisdiction": jurisdiction or "india",
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

            # Save assistant response
            asst_msg = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role="assistant",
                content=rag_response.answer,
                citations=citation_dicts,
                confidence=rag_response.confidence.level if rag_response.confidence else "MEDIUM",
                confidence_score=rag_response.confidence.score if rag_response.confidence else 0.5,
            )
            db.add(asst_msg)
            await db.commit()

            return {
                "conversation_id": conversation.id,
                "message_id": asst_msg.id,
                "answer": rag_response.answer,
                "citations": citation_dicts,
                "confidence": confidence_dict,
                "jurisdiction": rag_response.jurisdiction or "india",
                "requires_clarification": rag_response.requires_clarification,
                "clarification_questions": rag_response.clarification_questions or [],
                "disclaimer": rag_response.disclaimer,
                "tier": triage.tier,
                "model_name": triage.model_name,
                "statutory_risk": triage.statutory_risk_prediction,
            }

        except Exception as e:
            logger.exception("Error in process_message", error=str(e))
            raise
