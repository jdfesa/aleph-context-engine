import os
import chromadb
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"

class VectorDBManager:
    """
    Aleph Context Engine - Phase 4 Semantic Core
    Uses ChromaDB in Persistent Mode (Serverless/Local only).
    """
    def __init__(self):
        # Al inicializar esta clase por primera vez, Chroma descargara un modelo 
        # cuantizado y enano (all-MiniLM-L6-v2) de ~80MB en tu Mac que procesara 
        # todo el texto localmente de por vida sin necesidad de APIs externas.
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        
        self.collection = self.client.get_or_create_collection(
            name="obsidian_vault_memory",
            metadata={"hnsw:space": "cosine"}
        )

    def add_or_update(self, note_id: str, document: str, metadata: dict):
        """Indexes the raw text of the note associated with the SQL note_id."""
        try:
            self.collection.upsert(
                documents=[document],
                metadatas=[metadata],
                ids=[note_id]
            )
        except Exception as e:
            print(f"⚠️ ChromaDB Indexing Error: {e}")

    def search(self, query: str, n_results: int = 5):
        """Fetches the top N most semantically relevant memories."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"⚠️ ChromaDB Query Error: {e}")
            return {"ids": [[]], "documents": [[]], "metadatas": [[]]}

# Global instance
vector_db = VectorDBManager()
