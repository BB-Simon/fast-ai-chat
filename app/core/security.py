from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KET = "secret"
ALGHORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
  return pwd_context.has(password)

def verify_password(plain, hash):
  return pwd_context.verify(plain, hash)


def create_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})

  return jwt.encode(to_encode, SECRET_KET, ALGHORITHM)


def create_refresh_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(days=7)

  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KET, algorithm=ALGHORITHM)