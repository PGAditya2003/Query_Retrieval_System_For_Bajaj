from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import search_embeddings

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/query")
async def query_documents(request: QueryRequest):
    # Generate embedding for query
    embedding = generate_embeddings([request.query])[0]

    # Search in FAISS
    results = search_embeddings(embedding, request.top_k)

    return {"query": request.query, "results": results}
