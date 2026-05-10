from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.api import chat, analytic, auth
from app.db.database import Base, engine
from app.db.deps import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from app.service.billing_service import process_failed_payment

app = FastAPI()
Base.metadata.create_all(bind=engine)
scheduler = BackgroundScheduler()


app.include_router(chat.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(analytic.router, prefix="/api")

def billing_job(db: Session = Depends(get_db)):
  process_failed_payment(db)

  db.close()


scheduler.add_job(billing_job, "interval", hours=24)
scheduler.start()
