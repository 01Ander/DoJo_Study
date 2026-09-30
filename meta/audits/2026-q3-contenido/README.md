# Auditoría Técnica de Contenido Q3-2026

Este directorio centraliza las salidas en crudo y las matrices de consenso de la auditoría técnica triangulada (Gemini Pro, Claude Opus, Sonnet) sobre las 5 Chronicles completadas del DoJo Study.

## Protocolo de Referencia
* Gobernanza y Reglas: [`meta/ideas/protocolo-auditoria-contenido-tecnico.md`](../../ideas/protocolo-auditoria-contenido-tecnico.md)
* Payload del Prompt Maestro: [`meta/ideas/prompt-auditoria-modelos.md`](../../ideas/prompt-auditoria-modelos.md)

## Estructura por Subject
* `01-py-basico/` — Sintaxis, control de flujo, scripting base.
* `02-py-poo/` — OOP, TDD (`pytest`), modularización, logging estructurado.
* `03-sql-basico/` — DDL, JOINs, CTEs, Window Functions, ACID, Modelado dimensional.
* `04-de-pipelines/` — Consumo de APIs, Pandas, Data Quality, orquestación DAG local.
* `05-cloud-aws/` — S3, IAM, RDS/Postgres, Lambda, CloudWatch.

## Entregable Final
* `REPORTE-CONSOLIDADO-FINAL.md` — Síntesis ejecutiva de los 5 subjects, plan agrupado de remediación y propuesta para `05-syllabus-maestro.md`.
