import os

# Basisverzeichnisse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "clean_data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# Speichere-Pfade
DOCUMENTS_PATH = os.path.join(VECTORSTORE_DIR, "documents.json")
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")

# Modell- und Embedding-Konfiguration
MODEL_PATH = os.path.join(BASE_DIR, "models", "llama-2-7b-chat.Q4_K_M.gguf")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Chunking-Parameter (Anzahl Wörter)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval-Parameter
TOP_K = 3

# LLM-Generierung
MAX_TOKENS = 512
TEMPERATURE = 0.4
