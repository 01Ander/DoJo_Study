# Ola 3 — Portafolio y empleabilidad en Colombia

> **Objetivo:** conseguir el **primer empleo formal en datos en Colombia** con dos artefactos de portafolio defendibles, un carril de búsqueda paralelo y cloud AWS como diferenciador no bloqueante.
>
> **Fase:** activa · **Inicio:** Semana 1 (Corte 0) · **Postulaciones:** desde la Semana 9
>
> **Contexto histórico:** [`meta/remediacion/README.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/remediacion/README.md) — Ola 1 y Ola 2, ya cerradas.

Esta carpeta **no es remediación**. Aquí vive el plan de la fase nueva: qué construir, en qué orden, con qué criterios de aceptación y cómo convertirlo en entrevistas.

---

## 1. Documentos

| Documento | Qué contiene | Cuándo leerlo |
|---|---|---|
| [`roadmap.md`](roadmap.md) | Plan operativo: Cortes 0/0B/1/1B/2/3, Gates 1–5 y E1–E3, modelo dimensional, fuentes, DoD y riesgos | Primero; es la fuente de verdad técnica |
| [`empleabilidad-colombia.md`](empleabilidad-colombia.md) | Mercado local, roles, salarios, CV, LinkedIn, canales, tracker y checklist de aplicación | Después del roadmap; se usa desde la Semana 6 |

**Orden de lectura recomendado:**

1. `roadmap.md` §1–§3 → entender el cambio de estrategia y los Cortes 0 y 0B.
2. `roadmap.md` §4 → nivelación `BI-BASICO`/`EXCEL-BASICO`, modelo dimensional y alcance técnico del Artefacto 1.
3. `roadmap.md` §5–§6 → Artefacto 2, Carril E y publicación.
4. `roadmap.md` §7 → línea de tiempo.
5. `empleabilidad-colombia.md` → ejecución semanal de la búsqueda.

---

## 2. Estructura de la fase

```text
meta/ola-3/
├── README.md                 ← este índice
├── roadmap.md                ← plan operativo (técnico + gates)
├── empleabilidad-colombia.md ← plan de búsqueda de empleo
└── acceptance/               ← suite de caja negra del Corte 1 (se crea al abrirlo)
```

Los artefactos del portafolio y la nivelación de analista se construyen en el monorepo:

- `content/subjects/analitica/chronicles/BI-BASICO/` — 6 quests de Power BI (Power Query, modelo semántico 1:N, DAX I/II, storytelling, Service/RLS).
- `content/subjects/analitica/chronicles/EXCEL-BASICO/` — 4 quests de Excel (limpieza, `XLOOKUP`/`SUMIFS`, tablas dinámicas, Power Query + Power Pivot).
- `content/portfolio/capstone-slice-local/` — Artefacto 1 (pipeline E2E).
- `content/portfolio/caso-bi-colombia/` — Artefacto 2 (caso BI/SQL).

La publicación al repo público se hace por exportación con allowlist, según `roadmap.md` §6.4.

---

## 3. Resumen de decisiones

| Decisión | Definición |
|---|---|
| **Rol objetivo** | Analytics Engineer / Data Analyst junior. Data Engineer puro queda a 12–24 meses |
| **Nivelación de analista** | `BI-BASICO` (6 quests) + `EXCEL-BASICO` (4 quests) en `content/subjects/analitica/chronicles/` |
| **Portafolio** | 2 artefactos: pipeline E2E + caso BI/SQL de negocio |
| **Fuente principal** | SECOP II (`jbjy-vk9h`) + TRM (`32sa-8pi3`) en `datos.gov.co` |
| **Modelo** | `fact_contrato` a grano `id_contrato` + `dim_entidad_scd2` + `dim_fecha` con TRM + `dim_proveedor` |
| **Cloud** | AWS en Semanas 9–10, **no bloqueante** para postular |
| **Publicación** | Repo público único con dos carpetas, exportado por allowlist |
| **Búsqueda** | 10–15 postulaciones/semana desde la Semana 9 |

---

## 4. Gates de la fase

| Gate | Cuándo | Evidencia |
|---|---|---|
| **Corte 0** | Semana 1 | `MQ-01` (dbt-postgres) en verde + 20 ejercicios SQL + VM de Power BI con snapshot lista |
| **Corte 0B** | Semanas 2–5 | `BI-BASICO` (6 quests) + `EXCEL-BASICO` (4 quests) cerradas por artefacto (`.pbix`/`.xlsx`) y Rite de defensa oral (5 min) |
| **Corte 1** | Semanas 3–5 | Artefacto 1: `requirements.md`, pipeline, SCD2, dashboard, chaos drill y defensa oral |
| **Corte 1B** | Semanas 6–7 | Artefacto 2: caso BI/SQL con 3 hallazgos y 1 recomendación |
| **Gate E1** | Semana 8 | 2 artefactos publicados + CV + LinkedIn + tracker |
| **Gate E2** | Semana 8 | Pitch de 90 s, explicación técnica en <3 min y demo grabada |
| **Gate E3** | Semanas 9–12 | Postulaciones sostenidas, referidos, mocks y negociación |
| **Corte 2** | Semanas 9–10 | S3 + IAM + Secrets + `teardown.py`; no bloquea postular |

> **Regla de secuencia:** la Semana 8 cierra el portafolio y los Gates E1/E2. Las postulaciones empiezan en la Semana 9. Si hay conflicto entre una tarea técnica y la búsqueda, se recorta el alcance técnico.
