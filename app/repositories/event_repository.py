from app.db.models import Event

def log_event(db, user_id, event_type):
  event = Event(user_id=user_id, event_type=event_type)
  db.add(event)
  db.commit()
  return event