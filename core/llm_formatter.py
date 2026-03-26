import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuracion del Modelo Hibrido
# Por defecto asume que tienes Ollama en local corriendo Llama3, pero puedes cambiarlo a OpenAI o Groq en el .env
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
API_KEY = os.getenv("LLM_API_KEY", "ollama")
BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1") if LLM_PROVIDER == "ollama" else None

try:
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
except Exception:
    client = None

SYSTEM_PROMPT = """You are an expert Obsidian second-brain librarian.
Your task is to take raw, messy input and format it strictly for atomic_concept.md.
Rules:
1. Title MUST be in snake_case and ENGLISH (e.g. server_cache_issue). 
2. Content must be well structured Markdown, highlighting main ideas.
3. Tags must be in English with a hierarchical structure (e.g. area/servers/troubleshooting).

Always output raw JSON with the following keys:
- "title": The snake_case title.
- "tags": A list of formatting tags.
- "content": The generated markdown body.

Output ONLY valid JSON, without ```json markup block wrappers.
"""

def format_raw_input(raw_text: str) -> dict:
    """Takes raw text from the Web UI and formats it using the configured LLM."""
    if not client:
        return fallback_format(raw_text)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Format this raw note:\n{raw_text}"}
            ],
            temperature=0.2
        )
        
        reply = response.choices[0].message.content.strip()
        # Clean potential markdown codeblock formatting if the model disobeys
        if reply.startswith("```json"):
            reply = reply[7:-3]
        elif reply.startswith("```"):
            reply = reply[3:-3]
            
        return json.loads(reply.strip())

    except Exception as e:
        print(f"⚠️ LLM Error: {e}")
        return fallback_format(raw_text)

def fallback_format(raw_text: str) -> dict:
    """Fallback if LLM is down or not configured correctly."""
    title = f"draft_{int(datetime.now().timestamp())}"
    return {
        "title": title,
        "tags": ["area/inbox/unprocessed"],
        "content": raw_text
    }
