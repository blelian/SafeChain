# backend/ai-service/app/routes/audit.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import db_service
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=AuditLogResponse)
def create_audit(log: AuditLogCreate, db: Session = Depends(get_db)):
    return db_service.create_audit_log(db, log.action, log.detail)
