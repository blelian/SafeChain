from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def api_root():
    return {"message": "AI API OK"}
