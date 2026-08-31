# SQL Division – The DoJo Engineering Divisions

Este directorio alberga la división de **Bases de Datos & SQL** del DoJo Study.

---

## 1. Objetivo Operativo

El área de SQL capacita al Operador en el diseño, consulta, manipulación y optimización de bases de datos relacionales, habilidades indispensables para construir pipelines ETL/ELT robustos y realizar diagnósticos de datos en producción.

---

## 2. Chronicles del Área SQL (Syllabus 2.0)

- **`SQL-BASICO`** (🟢 Ready / En Ejecución): Relational Databases & SQL Foundations (Data Engineering Edition). Cubre desde DDL/DML básico hasta JOINs, agregaciones, CTEs, Window Functions, Set Operations, Transacciones ACID y fundamentos de Modelado Dimensional (Star Schema, Facts & Dims).

> **Nota de Arquitectura (DoJo v5.2.0):**  
> Para evitar la fragmentación de cursos, las propuestas anteriores de `SQL-PYBRIDGE` y `SQL-DESIGN` han sido **absorbidas**:
> 1. El modelado dimensional (*Star Schema*, *OLTP vs OLAP*) forma parte de la fase avanzada de **`SQL-BASICO`**.
> 2. La integración de Python con bases de datos relacionales (*DBAPIs*, *SQLAlchemy*, *Pandas*) se implementa directamente en **`DE-PIPELINES`**.

---

## 3. Estándares Operativos

Todas las Chronicles en este directorio operan bajo el estándar **Campaign as Course v5.1 / v5.2**:
- **Lore (`lore/`):** Explicaciones conceptuales desacopladas (Domain Shifting), densas y diluidas con setup explícito en macOS.
- **Quests (`quests/`):** Ejercicios prácticos con SQL interactivo en terminal y auto-validación de outputs.
- **Grimoire (`grimoire.md`):** Bitácora Feynman evaluada por el DM (`/scry`).
- **Rite (`rite/`):** Proyecto final integrador por fases (Public Library Data System).
