from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("", response_model=Dict[str, str])
async def health_check():
    # Try connecting to each service and report individual status in actual implementation
    status = {
        "status": "ok",
        "database": "ok",
        "qdrant": "ok",
        "redis": "ok"
    }
    return status
