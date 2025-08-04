# app/utils/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_CONFIG = {
    "dbname": "docdb",
    "user": "postgres",
    "password": "161202",
    "host": "localhost",
    "port": "5432"
}

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:161202@localhost:5432/docdb"
)

FAISS_INDEX_PATH = os.path.join(BASE_DIR, "../../vector_index.faiss")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # HuggingFace model
