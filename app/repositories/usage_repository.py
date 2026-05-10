from app.db.models import Usage

def add_usage(db, user_id, tokens):
  usage = Usage(user_id=user_id, tokens_used=tokens)
  db.add(usage)
  db.commit()