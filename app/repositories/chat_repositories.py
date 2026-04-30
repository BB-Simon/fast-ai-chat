from app.db.models import Chat, Message

def create_chat(db, user_id):
  chat = Chat(title="New chat", user_id=user_id)
  db.add(chat)
  db.commit()
  db.refresh(chat)
  return chat


def save_message(db, chat_id, role, content):
  msg = Message(chat_id = chat_id, role = role, content = content)
  db.add(msg)
  db.commit()
  return msg


def get_messages(db, chat_id):
  return db.query(Message).filter(Message.chat_id == chat_id).all()
