"""
build_index.py

Loads 'documents.json' (list of chunks with text),
computes sentence embeddings for each chunk using SentenceTransformer,
builds a FAISS index (IndexFlatL2), and saves it to disk.

Usage:
    python build_index.py
"""

import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import DOCUMENTS_PATH, VECTORSTORE_DIR, INDEX_PATH, EMBEDDING_MODEL_NAME

def main():
    """
    - Read DOCUMENTS_PATH to get a list of chunk entries.
    - Create embeddings for each chunk text.
    - Build a FAISS index using L2 distances.
    - Save the index to INDEX_PATH.
    """
    # Load all chunk entries
    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    # Extract the 'text' field from each chunk
    texts = [doc["text"] for doc in documents]

    # Initialize the embedding model
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # Generate embeddings (array of shape [num_chunks, embedding_dim])
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # Build a FAISS index (flat L2 index)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index with {len(texts)} vectors saved to {INDEX_PATH}.")

if __name__ == "__main__":
    main()
