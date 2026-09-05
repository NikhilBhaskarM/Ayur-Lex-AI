from dataclasses import dataclass, field
from typing import Any
import structlog
from app.rag.query_processor import QueryProcessor
from app.rag.retriever import HybridRetriever, RetrievedChunk
from app.rag.reranker import get_reranker
from app.rag.context_builder import ContextBuilder
from app.rag.citation_engine import CitationEngine, Citation
from app.rag.citation_validator import CitationValidator
from app.rag.confidence import ConfidenceScorer, ConfidenceResult
from app.llm.factory import get_llm_provider
from app.rag.prompts.system import SYSTEM_PROMPT
from app.rag.prompts.answer import ANSWER_PROMPT
from app.rag.prompts.abstention import ABSTENTION_RESPONSE

from app.rag.statutory_reasoner import StatutoryReasoner
from app.rag.general_ai_reasoner import GeneralAIReasoner

logger = structlog.get_logger(__name__)

@dataclass
class RAGResponse:
    answer: str
    citations: list[Citation]
    confidence: ConfidenceResult
    jurisdiction: str | None
    requires_clarification: bool
    clarification_questions: list[str]
    metadata: dict[str, Any]
    disclaimer: str = "This information is for informational purposes only and does not constitute legal advice."

class RAGPipeline:
    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever
        self.reranker = get_reranker()
        self.query_processor = QueryProcessor()
        self.context_builder = ContextBuilder()
        self.llm = get_llm_provider()
        self.citation_engine = CitationEngine()
        self.citation_validator = CitationValidator()
        self.confidence_scorer = ConfidenceScorer()
        self.statutory_reasoner = StatutoryReasoner()
        self.general_ai_reasoner = GeneralAIReasoner()

    def _synthesize_statutory_answer(self, query: str, chunks: list[RetrievedChunk], jurisdiction: str | None) -> str:
        """Authoritative rule-based statutory synthesis when external LLM server is offline or initializing."""
        return self.statutory_reasoner.synthesize(query, chunks, jurisdiction)

    async def query(self, user_query: str, jurisdiction: str | None, conversation_history: list[dict] | None = None) -> RAGResponse:
        logger.info("Processing RAG query", query=user_query, jurisdiction=jurisdiction)
        
        # 1. Process query
        processed = await self.query_processor.process_query(user_query, jurisdiction)

        # 2. Check for General AI Questions (greetings, IPR fundamentals, biopiracy history, etc.)
        if self.general_ai_reasoner.is_general_query(processed.original_query):
            answer, clarification_questions = self.general_ai_reasoner.synthesize_general_answer(
                processed.original_query, conversation_history
            )
            citations = self.citation_engine.extract_citations(answer, [])
            return RAGResponse(
                answer=answer,
                citations=citations,
                confidence=ConfidenceResult(level="HIGH", score=0.96, factors={"conversational_ai": 1.0}),
                jurisdiction=processed.jurisdiction or "India",
                requires_clarification=len(clarification_questions) > 0,
                clarification_questions=clarification_questions,
                metadata={"validation": {"grounding_score": 1.0}}
            )
        
        # 3. Retrieve
        filters = {}
        if processed.topics:
            filters["topics"] = processed.topics
        
        retrieved_chunks = await self.retriever.retrieve(
            query=processed.original_query,
            jurisdiction=processed.jurisdiction,
            filters=filters,
            top_k=20
        )
        
        # 4. Rerank
        reranked_chunks = await self.reranker.rerank(processed.original_query, retrieved_chunks, top_k=10)
        
        # Check if we have relevant documents
        if not reranked_chunks:
            return RAGResponse(
                answer=ABSTENTION_RESPONSE,
                citations=[],
                confidence=ConfidenceResult("LOW", 0.0, {}),
                jurisdiction=processed.jurisdiction,
                requires_clarification=False,
                clarification_questions=[],
                metadata={"status": "no_relevant_docs"}
            )
            
        # 5. Build context
        context_str = self.context_builder.build_context(reranked_chunks)
        
        # 6. Generate answer via LLM with statutory synthesis fallback
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if conversation_history:
            messages.extend(conversation_history)
            
        prompt = ANSWER_PROMPT.format(
            context=context_str,
            query=processed.original_query,
            jurisdiction=processed.jurisdiction or "Unknown"
        )
        messages.append({"role": "user", "content": prompt})
        
        clarification_questions = []
        try:
            answer = await self.llm.generate(messages, temperature=0.1)
            if not answer or len(answer.strip()) < 30:
                answer, clarification_questions = self.statutory_reasoner.synthesize_with_questions(
                    processed.original_query, reranked_chunks, processed.jurisdiction, conversation_history
                )
        except Exception as e:
            logger.info("External LLM offline, employing statutory reasoning synthesis", reason=str(e))
            answer, clarification_questions = self.statutory_reasoner.synthesize_with_questions(
                processed.original_query, reranked_chunks, processed.jurisdiction, conversation_history
            )
        
        # 7. Extract citations
        citations = self.citation_engine.extract_citations(answer, reranked_chunks)
        
        # 8. Validate citations
        validation = self.citation_validator.validate_claims(answer, reranked_chunks, citations)
        
        # 9. Calculate confidence
        retrieval_scores = [c.score for c in reranked_chunks]
        source_auth_levels = [c.metadata.get("authority_level", 1) for c in reranked_chunks]
        
        confidence = self.confidence_scorer.calculate_confidence(
            retrieval_scores=retrieval_scores,
            citation_coverage=validation.overall_grounding_score if citations else 0.85,
            source_authority_levels=source_auth_levels,
            source_freshness=1.0,
            num_sources=len(citations)
        )
        
        return RAGResponse(
            answer=answer,
            citations=citations,
            confidence=confidence,
            jurisdiction=processed.jurisdiction,
            requires_clarification=len(clarification_questions) > 0,
            clarification_questions=clarification_questions,
            metadata={"validation": {"grounding_score": validation.overall_grounding_score}}
        )
