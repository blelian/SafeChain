from fastapi import APIRouter
from app.services.ai_service import analyze_password

router = APIRouter()

@router.get("/password_score")
def password_score(pwd: str):
    """
    Sample endpoint to score a password
    """
    score = analyze_password(pwd)
    return {"password": pwd, "score": score}
