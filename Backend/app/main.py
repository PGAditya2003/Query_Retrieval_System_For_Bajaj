from fastapi import FastAPI
from app.routes import upload, files, query
from app.services.db_service import get_connection

conn = get_connection()
print("Connected to DB:", conn)
conn.close()

# Create FastAPI app instance
app = FastAPI(title="Intelligent File Storage API")


app.include_router(upload.router, prefix="/api/files")
app.include_router(files.router, prefix="/api/files")
app.include_router(query.router, prefix="/api/search")

@app.get("/")
def root():
    return {"status": "API Running"}
