from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.service.file_service import extract_text_from_pdf
from app.repositories.document_repository import save_document
from app.service.embedding_service import chunk_text
from app.service.openai_service import get_ambedding
from app.repositories.document_repository import save_chunks
from app.db.deps import get_db
import shutil

router = APIRouter()

@router.post('/upload')
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract the text
    content = extract_text_from_pdf(file_path)

    # Save to db
    doc = save_document(db, file.filename, content)

    chunks = chunk_text(content)
    embeddings = [get_ambedding(c) for c in chunks]
    save_chunks(db, doc.id, chunks, embeddings)

    return {"doc_id": doc}