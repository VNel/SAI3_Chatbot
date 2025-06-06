"""
app.py

Command-line interface for the Cybersecurity RAG Chatbot.
- Prompts the user for a question (German or English).
- Retrieves the top K relevant chunks from local FAISS.
- Builds a strict context-based prompt.
- Calls Together.ai for completion.
- Displays answer and source chunk metadata.

Usage:
    python app.py
"""

import sys
from query_pipeline import get_top_chunks, build_prompt
from llm_api import call_llm_via_together
from config import TOP_K

def main():
    """
    Loop: Read a question, retrieve context, call LLM, print answer and sources.
    Exit on 'exit', 'quit', or empty input.
    """
    print("=== Cybersecurity RAG Chatbot (CLI) ===")
    print("Type 'exit' or 'quit' to close.\n")

    while True:
        question = input("Question (in German or English): ").strip()
        if question.lower() in ("exit", "quit", ""):
            print("Goodbye.")
            sys.exit(0)

        # Retrieve and rerank chunks
        chunks = get_top_chunks(question)
        if not chunks:
            print("No relevant documents found.\n")
            continue

        # Build strict prompt and call the LLM via API
        prompt = build_prompt(chunks, question)
        answer = call_llm_via_together(prompt)

        # Output the answer and sources
        print("\n--- Answer ---")
        print(answer)
        print(f"\n--- Sources (Top {TOP_K} Chunks) ---")
        for chunk in chunks[:TOP_K]:
            print(f"- {chunk['source']} (Chunk ID: {chunk['id']})")
        print("\n")

if __name__ == "__main__":
    main()
