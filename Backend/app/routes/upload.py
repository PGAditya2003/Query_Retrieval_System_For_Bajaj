# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from app.services.file_service import save_file
from app.services.text_service import extract_text, chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import store_embeddings
from app.services.db_service import save_metadata

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Save file with original name
    saved_path, original_name = await save_file(file, file_id)

    # Extract text
    text = extract_text(saved_path, original_name)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file.")
    
    # Chunk text
    chunks = chunk_text(text)
    
    # Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Store in FAISS
    store_embeddings(file_id, chunks, embeddings)
    
    # Save metadata in DB (with original file name)
    save_metadata(file_id, original_name, saved_path)
    
    return {
        "file_id": file_id,
        "file_name": original_name,  # ✅ Clean name for user
        "status": "processed"
    }
