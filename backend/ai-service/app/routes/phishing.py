# backend/ai-service/app/routes/phishing.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.phishing import PhishingAttemptCreate, PhishingAttemptResponse
from app.db import get_db
from app.services import model_loader

router = APIRouter()

@router.post("/", response_model=PhishingAttemptResponse)
def create_phishing(event: PhishingAttemptCreate, db: Session = Depends(get_db)):
    return db_service.create_phishing_attempt(db, event.user_id, event.url, event.result)

# New: check endpoint
class PhishingCheckRequest(BaseModel):
    text: str
    user_id: int | None = None

class PhishingCheckResponse(BaseModel):
    text: str
    result: str

@router.post("/check", response_model=PhishingCheckResponse)
def check_phishing(req: PhishingCheckRequest, db: Session = Depends(get_db)):
    txt = req.text or ""
    try:
        result = model_loader.check_phishing(model_loader.phishing_model, txt)
    except Exception as e:
        print(f"⚠️ phishing model failed: {e}")
        # fallback heuristic: suspicious if it contains obvious patterns
        if "@" in txt and ("http" not in txt):
            result = "suspicious"
        elif "login" in txt.lower() or "password" in txt.lower():
            result = "suspicious"
        else:
            result = "safe"

    # Log attempt if user_id provided
    if req.user_id is not None:
        try:
            db_service.create_phishing_attempt(db, req.user_id, txt, result)
        except Exception as e:
            print(f"⚠️ Could not create phishing attempt record: {e}")

    return {"text": txt, "result": result}
