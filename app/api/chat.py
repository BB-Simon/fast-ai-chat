from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest
from app.service.openai_service import generate_reply
from app.db.deps import get_db
from app.repositories.chat_repositories import (
    get_messages,
    save_message,
    create_chat,
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/chat")
def new_chat(db: Session = Depends(get_db)):
    chat = create_chat(db)
    return {"chat_id": chat.id}

@router.post('/chat/{chat_id}')
async def chat(chat_id: int, req: ChatRequest, db: Session = Depends(get_db)):
    # Save user message
    save_message(db, chat_id, "user", req.message)

    # Get history
    messages = get_messages(db, chat_id)

    # format for OpenAI
    formatedContent = [
        {"role": m.role, "content": m.content }
        for m in messages
    ]

    # Get AI reply
    reply = await generate_reply(formatedContent)

    # Save assistant reply
    save_message(db, chat_id, 'assistant', reply)

    return {'reply': reply}