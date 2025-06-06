"""
llm_api.py

Defines a function to call the Together.ai API (Mixtral-8x7B-Instruct), sending the prompt
and returning the generated answer. The API key is loaded from the environment variable
specified in config.py.
"""

import os
import requests
from dotenv import load_dotenv
from config import TOGETHER_API_KEY_ENV, TOGETHER_MODEL_NAME, MAX_TOKENS, TEMPERATURE

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from environment
TOGETHER_API_KEY = os.getenv(TOGETHER_API_KEY_ENV)
if not TOGETHER_API_KEY:
    raise ValueError(f"Environment variable '{TOGETHER_API_KEY_ENV}' not found. "
                     "Please create a .env file with your Together.ai API key.")

def call_llm_via_together(prompt: str) -> str:
    """
    Sends a completion request to Together.ai's Mixtral-8x7B-Instruct model.
    Returns the answer text. If an error occurs, returns a descriptive message.

    Args:
        prompt (str): The full prompt, including context and question.

    Returns:
        str: The content of the LLM's answer, or an error message.
    """
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": TOGETHER_MODEL_NAME,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=data,
            timeout=30  # seconds
        )
        response.raise_for_status()
        json_resp = response.json()
        # Extract the first choice's text
        answer_text = json_resp["choices"][0]["text"].strip()
        return answer_text
    except requests.exceptions.RequestException as e:
        # In case of a network error or HTTP error
        return f"[Error calling LLM API] {str(e)}"
    except (KeyError, IndexError) as e:
        # In case the JSON format is unexpected
        return f"[Unexpected API response format] {str(e)}"
