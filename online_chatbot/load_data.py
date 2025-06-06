"""
load_data.py

Reads all .txt files from the DATA_DIR, splits them into overlapping word chunks,
and saves a JSON file listing every chunk with a global ID and source filename.

Usage:
    python load_data.py
"""

import os
import json
import re
from config import DATA_DIR, VECTORSTORE_DIR, DOCUMENTS_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def extract_text(path: str) -> str:
    """
    Read the entire text from a .txt file. Return an empty string if reading fails
    or if the file is not a .txt.
    """
    if not path.lower().endswith(".txt"):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def chunk_text(text: str) -> list:
    """
    Split a text into overlapping chunks of words.
    Each chunk is CHUNK_SIZE words long; consecutive chunks overlap by CHUNK_OVERLAP words.

    Returns:
        A list of dicts, each with keys "id" and "text".
    """
    # Normalize whitespace
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
    Main entry point:
    - Creates VECTORSTORE_DIR if it does not exist.
    - Iterates over every file in DATA_DIR.
    - Extracts text, splits into chunks, and collects metadata.
    - Saves a JSON file at DOCUMENTS_PATH containing all chunk dicts
      with a global unique ID and source filename.
    """
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    documents = []
    global_id = 0
    file_list = os.listdir(DATA_DIR)

    for filename in file_list:
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

    # Save all chunk entries to JSON
    with open(DOCUMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"Completed: {len(documents)} chunks extracted from {len(file_list)} files.")

if __name__ == "__main__":
    main()
