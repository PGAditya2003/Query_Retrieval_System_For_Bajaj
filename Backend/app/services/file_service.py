# app/services/file_service.py
import os
from fastapi import UploadFile
from app.utils.config import UPLOAD_FOLDER
from app.utils.compress import compress_pdf, compress_docx

async def save_file(file: UploadFile, file_id: str):
    file_ext = file.filename.split('.')[-1].lower()
    final_name = f"{file_id}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, final_name)
    
    # Save file temporarily
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # If file >10MB → compress
    if os.path.getsize(file_path) > 10 * 1024 * 1024:
        if file_ext == "pdf":
            file_path = compress_pdf(file_path)
        elif file_ext == "docx":
            file_path = compress_docx(file_path)
    
    return file_path, final_name
