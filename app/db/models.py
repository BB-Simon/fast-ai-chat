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

class Document(Base):
  
  __tablename__ = "documents"

  id = Column(Integer, primary_key=True, index=True)
  filename = Column(String)
  content = Column(Text)

class DocumentChunk(Base):

  __tablename__ = "document_chunks"
  
  id = Column(Integer, primary_key=True, index=True)
  document_id = Column(Integer, ForeignKey("documents.id"))
  content = Column(Text)
  embedding = Column(Text)
