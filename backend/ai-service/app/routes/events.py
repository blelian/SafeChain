# backend/ai-service/app/routes/events.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.event import EventResponse
from app.db import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[EventResponse])
def get_recent_events(limit: int = 10, db: Session = Depends(get_db)):
    return db_service.get_recent_events(db, limit)
