# DoJo Version Log

## 3.3.3 - 2026-04-09

### Added
- **Timeout AI (Umbral Dinámico):** Formalized a time-based anti-codependency protocol. Set thresholds of 30 mins (small tasks) and 60 mins (architecture) of independent effort before escalating AI assistance.
- **Degradación Transitoria:** Introduced a mandatory session reset (15-30 min break) if the Timeout AI threshold is reached without progress, preventing cognitive gridlock.

## 3.3.2 - 2026-04-09

### Added
- **Socratic AI Transformation:** Pivoted `MAIN` and `WORK` modes to prioritize questioning and theoretical guidance over direct code generation, preventing AI codependency and fostering autonomous engineering logic.
- **Mandatory Weekend Rest Policy:** Hardcoded Saturdays and Sundays as mandatory Rest Days (Modo 0) in the core system documentation to ensure physiological and cognitive sustainability.
- **Protocol Yellow Gatekeeper:** Integrated Protocol Yellow into the pre-session ritual; if initial friction > 6, the session is preemptively aborted to prevent low-voltage progression.

## 3.3.1 - 2026-04-08

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
- **System Documentation:** Appended `09-dojo-agent.md` to formally document the architectural boundaries and terminal deployment of the Data Engineering Co-pilot.

### Changed
- **Mission Modularization Architecture:** Refactored all static `.md` missions across `PY-BASICO` and `PY-POO-FINANCE` into full directory packages containing `requirements.md`, the `code/` logic, and an auto-managed `journal.md` for historical traceability.
- **Dynamic Persona Prompts:** Hardcoded exact behavioral matrices into the LLM system prompts mapping the `05-estructura-chats` dictates to specific `/mode` behaviors (MAIN, EXERCISES, WORK).
- **RAG Context Search Window:** Expanded vector retrieval window `k` from 4 to 6 to mathematically guarantee overlapping macro Campaign context with micro Mission context.
- **Taxonomy Restructuring:** Renamed `02-protocolo-misiones.md` to `02-misiones-framework.md` to correct the semantic boundaries between reactive *Protocols* and structural *Frameworks*.

## [3.2.1] - 2026-04-05

### Added
- **Protocol Yellow (Graceful Degradation):** Introduced `08-protocol-yellow.md` as a universal cognitive resilience mechanism to prevent Operator burnout.
- **Friction Level Tracking:** Embedded `Friction Level: [ ] / 10` KPI directly into the headers of all mission files and templates.

### Changed
- **Energy System & Operations:** Replaced the generic "Degradación Transitoria" with formal links and triggers for Protocol Yellow in `03-sistema-energia.md` and `07-manual-operativo-misiones.md`.
- **Mission Resilience Protocols:** Updated files `B00_assessment`, `M01_extractors`, and `M02_entities` allowing Language Switch (Spanish logic), De-abstraction, and Mock Data prioritization when friction peaks.

## [3.2.0] - 2026-04-03### Added
- **English-Only Zone:** Established English as the mandatory language for all code, variable naming, Docstrings, and commit messages. Spanish restricted to journal/personal reflections.
- **English Commando Block:** Integrated a new required 30-60min startup sequence in `03-sistema-energia.md` utilizing Busuu and Duolingo.
- **Syllabus English Integration:** Added a 3-phase, 12-month linguistic acquisition plan aligned with full immersion to `06-syllabus-maestro.md`.
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
