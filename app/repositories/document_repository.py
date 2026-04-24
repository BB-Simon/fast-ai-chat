from app.db.models import Document, DocumentChunk

def save_document(db, filename, content):
  doc = Document(filename=filename, content=content)
  db.add(doc)
  db.commit()
  db.refresh(doc)
  return doc


def get_document(db, doc_id):
  return db.query(Document).filter(Document.id == doc_id).first()


def save_chunks(db, document_id, chunks, embeddings):
  for content, emb in zip(chunks, embeddings):
    chunk = DocumentChunk(
      document_id=document_id,
      content=content,
      embedding=emb
    )
    db.add(chunk)
  db.commit()

def get_chunks(db, document_id):
  return db.query(DocumentChunk).filter(DocumentChunk.id == document_id).all()
