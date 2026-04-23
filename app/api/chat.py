from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest
from app.service.openai_service import generate_reply

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post('/chat')
async def chat(req: ChatRequest):
    reply = await generate_reply(req.message)
    return {'reply': reply}