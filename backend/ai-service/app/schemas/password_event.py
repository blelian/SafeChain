# backend/ai-service/app/schemas/password_event.py
from pydantic import BaseModel
from datetime import datetime

class PasswordEventCreate(BaseModel):
    user_id: int
    password_strength: str

class PasswordEventResponse(BaseModel):
    id: int
    user_id: int
    password_strength: str
    created_at: datetime

    class Config:
        orm_mode = True
