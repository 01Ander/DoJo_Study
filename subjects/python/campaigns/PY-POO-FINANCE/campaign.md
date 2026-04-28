# Campaign: PY-POO-FINANCE – Object Oriented ETL Pipeline

## General Information
Campaign Name: POO Financial Pipelines (Data Engineering Edition)  
Campaign Code: PY-POO-FINANCE  
Version: 3.3 (Production Ready)  
Status: 🟢 Ready  
Campaign Type: CUMULATIVE

---

## 💼 Business Context & Value Proposition
Monolithic and procedural financial scripts are difficult to maintain and scale, leading to high operational costs and critical data risks. Transitioning to a decoupled, Object-Oriented architecture allows the organization to reduce technical debt and onboard new data sources with 50% less engineering effort.

## 💰 ROI & Impact
- **Automation Efficiency:** Increases pipeline scalability by 40%.
- **Error Mitigation:** Reduces manual data remediation costs by providing robust, testable logic.
- **Maintenance Cost:** Decreases the 'Cost of Change' for new financial regulations or schema updates.

---

## 🎯 Technical Objective
Substitute basic procedural scripting with a robust, modular, and decoupled **ETL system grounded purely in Object-Oriented Programming** (Design Patterns, Abstraction, SOLID principles).

The engine must ingest raw transactional data, isolate the inputs dynamically via abstract interfaces, execute transformation business logic (sanitization, calculations), and stream the output to designated loaders securely. The architecture must natively rely on defensive testings implemented via TDD.

---

## 🏗️ Mission Structure (Engineering Modules)

### Main Missions (M - Core Architecture)
- **M00: Hello, Classes — From Functions to Objects.** (Bridge mission: Refactor procedural ETL from PY-BASICO B01 into a `LogAnalyzer` class. Introduces `class`, `__init__`, `self`, and instance methods without advanced patterns).
- **M01: Abstract Extractors & Interface Segregation.** (Enforce `abc` Abstract Base Classes mapping to dynamic mock CSV parsers).
- **M02: Domain Entities & Polymorphism.** (Mapping raw outputs into memory-safe instantiated objects differentiating between `Income` and `Expense`).
- **M03: The Transformation Engine.** (Stateless calculation layer dedicated purely to metrics extraction leveraging `collections`).
- **M04: Output Loaders & Orchestration.** (Abstract load mechanics mapped to a decoupled `PipelineOrchestrator` invoking the E2E steps).

### Scaling Refactors (S - Quality & Data Engineering)
- **S01: Automated TDD Suite & Coverage.** (Inject `pytest-cov`, forcing >80% coverage on `src/` alongside E2E test suites with isolated `tmp_path` fixtures).
- **S02: Robust Validation & Centralized Logging.** (Re-engineer domain classes utilizing `Pydantic` and deploy formal module `.log` histories).

### Boss Mission (B - Continuous Integration)
- **B01: The Financial Projector CLI.** (Wrap the orchestrator onto a consumable, native Terminal App using `Typer` or `Click` yielding rich progress bars).

### Exit Gate (EG - Verificación de Asimilación)
- **EG01: New Extractor Integration.** (Implementar un `JSONExtractor` completo que cumpla `AbstractExtractor`, con test escrito antes del código, en Fase 2 pura — sin andamiaje del tutor).

---

## 📗 Required Engineering Knowledge
- Clean Architecture principles.
- `pytest` standard assertions & mock fixtures.
- Abstract Base Classes (`abc`). Pydantic models.
- Formal Error Handling strategies mapping exceptions to dedicated loggers.

---

## ✅ Definition of Done (DoD)
1. **Test-Driven Mechanics:** All logic has spawned strictly trailing a red `pytest` rejection beforehand.
2. **Mini-RFC Drafts Pre-Deployment:** Documentation mapping the design trade-offs resides properly inside all mission files before execution.
3. **Decoupled Mechanics:** Input parsing modifications strictly don't cascade down into the Transformation layer. 
4. **Social README (Visibility Layer):** Include a `README.md` at the campaign root that explains the project's business impact and architecture in simple terms for non-technical stakeholders (HR/PMs).
5. **English Friendly:** Naming (variables, classes, methods) MUST remain in professional English. Documentation (docstrings, comments, deployment instructions) can be Hybrid-English or simplified English. Exception logs can be bilingual (Spanish/English). This aligns with the system-wide "English Friendly" standard.