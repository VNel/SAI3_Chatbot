"""
config.py

Configuration settings for the Cybersecurity RAG Chatbot.
All paths, model names, and parameters are defined here.
"""

import os

# Base directories (assumes this file is in the project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory where your 500+ .txt research papers live
DATA_DIR = os.path.join(BASE_DIR, "clean_data")

# Directory to store vector index and related files
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# Path to save chunked documents metadata (JSON)
DOCUMENTS_PATH = os.path.join(VECTORSTORE_DIR, "documents.json")

# Path to save FAISS index file
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")

# Embedding model name for SentenceTransformers
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Chunking parameters (number of words per chunk, overlap between chunks)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Number of top chunks to retrieve for each query
TOP_K = 3

# Maximum tokens for LLM completion
MAX_TOKENS = 512

# Temperature setting for LLM generation (lower => more deterministic)
TEMPERATURE = 0.4

# Together.ai API model name (Mixtral-8x7B Instruct)
TOGETHER_MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Environment variable name where the Together.ai API key is stored
TOGETHER_API_KEY_ENV = "TOGETHER_API_KEY"
