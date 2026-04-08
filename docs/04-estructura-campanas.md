# 04 - Estructura Campañas

En el DoJo, una **campaña** no es una simple agrupación de ejercicios al azar, sino un **Proyecto de Ingeniería Modular** diseñado para crear un artefacto técnico real y medible. El aprendizaje emerge de la construcción de sistemas profesionales.

---

## Estructura Base de una Campaña de Ingeniería

### 1️ Blueprint y Alcance 
Cada campaña debe simular un ecosistema productivo. No resolvemos un problema abstracto de codificación; desarrollamos un servicio.
Ej.: *Finance ETL Pipeline basado en POO*, *Data Quality Checker Automatizado*, *Deploy de Lambda Serverless*.

### 2️ Requisitos Restrictivos
Todas las campañas deben contemplar por diseño:
- **Testing Obligatorio (Automated):** Las misiones principales exigen pruebas escritas en `pytest` o similar (Desarrollo guiado por pruebas TDD, o Unit Testing estricto).
- **Documentación Arquitectónica (Mini-RFC):** Antes del `feature` técnico, debe escribirse un pequeño documento de Request For Comments en la misión, indicando el patrón a utilizar.
- **Clean Code & Tipados:** Chequeos estáticos requeridos (`mypy`, `flake8` u homólogos).

### 3️ Desglose Estructural (Epics & Missions)

Las campañas se dividen de forma homóloga al ciclo de Desarrollo de Software (SDLC):

- **Misiones Principales (M):** Módulos Core del software. Ej. Implementar la interfaz abstracta del Extractor, Montar la conexión a DB, Orquestar el Job.
- **Módulos de Refactorización y Escalado (S - Sustitución de Side Missions):** Antiguamente misiones "secundarias", ahora representan evoluciones técnicas (Ej. Migrar almacenamiento CSV local a DuckDB o a PostgreSQL en AWS).
- **Boss Mission (B - Milestone de Integración):** Integración continua (CI/CD o Pipeline End-to-End). Cierre del proyecto donde todas las piezas ensamblan juntas bajo un CLI (como Click/Typer) o API (FastAPI) funcional.

---

## 🏛 Convención de Nombrado (Engineering Identifiers)

Para las ramas de Git y las carpetas, la nomenclatura debe indicar el enfoque de Ingeniería:
- `PY-POO-FINANCE` (Python OOP Data Modeling)
- `DE-ETL-BATCH` (Data Engineering Batch Pipeline)
- `QA-AUTO-API` (Quality Assurance Automated API Testing)

---

## Flujo Operativo del "Arquitecto" (Creación de la Campaña)

El día de mantenimiento (Modo Arquitecto), tu responsabilidad al abrir una campaña es:
1. Documentar el estado esperado del componente de software.
2. Definir 4-6 misiones como "Módulos de Sistema Mínimo Viable (MVP)".
3. Mapear explícitamente los inputs y outputs de estos módulos.
4. Generar el esqueleto `tests/` que se debe ir llenando durante la campaña.
5. Dejar la campaña en Status: `🟢 Ready` para que en la semana, operes sin pensar.
