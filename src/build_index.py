import os
import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from config import DOCUMENTS_PATH, VECTORSTORE_DIR, INDEX_PATH, EMBEDDING_MODEL_NAME

def main():
    """
    - Lädt documents.json (Liste von Diktaten mit 'text')
    - Erzeugt Sentence-Embeddings für jeden Chunk
    - Baut FAISS-Index (L2) und speichert ihn in vectorstore/index.faiss
    """
    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    texts = [doc["text"] for doc in documents]
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # Embeddings generieren (2D-Array: num_chunks x dim)
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # FAISS IndexFlatL2 (L2-Distanz)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS-Index mit {len(texts)} Vektoren gespeichert.")

if __name__ == "__main__":
    main()
