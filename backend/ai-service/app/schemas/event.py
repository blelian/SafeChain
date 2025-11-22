# backend/ai-service/app/schemas/event.py
from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    user_id: int
    type: str
    detail: str | None = None

class EventResponse(BaseModel):
    id: int
    user_id: int
    type: str
    detail: str | None
    created_at: datetime

    class Config:
        orm_mode = True
