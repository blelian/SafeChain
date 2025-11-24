# backend/ai-service/app/routes/password.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.password_event import PasswordEventCreate, PasswordEventResponse
from app.db import get_db
from app.services import model_loader

router = APIRouter()

# Existing DB-backed route
@router.post("/", response_model=PasswordEventResponse)
def add_password_event(event: PasswordEventCreate, db: Session = Depends(get_db)):
    return db_service.create_password_event(db, event.user_id, event.password_strength)

# New: AI-backed password check route
class PasswordCheckRequest(BaseModel):
    password: str
    user_id: int | None = None  # optional, will be logged if provided

class PasswordCheckResponse(BaseModel):
    password: str
    strength: str
    reasons: list[str] = []
    suggestions: list[str] = []

@router.post("/check", response_model=PasswordCheckResponse)
def check_password(req: PasswordCheckRequest, db: Session = Depends(get_db)):
    pw = req.password or ""
    # Use model_loader's predict_password_strength (provided by your model_loader)
    try:
        strength = model_loader.predict_password_strength(model_loader.password_model, pw)
    except Exception as e:
        # In case the model fails, fall back to a simple heuristic
        print(f"⚠️ password model failed: {e}")
        # fallback heuristic
        if len(pw) >= 12 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw) and any(not c.isalnum() for c in pw):
            strength = "strong"
        elif len(pw) >= 8:
            strength = "medium"
        else:
            strength = "weak"

    # Produce human readable reasons & suggestions (lightweight)
    reasons = []
    suggestions = []

    if len(pw) < 8:
        reasons.append("Too short")
        suggestions.append("Make it at least 12 characters long (use a passphrase).")
    elif len(pw) < 12:
        reasons.append("Short length")
        suggestions.append("Consider using 12+ characters for better protection.")

    if not any(c.isupper() for c in pw):
        reasons.append("No uppercase letters")
        suggestions.append("Add at least one uppercase letter.")
    if not any(c.islower() for c in pw):
        reasons.append("No lowercase letters")
        suggestions.append("Use lowercase letters.")
    if not any(c.isdigit() for c in pw):
        reasons.append("No digits")
        suggestions.append("Include at least one digit.")
    if not any(not c.isalnum() for c in pw):
        reasons.append("No special characters")
        suggestions.append("Include symbols like !@#$%^&*() to increase entropy.")

    # Log password event if a user_id was provided
    if req.user_id is not None:
        try:
            db_service.create_password_event(db, req.user_id, strength)
        except Exception as e:
            print(f"⚠️ Could not create password event: {e}")

    return {
        "password": pw,
        "strength": strength,
        "reasons": reasons,
        "suggestions": suggestions
    }
