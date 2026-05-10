from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from app.db.database import Base

class Chat(Base):

  __tablename__ = "chats"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  user_id = Column(Integer, ForeignKey("user.id")) # Link to user

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


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)

  role = Column(String, default="user") # user/admin
  plan = Column(String, default="free") # free/pro

  stripe_customer_id = Column(String, nullable=True)
  stripe_subscription_id = Column(String, nullable=True)

  payment_failed_At = Column(DateTime, nullable=True)


class Usage(Base):
  __tablename__ = "usages"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  tokens_used = Column(Integer, default=0)


class Event(Base):
  __tablename__ = "events"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer)
  event_type = Column(String)