# app/services/file_service.py
import os
from fastapi import UploadFile
from pathlib import Path
from app.utils.config import UPLOAD_FOLDER
from app.utils.compress import compress_pdf, compress_docx

async def save_file(file: UploadFile, file_id: str):
    """
    Save uploaded file with improved naming: 
    {file_id}_{original_filename.ext}, then compress if size > 10MB.
    Returns: (file_path, original_file_name)
    """
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Clean original filename (remove spaces, keep extension)
    original_name = Path(file.filename).name.replace(" ", "_")
    final_name = f"{file_id}_{original_name}"
    file_path = os.path.join(UPLOAD_FOLDER, final_name)

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # If file > 10MB → compress based on type
    if os.path.getsize(file_path) > 10 * 1024 * 1024:
        file_ext = original_name.split('.')[-1].lower()
        if file_ext == "pdf":
            file_path = compress_pdf(file_path)
        elif file_ext == "docx":
            file_path = compress_docx(file_path)

    return file_path, original_name  # Return original name for DB
