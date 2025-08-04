import os
import faiss
import numpy as np
import pickle

# Paths for FAISS index and metadata
FAISS_INDEX_PATH = "vector_index/faiss.index"
METADATA_PATH = "vector_index/metadata.pkl"

# Dimensions of embeddings (SentenceTransformer all-MiniLM-L6-v2 = 384)
EMBEDDING_DIM = 384

# Global index and metadata
index = None
metadata = {}

# Initialize FAISS index
def init_faiss():
    global index, metadata
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)
        print("✅ Loaded existing FAISS index with", index.ntotal, "vectors")
    else:
        index = faiss.IndexFlatIP(EMBEDDING_DIM)  # Inner Product for cosine similarity
        metadata = {}
        print("✅ Created new FAISS index")

# Call at startup
init_faiss()

def store_embeddings(file_id, chunks, embeddings):
    global index, metadata

    vectors = np.array(embeddings).astype("float32")
    faiss.normalize_L2(vectors)  # Normalize for cosine similarity

    start_id = len(metadata)
    index.add(vectors)

    for i, chunk in enumerate(chunks):
        metadata[start_id + i] = {"file_id": file_id, "chunk": chunk}

    # Save index and metadata
    os.makedirs("vector_index", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"✅ Stored {len(chunks)} embeddings for file {file_id}")

def search_embeddings(query_embedding, top_k=5):
    global index, metadata
    if index.ntotal == 0:
        return []

    query = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(query)

    distances, indices = index.search(query, top_k)
    results = []
    for idx in indices[0]:
        if idx in metadata:
            results.append(metadata[idx])
    return results
