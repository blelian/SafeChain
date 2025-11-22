# backend/ai-service/app/routes/phishing.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.phishing import PhishingAttemptCreate, PhishingAttemptResponse
from app.db import get_db
# Note: ai_service is imported if needed, but we no longer import MODEL directly

router = APIRouter()

@router.post("/", response_model=PhishingAttemptResponse)
def check_phishing(event: PhishingAttemptCreate, db: Session = Depends(get_db)):
    # Example: call ML service for phishing detection
    # For now we just trust event.result, could replace with AI prediction
    return db_service.create_phishing_attempt(db, event.user_id, event.url, event.result)
