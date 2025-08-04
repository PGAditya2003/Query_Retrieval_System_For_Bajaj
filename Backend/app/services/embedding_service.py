# app/services/embedding_service.py
from sentence_transformers import SentenceTransformer
from app.utils.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def generate_embeddings(chunks):
    return model.encode(chunks)
