# backend/ai-service/app/schemas/phishing.py
from pydantic import BaseModel
from datetime import datetime

class PhishingAttemptCreate(BaseModel):
    user_id: int
    url: str
    result: str

class PhishingAttemptResponse(BaseModel):
    id: int
    user_id: int
    url: str
    result: str
    created_at: datetime

    class Config:
        orm_mode = True
