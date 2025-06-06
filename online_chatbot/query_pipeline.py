"""
query_pipeline.py
 
- Loads the FAISS index and documents metadata once at import time.
- Defines functions to retrieve and rerank the top-K relevant chunks.
- Builds a final prompt that instructs the LLM to answer strictly from context,
  in the same language as the question.
 
Imports from llm_api are used by app.py or web_ui.py to call Together.ai.
"""
 
import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import DOCUMENTS_PATH, INDEX_PATH, EMBEDDING_MODEL_NAME, TOP_K
 
# Load FAISS index and chunk metadata at module import
index = faiss.read_index(INDEX_PATH)
with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
    documents = json.load(f)
 
# Initialize the embedding model once
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
 
def clean_text(text: str) -> str:
    """
    Lowercase text and remove punctuation (except German umlauts).
    Used for a simple overlap-based reranking.
    """
    text = re.sub(r"[^\w\säöüÄÖÜß]", " ", text)
    return text.lower()
 
def retrieve_chunks(query: str, top_k: int = TOP_K) -> list:
    """
    1. Embed the query using the same embedding model.
    2. Search the FAISS index for the top_k most similar chunk embeddings.
    3. Return a list of chunk dicts (each dict has keys 'id', 'text', 'source').
    """
    query_embedding = embedding_model.encode([query])
    query_vector = np.array(query_embedding).astype("float32")
    distances, indices = index.search(query_vector, top_k)
 
    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])
    return results
 
def rerank_chunks(query: str, chunks: list) -> list:
    """
    Perform a simple overlap-based reranking:
    - Count the number of overlapping words between query and each chunk.
    - Return the chunks sorted by descending overlap count.
    """
    query_words = set(clean_text(query).split())
    scored = []
    for chunk in chunks:
        chunk_words = set(clean_text(chunk["text"]).split())
        overlap_score = len(query_words & chunk_words)
        scored.append((overlap_score, chunk))
 
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored]
 
def get_top_chunks(query: str) -> list:
    """
    Retrieves the initial set of top_k chunks via FAISS,
    then reranks them by simple word-overlap, and returns the reranked list.
    """
    initial_chunks = retrieve_chunks(query, top_k=TOP_K)
    reranked = rerank_chunks(query, initial_chunks)
    return reranked
 
def build_prompt(chunks: list, question: str) -> str:
    """
    Constructs the final prompt to send to the LLM:
    - Explains that the model must answer strictly from the provided context.
    - Instructs the LLM to respond in the same language as the question.
    - If no information is found, instructs the model to say so clearly.
 
    Chunks are English excerpts from academic papers.
    Question can be in German or English.
    """
    # Concatenate top K chunk texts
    context = "\n\n".join(chunk["text"] for chunk in chunks[:TOP_K])
 
    prompt = (
        "You are a cybersecurity expert. "
        "Below are excerpts from peer-reviewed academic papers (in English). "
        "Answer the question strictly based on this context. "
        "Do not add any information that is not in the context. "
        "If the context does not contain an answer, say 'No relevant information in context.'\n\n"
        f"--- CONTEXT START ---\n{context}\n--- CONTEXT END ---\n\n"
        f"--- QUESTION ({'German' if contains_german(question) else 'English'}) ---\n"
        f"{question}\n\n"
        "Please respond in the same language as the question."
    )
    return prompt
 
def contains_german(text: str) -> bool:
    """
    Simple heuristic to decide if the text is German:
    - Checks for presence of common German words/characters.
    """
    # If text contains umlauts or certain German words, assume German
    german_indicators = [
    # Umlaute & scharfes ß
    "ä", "ö", "ü", "ß",
 
    # Artikel (bestimmt & unbestimmt)
    " der ", " die ", " das ",      # bestimmte Artikel
    " den ", " dem ", " des ",
    " ein ", " eine ", " einem ", " einer ", " eines ",
 
    # Pronomen (Personal- & Possessivpronomen)
    " ich ", " du ", " er ", " sie ", " es ", " wir ", " ihr ", " sie ",  # Personal
    " mich ", " mir ", " dich ", " dir ",
    " ihn ", " ihm ", " sie ", " uns ", " euch ",
    " mein ", " meine ", " meinen ", " meinen ", " meines ", " meiner ",
    " dein ", " deine ", " deinen ", " deinen ", " deines ", " deiner ",
    " sein ", " seine ", " seinen ", " seinem ", " seines ",
    " unser ", " unsere ", " unseren ", " unserem ", " unseres ",
    " euer ", " eure ", " euren ", " eurem ", " eures ",
 
    # Häufige Verben im Infinitiv
    " sein ", " haben ", " werden ", " können ", " müssen ", " sollen ", " wollen ", " dürfen ",
    " wissen ", " machen ", " geben ", " kommen ", " gehen ", " sehen ", " lassen ", " finden ",
 
    # Häufige Hilfs- & Modalverben (Konjugationsformen)
    " bin ", " bist ", " ist ", " sind ", " seid ",
    " hatte ", " hattest ", " hatte ", " hatten ", " hattet ",
    " werde ", " wirst ", " wird ", " werden ", " werdet ",
    " kann ", " kannst ", " kann ", " können ", " könnt ",
    " muss ", " musst ", " muss ", " müssen ", " müsst ",
    " soll ", " sollst ", " soll ", " sollen ", " sollt ",
    " will ", " willst ", " will ", " wollen ", " wollt ",
    " darf ", " darfst ", " darf ", " dürfen ", " dürft ",
 
    # Häufige Präpositionen
    " in ", " an ", " auf ", " aus ", " bei ", " mit ", " nach ", " von ", " zu ", " für ", " über ", " unter ", " vor ", " hinter ", " zwischen ",
 
    # Häufige Konjunktionen & Bindewörter
    " und ", " oder ", " aber ", " denn ", " weil ", " da ", " dass ", " ob ", " wenn ", " als ", " obwohl ", " während ", " nachdem ", " bevor ", " damit ", " sobald ",
 
    # Häufige Partikeln & Füllwörter
    " doch ", " nur ", " noch ", " schon ", " auch ", " sehr ", " ganz ", " viel ", " mehr ", " weniger ", " nicht ", " kein ", " keine ", " keinen ", " meines Erachtens ", " übrigens ",
 
    # Fragewörter
    " wie ", " was ", " wo ", " warum ", " wann ", " wer ", " wessen ", " wem ", " wen ", " wohin ", " woher ",
 
    # Typische Endungen, die in deutschen Wörtern stecken
    "keit", "heit", "ung", "schaft", "tion", "tät",  # Substantivierung
    "isch", "lich",                                   # Adjektivendung
    "sam", "bar", "los", "voll", "haft",              # Adjektiv- oder Partikelbereich
 
    # Sonstige typische deutsche Wörter
    " bitte ", " danke ", " bitte schön ", " danke schön ", " leider ", " genau ", " eigentlich ", " nämlich ", " bestimmt ",
    " vielleicht ", " schließlich ", " trotzdem ", " zumindest ", " jedenfalls "
]
 
    text_lower = text.lower()
    return any(token in text_lower for token in german_indicators)