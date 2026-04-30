from app.db.models import User
from app.core.security import hash_password, verify_password

def create_user(db, email, password):
  user = User(email=email, password=hash_password(password))
  db.add(user)
  db.commit()
  db.refresh(user)
  return user


def authenticate_user(db, email, password):
  user = db.query(User).filter(User.email == email).first()

  if not user:
    return None
  
  if not verify_password(password, user.password):
    return None
  
  return user
