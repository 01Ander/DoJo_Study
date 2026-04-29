# Campaign: PY-POO – Object Oriented ETL Pipeline (Beta v5.0)

## General Information
Campaign Name: POO Financial Pipelines (Data Engineering Edition)
Campaign Code: PY-POO
Version: 5.0.0 (Beta)
Status: 🔵 En Ejecución
Campaign Type: CORE-SUBTEMA (Campaign as Course)

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

## 🏗️ Syllabus (Course Structure)

### Capa Teórica y Laboratorios (`lore/` y `quests/`)
- **Cap 00: Hello, Classes — From Functions to Objects.** `class`, `__init__`, `self`.
- **Cap 01: Abstract Classes & Interfaces.** `abc`, `ABC`, `abstractmethod`, contratos lógicos.
- **Cap 02: Domain Entities & Polymorphism.** Herencia, constructores `super()`, polimorfismo.
- **Cap 03: Data Transformation Patterns.** Stateless functions, `collections.defaultdict`.
- **Cap 04: Output Loaders & Orchestration.** Dependency injection, Orchestrator pattern.
- **Cap 05: Testing with Pytest.** TDD lifecycle, GIVEN/WHEN/THEN, fixtures, mocks.
- **Cap 06: Validation & Logging.** Pydantic models, error handling strategies.
- **Cap 07: CLI Applications.** Typer/Click, arg parsing, terminal styling.

### 🛡️ Boss: The Financial Projector CLI (`boss/`)
Proyecto monolítico con fases internas desbloqueables (Solo accesible bajo auditoría del DM).
1. **Extraction Layer:** Implementar `AbstractExtractor` y dependencias (CSV/JSON).
2. **Domain Entities:** Modelar Transacciones (Income/Expense).
3. **Transformation Engine:** Capa de cálculo (AnalyticsEngine).
4. **Orchestration + CLI:** Envolver la aplicación de consola con `Typer`.

---

## 📗 Required Engineering Knowledge
- Clean Architecture principles.
- `pytest` standard assertions & mock fixtures.
- Abstract Base Classes (`abc`). Pydantic models.
- Formal Error Handling strategies mapping exceptions to dedicated loggers.

---

## ✅ Definition of Done (DoD) Global
1. **Academic Assimilation:** `grimoire.md` completado y auditado por el DM usando la Técnica Feynman para cada capítulo.
2. **Test-Driven Mechanics:** Todo código de producción en el Boss debe originarse tras un test fallido.
3. **Architecture First:** Documentación de trade-offs de diseño en el `journal.md` del Boss.
4. **English Friendly:** Nomenclatura en inglés. Bitácoras y dudas conceptuales en español.
