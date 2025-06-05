from llama_cpp import Llama
from config import MODEL_PATH, MAX_TOKENS, TEMPERATURE

# Einmaliges Laden des lokalen LLM-Modells (GGUF)
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=16  # Passe die Anzahl der Threads an deine CPU an
)

def call_local_llm(prompt: str) -> str:
    """
    Sendet den Prompt an das lokale Modell und gibt die generierte Antwort zurück.
    Die Prompt-Einbettung erfolgt im [INST] ... [/INST] Format.
    """
    response = llm(
        prompt=f"[INST] {prompt} [/INST]",
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return response["choices"][0]["text"].strip()
