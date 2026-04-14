# Changelog

All notable changes to DoJo Study will be documented in this file.

## [4.0.0] - 2026-04-13

### 🏗️ BREAKING: Platform Migration to Hermes Agent

DoJo Study migra de un agente monolítico custom (`main.py`, 565 líneas, LangChain + ChromaDB) a **Hermes Agent** (NousResearch) como plataforma de runtime.

### Added
- `.hermes.md` — Constitución del DoJo como Context File (inyección automática)
- 3 personalidades Hermes: `dojo-tutor`, `dojo-reviewer`, `dojo-architect`
- 6 Skills del DoJo como paquetes Hermes:
  - `dojo-start` — Iniciar sesiones de estudio
  - `dojo-log` — Registrar en bitácora
  - `domain-shifting` — Protocolo de analogías
  - `socratic-review` — Protocolo de revisión socrática
  - `mini-rfc` — Templates de diseño previo
  - `dojo-done` — Marcar misiones completadas (planned)
- `CHANGELOG.md`
- Soporte multi-modelo via OpenRouter:
  - **Qwen3.6 Plus** (Tutor/Reviewer) — $0.325/$1.95 per M tokens
  - **Gemma 4 31B** (Scribe) — FREE
  - **Gemini 3.1 Pro / Opus 4.6** (Architect) — Premium

### Changed
- Comando `/mode work` → `/personality dojo-reviewer`
- Comando `/mode main` → `/personality dojo-tutor`  
- Comando `/mode think` / `/mode global` → `/personality dojo-architect`
- Comando `/start` → `/dojo-start`
- Comando `/log` → `/dojo-log`
- Comando `/audit` → Eliminado (reemplazado por switch directo de personalidad + modelo)
- RAG via ChromaDB → Context Files + Skills de Hermes
- Memoria conversacional (lista Python) → SQLite + FTS5 persistente de Hermes
- Terminal rendering (glow) → Hermes terminal UI nativa

### Removed
- `dojo_agent/main.py` — Archivado en `archive/legacy_main_v3.py`
- `dojo_agent/requirements.txt` — Archivado  
- Dependencia de ChromaDB, LangChain, Watchdog
- Dependencia de Ollama como backend primario (mantiene como fallback)
- Comando `/audit` (ahora innecesario)

### Architecture
- De monolito Python (1 archivo, 5 personalidades vía prompt switching) a plataforma Hermes con personalidades SOUL.md + Skills modulares
- De embeddings locales (nomic-embed-text) a Context Files estáticos
- De memoria volátil (lista Python capped a 10) a SQLite persistente entre sesiones
- Multi-agente via `delegate_task` (Scribe como sub-agente para auto-logging)

---

## [3.3.0] - 2026-04-10

### Added
- Integración de `glow` para rendering de Markdown en terminal
- Rich console como fallback
- Limpieza de artefactos LaTeX en respuestas

## [3.2.0] - 2026-04-08

### Added
- Employability Guardian (Tarea 2 del WORK mode)
- MVP Discernment Protocol (Tarea 3 del WORK mode)
- Executive Override (Tarea 4 del WORK mode)
- RAG context injection con lectura física de requirements.md

## [3.0.0] - 2026-04-03

### Added
- DoJo Agent v3 — Agente monolítico con 5 personalidades
- ChromaDB para base vectorial local
- Watchdog para file watching
- Auto-logging en journals
- CLI middleware con NLP heurístico
