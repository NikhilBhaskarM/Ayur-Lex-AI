from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.api.deps import get_current_active_user
from app.models import User
from app.schemas.tk_search import TKSearchRequest, TKSearchResponse
from app.services.tk_search_service import TKSearchService

router = APIRouter(tags=["tk_search"])
tk_service = TKSearchService()

@router.post("/search", response_model=TKSearchResponse)
@router.post("", response_model=TKSearchResponse)
async def search_traditional_knowledge(
    request: TKSearchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Search Traditional Knowledge prior art, classical treatise verses, and landmark patent revocation precedents."""
    return await tk_service.search(request)

@router.get("/search", response_model=TKSearchResponse)
@router.get("", response_model=TKSearchResponse)
async def search_traditional_knowledge_get(
    query: str = Query(..., description="Herb name, formulation, or therapeutic claim"),
    herb_name: Optional[str] = Query(None),
    therapeutic_claim: Optional[str] = Query(None),
    jurisdiction: Optional[str] = Query("India"),
    current_user: User = Depends(get_current_active_user)
):
    """GET endpoint for searching Traditional Knowledge and classical treatise prior art."""
    request = TKSearchRequest(
        query=query,
        herb_name=herb_name,
        therapeutic_claim=therapeutic_claim,
        jurisdiction=jurisdiction
    )
    return await tk_service.search(request)
