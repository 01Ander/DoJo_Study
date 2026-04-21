# Changelog

All notable changes to DoJo Study will be documented in this file.

## [4.2.1] - 2026-04-20

### Changed
- **Mission Structural Standardization:** Mandated and implemented a strict, isolated topology for all missions. Each mission now holds its own `requirements.md`, `Mini-RFC.md`, `journal.md`, and an isolated `code/` execution directory (`src/`, `tests/`, `data/`).
- **Campaign Pure Nomenclature:** Cleaned all mission folder names in `PY-POO-FINANCE` to strictly use alphanumeric IDs (e.g., `M01`, `B01`) without descriptive suffixes, maintaining descriptions only in Markdown lists.
- **Legacy Freezing:** Officially marked the `PY-BASICO` campaign as `✅ Done` in the global Python scope, anchoring it as legacy and excluding it from the new `code/` folder topology requirements. 

---

## [4.2.0] - 2026-04-18

### 🏗️ "The On-Demand Automation Update"

### Added
- **Idea Capture Skill:** Created `/dojo-idea` for atomic, fire-and-forget idea registration during deep work sessions.
- **Mini-RFC Template:** Created `templates/mini-rfc-template.md` with guided questions across 6 sections (Business Context, Technical Scope, Architecture Decision, Edge Cases, Testing Strategy, Approval Checklist).
- **Triage Protocol:** Formalized a binary decision tree in `guia-operaciones-v4.md` for handling bugs detected during deep work (patch vs defer).
- **WakaTime Integration:** `/dojo-log --summary` now attempts to inject coding time from the local WakaTime API (best-effort with graceful fallback).

### Changed
- **Bidirectional Meta-Documents:** `/dojo-start` now updates mission Status from `🟢 Ready` to `🔵 En Ejecución` when starting work.
- **Journal Log v2:** Upgraded `/dojo-log` to v2.0.0 with structured summary templates, LLM model auto-identification, and `--summary` mode.

---

## [4.1.2] - 2026-04-17

### Added
- **Mini-RFC Template Prioritization:** Marked the creation of a standardized Mini-RFC template as a high-priority feature in the pending ideas list.
- **Automated Dojo Logging Template:** Explicitly defined a new feature request to standardize the `/dojo-log` skill, forcing the LLM to auto-identify and fetch precise timings via the WakaTime API when writing to the mission journal.

### Changed
- **Testing Configuration:** Migrated `SETUP_TESTING.md` from the isolated B01 mission folder to the `PY-BASICO` campaign root for global, campaign-wide testing guidelines.
- **Implemented Live Features:** Cleared `/stop_sesion` and `/stop` de-anchoring ideas from `ideas-in-live.md` as they have now been fully integrated into the live agent skills (`session-pause` and `mission-done`).

---

## [4.1.1] - 2026-04-16

### Changed
- **System Documentation DRYing:** Centralized AI operational personality logic (`dojo-tutor`, `reviewer`, `architect`) strictly into `08-dojo-agent.md` and `.hermes.md`.
- **System Documentation Normalization:** Removed deprecated file `05-estructura-chats-XX-MAIN-EXERCISES-WORK.md`, shifting index numbering accordingly for a cleaner `docs/` structure.
- **Rest Day Clarification:** Resolved conflicting timelines. Architect windows are strictly Saturday mornings (if necessary). Absolute Rest Days (*Zero-Code Policy*) cover Saturday afternoons and Sundays across all core docs.
- **Git Hygiene:** Added `.mypy_cache/` to `.gitignore` and purged cached development artifacts from tracked mission folders.

---

## [4.1.0] - 2026-04-16

### Added
- **Skills Expansion:** Created `/dojo-done` to formally close missions, log them to the journal, and update their states.
- **Cognitive Sustainability:** Created `/stop-sesion` allowing Operators to pause a Deep Work block mid-session, persisting state into `.dojo-session.json`.
- **Session Inference:** Enhanced `/dojo-start` with a local state scanning algorithm to automatically suggest resuming paused sessions.
- **Mission B01:** Formally created the *Log Analyzer* B01 mission within PY-BASICO, enforcing Phase 2 (Socratic Reviewer) methodology.

### Changed
- `.hermes.md` Constitution updated with new available skills.
- `docs/guia-operaciones-v4.md` updated with new fast-commands and workflow references.
- Added `.dojo-session.json` to `.gitignore`.
- Marked `PY-BASICO/missions/B00/requirements.md` as completed.

---

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

## [3.3.4] - 2026-04-09

### Added
- **Employability Guardian:** Upgraded the `DojoAgent` with a global logic interceptor that mandates "Business Context" and "ROI" for all mission implementations.
- **Pillar 6 (The Business Translation):** Integrated the 6th philosophical pillar into the core document, establishing that technical artifacts must solve business problems.
- **Business-First Templates:** Refactored Campaign and Mission templates to include mandatory sections for Value Proposition and ROI metrics.
- **Social DoD:** Added a mandatory "Social README" criterion for all Boss Missions to ensure visibility for non-technical stakeholders (HR/PMs).

## [3.3.3] - 2026-04-09

### Added
- **Timeout AI (Umbral Dinámico):** Formalized a time-based anti-codependency protocol. Set thresholds of 30 mins (small tasks) and 60 mins (architecture) of independent effort before escalating AI assistance.
- **Degradación Transitoria:** Introduced a mandatory session reset (15-30 min break) if the Timeout AI threshold is reached without progress, preventing cognitive gridlock.

## [3.3.2] - 2026-04-09

### Added
- **Socratic AI Transformation:** Pivoted `MAIN` and `WORK` modes to prioritize questioning and theoretical guidance over direct code generation, preventing AI codependency and fostering autonomous engineering logic.
- **Mandatory Weekend Rest Policy:** Hardcoded Saturdays and Sundays as mandatory Rest Days (Modo 0) in the core system documentation to ensure physiological and cognitive sustainability.
- **Protocol Yellow Gatekeeper:** Integrated Protocol Yellow into the pre-session ritual; if initial friction > 6, the session is preemptively aborted to prevent low-voltage progression.

## [3.3.1] - 2026-04-08

### Added
- **Hybrid RAG Architecture:** Implemented a physical injection layer that bypasses vector semantic "fade-out". The Operator now forcefully reads `requirements.md` and the last 10 lines of `journal.md` directly from the disk when a mission context is active.
- **Inter-Session Episodic Memory:** Enabled persistent "yesterday memory" by treating the physical journal tail as a primary context source, allowing the agent to remember progress even after a full application restart.
- **Deep Visibility Indexing:** Modified the ingestion pipeline to "tattoo" the relative file path into the `page_content` of every chunk, ensuring 100% retrieval accuracy for folder-specific keywords like "B00".
- **Traceable Auto-Logging:** Refactored the journal logging format to include the User's Query (Q) alongside the Agent's Response (A) and the active Mode, creating a full forensic audit trail of the study session.
- **New Operational Mode (`/mode think`):** Introduced a cognitive "Fellow Partner" persona that allows the AI to provide subjective analyses, opinions, and philosophical reasoning about the system and the user's progress.

### Changed
- **Mission Name Standardization:** Renamed `B00_assessment` to `B00` across the entire repository (filesystem, code references, and documentation) for a cleaner UX.
- **Enhanced NLP Parser:** Improved the regex-free path detection to be more resilient to casing and partial matches during mission binding.

## [3.3.0] - 2026-04-08

### Added
- **DoJo Operator CLI:** Transformed the passive watcher into an interactive CLI (`dojo_agent/main.py`) featuring Slash Commands (`/start`, `/log`, `/audit`, `/mode`) and Natural Language Processing capable of intercepting and binding project context dynamically.
- **RAG Conversational Memory:** Engineered an invisible short-term rolling window memory mapped into LCEL dictionaries to allow coherent back-and-forth Pair Programming turns without context loss, bounded by a 10-item cap to prevent RAM leaks.
- **RAG Atomicity Controls:** Hardened the SQLite / ChromaDB indexing flow by applying transactional inserts and deferring vector deletions to guarantee zero orphaned knowledge if an indexing operation fails.
- **Audit Payload Generator:** Added `/audit` command to auto-generate high-density RAG queries containing exact local codebase implementations, optimizing external cloud evaluations.
- **The DoJo Agent (AI Co-Pilot):** Created a fully local RAG interactive system based on `ChromaDB` and `gemma4:latest` using `nomic-embed-text` embeddings.
- **Agent Delta Updates Watchdog:** Implemented a Python background process (`dojo_agent/main.py`) to monitor and index live changes of the workspace ignoring legacy archives.
- **System Documentation:** Appended `08-dojo-agent.md` to formally document the architectural boundaries and terminal deployment of the Data Engineering Co-pilot.

### Changed
- **Mission Modularization Architecture:** Refactored all static `.md` missions across `PY-BASICO` and `PY-POO-FINANCE` into full directory packages containing `requirements.md`, the `code/` logic, and an auto-managed `journal.md` for historical traceability.
- **Dynamic Persona Prompts:** Hardcoded exact behavioral matrices into the LLM system prompts mapping the `05-estructura-chats` dictates to specific `/mode` behaviors (MAIN, EXERCISES, WORK).
- **RAG Context Search Window:** Expanded vector retrieval window `k` from 4 to 6 to mathematically guarantee overlapping macro Campaign context with micro Mission context.
- **Taxonomy Restructuring:** Renamed `02-protocolo-misiones.md` to `02-misiones-framework.md` to correct the semantic boundaries between reactive *Protocols* and structural *Frameworks*.

## [3.2.1] - 2026-04-05

### Added
- **Protocol Yellow (Graceful Degradation):** Introduced `07-protocol-yellow.md` as a universal cognitive resilience mechanism to prevent Operator burnout.
- **Friction Level Tracking:** Embedded `Friction Level: [ ] / 10` KPI directly into the headers of all mission files and templates.

### Changed
- **Energy System & Operations:** Replaced the generic "Degradación Transitoria" with formal links and triggers for Protocol Yellow in `03-sistema-energia.md` and `06-manual-operativo-misiones.md`.
- **Mission Resilience Protocols:** Updated files `B00_assessment`, `M01_extractors`, and `M02_entities` allowing Language Switch (Spanish logic), De-abstraction, and Mock Data prioritization when friction peaks.

## [3.2.0] - 2026-04-03

### Added
- **English-Only Zone:** Established English as the mandatory language for all code, variable naming, Docstrings, and commit messages. Spanish restricted to journal/personal reflections.
- **English Commando Block:** Integrated a new required 30-60min startup sequence in `03-sistema-energia.md` utilizing Busuu and Duolingo.
- **Syllabus English Integration:** Added a 3-phase, 12-month linguistic acquisition plan aligned with full immersion to `05-syllabus-maestro.md`.
- **Mini-RFC & TDD Prerequisites:** Updated `mission-template.md`. Writing an architecture RFC and failing a `pytest` module are now hard requirements before writing logic.
- **Binary Performance Model:** Discarded 'low energy' concepts. You're either in a Deep Work Session or taking a Rest Day (`03-sistema-energia.md`).
- **Archive System:** Moved all original DoJo v2.0 templates and documents into `/archive/v2_canada/`.
- **Engineering Missions:** Generated Data Engineering oriented missions (M01-M04, S01-S02, B01) for PY-POO-FINANCE and the robust B00 assessment for PY-BASICO, strictly enforcing TDD natively.

### Changed
- **DoJo Core Updated:** Replaced low-energy philosophy with High Performance 8-12 month full availability protocols. Added Operator vs Architect concepts (`01-dojo-core.md`).
- **Campaign Architecture:** Redefined campaign logic from simple tasks to complete Object-Oriented Pipelines (`04-estructura-campanas.md`).
- **Python Finance Campaign (`PY-POO-FINANCE`):** Translated fully into English and restructured into an OOP ETL Pipeline demanding Data Engineering standards.
- **Subjects Refactor:** Standardized `subjects/README.md` and `PY-BASICO` documentation towards the new Deep Work and Data Engineering standards.
- **Documentation Normalization:** Standardized all H1 headers across `docs/` to perfectly match their internal filenames.

## [2.0.0] - 2025-11-25

### Added
- **Core/Campaign Separation**: Established a clear distinction between the DoJo framework (Core) and specific learning paths (Campaigns).
- **Branch Strategy**:
    - `main`: Contains only the stable core system (structure, protocols, templates).
    - `campaign/*`: Dedicated branches for specific subjects (e.g., `campaign/python`).
- **Git Configuration**: Added `.gitignore` to exclude local configuration files (e.g., Obsidian).

### Changed
- Moved all Python-specific content to `campaign/python` branch.
- Cleaned `main` branch to serve as a generic starting point for any student.

### Fixed
- Removed local `.obsidian` configuration from version control.
