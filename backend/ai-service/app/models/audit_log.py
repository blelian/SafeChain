# backend/ai-service/app/models/audit_log.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    detail = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
