import sys
from query_pipeline import get_top_chunks, build_prompt
from llm_local import call_local_llm
from config import TOP_K

def main():
    """
    Einfache Kommandozeilen-Schleife:
    - Fragt eine Frage auf Deutsch ab
    - Holt relevante Chunks (englisch) aus dem RAG-Index
    - Baut den Prompt und ruft das lokale LLM
    - Gibt die Antwort auf Deutsch aus und zeigt die Quellen an
    """
    print("=== Cybersecurity RAG Chatbot (lokal, offline) ===")
    print("Tippe 'exit' oder 'quit', um zu beenden.\n")
    while True:
        question = input("Frage (auf Deutsch): ").strip()
        if question.lower() in ("exit", "quit", ""):
            print("Auf Wiedersehen.")
            sys.exit(0)

        # Retrieval & Reranking
        chunks = get_top_chunks(question)
        if not chunks:
            print("Keine relevanten Dokumente gefunden.\n")
            continue

        # Prompt-Building & LLM-Call
        prompt = build_prompt(chunks, question)
        answer = call_local_llm(prompt)

        # Ausgabe
        print("\n--- Antwort ---")
        print(answer)
        print("\n--- Quellen (Top {} Chunks) ---".format(TOP_K))
        for chunk in chunks[:TOP_K]:
            print(f"- {chunk['source']} (Chunk ID: {chunk['id']})")
        print("\n")

if __name__ == "__main__":
    main()
