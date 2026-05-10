from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from app.db.database import session_local

from app.core.security import SECRET_KET, ALGHORITHM

security = HTTPBearer()

def get_db():
  db = session_local()
  try:
    yield db
  finally:
    db.close()


def get_current_user(token=Depends(security)):
  try:
    payload = jwt.decode(token.credentials, SECRET_KET, ALGHORITHM)
    return payload['user_id']
  except:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  

def require_admin(user=Depends(get_current_user)):
  if user.get("user").role != "admin":
    raise HTTPException(status_code=403, detail="Admin only")
  
  return user

def require_pro(user=Depends(get_current_user)):
  if user.get("user").plan != "pro":
    raise HTTPException(status_code=403, detail="Upgrade required!")