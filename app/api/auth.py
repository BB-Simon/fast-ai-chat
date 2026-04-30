from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth_schema import SignupRequest, LoginRequest
from app.service.auth_service import create_user, authenticate_user
from app.core.security import create_token, create_refresh_token, SECRET_KET, ALGHORITHM
from app.db.deps import get_db, require_admin
from jose import jwt

router = APIRouter()

@router.post("/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
  user = create_user(db, email=req.email, password=req.password, role="user")
  return {"id": user.id, "email": user.email}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
  user = authenticate_user(db, email=req.email, password=req.password)

  if not user:
    return {"error": "Invalid creadentials"}
  
  token = create_token({"user_id": user.id, "role": user.role})
  refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

  return {"access_token": token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh_token(refresh_token: str):
  try:
    payload = jwt.decode(refresh_token, SECRET_KET, algorithms=[ALGHORITHM])
    new_token = create_refresh_token({
      "user_id": payload["user_id"],
      "role": payload["role"]
    })

    return {"refresh_token": new_token}
  
  except:
    raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/admin-only")
def admin_only(user=Depends(require_admin)):
  return "admin only access"