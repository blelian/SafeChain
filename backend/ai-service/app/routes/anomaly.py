# backend/ai-service/app/routes/anomaly.py
from fastapi import APIRouter, Depends, HTTPException
from app.services import ai_service
from sqlalchemy.orm import Session
from app.db import get_db

from pydantic import BaseModel
from typing import List

router = APIRouter()

class AnomalyRequest(BaseModel):
    input: List[float]

class AnomalyResponse(BaseModel):
    score: float

@router.post("/", response_model=AnomalyResponse)
def detect_anomaly(req: AnomalyRequest, db: Session = Depends(get_db)):
    try:
        prediction = ai_service.run_inference(req.input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Simple example: use first output as anomaly score
    score = float(prediction[0])
    return {"score": score}
