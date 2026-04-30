from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth_schema import SignupRequest, LoginRequest
from app.service.auth_service import create_user, authenticate_user
from app.core.security import create_token
from app.db.deps import get_db

router = APIRouter()

@router.post("/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
  user = create_user(db, email=req.email, password=req.password)
  return {"id": user.id, "email": user.email}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
  user = authenticate_user(db, email=req.email, password=req.password)

  if not user:
    return {"error": "Invalid creadentials"}
  
  token = create_token({"user_id": user.id})

  return {"access_token": token}