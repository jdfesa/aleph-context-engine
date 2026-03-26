---
title: live_second_brain_architecture
status: active
tags: [meta/architecture/obsidian, ai/second_brain/agent]
last_reviewed: 2026-03-26
---
# 🧠 Live Second Brain Architecture (Aleph Context Engine)

## 💡 Concept

### 1. El Objetivo Principal (La Visión)
Construir un "Segundo Cerebro Vivo" (Aleph Context Engine). Un sistema donde el conocimiento se mantiene íntegramente bajo control local y en formato Markdown (Obsidian) siguiendo reglas de formato estrictas (SOPs), pero potenciado por un Motor Híbrido de IA que actúa como un bibliotecario inteligente. La IA procesa notas en crudo, las estructura, evita colisiones y permite recuperar conocimiento semántico (RAG) entre decenas de miles de archivos instantáneamente.

### 2. La Arquitectura del Sistema (Modelo Híbrido)

El sistema se compone de cuatro capas fundamentales para garantizar la escalabilidad y el respeto a la "Fuente de la Verdad" (Obsidian):

**Capa 1: Interfaz de Ingreso (Frontend Web Local)**
La "Aduana Rápida". Interfaz web minimalista (Flask/FastAPI) para capturar ideas sueltas, fragmentos de código o transcripciones sin fricción ni preocupación por el formato.

**Capa 2: El Orquestador (Middleware en Python)**
El script central que intercepta la entrada web. Usa llamadas a LLMs para:
* Reestructurar el texto crudo aplicando la plantilla externa `atomic_concept.md`.
* Forzar el título en `snake_case`, idioma inglés y asignar el estado inicial (`seed`).

**Capa 3: Persistencia Dual (El Cerebro Rápido)**
Mezcla de bases de datos para resolver colisiones y búsquedas a escala (RAG):
*   **SQLite (El Inventario):** Guarda la metadata exacta (Ruta física actual, nombre de archivo, hash único). Evita que la IA sobrescriba notas existentes al crear nuevas, sin importar a qué carpeta de Obsidian las muevas.
*   **ChromaDB (El Buscador Semántico):** Guarda solo los vectores matemáticos del texto y el ID de SQLite. Permite búsquedas instantáneas por significado sin necesidad de leer todos los archivos `.md`.

**Capa 4: Almacenamiento Físico (La Fuente de la Verdad - Obsidian)**
Archivos `.md` puros. El Middleware guardará físicamente el archivo resultante **únicamente** en la carpeta `00_inbox/` para revisión humana obligatoria antes de moverlo a su carpeta definitiva (ej. `20_areas/`).

### 3. El Flujo de Resolución de Colisiones (No-Overwrite)
Si desde la Web UI se envía información sobre un concepto existente:
1. El Middleware consulta **SQLite** para ver si el concepto ya existe en cualquier rama de la bóveda.
2. Si existe, la IA no sobrescribe. Crea una nueva nota con el sufijo `_conflict.md` (ej. `[ID]_nombre_nota_conflict.md`) y la deja en `00_inbox/` para su fusión manual.

### 4. Flujo de Recuperación a Larga Escala (RAG)
1. Preguntas a la IA sobre un tema en la Web UI o MCP.
2. El sistema vectoriza la pregunta y busca en **ChromaDB**.
3. ChromaDB devuelve en milisegundos los 3-5 IDs matemáticamente más relevantes.
4. Con esos IDs, **SQLite** provee las rutas exactas de esos archivos hoy en día.
5. El sistema lee **solo esos 3-5 archivos `.md`** y la IA redacta una respuesta precisa.

### 5. Hoja de Ruta de Desarrollo
*   **Fase 1: Limpieza del Fork Actual.** Eliminar dependencias innecesarias y aislar la Web UI y el esquema básico de servidor.
*   **Fase 2: El Motor de Guardado a Inbox.** Modificar la lógica para que las peticiones web pasen por el LLM (formateo), aseguren un ID y creen el archivo físicamente en `00_inbox/`.
*   **Fase 3: Implementación SQLite.** Crear la base de datos ligera para registrar la ruta y el nombre del archivo al guardarlo.
*   **Fase 4: Integración ChromaDB y RAG.** Añadir la capa de embeddings para indexar el contenido en ChromaDB vinculado al ID de SQLite.

## 🔗 Connections
- MOC: [[architecture_moc]]
- SOP: [[vault_standard_operating_procedure]]
- Strategy: [[obsidian_scaling_and_publishing_strategy]]
