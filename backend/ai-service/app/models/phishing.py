# backend/ai-service/app/models/phishing.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base

class PhishingAttempt(Base):
    __tablename__ = "phishing_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String)
    result = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
