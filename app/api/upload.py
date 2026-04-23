from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()

@router.post('/upload')
def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": file.filename}