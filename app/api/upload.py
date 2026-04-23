from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.service.file_service import extract_text_from_pdf
from app.repositories.document_repository import save_document
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

    return {"doc_id": doc}