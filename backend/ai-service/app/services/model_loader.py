# backend/ai-service/app/services/model_loader.py
import os
import traceback
import torch
import torch.nn as nn
import torch.nn.functional as F
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Configuration
# -------------------------------
MODEL_PATH = os.environ.get("MODEL_PATH", "password_model.pt")
MODEL_INPUT_SIZE = int(os.environ.get("MODEL_INPUT_SIZE", "4"))  # feature count used by PasswordModel
PHISHING_MODEL_NAME = os.environ.get("PHISHING_MODEL", "facebook/bart-large-mnli")
MAP_LOCATION = os.environ.get("TORCH_MAP_LOCATION", "cpu")

# Try to import transformers.pipeline if available
try:
    from transformers import pipeline
    _HF_AVAILABLE = True
except Exception:
    pipeline = None
    _HF_AVAILABLE = False

# -------------------------------
# Password Strength Model
# -------------------------------
class PasswordModel(nn.Module):
    def __init__(self, input_size: int = MODEL_INPUT_SIZE, hidden_size: int = 8, output_size: int = 3):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

def _try_torchscript_load(path: str):
    try:
        model = torch.jit.load(path, map_location=MAP_LOCATION)
        model.eval()
        print(f"✅ Loaded TorchScript model from '{path}'")
        return model
    except Exception:
        return None

def _try_torch_load(path: str):
    try:
        obj = torch.load(path, map_location=MAP_LOCATION)
        return obj
    except Exception:
        return None

def load_password_model(path: str = MODEL_PATH):
    """
    Load a password model. Order:
      1) torch.jit.load (scripted/traced)
      2) torch.load -> nn.Module instance
      3) torch.load -> state_dict (load into PasswordModel)
      4) fallback: return untrained PasswordModel
    """
    if os.path.exists(path):
        # 1) try TorchScript
        ts = _try_torchscript_load(path)
        if ts is not None:
            return ts

        # 2) try torch.load
        obj = _try_torch_load(path)
        if obj is None:
            print(f"⚠️ Could not load model file '{path}' with torch.jit or torch.load. Using fresh model.")
            return PasswordModel(input_size=MODEL_INPUT_SIZE)

        # If obj is nn.Module
        if isinstance(obj, nn.Module):
            obj.eval()
            print(f"✅ Loaded nn.Module instance from '{path}'")
            return obj

        # If obj is state_dict
        if isinstance(obj, dict):
            model = PasswordModel(input_size=MODEL_INPUT_SIZE)
            try:
                model.load_state_dict(obj)
                model.eval()
                print(f"✅ Loaded state_dict into PasswordModel (input_size={MODEL_INPUT_SIZE})")
                return model
            except Exception as e:
                print(f"⚠️ Failed to load state_dict into PasswordModel: {e}\nFalling back to fresh model.")
                return PasswordModel(input_size=MODEL_INPUT_SIZE)

        # Unknown object type
        print(f"⚠️ torch.load returned unsupported type {type(obj)} for '{path}'. Using fresh model.")
        return PasswordModel(input_size=MODEL_INPUT_SIZE)
    else:
        print(f"ℹ️ No password model file at '{path}'. Using untrained PasswordModel.")
        return PasswordModel(input_size=MODEL_INPUT_SIZE)

def extract_password_features(password: str):
    length = len(password)
    digits = sum(c.isdigit() for c in password)
    symbols = sum(not c.isalnum() for c in password)
    upper = sum(c.isupper() for c in password)
    # normalize or scale here if you later train a model requiring scaled inputs
    return torch.tensor([[length, digits, symbols, upper]], dtype=torch.float)

def predict_password_strength(model, password: str) -> str:
    """
    Returns one of: "weak", "medium", "strong".
    Falls back to heuristic on any failure.
    """
    try:
        features = extract_password_features(password)
        model.eval()
        with torch.no_grad():
            logits = model(features)
            if isinstance(logits, torch.Tensor):
                pred = int(torch.argmax(logits, dim=1).item())
                label = ["weak", "medium", "strong"][max(0, min(2, pred))]
                return label
            else:
                # unexpected output
                raise RuntimeError("Model returned non-tensor output")
    except Exception as e:
        print(f"⚠️ predict_password_strength failed: {e}")
        traceback.print_exc()
        # fallback heuristic
        pw = password or ""
        if len(pw) >= 12 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw) and any(not c.isalnum() for c in pw):
            return "strong"
        if len(pw) >= 8:
            return "medium"
        return "weak"

# -------------------------------
# Phishing Detection (optional HF pipeline)
# -------------------------------
def load_phishing_model(model_name: str = PHISHING_MODEL_NAME):
    """
    Load a Hugging Face zero-shot classification model for phishing detection.
    Returns a transformers pipeline or None if HF not available.
    """
    if not _HF_AVAILABLE:
        print("⚠️ Hugging Face transformers not available. Phishing detection disabled.")
        return None

    try:
        model = pipeline("zero-shot-classification", model=model_name)
        print(f"✅ Loaded phishing detection model '{model_name}'")
        return model
    except Exception as e:
        print(f"⚠️ Failed to load phishing model '{model_name}': {e}")
        return None

# Initialize phishing model
phishing_model = load_phishing_model()
