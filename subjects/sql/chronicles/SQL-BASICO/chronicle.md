# Chronicle: SQL-BASICO – Relational Databases & SQL Foundations (v5.1)

## General Information
Chronicle Name: Relational Databases & SQL Foundations (Data Engineering Edition)
Chronicle Code: SQL-BASICO
Version: 5.1.0
Status: 🟢 Ready
Chronicle Type: CORE-SUBTEMA (Campaign as Course)

---

## 💼 Business Context & Value Proposition
Las organizaciones modernas dependen críticamente de datos estructurados almacenados en bases de datos relacionales. La incapacidad de consultar, transformar, modelar e inspeccionar datos usando SQL directamente impide a los ingenieros de datos validar pipelines, realizar depuración de fallos en producción y ejecutar transformaciones analíticas complejas. El dominio de SQL no es opcional: es el pilar de ingeniería sobre el cual operan herramientas como dbt, Spark SQL, BigQuery, Snowflake y motores de orquestación.

## 💰 ROI & Impact
- **Pipeline Debugging Efficiency:** Reduce en un 60% el tiempo de diagnóstico de anomalías de datos al poder consultar directamente la BD relacional subyacente.
- **ETL Transformation Native Engine:** Permite delegar transformaciones pesadas al motor SQL (ELT), optimizando consumo de memoria en workers de Python.
- **Technical Assessment Readiness:** Cubre el 100% de las habilidades de consulta evaluadas en entrevistas técnicas para roles de Data & Automation Engineer.

---

## 🎯 Technical Objective
Dominar la sintaxis y semántica de SQL desde sus fundamentos relacionales (DDL/DML, constraints, normalización) hasta patrones avanzados de Data Engineering (JOINs multi-tabla, agregaciones con `HAVING`, subqueries correlacionadas, Common Table Expressions - CTEs, Window Functions como `ROW_NUMBER`/`LAG`/`LEAD`, operaciones de conjuntos y transacciones ACID). La práctica se ejecutará de forma interactiva en consola usando **SQLite** en macOS.

---

## 🏗️ Syllabus (Course Structure)

### Capa Teórica y Laboratorios (`lore/` y `quests/`)
- [**Cap 00: Hello, SQL — Introduction to Databases & SQLite**](lore/00-hello-sql) Concepto relacional, setup macOS, `sqlite3` CLI, `CREATE TABLE`, `INSERT`, `SELECT`.
- [**Cap 01: DDL & Relational Modeling**](lore/01-creating-and-modeling) Constraints (`PK`, `FK`, `UNIQUE`, `CHECK`), relaciones 1:N y N:M, Normalización 1NF-3NF.
- [**Cap 02: Filtering & Sorting — WHERE, ORDER BY & CRUD**](lore/02-filtering-and-sorting) Operadores lógicos, `LIKE`, `IN`, `BETWEEN`, `NULL`, `LIMIT`, `UPDATE`, `DELETE`.
- [**Cap 03: Scalar Functions, CASE WHEN & Data Types**](lore/03-functions-and-expressions) Funciones de texto, fecha, `CAST`, `COALESCE`, condicionales `CASE WHEN`.
- [**Cap 04: JOINs & Table Relationships**](lore/04-joins-and-relationships) `INNER`, `LEFT`, `CROSS`, Self-Join, Aliases, Anti-patterns.
- [**Cap 05: Aggregations & Grouping**](lore/05-aggregations-and-grouping) `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING` vs `WHERE`.
- [**Cap 06: Subqueries & Common Table Expressions (CTEs)**](lore/06-subqueries-and-ctes) Subqueries escalares/en FROM/correlacionadas, `WITH` CTEs encadenadas.
- [**Cap 07: Window Functions — Analytics & Deduplication**](lore/07-window-functions) `OVER()`, `PARTITION BY`, `ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, running totals.
- [**Cap 08: Set Operations & ETL Patterns**](lore/08-set-operations-and-etl-patterns) `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`, `INSERT INTO ... SELECT`.
- [**Cap 09: Views, Indexes & Transactions (ACID)**](lore/09-views-indexes-and-transactions) `CREATE VIEW`, `CREATE INDEX`, `EXPLAIN QUERY PLAN`, `BEGIN/COMMIT/ROLLBACK`, ACID.

---

### 🛡️ Rite: Public Library Data System (rite/)
[Proyecto integrador con 5 fases desbloqueables](rite/requirements) (Solo accesible bajo auditoría del DM — `/scry`).
1. **Fase 1: Schema Design & Modeling** (DDL, FKs, Normalización 3NF).
2. **Fase 2: Data Ingestion & Sanitization** (CRUD, CASE WHEN, Funciones escalares).
3. **Fase 3: Core Analytics** (JOINs multi-tabla, Aggregation & HAVING).
4. **Fase 4: Advanced Engineering & Windowing** (CTEs, Deduplicación con `ROW_NUMBER`, `LAG`/`LEAD`).
5. **Fase 5: Production & Optimization** (Views, Indexes, Transacciones ACID).

---

## 📗 Required Engineering Knowledge
- Conceptos relacionales: tablas, registros, atributos, llaves primarias y foráneas.
- Uso básico de la terminal bash/zsh en macOS.
- Pensamiento declarativo ("qué datos quiero") vs imperativo ("cómo iterar").

---

## 🧰 Toolkit & Study Workflow
- **macOS Terminal (`zsh`):** Ejecución de `sqlite3` CLI interactiva para testing instantáneo de queries.
- **Obsidian / VS Code:** Lectura de capítulos en `lore/`, resolución de laboratorios en `quests/`, actualización de `grimoire.md`.

---

## ✅ Definition of Done (DoD) Global
1. **Academic Assimilation:** `grimoire.md` completado y auditado por el DM (`/scry`) usando la Técnica Feynman para los 10 capítulos.
2. **Sequential Mastery:** Resolución completa de ejercicios en `quests/` de los 10 capítulos (incluyendo Spaced Repetition).
3. **Rite Validation:** Ejecución limpia de las 5 fases del Rite con validación final por el DM.
4. **English Friendly:** Código SQL (tablas, columnas, aliases) y documentación técnica en inglés. Bitácora personal y reflexiones en español.
