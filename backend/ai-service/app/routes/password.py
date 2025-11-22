# backend/ai-service/app/routes/password.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.password_event import PasswordEventCreate, PasswordEventResponse
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=PasswordEventResponse)
def add_password_event(event: PasswordEventCreate, db: Session = Depends(get_db)):
    return db_service.create_password_event(db, event.user_id, event.password_strength)
