# 🧠 Aleph Context Engine

A Local-First, AI-driven Second Brain built on top of Obsidian. **Aleph Context Engine** acts as an intelligent middleware and vector database for your Zettelkasten, allowing you to capture raw thoughts instantly and retrieve them semantically, without ever losing control of your Markdown files.

## 💡 System Architecture

Aleph Context Engine works as a hybrid-RAG (Retrieval-Augmented Generation) system specifically designed to respect strict Obsidian conventions (SOPs).

1. **Frontend (Local Web UI):** A frictionless capture web interface to drop raw thoughts, code snippets, or ideas.
2. **Middleware Output (`core/llm_formatter.py`):** An AI orchestrator that automatically structures your raw input following the `atomic_concept.md` template, enforcing `snake_case` naming and proper metadata tracking. Fully supports local models via **Ollama** or cloud APIs (OpenAI, Groq, etc).
3. **Dual Persistence Core:** 
   - **SQLite (`vault_inventory.db`):** Acts as a precise inventory to prevent note collisions and track the exact physical paths of your `.md` files, even when you move them manually inside Obsidian.
   - **ChromaDB (`vector_db.py`):** A silent semantic search engine (Vector DB) that maps the mathematical meaning of your notes, allowing instant insight-retrieval across tens of thousands of concepts.
4. **Backend (Obsidian Vault):** The Single Source of Truth. All processed notes are materialized as pure `.md` files and sequentially dropped into your `00_inbox/` for human review before final classification. 

## 🚀 Key Features

*   **No-Overwrite Policy:** The engine strictly respects your permanent folders. If an AI agent attempts to save a note that semantically collides with an existing internal note (tracked by SQLite), it generates a `_conflict.md` draft for manual merging. No data is ever overwritten.
*   **Semantic O(1) Retrieval:** Ask questions about concepts you saved years ago. The engine uses ChromaDB to fetch only the 3-5 most relevant `.md` files without iterating over your entire vault folder structure.
*   **Vault Scanner Tool:** A built-in script (`core/vault_scanner.py`) that syncs your entire vault's historical data into the DBs, reliably tracking any file you physically drag-and-drop within your Obsidian folders.
*   **100% Extensible & Local:** Built to run on macOS cleanly using lightweight dependencies, with no background Linux daemons or heavy document-based databases (MongoDB/PostgreSQL) required.

## 🛠️ Installation & Setup

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Configure your Environment:**
    Copy the example `.env` file and adjust the paths to your local setup:
    ```bash
    cp .env.example .env
    ```
    **Required Configuration in `.env`:**
    *   `OBSIDIAN_VAULT_PATH=/absolute/path/to/your/Vault` (The engine uses this to route files into `00_inbox/`).
    *   Configure your preferred `LLM_PROVIDER` (defaults to `ollama` for total privacy).

3. **(Optional) Run the Vault Scanner:**
    If you are connecting an existing Obsidian vault, run the scanner once to index all your current files into SQLite and ChromaDB:
    ```bash
    python core/vault_scanner.py
    ```

4. **Start the Capture Engine:**
    Launch the Web UI to start dropping notes:
    ```bash
    python webui.py
    ```

## 📂 Project Structure

*   `webui.py`: Flask-based capture interface.
*   `server.py`: MCP (Model Context Protocol) server for IDE integration.
*   `core/llm_formatter.py`: LLM formatting pipeline for raw-to-Markdown translation.
*   `core/memory_manager.py`: Core logic for saving to Obsidian and registering to DBs.
*   `core/db_manager.py`: SQLite collision tracker.
*   `core/vector_db.py`: ChromaDB semantic embedding engine.
*   `core/vault_scanner.py`: Full vault syncing and ingestion script.

---
*Built to enforce strict Obsidian Vault SOPs while unlocking AI capabilities.*
