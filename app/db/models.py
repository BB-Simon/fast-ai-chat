from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.database import Base

class Chat(Base):

  __tablename__ = "chats"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)

class Message(Base):

  __tablename__ = "messages"

  id = Column(Integer, primary_key=True, index=True)
  chat_id =  Column(Integer, ForeignKey("chats.id"))
  role = Column(String) # user | assistant
  content = Column(Text)