# Chronicle: PY-POO – Object Oriented ETL Pipeline (v5.1)

## General Information
Chronicle Name: POO Financial Pipelines (Data Engineering Edition)
Chronicle Code: PY-POO
Version: 5.1.0
Status: 🔵 En Ejecución
Chronicle Type: CORE-SUBTEMA (Campaign as Course)

---

## 💼 Business Context & Value Proposition
Los scripts financieros monolíticos y procedimentales son difíciles de mantener y escalar, lo que genera altos costos operativos y riesgos críticos para los datos. La transición a una arquitectura desacoplada y orientada a objetos (Object-Oriented) permite a la organización reducir la deuda técnica e incorporar nuevas fuentes de datos con un 50% menos de esfuerzo de ingeniería.

## 💰 ROI & Impact
- **Automation Efficiency:** Incrementa la escalabilidad del pipeline en un 40%.
- **Error Mitigation:** Reduce los costos de corrección manual de datos al proporcionar lógica robusta y testeable.
- **Maintenance Cost:** Disminuye el 'Costo de Cambio' para nuevas regulaciones financieras o actualizaciones de esquemas.

---

## 🎯 Technical Objective
Sustituir el scripting procedimental básico por un **sistema ETL robusto, modular y desacoplado, basado puramente en la Programación Orientada a Objetos** (Design Patterns, Abstraction, principios SOLID).

El motor debe ingerir datos transaccionales sin procesar, aislar las entradas dinámicamente mediante interfaces abstractas, ejecutar la lógica de negocio de transformación (sanitización, cálculos) y transmitir la salida a los cargadores designados de forma segura. La arquitectura debe apoyarse nativamente en pruebas defensivas implementadas mediante TDD.

---

## 🏗️ Syllabus (Course Structure)

### Capa Teórica y Laboratorios (lore/ y quests/)
- [**Cap 00: Hello, Classes — From Functions to Objects.** ](lore/00-from-functions-to-classes)`class`, `__init__`, `self`.
- [**Cap 01: Abstract Classes & Interfaces.**](lore/01-abstract-classes-and-interfaces) `abc`, `ABC`, `abstractmethod`, contratos lógicos.
- [**Cap 02: Domain Entities & Polymorphism.**](lore/02-domain-entities-and-dataclasses) Herencia, constructores `super()`, polimorfismo.
- [**Cap 03: Data Transformation Patterns.**](lore/03-stateless-engines-and-composition) Stateless functions, `collections.defaultdict`.
- [**Cap 04: Output Loaders & Orchestration.**](lore/04-orchestration-and-io) Dependency injection, Orchestrator pattern.
- [**Cap 05: Testing with Pytest.**](lore/05-testing-with-pytest) TDD lifecycle, GIVEN/WHEN/THEN, fixtures, mocks.
- [**Cap 06: Validation & Logging.**](lore/06-logging-and-error-handling) Pydantic models, error handling strategies.
- [**Cap 07: CLI Applications.**](lore/07-cli-and-production) Typer/Click, arg parsing, terminal styling.

### 🛡️ Rite: The Financial Projector CLI (rite/)
[Proyecto monolítico con fases internas desbloqueables](rite/requirements) (Solo accesible bajo auditoría del DM — `/scry`).
1. **Extraction Layer:** Implementar `AbstractExtractor` y dependencias (CSV/JSON).
2. **Domain Entities:** Modelar Transacciones (Income/Expense).
3. **Transformation Engine:** Capa de cálculo (AnalyticsEngine).
4. **Orchestration + CLI:** Envolver la aplicación de consola con `Typer`.

---

## 📗 Required Engineering Knowledge
- Principios de Clean Architecture.
- Assertions estándar y mock fixtures de `pytest`.
- Abstract Base Classes (`abc`). Modelos de Pydantic.
- Estrategias formales de Error Handling mapeando excepciones a loggers dedicados.

---

## 🧰 Toolkit & Study Workflow
- **Obsidian:** Utilizado para la lectura y navegación del *Lore* y *Quests*. Aprovecha los enlaces bidireccionales (`[[enlace]]` o `[texto](enlace)`) y el formato nativo para conectar conceptos y hacer la lectura más efectiva.
- **VS Code:** Entorno principal para la codificación, ejecución de scripts y validación de testing (TDD) en los laboratorios y el Rite.

---

## ✅ Definition of Done (DoD) Global
1. **Academic Assimilation:** [[grimoire.md]] completado y auditado por el DM (`/scry`) usando la Técnica Feynman para cada capítulo.
2. **Test-Driven Mechanics:** Todo código de producción en el Rite debe originarse tras un test fallido.
3. **Architecture First:** Documentación de trade-offs de diseño en el journal.md del Rite.
4. **English Friendly:** Nomenclatura en inglés. Bitácoras y dudas conceptuales en español.
