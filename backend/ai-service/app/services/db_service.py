# backend/ai-service/app/services/db_service.py
from sqlalchemy.orm import Session
from app import models

# ------------------------
# User
# ------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    user = models.User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ------------------------
# Event
# ------------------------
def create_event(db: Session, user_id: int, type: str, detail: str | None = None):
    event = models.Event(user_id=user_id, type=type, detail=detail)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_recent_events(db: Session, limit: int = 10):
    return db.query(models.Event).order_by(models.Event.created_at.desc()).limit(limit).all()

# ------------------------
# PasswordEvent
# ------------------------
def create_password_event(db: Session, user_id: int, password_strength: str):
    pe = models.PasswordEvent(user_id=user_id, password_strength=password_strength)
    db.add(pe)
    db.commit()
    db.refresh(pe)
    return pe

# ------------------------
# PhishingAttempt
# ------------------------
def create_phishing_attempt(db: Session, user_id: int, url: str, result: str):
    pa = models.PhishingAttempt(user_id=user_id, url=url, result=result)
    db.add(pa)
    db.commit()
    db.refresh(pa)
    return pa

# ------------------------
# AuditLog
# ------------------------
def create_audit_log(db: Session, action: str, detail: str | None = None):
    log = models.AuditLog(action=action, detail=detail)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
