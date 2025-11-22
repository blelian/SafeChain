# backend/ai-service/app/services/model_loader.py
import os
import torch
import torch.nn as nn
from dotenv import load_dotenv

load_dotenv()  # read .env in project root

# Configurable via .env
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pt")
MODEL_INPUT_SIZE = int(os.environ.get("MODEL_INPUT_SIZE", "3"))
MAP_LOCATION = os.environ.get("TORCH_MAP_LOCATION", "cpu")  # usually 'cpu' for server

class SimpleModel(nn.Module):
    """
    Minimal architecture used ONLY when the file at MODEL_PATH is a state_dict.
    This is not training code — it's only here so we can load state_dicts.
    If you have a full serialized Module or a scripted model, that will be used instead.
    """
    def __init__(self, input_size: int = MODEL_INPUT_SIZE, output_size: int = 1):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.linear(x)

def _load_torchscript(path: str):
    """Try to load a scripted/traced model (torch.jit)."""
    try:
        model = torch.jit.load(path, map_location=MAP_LOCATION)
        return model
    except Exception:
        return None

def _load_torch_object(path: str):
    """
    Try to torch.load the file. The file may be:
      - an nn.Module instance (saved with torch.save(model))
      - a state_dict (dict)
    """
    try:
        obj = torch.load(path, map_location=MAP_LOCATION)
        return obj
    except Exception:
        return None

def load_model():
    """
    Robust loader:
      1. try torch.jit.load (scripted/traced model)
      2. try torch.load -> if Module instance, use it
      3. if dict (state_dict), instantiate SimpleModel and load state dict
      4. otherwise raise informative error
    """
    path = MODEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found at '{path}'.\n"
            "Please place your PyTorch model there (scripted model, saved Module, or state_dict).\n"
            "Set MODEL_PATH in .env if using another filename."
        )

    # 1) Try TorchScript
    ts_model = _load_torchscript(path)
    if ts_model is not None:
        ts_model.eval()
        print(f"✅ Loaded TorchScript model from '{path}'")
        return ts_model

    # 2) Try regular torch.load
    obj = _load_torch_object(path)
    if obj is None:
        raise RuntimeError(
            f"Failed to load model using torch.jit.load and torch.load for file '{path}'. "
            "Ensure the file is a valid PyTorch scripted model, saved Module, or a state_dict."
        )

    # If torch.load returned an nn.Module instance
    if isinstance(obj, nn.Module):
        obj.eval()
        print(f"✅ Loaded nn.Module object from '{path}'")
        return obj

    # If torch.load returned a state_dict (dict)
    if isinstance(obj, dict):
        # instantiate a matching architecture and try to load
        print(f"ℹ️  Loaded state_dict from '{path}', attempting to load into SimpleModel(input_size={MODEL_INPUT_SIZE})")
        model = SimpleModel(input_size=MODEL_INPUT_SIZE)
        try:
            model.load_state_dict(obj)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load provided state_dict into SimpleModel (input_size={MODEL_INPUT_SIZE}). "
                f"This usually means the saved state_dict uses a different architecture. Error: {e}"
            )
        model.eval()
        print(f"✅ Loaded state_dict into SimpleModel and ready.")
        return model

    # Unknown object returned
    raise RuntimeError(
        f"torch.load returned object of unsupported type {type(obj)} for file '{path}'. "
        "Expected torchscript, nn.Module, or state_dict(dict)."
    )
