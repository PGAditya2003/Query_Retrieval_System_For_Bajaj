import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import DB_CONFIG, DATABASE_URL
from datetime import datetime

# ✅ SQLAlchemy Engine & Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Raw PostgreSQL connection
def get_connection():
    """Direct psycopg2 connection for raw SQL operations."""
    return psycopg2.connect(**DB_CONFIG)

# ✅ Fetch all files from DB
def get_all_files():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT file_id, file_name, storage_path, upload_time FROM files ORDER BY upload_time DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "file_id": str(r[0]),
                "file_name": r[1],
                "storage_path": r[2],
                "upload_time": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else None
            }
            for r in rows
        ]
    except Exception as e:
        print(f"❌ Error fetching files: {e}")
        return []

# ✅ Save file metadata
def save_metadata(file_id, file_name, storage_path):
    """
    Insert metadata into 'files' table.
    file_id: UUID string
    file_name: Original file name
    storage_path: Full path of saved file
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO files (file_id, file_name, storage_path)
            VALUES (%s, %s, %s)
            """,
            (file_id, file_name, storage_path)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ File metadata saved successfully")
    except Exception as e:
        print(f"❌ Error saving metadata: {e}")

# ✅ FastAPI DB Dependency
def get_db():
    """Provide SQLAlchemy session for DB operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
