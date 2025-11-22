# backend/ai-service/app/schemas/audit_log.py
from pydantic import BaseModel
from datetime import datetime

class AuditLogCreate(BaseModel):
    action: str
    detail: str | None = None

class AuditLogResponse(BaseModel):
    id: int
    action: str
    detail: str | None
    created_at: datetime

    class Config:
        orm_mode = True
