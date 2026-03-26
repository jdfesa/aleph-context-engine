import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Import our new SQLite manager
from core.db_manager import db
from core.vector_db import vector_db

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_PATH_STR = os.getenv("OBSIDIAN_VAULT_PATH", str(PROJECT_ROOT / "00_inbox_fallback"))
VAULT_ROOT = Path(VAULT_PATH_STR)

# We enforce the SOP: All AI generated content goes to 00_inbox
INBOX_DIR = VAULT_ROOT / "00_inbox"
INBOX_DIR.mkdir(parents=True, exist_ok=True)

class MemoryManager:
    """
    Aleph Context Engine - Phase 2 Memory Manager
    Handles writing physical Markdown files to the Inbox directory obeying the Vault SOP.
    """
    def __init__(self):
        self.inbox_dir = INBOX_DIR

    def _get_file_path(self, title: str) -> Path:
        """Returns physical .md path using Zettelkasten prefix to avoid collisions."""
        timestamp = datetime.now().astimezone().strftime('%y%m%d%H%M')
        clean_title = title.replace('.md', '').strip().replace(' ', '_')
        
        # Base format: YYMMDDHHMM_snake_case_title.md
        filename = f"{timestamp}_{clean_title}.md"
        path = self.inbox_dir / filename
        
        # Collision Prevention (Phase 3 via SQLite)
        # If the DB knows this title exists ANYWHERE in the vault, we append conflict to obey SOPs.
        counter = 1
        final_title = clean_title
        while db.note_exists(final_title) or path.exists():
            final_title = f"{clean_title}_conflict_{counter}"
            filename = f"{timestamp}_{final_title}.md"
            path = self.inbox_dir / filename
            counter += 1
            
        return path, timestamp, final_title

    def store_memory(self, raw_input: str, formatted_data: dict) -> Dict[str, Any]:
        """Saves formatted memory directly to the 00_inbox as an atomic Concept .md file."""
        title = formatted_data.get("title", "untitled_concept")
        tags_list = formatted_data.get("tags", ["area/inbox/unprocessed"])
        content = formatted_data.get("content", raw_input)
        
        # Format tags properly for frontmatter
        tags_str = ", ".join(tags_list) if isinstance(tags_list, list) else tags_list
        tags_array = f"[{tags_str}]"
        
        now = datetime.now().astimezone().strftime('%Y-%m-%d')
        file_path, note_id, safe_title = self._get_file_path(title)
        
        # Build Obsidian YAML Frontmatter (Adhering to Vault SOP)
        md_content = f"""---
title: {safe_title}
status: seed
tags: {tags_array}
last_reviewed: {now}
---
# {safe_title}

## 💡 Concept
{content}

## 🔗 Connections
- MOC: [[architecture_moc]]
"""
        # Save to real Obsidian Vault
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        # Phase 3: Register in SQLite Inventory!
        relative_path = f"00_inbox/{file_path.name}"
        db.add_note(note_id, safe_title, relative_path)
            
        # Phase 4: Register in ChromaDB (Semantic Vector Store)
        # We index the raw Concept only (not the YAML tags) for better math representation
        vector_db.add_or_update(
            note_id=note_id,
            document=content,
            metadata={"title": safe_title, "path": relative_path}
        )
            
        return {
            "key": note_id,
            "title": safe_title,
            "path": relative_path,
            "updated_at": now,
            "content": content
        }

    # Dummy methods to keep WebUI and Server from crashing until Phase 3/4 (SQLite/Chroma)
    def list_memories(self) -> List[Dict[str, Any]]:
        return []
    
    def retrieve_memory(self, key: str) -> Optional[Dict[str, Any]]:
        return None
        
    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Semantic search using ChromaDB."""
        results = vector_db.search(query, n_results=5)
        
        formatted_results = []
        if results and results.get('ids') and results['ids'][0]:
            ids = results['ids'][0]
            metadatas = results['metadatas'][0]
            documents = results['documents'][0]
            
            for i, note_id in enumerate(ids):
                # Resolve title and path directly from metadata fast-cache
                title = metadatas[i].get('title', 'Unknown Title')
                path = metadatas[i].get('path', 'Unknown Path')
                snippet = documents[i][:150] + "..." if len(documents[i]) > 150 else documents[i]
                
                formatted_results.append({
                    "key": note_id,
                    "title": title,
                    "path": path,
                    "snippet": snippet,
                    "updated_at": "vector_search" 
                })
        return formatted_results
        
    def delete_memory(self, key: str) -> bool:
        return False

# Global instance
memory_manager = MemoryManager()
