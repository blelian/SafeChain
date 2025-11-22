# backend/ai-service/app/routes/infer.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import torch
import jwt
from app import config
from app.services.ai_service import get_model

router = APIRouter()
security = HTTPBearer()

# ---------------------
# Request/Response schemas
# ---------------------
class InferRequest(BaseModel):
    input: List[float]

class InferResponse(BaseModel):
    prediction: List[float]

# ---------------------
# Helper: verify JWT
# ---------------------
def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = creds.credentials
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub") or payload.get("email")
        return sub
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ---------------------
# Route: inference
# ---------------------
@router.post("/", response_model=InferResponse)
def infer(req: InferRequest, subject: str = Depends(verify_token)):
    MODEL = get_model()  # Get the model via ai_service

    # Determine expected input size robustly
    expected_input_size = None
    try:
        if hasattr(MODEL, "linear") and hasattr(MODEL.linear, "in_features"):
            expected_input_size = int(MODEL.linear.in_features)
        elif hasattr(MODEL, "in_features"):
            expected_input_size = int(MODEL.in_features)
        else:
            expected_input_size = int(config.MODEL_INPUT_SIZE)
    except Exception:
        expected_input_size = int(config.MODEL_INPUT_SIZE)

    if len(req.input) != expected_input_size:
        raise HTTPException(
            status_code=400,
            detail=f"Input must be a list of {expected_input_size} numbers"
        )

    # Convert input to tensor
    x = torch.tensor([req.input], dtype=torch.float32)

    with torch.no_grad():
        y = MODEL(x)

    # Convert output to list of floats
    if isinstance(y, torch.Tensor):
        out = y.squeeze().cpu().tolist()
    elif isinstance(y, (float, int)):
        out = [float(y)]
    elif isinstance(y, list):
        out = [float(v) for v in y]
    else:
        try:
            out = list(map(float, y))
        except Exception:
            raise HTTPException(status_code=500, detail="Model returned unsupported output format")

    if isinstance(out, float):
        out = [out]

    return {"prediction": out}
