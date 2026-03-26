---
title: vault_standard_operating_procedure
aliases: [Vault SOP, Estándares de la Bóveda, Reglas]
tags: [meta/architecture/obsidian, sop]
status: active
last_reviewed: 2026-03-22
---

# 🏗️ Vault Standard Operating Procedure (SOP)

Este documento define la arquitectura para un Segundo Cerebro escalable, portable y optimizado para el uso manual y automatizado (IA, scripts, CLI).

## 1. 🔤 Nomenclatura Estricta (Naming)
Para garantizar la compatibilidad universal con terminales, scripts y sistemas de archivos:

*   **Regla de Oro**: Todo archivo y carpeta usará estrictamente `snake_case` (minúsculas y guiones bajos). **Prohibido**: espacios, mayúsculas, tildes, eñes o caracteres especiales.
*   **Idioma Global**: Todos los nombres de archivos (notas y assets) serán en **Inglés**.
*   **Notas (`.md`)**: Nombres descriptivos directos.
    *   *Ejemplo*: `relational_database_model.md`
*   **Assets (Images/Diagrams)**: Deben incluir un prefijo para clasificación rápida:
    *   `img_`: Para capturas de pantalla, fotos o ilustraciones generales.
    *   `diag_`: Para diagramas de flujo, arquitectura, UML o esquemas lógicos.
    *   *Ejemplo*: `diag_entity_relationship_v1.png`, `img_proxmox_dashboard.jpg`
*   **Etiquetas (Nested Tags)**: Jerarquías `#area/subtema/detalle`.

## 2. 🤖 Generación por IA y Automatizaciones (La Aduana)
*   Todo contenido generado externamente (Gemini CLI, scripts, LLMs) **debe aterrizar en `00_inbox/`**.
*   Revisión manual obligatoria antes de "nacionalizar" la nota en su directorio permanente.

### 2.1 Reglas Estrictas Anti-Colisión (No-Overwrite)
Para proteger la integridad del Segundo Cerebro de reemplazos accidentales por automatizaciones o IAs:
*   **Prohibición de Sobrescritura**: Ningún bot, IA o script tiene autorización para sobrescribir (overwrite/clobber) un archivo existente en los directorios permanentes de la bóveda (como `10_projects`, `20_areas`).
*   **Resolución de Conflictos (`_conflict`)**: Si una IA o script debe mover una nota desde la Aduana hacia un directorio temporal o permanente, y detecta que ya existe un archivo con exactamente el mismo nombre, **está obligada** a renombrar la nota entrante agregándole el sufijo `_conflict` (ej. `nombre_nota_conflict.md`). Ambas notas deben coexistir hasta que el humano las procese manualmente.
*   **Directiva de Fusión (Append)**: Si la instrucción explícita es *actualizar* información en una nota, la IA debe añadir (`append`) la información nueva al archivo original bajo un nuevo encabezado (ej. `## Update`), pero jamás reemplazar su contenido total basándose únicamente en propiedades como `last_reviewed`.

## 3. 🧠 Estructura de Conocimiento (MOCs y Conectividad)
1.  **Notas Atómicas**: Cada concepto es una nota propia (un solo archivo = una sola idea).
2.  **Dashboard / Unidad (MOC)**: Nota que actúa como índice estructurado.
3.  **Enlace Ascendente (Upward Link)**: Toda nota atómica debe finalizar con un enlace a su MOC padre (ej: `## 🔗 Connections: [[unit_1_intro]]`).
4.  **Transclusión**: Usar `![[nota_atomica]]` en el MOC para lectura lineal al estudiar.

## 4. 📂 Silos de Contexto y Modularidad
*   **Silos**: `00_inbox`, `01_daily`, `05_notes`, `10_projects`, `20_areas`, `30_resources`, `40_archive`.
*   **Assets de Proximidad**: Las imágenes/diagramas viven en una subcarpeta `img/` dentro de la carpeta del proyecto o materia.
    *   *Ruta*: `20_areas/academics/tads/subjects/databases/img/diag_relational_schema.png`
*   **Excepción de Inmersión**: La carpeta `20_areas/english/` es íntegramente en inglés (nombre y contenido).

## 5. ⏳ Ciclo de Vida y Mantenimiento (Status)
Toda nota debe incluir:
*   `status`: `seed` (bruto), `growth` (en curso), `evergreen` (validado), `archived` (histórico).
*   `last_reviewed`: `YYYY-MM-DD` (obligatorio para `tech_setup` y `servers`). **Regla de Actualización Estricta**: Cada vez que se modifique, expanda o corrija el contenido de una nota existente (sea manual o mediante IA), se debe actualizar obligatoriamente esta fecha al día corriente.

## 6. 🛠️ Protocolo de Refactorización
1.  **Atomicidad**: Separar conceptos largos en notas individuales.
2.  **Renombrar**: Aplicar `snake_case` e **Inglés** a todo. Añadir prefijos `img_` o `diag_` a los assets.
3.  **Actualizar Tags**: Seguir la estructura jerárquica.
4.  **Localizar Assets**: Mover archivos de `99_assets` a la carpeta `img/` local.

## 7. 📄 Plantillas Maestras

### `atomic_concept.md`
```yaml
---
title: {{title}}
status: seed
tags: [area/topic/subtopic]
last_reviewed: {{date}}
---
# {{title}}

## 💡 Concept
...

## 🔗 Connections
- MOC: [[parent_moc]]
```

---
*Última revisión: 2026-03-14*
