import sqlite3
import os
from datetime import datetime
from pathlib import Path

# La DB se guarda en la carpeta data del motor, no ensucia la Bóveda del usuario.
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "vault_inventory.db"

class DBManager:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Creates the inventory table if it doesn't exist."""
        os.makedirs(DB_PATH.parent, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    current_path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            # Indice para búsquedas rápidas por titulo (para evitar colisiones)
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON notes(title)')
            conn.commit()

    def note_exists(self, title: str) -> bool:
        """Checks if a note with the exact snake_case title already exists ANYWHERE in the vault."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM notes WHERE title = ?', (title,))
            return cursor.fetchone() is not None

    def add_note(self, note_id: str, title: str, relative_path: str):
        """Registers a newly created note in the inventory."""
        now = datetime.now().astimezone().isoformat()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notes (id, title, current_path, created_at)
                VALUES (?, ?, ?, ?)
            ''', (note_id, title, relative_path, now))
            conn.commit()

    def update_note_path(self, note_id: str, new_relative_path: str):
        """Updates where the note lives after the user moves it manually in Obsidian."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE notes SET current_path = ? WHERE id = ?
            ''', (new_relative_path, note_id))
            conn.commit()

# Expose global instance
db = DBManager()
