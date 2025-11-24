# backend/ai-service/app/schemas/infer.py
from pydantic import BaseModel
from typing import List

class InferRequest(BaseModel):
    # list of floats as model input
    input: List[float]

class InferResponse(BaseModel):
    prediction: List[float]
