# app/routes/files.py
from fastapi import APIRouter
from app.services.db_service import get_all_files

router = APIRouter()

@router.get("/files")
def list_files():
    """
    Fetch all files stored in the database.
    """
    files = get_all_files()
    return {"files": files}
