from app.db.models import Document

def save_document(db, filename, content):
  doc = Document(filename=filename, content=content)
  db.add(doc)
  db.commit()
  db.refresh(doc)
  return doc


def get_document(db, doc_id):
  return db.query(Document).filter(Document.id == doc_id).first()
