from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models import User, Document, Chat

router = APIRouter()

@router.get('/analytics')
def get_analytic(db: Session = Depends(get_db)):
  users = db.query(User).count()
  uploads = db.query(Document).count()
  chats = db.query(Chat).count()

  return {
    "total_users": users,
    "total_chat": chats,
    "total_document": uploads
  }