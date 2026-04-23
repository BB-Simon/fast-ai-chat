from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:123$$$sss@localhost:5432/ai-chat"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(bind=engine)
Base = declarative_base()