---
title: obsidian_scaling_and_publishing_strategy
status: seed
tags: [tech_setup/obsidian/strategy]
last_reviewed: 2026-03-21
---
# 🚀 Estrategia de Escalado y Publicación de la Bóveda

Este documento consolida las mejores prácticas para estructurar el "Segundo Cerebro" con un enfoque técnico robusto y escalable, pensado en la sincronización, control de versiones (Git) y su eventual publicación online.

## 1. Sincronización y Control de Versiones con GitHub
Para un control de cambios confiable (esencial en documentación de ingeniería) y acceso remoto:
- **Obsidian Git**: Instalar este plugin comunitario para gestionar commits y pushes automatizados hacia un repositorio de GitHub.
- **Configuración Local**:
  - Asegurar la existencia de un `.gitignore` en la carpeta raíz.
  - *Archivos a ignorar*: Agregar `.obsidian/workspace.json` (o `.obsidian/workspace*`) al `.gitignore`. Esto evita conflictos constantes generados al abrir y cerrar paneles en la aplicación local.

## 2. Enlaces Relativos (Compatibilidad Universal)
Al tratar la bóveda como documentación nativa en Markdown, debe poder leerse sin depender del motor de Obsidian (por ejemplo, navegando el repositorio directamente desde GitHub).
- En *Settings > Files and links*:
  - **Default location for new attachments**: Cambiar a *In subfolder under current folder*. Nombrar la carpeta: `img`.
  - **New link format**: Cambiar a **Relative path to file**.
- **Wikilinks (`[[nota]]`) vs. Markdown Standard (`[nota](./nota.md)`)**:
  - Se recomienda usar los links nativos de Markdown (`[texto](ruta_relativa)`) para garantizar 100% de compatibilidad pura con plataformas externas y GitHub.
  - *Excepción*: Si la herramienta de publicación (como Quartz) soporta Wikilinks nativamente, entonces desactivar las rutas relativas no es estrictamente necesario, pero para portabilidad total a nivel archivo, el path relativo es la "Aduana".

## 3. Frameworks de Publicación
Para exponer este conocimiento como una wiki técnica interna o un portal técnico:
- **Quartz**: Construido nativamente para integrarse con bóvedas de Obsidian. Soporta carpetas y Wikilinks de inmediato. Renderiza gráficos interactivos (como el network graph) y callouts como en la app nativa.
- **MkDocs (Material for MkDocs)**: El estándar absoluto de la industria para documentación de software. Funciona perfectamente si todas las notas siguen la regla de enlaces Markdown estándar y jerarquía estricta.

## 4. Filosofía de Arquitectura de Contenido (Orquestación Continua)
Como repositorio de conocimiento técnico, se adoptan estos principios implacables:
- **Modularidad Asfíctica (Atomicidad)**: Separar conceptos largos en notas discretas. No crear monolitos, usar un MOC que vincule a múltiples sub-recursos lógicos.
- **Nomenclatura (Snake Case)**: Todo recurso, imagen, diagrama y documento de texto irá en minúsculas y separado por guiones bajos. Preserva los enlaces y garantiza interoperabilidad con automatizaciones CLI/Bash.

## 🔗 Connections
- MOC: [[vault_standard_operating_procedure]]
