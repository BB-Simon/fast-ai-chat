from fastapi import FastAPI
from app.api import chat
from app.db.database import Base, engine
from app.db import models

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api")