import os
import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import DOCUMENTS_PATH, INDEX_PATH, EMBEDDING_MODEL_NAME, TOP_K

# Einmaliges Laden des FAISS-Index und der Chunks
index = faiss.read_index(INDEX_PATH)
with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
    documents = json.load(f)

# Embedding-Modell initialisieren
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def clean_text(text: str) -> str:
    """
    Entfernt Sonderzeichen (außer Umlaute) und wandelt in Kleinbuchstaben um.
    """
    text = re.sub(r"[^\w\säöüÄÖÜß]", " ", text)
    return text.lower()

def retrieve_chunks(query: str, top_k: int = TOP_K) -> list:
    """
    - Wandelt Query in ein Embedding um
    - Sucht die top_k ähnlichsten Chunks im FAISS-Index
    - Gibt die Liste der entsprechenden Dokument-Diktate zurück
    """
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), top_k)
    results = []
    for idx in I[0]:
        if idx < len(documents):
            results.append(documents[idx])
    return results

def rerank_chunks(query: str, chunks: list) -> list:
    """
    Ranks die Chunks anhand der Wortüberschneidung (Overlap).
    Höhere Überschneidung = höherer Score.
    """
    query_words = set(clean_text(query).split())
    scored = []
    for chunk in chunks:
        chunk_words = set(clean_text(chunk["text"]).split())
        overlap = len(query_words & chunk_words)
        scored.append((overlap, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored]

def get_top_chunks(query: str) -> list:
    """
    Führt Retrieval + Reranking aus und liefert dann die finalen Chunks zurück.
    """
    chunks = retrieve_chunks(query, top_k=TOP_K)
    reranked = rerank_chunks(query, chunks)
    return reranked

def build_prompt(chunks: list, question: str) -> str:
    """
    Baut den finalen Prompt:
    - Erläuterung, dass nur englische Chunks verwendet werden
    - Konkateniert die TOP_K Chunk-Texte als Kontext
    - Fragt auf Deutsch
    """
    context = "\n\n".join([chunk["text"] for chunk in chunks[:TOP_K]])
    prompt = (
        "Du bist ein deutschsprachiger Cybersecurity-Experte.\n"
        "Unten findest du Auszüge aus englischsprachigen wissenschaftlichen Papern.\n"
        "Beantworte die folgende Frage **ausschließlich** basierend auf diesen Informationen und auf Deutsch.\n\n"
        f"KONTEXT:\n{context}\n\n"
        f"FRAGE: {question}\n\n"
        "ANTWORT:"
    )
    return prompt
