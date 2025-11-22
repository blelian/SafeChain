# backend/ai-service/app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/safechain")
JWT_SECRET = os.environ.get("JWT_SECRET", "SAFECHAIN_SECRET_please_change_me")
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pt")
MODEL_INPUT_SIZE = int(os.environ.get("MODEL_INPUT_SIZE", 3))
