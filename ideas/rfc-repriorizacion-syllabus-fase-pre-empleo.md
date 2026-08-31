# RFC: Repriorización del Syllabus Maestro (Fase Pre-Empleo)

**Estado:** Aceptado e Integrado en DoJo v5.2.0 (Syllabus 2.0)
**Fecha:** 2026-08-31
**Referencia:** Absorbió y actualizó `docs/03-syllabus-maestro.md`, delegando Fase 2 a `docs/08-syllabus-post-empleo-fase2.md`.

---

## 1. Contexto

El syllabus maestro define el perfil completo de Data & Automation Engineer como visión de largo plazo. Sin embargo, el objetivo inmediato cambió: conseguir un primer empleo remoto internacional antes de mediados de 2027, no completar el mapa entero antes de aplicar.

Esta decisión fue validada externamente con 4 modelos distintos, en conversaciones separadas y sin contexto compartido entre ellos: ChatGPT, Perplexity y Grok (los tres con búsqueda web activa sobre datos de mercado 2026) y Gemini (sin búsqueda web, validando desde razonamiento de industria). Los cuatro convergieron en los mismos huecos del plan original, lo cual se toma como señal fuerte de que son estructurales al rol, no artefactos de una muestra de vacantes puntual.

## 2. Decisión

Se introduce una etiqueta de **Prioridad** sobre cada bloque del syllabus maestro: **Fase 1 (pre-empleo)** o **Fase 2 (post-empleo)**. El mapa de Fase 1 se convierte en el Syllabus 2.0 (`docs/03-syllabus-maestro.md`) y la Fase 2 se extrae a `docs/08-syllabus-post-empleo-fase2.md`.

## 3. Tabla de prioridades

| Bloque (syllabus maestro) | Prioridad | Alcance ampliado para Fase 1 |
|---|---|---|
| SQL | Fase 1 | + DDL, constraints, índices básicos, modelado dimensional (hechos/dimensiones, OLTP vs OLAP) — no estaba en el plan original |
| PY | Fase 1 | pandas, requests/httpx, consumo de APIs, JSON |
| DE | Fase 1 | ETL/ELT + **orquestación básica** (Prefect o Airflow local: un DAG con reintentos y logging) — nuevo respecto al plan original |
| (nuevo, no listado como bloque propio) | Fase 1 | **Data quality & observabilidad**: validación de esquema, detección de nulls/duplicados, row counts, manejo de errores/reintentos. Se apalanca en pytest/logging ya dominado de PY-POO |
| CLOUD | Fase 1 (alcance ampliado) | S3, IAM, **Lambda, RDS/Postgres, CloudWatch** — el plan original se quedaba en S3+IAM |
| GIT | Fase 1 (alcance ampliado) | Commits semánticos, branching, PRs + **GitHub Actions corriendo pytest en cada push** — antes esto vivía dentro de "DevOps avanzado", se separa como núcleo |
| AUTO | Fase 1 (mantener alcance actual) | Uso aplicado de APIs/LLMs (function calling) — no profundizar más allá de lo ya practicado con DoJo/Hermes |
| PORT | Fase 1 (alcance recalibrado) | **1 proyecto robusto end-to-end**, no 2-4 proyectos medianos |
| ENG-INT | Fase 1 (prioridad elevada) | Objetivo B2+ funcional para entrevista técnica en vivo, no solo comprensión pasiva/escrita |
| QA | Fase 2 | Sin cambios — se retoma post-empleo |
| DEV (CI/CD avanzado, Kubernetes, Terraform) | Fase 2 | Sin cambios |
| DA | Fase 2 | Sin cambios |
| SEC (avanzado) | Fase 2 | Solo se mantiene en Fase 1 lo mínimo: IAM básico + manejo de secrets/variables de entorno |
| ENG (fundamentos generales) | Ya integrado a la filosofía DoJo | Sin cambios |

## 4. Especificación del proyecto de portafolio (Fase 1)

Un único pipeline end-to-end que demuestre la cadena completa:

```
API externa
  → Ingesta en Python
  → Validación (schema, nulls, duplicados)
  → Almacenamiento raw en S3
  → Transformación (pandas / SQL)
  → Carga a RDS/Postgres (modelado con hechos/dimensiones)
  → Quality checks post-carga
  → Orquestación periódica (Prefect/Airflow, con reintentos)
  → Logging y monitoring básico (CloudWatch)
  → [Opcional] Capa ligera de LLM como diferenciador
```

README en inglés, explicando arquitectura y decisiones de diseño (por qué ELT vs ETL, por qué esa herramienta de orquestación, trade-offs).

## 5. Búsqueda de empleo — corre en paralelo, no en secuencia

Antes: `estudiar todo → aplicar`.  
Ahora: `núcleo técnico + búsqueda + entrevistas` corriendo simultáneamente.

- Reposicionamiento de perfil: **Data Automation Engineer / Python Automation Developer / ETL Integration Developer** — no "Data Engineer" puro.
- Mock interviews técnicas en inglés desde el cierre del Rite de SQL-BASICO.
- CV y GitHub en inglés desde el primer proyecto terminado, no al cierre del plan.
- Aplicar de forma continua conforme el proyecto de portafolio avanza.

## 6. Fuera de alcance para Fase 1 (Fase 2)

QA formal, DevOps avanzado (Kubernetes, Terraform, pipelines CI/CD complejos), DA/dashboards como especialización, seguridad avanzada, y cualquier profundización en LLM/RAG/embeddings más allá del uso ya practicado en el propio sistema DoJo.

## 7. Fuentes de validación

- ChatGPT (búsqueda web activa, datos de mercado 2026)
- Perplexity (búsqueda web activa, datos de mercado 2026)
- Grok (búsqueda web activa, datos de mercado 2026)
- Gemini (validación por razonamiento de industria, sin búsqueda web)
- Claude (con contexto histórico del Grimoire, journal del Rite de PY-POO, y el syllabus maestro original)
