import os
import glob
from pathlib import Path
from dotenv import load_dotenv

# Import the DB managers
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.db_manager import db
from core.vector_db import vector_db

load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent
VAULT_PATH_STR = os.getenv("OBSIDIAN_VAULT_PATH", str(PROJECT_ROOT / "00_inbox_fallback"))
VAULT_ROOT = Path(VAULT_PATH_STR)

def scan_vault():
    """Scans the physical Obsidian vault and updates SQLite inventory."""
    print(f"🔍 Escaneando la Bóveda en: {VAULT_ROOT}")
    
    if not VAULT_ROOT.exists():
        print("❌ Error: La ruta de Obsidian configurada en .env no existe.")
        return

    # Usar .rglob para buscar todos los .md de forma recursiva (todas las carpetas)
    md_files = list(VAULT_ROOT.rglob("*.md"))
    
    updated_count = 0
    added_count = 0
    
    for path in md_files:
        filename = path.name
        
        # Ignorar archivos ocultos o de configuracion
        if filename.startswith('.'):
            continue
            
        # Extraer ID de Zettelkasten y Titulo (Ej: 2603260715_mi_concepto.md)
        # Asume formato: ID_title.md
        parts = filename.replace('.md', '').split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            note_id = parts[0]
            title = parts[1]
            relative_path = str(path.relative_to(VAULT_ROOT))
            
            if db.note_exists(title):
                db.update_note_path(note_id, relative_path)
                updated_count += 1
            else:
                db.add_note(note_id, title, relative_path)
                added_count += 1
                
            # Full Vault Semantic Indexing via ChromaDB
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                vector_db.add_or_update(
                    note_id=note_id,
                    document=content,
                    metadata={"title": title, "path": relative_path}
                )
            except Exception as e:
                pass
                
    print(f"✅ Escaneo completado y BD Sincronizada.")
    print(f"   => {updated_count} rutas actualizadas.")
    print(f"   => {added_count} notas nativas descubiertas e ingresadas.")

if __name__ == "__main__":
    scan_vault()
