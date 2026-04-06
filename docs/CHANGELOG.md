# DoJo Version Log

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
