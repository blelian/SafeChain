# backend/ai-service/app/services/ai_service.py
import torch

# Internal storage for the AI model
_MODEL = None

def set_model(model):
    """Set the global AI model."""
    global _MODEL
    _MODEL = model

def get_model():
    """Get the global AI model. Raises RuntimeError if not loaded."""
    if _MODEL is None:
        raise RuntimeError("AI model not loaded. Call set_model() first.")
    return _MODEL

def run_inference(input_list: list[float]) -> list[float]:
    """
    Run inference on a single input list.
    Returns a list of floats.
    """
    model = get_model()
    x = torch.tensor([input_list], dtype=torch.float32)
    
    with torch.no_grad():
        y = model(x)

    # Convert output to a list of floats
    if isinstance(y, torch.Tensor):
        out = y.squeeze().cpu().tolist()
    elif isinstance(y, (float, int)):
        out = [float(y)]
    elif isinstance(y, list):
        out = [float(v) for v in y]
    else:
        raise RuntimeError(f"Model returned unsupported type: {type(y)}")

    # Ensure result is always a list
    if isinstance(out, float):
        out = [out]

    return out
