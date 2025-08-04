from fastapi import APIRouter
from app.services.db_service import get_all_files

router = APIRouter()

@router.get("/")
def list_files():
    return {"files": get_all_files()}
