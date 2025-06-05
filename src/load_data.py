import os
import json
import re
from config import DATA_DIR, VECTORSTORE_DIR, DOCUMENTS_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def extract_text(path: str) -> str:
    """
    Liest den Text aus einer .txt-Datei.
    Andere Dateitypen werden ignoriert.
    """
    if not path.lower().endswith(".txt"):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Fehler beim Lesen von {path}: {e}")
        return ""

def chunk_text(text: str) -> list:
    """
    Zerlegt den Text in überlappende Wort-Chunks.
    Gibt Liste von Dicts mit 'id' und 'text' zurück.
    """
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split(" ")
    chunks = []
    chunk_id = 0
    idx = 0
    while idx < len(words):
        chunk_words = words[idx : idx + CHUNK_SIZE]
        chunk_text = " ".join(chunk_words)
        chunks.append({"id": chunk_id, "text": chunk_text})
        chunk_id += 1
        idx += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def main():
    """
    Liest alle .txt-Dateien in DATA_DIR, zerlegt sie in Chunks,
    und speichert alle Chunks mit globaler ID in DOCUMENTS_PATH.
    """
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    documents = []
    global_id = 0

    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        text = extract_text(path)
        if not text:
            continue

        chunks = chunk_text(text)
        for chunk in chunks:
            documents.append({
                "id": global_id,
                "text": chunk["text"],
                "source": filename
            })
            global_id += 1

    with open(DOCUMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"Fertig: {len(documents)} Chunks aus {len(os.listdir(DATA_DIR))} Dateien.")

if __name__ == "__main__":
    main()
