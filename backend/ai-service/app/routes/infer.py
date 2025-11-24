# backend/ai-service/app/routes/infer.py
from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas.infer import InferRequest, InferResponse
from app.services.ai_service import get_model
from app.services.model_loader import MODEL_INPUT_SIZE
import torch

router = APIRouter()

# Simple token dependency — adjust to decode/verify JWT if you want full auth
def verify_token(authorization: str | None = Header(None)) -> str:
    """
    Minimal check: expects header 'Authorization: Bearer <token>'.
    Replace with proper JWT verification if desired.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    return token

@router.post("/", response_model=InferResponse)
def infer(req: InferRequest, subject: str = Depends(verify_token)):
    MODEL = get_model()

    # Determine expected input size (robust to different model shapes)
    try:
        if hasattr(MODEL, "linear") and hasattr(MODEL.linear, "in_features"):
            expected_input_size = int(MODEL.linear.in_features)
        elif hasattr(MODEL, "in_features"):
            expected_input_size = int(MODEL.in_features)
        else:
            expected_input_size = int(MODEL_INPUT_SIZE)
    except Exception:
        expected_input_size = int(MODEL_INPUT_SIZE)

    # Debug prints (visible in uvicorn logs)
    print("DEBUG — User input length:", len(req.input))
    print("DEBUG — Expected size:", expected_input_size)

    # Validate size
    if len(req.input) != expected_input_size:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Wrong input size",
                "given": len(req.input),
                "expected": expected_input_size
            }
        )

    # Convert input to tensor and run model
    x = torch.tensor([req.input], dtype=torch.float32)
    with torch.no_grad():
        y = MODEL(x)

    # Normalize output to a list of floats
    if isinstance(y, torch.Tensor):
        out = y.squeeze().cpu().tolist()
    else:
        out = [float(o) for o in y]

    if isinstance(out, float):
        out = [out]

    return {"prediction": out}
