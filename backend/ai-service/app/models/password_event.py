# backend/ai-service/app/models/password_event.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base

class PasswordEvent(Base):
    __tablename__ = "password_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password_strength = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
