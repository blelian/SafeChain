from fastapi import FastAPI
from app.routes import api

app = FastAPI(
    title="SafeChain AI Service",
    description="AI microservice for password scoring and security analysis",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "SafeChain AI Service is running"}

# Include API router
app.include_router(api.router, prefix="/api")
