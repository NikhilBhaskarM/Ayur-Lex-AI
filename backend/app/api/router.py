from fastapi import APIRouter
from app.api.v1 import (
    auth, health, chat, classification, sources, admin, assessments,
    ip_assessment, abs_compliance, tk_search, human_review, debate_stream
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(classification.router, prefix="/classification", tags=["classification"])
api_router.include_router(ip_assessment.router, prefix="/ip-assessment", tags=["ip_assessment"])
api_router.include_router(abs_compliance.router, prefix="/abs", tags=["abs_compliance"])
api_router.include_router(tk_search.router, prefix="/tk", tags=["tk_search"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(human_review.router, prefix="/human-review", tags=["human_review"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(debate_stream.router, prefix="/ws", tags=["debate"])

