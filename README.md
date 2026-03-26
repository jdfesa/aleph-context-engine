# 🧠 Aleph Context Engine

A Local-First, AI-driven Second Brain built on top of Obsidian. **Aleph Context Engine** acts as an intelligent middleware and vector database for your Zettelkasten, allowing you to capture raw thoughts instantly and retrieve them semantically, without ever losing control of your Markdown files.

## 💡 Architecture Overview

Aleph Context Engine works as a hybrid-RAG (Retrieval-Augmented Generation) system specifically designed to respect strict Obsidian conventions (SOPs).

1. **Frontend (Local Web UI):** A frictionless capture web interface to drop raw thoughts, code snippets, or ideas.
2. **Middleware (Python):** An AI orchestrator that automatically structures your raw input following the `atomic_concept.md` template, enforcing `snake_case` naming and English tags.
3. **Dual Persistence (Hybrid Core):** 
   - **SQLite:** Acts as a precise inventory to prevent note collisions and track the exact physical paths of your `.md` files, even when you move them during refactoring.
   - **ChromaDB:** A silent semantic search engine (Vector DB) that maps the meaning of your notes, allowing instant retrieval across tens of thousands of concepts.
4. **Backend (Obsidian Vault):** The single source of truth. All processed notes are materialized as pure `.md` files sequentially dropped into your `00_inbox/` for human review before final classification. 

## 🚀 Key Features

*   **No-Overwrite Policy:** The engine strictly respects your permanent folders. If an AI agent attempts to save a note that semantically collides with an existing internal note, it generates a `_conflict.md` draft for manual merging.
*   **Semantic O(1) Retrieval:** Ask questions about concepts you saved years ago. The engine uses ChromaDB to fetch only the 3-5 most relevant `.md` files without iterating over your entire Vault.
*   **100% Extensible:** Built to run on macOS cleanly using lightweight dependencies, with no background Linux daemons or heavy document-based databases (MongoDB/PostgreSQL) required.

## 🛠️ Setup (Mac)

*(Installation instructions coming soon during Phase 2).*

---
*Forked originally from ContextKeep, heavily modified for Local Obsidian AI Workflows.*
