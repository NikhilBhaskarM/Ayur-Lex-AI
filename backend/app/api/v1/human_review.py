from fastapi import APIRouter

router = APIRouter(tags=["human_review"])

@router.get("/")
async def human_review():
    return {"message": "Human Review Placeholder"}
