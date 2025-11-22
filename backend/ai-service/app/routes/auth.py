# backend/ai-service/app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services import db_service
from app.db import get_db
import jwt
from app.config import JWT_SECRET
from passlib.context import CryptContext

router = APIRouter()

# Use argon2 instead of bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ------------------------
# Register
# ------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db_service.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(user.password)
    new_user = db_service.create_user(db, user.email, hashed)
    return new_user

# ------------------------
# Login
# ------------------------
class LoginRequest(UserCreate):
    pass

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db_service.get_user_by_email(db, req.email)
    if not user or not pwd_context.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.email}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
