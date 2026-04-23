from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest
from app.service.openai_service import generate_reply
from app.db.deps import get_db
from app.repositories.document_repository import get_document
from app.service.rag_service import build_prompt

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
    async def generator():
        full_reply = ""

        async for chunk in generate_reply(formatedContent):
            full_reply += chunk
            yield chunk

        # Save assistant reply
        save_message(db, chat_id, 'assistant', full_reply)

    return StreamingResponse(generator(), media_type="text/plain")


@router.post("/ask/{doc_id}")
async def ask_doc(doc_id: int, req: ChatRequest, db: Session = Depends(get_db)):
    doc = get_document(db, doc_id)

    if not doc:
        return {"error": "Document not found!"}
    
    prompt = build_prompt(req.message, doc.content)

    reply = generate_reply([
        {"role": "user", "content": prompt}
    ])

    return {"Answer": reply}
