"""
web_ui.py

Gradio-based web interface for the Cybersecurity RAG Chatbot.
- Accepts a user question (German or English).
- Retrieves the top K relevant chunks from local FAISS.
- Builds a strict context-based prompt.
- Calls Together.ai for completion.
- Cleans any unwanted separators (e.g., '--- ANSWER ---') from the LLM output.
- Returns the cleaned answer and the list of sources to display.

Usage:
    python web_ui.py
Then open http://localhost:7860 in your browser.
"""

import re
import gradio as gr
from query_pipeline import get_top_chunks, build_prompt
from llm_api import call_llm_via_together
from config import TOP_K

def clean_answer_text(raw_text: str) -> str:
    """
    Remove any lines that look like a separator (e.g., '--- ANSWER ---') 
    or are blank/whitespace at the very beginning of the response. 
    Ensures only the pure answer text remains.
    """
    if not raw_text:
        return ""

    # Split into individual lines
    lines = raw_text.splitlines()
    cleaned_lines = []
    skip_zone = True

    for line in lines:
        # Trim leading/trailing whitespace from this line
        stripped = line.strip()

        # If we are still skipping leading separators/blanks:
        if skip_zone:
            # Detect a separator if the line consists mostly of hyphens and the word "answer" (case‐insensitive)
            # e.g., "--- ANSWER ---", "-- answer --", "-----Answer-----", etc.
            if re.fullmatch(r"-*\s*answer\s*-*", stripped, flags=re.IGNORECASE):
                # Continue skipping this line
                continue
            # Also skip any empty/whitespace‐only lines at the very top
            if stripped == "":
                continue
            # As soon as we hit a non‐separator, non‐blank line, stop skipping
            skip_zone = False

        # Once skip_zone is False, keep all subsequent lines exactly as they are
        cleaned_lines.append(line)

    # Join the remaining lines back into a single text,
    # then strip any trailing blank lines
    result = "\n".join(cleaned_lines).rstrip()
    return result

def chat_interface(user_input: str):
    """
    Handles the Gradio chat logic:
    1. Retrieve top-K chunks from FAISS.
    2. Build the strict context-based prompt instructing the LLM not to invent facts.
    3. Call Together.ai and get the raw answer.
    4. Clean any leading separators (e.g., '--- ANSWER ---') or blank lines.
    5. Return the cleaned answer plus a newline-separated list of sources.
    """
    # Step 1: Retrieve and rerank chunks
    chunks = get_top_chunks(user_input)
    if not chunks:
        return "No relevant content found.", ""

    # Step 2: Build prompt
    prompt = build_prompt(chunks, user_input)

    # Step 3: Call Together.ai
    raw_answer = call_llm_via_together(prompt)

    # Step 4: Clean out any leading separator lines (like '--- ANSWER ---')
    answer = clean_answer_text(raw_answer)

    # Step 5: Build the source list
    sources_text = "\n".join(
        f"- {chunk['source']} (Chunk ID: {chunk['id']})"
        for chunk in chunks[:TOP_K]
    )

    return answer, sources_text

# Create Gradio Blocks UI
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 🛡️ Cybersecurity RAG Chatbot
        **Offline & Local Context** – Powered by 500+ curated cybersecurity research papers.  
        Ask questions in **German or English** and receive strictly context-based responses.
        """
    )

    user_input = gr.Textbox(
        placeholder="Type your question here...",
        label="Question",
        lines=3
    )
    btn = gr.Button(value="Generate Answer", variant="primary")
    answer_output = gr.Textbox(label="Answer", lines=8, interactive=False)
    sources_output = gr.Textbox(label="Sources Used", lines=6, interactive=False)

    btn.click(
        fn=chat_interface,
        inputs=[user_input],
        outputs=[answer_output, sources_output]
    )

# Launch the app on localhost:7860
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, show_error=True)
