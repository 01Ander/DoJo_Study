# Chronicle: DE-PIPELINES

**Estado:** ⚪ Pendiente
**Área:** Data Engineering
**Core:** ETL, Python+SQL, Data Quality, Flows & Tasks con Prefect

## Descripción
Esta chronicle se enfoca en la construcción de pipelines de datos (ETL y ELT). Integra los conocimientos de Python (`PY-POO`) y bases de datos (`SQL-BASICO`) para extraer datos desde APIs REST, limpiarlos, transformarlos usando Pandas, asegurar la calidad de datos y cargarlos en bases de datos relacionales PostgreSQL. Todo esto orquestado de manera periódica utilizando flujos mediante **Prefect** (local).

## Temario / Capítulos
- **Capítulo 00:** Arquitecturas de Ingesta (ETL vs ELT), Zonas Medallion (Bronze, Silver, Gold), transformación declarativa (`dbt`), almacenamiento columnar vs filas y perspectiva de procesamiento distribuido (`Spark`).
- **Capítulo 01:** Extracción Automatizada Resiliente (APIs REST, Auth tokens, Paginación offset/cursor, rate limiting, librería `requests`, mocking con `responses` y chequeo estático con `mypy`).
- **Capítulo 02:** Manipulación, Limpieza, Tipado Estricto y Agregaciones (`df.groupby`) con Pandas.
- **Capítulo 03:** Data Quality & Observability (Validación de esquemas, manejo de nulos, deduplicación, reconciliación de pérdida y excepciones de dominio sin `assert`).
- **Capítulo 04:** Carga de Datos Estructurados hacia PostgreSQL Real (Docker Compose, `psycopg2`, SQLAlchemy Connection Pools y carga por chunks).
- **Capítulo 05:** Orquestación de Flujos y DAGs con Prefect y equivalencia Airflow (Tasks, Flows, reintentos automáticos, logs estructurados con `get_run_logger` y calendarización periódica con Cron).

## Reglas del LORE (Domain Shifting)
Los ejemplos y el código enseñado a lo largo de los capítulos aplicarán un *Domain Shifting*.
**Dominio Temático Elegido:** Logística y Distribución de Pociones Mágicas y Artefactos Arcanos (Gremio de Alquimistas).
