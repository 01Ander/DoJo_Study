# 09 - The DoJo Agent (AI Co-Pilot)

## ¿Qué es el DoJo Agent?

Es el componente "vivo" del ecosistema DoJo v3.2. Actúa como un *Pair Programmer* y vigilante RAG (Retrieval-Augmented Generation) que tiene acceso de lectura instantánea a todos los protocolos, misiones y notas del repositorio.

El objetivo del Agente es reducir la carga cognitiva (apoyando el *Protocol Yellow*), brindando respuestas precisas y basadas **estrictamente en el contexto** de tus propios apuntes, sin alucinaciones de internet.

---

## Arquitectura y MVD (Pair Programmer)

Actualmente, el Agente opera en **Modo Lectura (Vigilante)** bajo las siguientes tecnologías:

*   **Motor Lógico (LLM):** `gemma4:latest` mediante Ollama (modelo optimizado para 24GB de Unified Memory sin colapsar en *Memory Swap*).
*   **Memoria Vectorial:** `ChromaDB` estructurada de forma 100% local en tu disco.
*   **Procesamiento Semántico:** `nomic-embed-text` (Ollama) para crear *Embeddings* instantáneos.
*   **The Watcher (Watchdog en Python):** Un script demonio que monitorea el sistema de archivos del DoJo. Detecta modificaciones o guardados (`Cmd + S`) y ejecuta **Delta Updates** (borra el vector viejo específico de un archivo y le indexa la versión nueva en milisegundos) en lugar de quemar CPU re-indexando todo.

> *(Nota Arquitectónica: La carpeta `dojo_agent/.venv` y la base de datos `dojo_agent/chroma_db` viven estrictamente en tu local y están añadidas al `.gitignore` para no contaminar el versionado del repositorio Misiones).*

---

## Instrucciones de Despliegue (En Local)

Para despertar al Agente debes activar su entorno virtual de Python y arrancar el bucle principal. 

Abre una terminal en la raíz de tu proyecto `DoJo_Study` y ejecuta:

```bash
# Iniciar el servidor local de IA
./dojo_agent/.venv/bin/python dojo_agent/main.py
```

El script revisará todas las rutas permitidas (ignorando explícitamente zonas de legado como `@archive` o directorios de caché) y dejará abierta una CLI interactiva con la etiqueta `DoJo Prompt >>`.
