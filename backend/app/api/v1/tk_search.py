from fastapi import APIRouter

router = APIRouter(tags=["tk_search"])

@router.get("/")
async def tk_search():
    return {"message": "TK Search Placeholder"}
