# backend/ai-service/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import api, infer, auth, password, phishing, anomaly, audit, events
from app.services.model_loader import load_model
from app.services import ai_service
from app.db import engine, Base

# Load environment variables
load_dotenv()

# Create database tables safely
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️ Could not create tables: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="SafeChain AI Service",
    version="1.0.0"
)

# ---------- CORS (Required for Next.js) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------

# Startup event: load AI model
@app.on_event("startup")
async def startup_event():
    try:
        model = load_model()
        ai_service.set_model(model)
        print("✅ AI model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load AI model: {e}")

# Health check
@app.get("/")
def root():
    return {"message": "SafeChain AI Service is running"}

# Include all routers
app.include_router(api.router, prefix="/api")
app.include_router(infer.router, prefix="/api/infer")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(password.router, prefix="/api/password")
app.include_router(phishing.router, prefix="/api/phishing")
app.include_router(anomaly.router, prefix="/api/anomaly")
app.include_router(audit.router, prefix="/api/audit")
app.include_router(events.router, prefix="/api/events")
