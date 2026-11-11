# Plan de empleabilidad rápida — primer empleo en Colombia

> **Objetivo:** conseguir el **primer empleo formal en datos en Colombia** en el menor tiempo razonable, usando el DoJo Study como base técnica y sin depender de open source ni freelance.
>
> **Fecha:** noviembre de 2026 · **Mercado:** Colombia (Bogotá, Medellín, Cali, remoto nacional).
>
> **Documento relacionado:** [`roadmap-ola-3.md`](roadmap-ola-3.md) — los dos artefactos de la Ola 3 (Corte 1 + Corte 1B) son la base de este plan.

---

## 0. Resumen ejecutivo

| Decisión | Definición |
|---|---|
| **Rol objetivo** | **Analista de Datos / Analytics Engineer junior**. “Data Engineer” puro es el destino a 12–24 meses, no la puerta de entrada. |
| **Tiempo de preparación** | **10–12 semanas** (20–25 h/semana) |
| **Tiempo de búsqueda** | **8–16 semanas** en paralelo desde la semana 9 |
| **Meta realista** | Oferta entre el **mes 4 y el mes 7** desde hoy |
| **Salario esperado** | **COP 3,0–7,0 M/mes** según rol, ciudad e inglés (ver §10) |
| **Ventaja del DoJo** | Ya tienes base sólida de SQL, Python y AWS, con testing y CI. **dbt, Star Schema/SCD2 y el capstone están en construcción en la Ola 3 (Semanas 1–7)**; falta traducirlos al lenguaje del mercado local. |
| **Regla de oro** | No esperes a “terminar de aprender” para aplicar. Se aplica desde la semana 9 con el portafolio mínimo viable. |

**Las cinco apuestas de este plan:**

1. **SQL + Excel/BI primero.** Es lo que más se pide y lo que más rápido se evalúa en entrevistas locales.
2. **Un portafolio de 2 artefactos**, no de 10. Un pipeline end-to-end y un caso de BI con datos colombianos.
3. **Inglés B2 demostrable.** En Colombia vale entre **30% y 50%** más de salario y abre las vacantes remotas locales de multinacionales.
4. **Aplicar por canal + referido.** El portal solo no basta; la red acelera.
5. **Aceptar el primer empleo que dé experiencia verificable**, aunque el título no sea “Data Engineer”.

---

## 1. Qué significa “rápido” (y cómo medirlo)

“Rápido” no es una semana. En el mercado junior colombiano, un proceso serio toma **2–4 semanas** y el cuello de botella es conseguir entrevistas, no aprobarlas.

| Hito | Tiempo objetivo | Métrica |
|---|---|---|
| Diagnóstico técnico | Semana 1 | Test SQL + Python propio, sin apuntes |
| Portafolio mínimo viable | Semana 8 | 2 artefactos publicados y con README |
| CV + LinkedIn listos | Semana 8 | 1 página, keywords, GitHub, nivel de inglés |
| Inicio de aplicaciones | Semana 9 | **10–15 postulaciones/semana** |
| Primeras entrevistas | Semana 10–12 | 3–5 procesos activos |
| Oferta | Mes 4–7 | 1 oferta aceptada |

**KPIs semanales (no negociables):**

- 10–15 postulaciones **personalizadas**.
- 3–5 contactos nuevos en LinkedIn (reclutadores, egresados, líderes de datos).
- 5 h de inglés técnico.
- 1 mock interview o 1 entrevista real.
- 1 mejora concreta al portafolio o al CV.

> Si en 6 semanas no hay ni una entrevista, el problema es el **CV/posicionamiento**, no el mercado. Si hay entrevistas pero no ofertas, el problema es la **prueba técnica o el inglés**.

---

## 2. Mercado local: qué se contrata y dónde

### 2.1 Roles y dificultad real de entrada

| Rol | Volumen local | Dificultad junior | Salario junior (COP/mes) | Encaje con tu perfil |
|---|---|---|---|---|
| **Analista de Datos / BI** | Alto (440+ vacantes de data analyst en Colombia) | **Baja-media** | 2,5–5,0 M | Alto: SQL + Excel + Power BI |
| **Analytics Engineer** | Medio (228 vacantes) | **Media** | 4,5–7,0 M | **Muy alto**: dbt + SQL + modelado |
| **Data Engineer junior** | Medio | Media-alta | 5,0–7,0 M | Alto: Python + AWS + pipelines |
| **Data Scientist junior** | Medio | Alta | 4,5–7,0 M | Bajo: no es el foco |
| **Data Analyst remoto para EE. UU.** | Bajo | Media | USD 1.200–1.850 | Medio: requiere inglés B2+ |

**Conclusión:** empieza por **Analista de Datos/Analytics Engineer**. Es más fácil entrar, se aprende el negocio y se pivota a DE con experiencia.

### 2.2 Dónde están las vacantes

| Ciudad | Participación de vacantes IT | Nota |
|---|---|---|
| **Bogotá** | ~73% | Banca, consultoría, multinacionales, centros de servicios |
| **Medellín** | ~14% | Startups, fintech, ecosistema Ruta N, nearshore |
| **Cali / Barranquilla** | ~4% y menor | Menos volumen, menos competencia, salarios más bajos |
| **Remoto nacional** | Creciente | Muchas empresas ya contratan remoto dentro de Colombia |

### 2.3 Segmentos de empresas a atacar (por orden de probabilidad)

1. **Banca y seguros:** Bancolombia, Davivienda, Banco de Bogotá, Grupo Aval, Sura, Bolívar. Procesos formales, buenos beneficios, exigen SQL y Excel.
2. **Fintech y retail tech:** Rappi, Addi, Bold, Nu Colombia, Ualá, Mercado Libre Colombia, Éxito, Falabella. Más ágiles, valoran portafolio.
3. **Consultoría y servicios:** Accenture, Deloitte, EY, KPMG, PwC, IBM, Globant, Stefanini, Sonda, TCS, Perficient, EPAM. Contratan juniors en volumen y capacitan.
4. **Multinacionales con centro de servicios:** centros de datos, finanzas y operaciones en Bogotá/Medellín. Piden inglés B2+.
5. **Startups y scaleups:** menos estructura, más riesgo, más aprendizaje; suelen pagar menos al inicio pero dar responsabilidad rápida.

### 2.4 Puertas de entrada que casi nadie usa bien

- **Prácticas / etapa productiva (SENA o universidad):** es la vía más rápida de “cero experiencia” a primer empleo. Si aplica a tu caso, priorízala.
- **Programas de primer empleo:** Talento Tech (MinTIC), Talento B de Bancolombia, programas de aprendices de bancos y consultoras. Revisa convocatorias cada mes.
- **Ferias de empleo universitarias y de cámara de comercio:** poco glamurosas, mucha conversión.
- **Referidos internos:** la mayoría de vacantes junior se cubren antes de publicarse.

---

## 3. Perfil objetivo y posicionamiento

No te presentes como “aspirante a Data Engineer”. Preséntate como alguien que **ya resuelve problemas de datos con SQL, Python y BI**, y que además sabe construir pipelines.

### 3.1 Titular del CV (elige uno)

- **Analista de Datos Junior** — SQL, Python y Power BI para decisiones de negocio.
- **Analytics Engineer Junior** — modelos dbt, calidad de datos y dashboards.
- **Data Engineer Junior** — pipelines ETL/ELT en Python, PostgreSQL y AWS.

> **Nota macOS:** Power BI Desktop no corre nativo en Mac. **Power BI Service** (navegador) sirve para mostrar dashboards ya publicados, pero **no puede conectarse a un PostgreSQL local sin gateway on-premises**. Para construir el `.pbix` desde los marts usa Desktop en una VM Windows o exporta a CSV; si no es viable, usa Looker Studio y explica la equivalencia de conceptos (medidas, modelado, visualización).

### 3.2 Keywords que el ATS local busca

`SQL` · `Python` · `Power BI` · `Excel avanzado` · `ETL` · `PostgreSQL` · `AWS` · `dbt` · `Git` · `pandas` · `modelado de datos` · `calidad de datos` · `inglés B2`

### 3.3 Qué demostrar en la primera pantalla

1. Que sabes **SQL de verdad** (joins, CTEs, window functions).
2. Que sabes **limpiar y modelar datos**, no solo graficar.
3. Que entiendes **el negocio** (métricas, impacto, decisiones).
4. Que tienes **inglés funcional**.
5. Que tu trabajo es **reproducible** (README, tests, instrucciones).

---

## 4. Teoría mínima necesaria (y qué ya tienes)

> Prioridad: **P0 = sin esto no pasas la prueba técnica**; P1 = te diferencia; P2 = deseable.
> Horas estimadas para llevarlo a nivel entrevista, no a nivel experto.

| # | Tema | Prioridad | Horas | Evidencia de que lo sabes | Estado en tu DoJo |
|---|---|---|---|---|---|
| 1 | **SQL**: joins, agregaciones, subconsultas, CTEs, window functions, `NULL`s, deduplicación | **P0** | 40–60 h | Resolver 20–30 ejercicios sin mirar; explicar un plan de ejecución básico | Cubierto; **refuerza window functions y performance** |
| 2 | **Excel / Google Sheets**: tablas dinámicas, `BUSCARV`/`XLOOKUP`, limpieza, gráficos | **P0** | 10–15 h | Dashboard operativo en una hoja | Probablemente cubierto; úsalo para el día a día |
| 3 | **Estadística descriptiva y métricas de negocio**: media/mediana, distribución, correlación, variación, funnel, cohortes | **P0** | 15–20 h | Definir una métrica y explicar qué la mueve | Parcial; falta práctica de negocio |
| 4 | **Python para datos**: pandas, `requests`, funciones, lectura/escritura de archivos, tests básicos | **P0** | 40–50 h | Script que ingesta, limpia y exporta con tests | **Cubierto** (PY-POO + pipelines) |
| 5 | **Modelado de datos**: normalización, star schema, hechos/dimensiones, SCD2, grano | **P0** | 15–20 h | Explicar tu modelo en una pizarra | **En construcción** (Ola 3, Corte 1) |
| 6 | **ETL/ELT y orquestación**: incremental vs full, idempotencia, retries, backfill, dependencias | **P1** | 20 h | Diseñar un pipeline y justificar decisiones | **En construcción** (Ola 3, Corte 1) |
| 7 | **BI y visualización**: Power BI (DAX básico), Tableau, storytelling | **P1** | 25–30 h | Dashboard con 1 pregunta de negocio y 1 recomendación | **Nuevo** (MQ-02, Ola 3) |
| 8 | **Git y CI**: ramas, PR, revisión, tests automáticos | **P1** | 10 h | Repo con CI verde | **Cubierto** |
| 9 | **Cloud fundamentals**: S3, IAM, Lambda, RDS, costes; o GCP equivalente | **P1** | 15–20 h | Desplegar y destruir un recurso | **Base cubierta**; despliegue real en Ola 3, Corte 2 |
| 10 | **dbt**: modelos staging/marts, tests, `dbt run`/`dbt test` | **P1** | 15–20 h | Repo dbt con tests en verde | **En construcción** (Ola 3, Corte 0) |
| 11 | **Calidad y gobierno de datos**: validación, contratos, linaje, PII, Ley 1581 | **P1** | 10 h | Checklist de calidad en el README | Parcial |
| 12 | **Inglés técnico** | **P1** | 3–5 h/semana | Daily, documentación y entrevista | Ver §7 |
| 13 | **Spark / Kafka / Terraform** | P2 | 40+ h | — | **No ahora** |

**Total P0 + P1:** ~220–290 horas → **10–12 semanas a 20–25 h/semana**.

> **Estado real a noviembre de 2026:** SQL, Python, Git/CI y la base de AWS están cubiertos. dbt, Star Schema/SCD2, el pipeline y el dashboard están **en construcción** dentro de la Ola 3; no los cuentes como “terminados” en el CV hasta que existan y pasen tests.

> **Nota macOS:** Power BI Desktop es Windows-only y **Power BI Service no puede conectarse a un PostgreSQL local sin un gateway on-premises**, que también es Windows-only. Para MQ-02 usa **Power BI Desktop en una VM Windows** (UTM/Parallels/Windows 365) conectada al Postgres del host, o exporta los marts a CSV. **Prepara la VM antes de MQ-02**; la instalación no entra en el límite de 180 minutos. **Looker Studio** es el respaldo nativo si la VM se vuelve un problema; conserva Power BI como keyword principal.

### 4.1 Regla de estudio

- **60% práctica, 40% teoría.** Cada tema termina en un artefacto, no en un apunte.
- **Una sola fuente por tema.** No acumules cursos.
- **Explica en voz alta.** Si no puedes explicar SCD2 o idempotencia en 3 minutos, no lo sabes.
- **Todo en inglés técnico cuando sea posible** (documentación, nombres de columnas, README del portafolio).

---

## 5. Plan de 12 semanas

| Semana | Foco | Entregable concreto | Horas |
|---|---|---|---|
| 1 | Corte 0 — dbt + BI + diagnóstico SQL | `MQ-01` (dbt run/test) + `MQ-02` (dashboard con 3 hallazgos) + 20 ejercicios SQL + VM de Power BI operativa | 22 |
| 2 | Corte 0 — cierre + Excel | Cerrar `MQ-01`/`MQ-02`; `MQ-05` (DAG, P1) si sobra tiempo + tablas dinámicas/XLOOKUP | 22 |
| 3 | Corte 1 — PRD y fuente colombiana | `requirements.md` con el modelo dimensional del roadmap (grano, claves, join as-of) + Data Contract Socrata + ingesta paginada | 22 |
| 4 | Corte 1 — PostgreSQL + dbt + SCD2 | Carga transaccional, `fact_contrato` + `dim_entidad_scd2` + `dim_fecha` con TRM | 24 |
| 5 | Corte 1 — métricas, dashboard y README | 5 métricas + 3 insights + 1 recomendación + README bilingüe + Defensa Oral #1 | 25 |
| 6 | Corte 1B — caso BI/SQL + Carril E | Pregunta de negocio, SQL analítico y primer dashboard del caso; CV inicial | 25 |
| 7 | Corte 1B — cierre + perfil | Caso defendible publicado; LinkedIn ES/EN; lista de 40 empresas y tracker | 24 |
| 8 | Pre-cloud + Gate E1 + Gate E2 | `MQ-03`/`MQ-04` (máx. 2 días) + 2 artefactos publicados + CV/LinkedIn + pitch y demo | 24 |
| 9 | **Inicio de postulaciones** + Corte 2 (núcleo) | 10–15 postulaciones; S3 + IAM + Secrets + `teardown.py`; 1 mock | 22 |
| 10 | Corte 3 + Corte 2 opcional | Drills de SQL/take-home/caso/STAR; Lambda/Glue/Athena si el tiempo alcanza | 22 |
| 11 | Procesos activos | 10–15 postulaciones; 3–5 referidos/semana; mock semanal | 20 |
| 12 | Cierre y negociación | Simulación de oferta; banda salarial; plan de 90 días | 18 |

> Las semanas 9–12 se solapan con la búsqueda. **No pares el estudio para buscar, ni pares la búsqueda para estudiar.** Si hay conflicto, se recorta alcance técnico (Corte 2), nunca las 10 postulaciones semanales.

---

## 6. Portafolio para el mercado colombiano

### 6.1 Dos artefactos, no diez

**Artefacto 1 — Pipeline end-to-end con impacto de negocio**

- Fuente real y pública: **SECOP II (`jbjy-vk9h`)** para contratos y **TRM histórica COP/USD** en `datos.gov.co` (API Socrata con `$limit/$offset` y criterio de parada).
- Alcance acotado: sector **Salud y Protección Social**, 2024-01-01 a 2026-10-31, `valor_del_contrato > 0` (~426.000 contratos al 2026-11-11).
- Modelo: `fact_contrato` a grano `id_contrato` → `dim_entidad_scd2` (clave `codigo_entidad`, versión vigente a la fecha de firma) + `dim_fecha` (TRM COP/USD) + `dim_proveedor` (hasheado para personas naturales).
- Ingesta → PostgreSQL → dbt → dashboard (Power BI Desktop en VM / Looker Studio).
- README con: problema, arquitectura, decisiones, tests, cómo ejecutarlo, resultados y limitaciones.
- Métrica de impacto: “redujo el tiempo de consolidación de X a Y”, “detectó Z registros inválidos”, “automatiza un reporte semanal”.

**Artefacto 2 — Caso de BI / análisis**

- Ubicación: `content/portfolio/caso-bi-colombia/`.
- Una pregunta de negocio concreta (ej. morosidad, embudo de pagos, cohortes de retención, accidentalidad). Si reutilizas SECOP, la pregunta y el SQL deben ser distintos del Artefacto 1.
- SQL reproducible + dashboard + 3 hallazgos + 1 recomendación.
- **Ley 1581:** anonimiza identificadores de **personas naturales** (hash/agregación). Conserva el NIT de **personas jurídicas**; hashea el de personas naturales. La clave del SCD2 es **`codigo_entidad`**, no el NIT; no hashees `codigo_entidad`.

### 6.1.1 Publicación

Los dos artefactos se publican en un **repo público único** (sugerido: `github.com/01Ander/portafolio-datos-colombia`) con dos carpetas y un README raíz. La fuente de verdad sigue siendo el monorepo; la exportación se hace con un script por **allowlist** (`README`, `src/`, `tests/`, `models_dbt/`, `docker-compose.yml`, workflows y fixtures mínimos), que se crea al cerrar el Corte 1B. **Nunca** se publican `.env`, `data/`, Parquet crudos, credenciales ni acceptance tests internos. Antes del push: `gitleaks`/`git secrets`, revisión de cédulas y nombres de personas naturales, y prueba de que el README funciona en incógnito. El checklist vive en `PUBLICAR.md`.

### 6.2 Qué NO hacer

- Titanic, Iris, Netflix o cualquier dataset de tutorial.
- 10 repositorios a medio terminar.
- Notebooks sin README ni instrucciones.
- Gráficos sin pregunta de negocio.
- “Machine Learning” decorativo que no puedes defender.

### 6.3 README mínimo (plantilla)

```
1. Problema de negocio (2–3 líneas)
2. Arquitectura (diagrama simple)
3. Stack y por qué
4. Cómo ejecutarlo (1 comando)
5. Tests y calidad (qué validas)
6. Resultados (números, no adjetivos)
7. Limitaciones y siguientes pasos
```

---

## 7. Inglés: el multiplicador silencioso (incluido en el plan)

En Colombia, el inglés **no es un extra**: es un diferenciador salarial y de acceso.

### 7.1 Por qué importa incluso en empleos locales

- **Prima salarial del 30% al 50%** para perfiles C1 frente al mismo perfil sin inglés (benchmarks Colombia 2026).
- Muchas multinacionales con sede en Bogotá/Medellín entrevistan **parte del proceso en inglés**, aunque el día a día sea en español.
- Las vacantes **remotas para clientes de EE. UU. desde Colombia** exigen inglés funcional; son las que pagan en USD.
- Documentación, herramientas y comunidades técnicas están en inglés.

### 7.2 Nivel objetivo y evidencia

| Nivel | Cuándo basta | Evidencia que debes poder mostrar |
|---|---|---|
| **B1** | Leer documentación, escribir correos simples | README en inglés, CV con nivel declarado |
| **B2** | **Daily standups, reuniones técnicas, entrevistas** | Presentarte 2 minutos, explicar tu proyecto, responder “tell me about yourself” |
| **C1** | Cliente externo, presentaciones, negociación | Mock interview grabada, demo de 5 minutos |

**Meta del plan: B2 funcional demostrable en 12 semanas.**

### 7.3 Rutina semanal (3–5 h)

- **1 h** de listening técnico (podcast/video de data engineering) con notas.
- **1 h** de speaking: grabarse explicando un concepto del capstone.
- **1 h** de escritura: README, PR, mensaje a reclutador.
- **1 h** de vocabulario específico de datos (no inglés genérico).
- **1 h** de mock interview con alguien o con IA, corregida.

### 7.4 Cómo ponerlo en el CV y LinkedIn

- Línea explícita: `Inglés: B2 — entrevistas técnicas, documentación y comunicación escrita`.
- LinkedIn en inglés (titular y “About”) y español.
- Una sección “Projects” con descripciones en inglés.
- Ten listo un **guion de 90 segundos** en inglés sobre tu capstone.

> No inventes el nivel. Si te preguntan en inglés y no puedes sostener 5 minutos, el proceso termina ahí.

---

## 8. Búsqueda de empleo: canales y cadencia

### 8.1 Canales (por efectividad local)

| Canal | Uso | Frecuencia |
|---|---|---|
| **LinkedIn** | Vacantes + reclutadores + referidos | Diario, 20 min |
| **Computrabajo / Elempleo** | Volumen de vacantes junior | 2–3 veces/semana |
| **Magneto / GetOnBrd / Torre** | Tech y startups | 2 veces/semana |
| **Portales universitarios / SENA** | Prácticas y primer empleo | Semanal |
| **Referidos internos** | La vía más rápida | 3–5 contactos/semana |
| **Ferias y meetups** | Comunidad: Python Colombia, Data Science Colombia, Ruta N | Mensual |

### 8.2 Regla de aplicación

- **10–15 por semana**, no 100 genéricas.
- Adapta el 20% superior del CV a la vacante (keywords reales del anuncio).
- Si la vacante pide “2 años”, aplica igual si tienes el 60–70% del stack.
- Registra todo en una hoja: empresa, rol, canal, fecha, estado, contacto.
- **Seguimiento a los 7 días** por LinkedIn, breve y específico.

### 8.3 Guion de referido (LinkedIn)

> “Hola [nombre], vi que trabajas en [empresa] como [rol]. Estoy buscando mi primer rol en datos y tengo un proyecto con SQL, Python y dbt sobre datos públicos colombianos. ¿Te parece si te comparto el repo y me dices si el perfil encaja con alguna vacante junior de tu equipo?”

Corto, específico, sin pedir “una oportunidad” en abstracto.

---

## 9. Entrevistas: qué te van a preguntar

| Etapa | Qué evalúan | Cómo prepararlo |
|---|---|---|
| **Screening** | Motivación, salario, disponibilidad, inglés | Guion de 90 s; rango salarial claro; nivel de inglés honesto |
| **Prueba SQL** | Joins, agregaciones, CTEs, window functions, deduplicación | 20–30 ejercicios cronometrados; explicar el razonamiento |
| **Take-home** | Limpieza, modelado, reproducibilidad, comunicación | README, tests, supuestos explícitos; no sobre-ingenierices |
| **Caso de negocio** | Métricas, segmentación, trade-offs | Estructura: pregunta → datos → hipótesis → análisis → recomendación |
| **Behavioral** | Trabajo en equipo, conflicto, aprendizaje | STAR: situación, tarea, acción, resultado |
| **Inglés** | Fluidez y comprensión | Mock interviews; explicar el capstone sin leer |

**Error fatal:** entregar un take-home perfecto técnicamente pero sin README, sin supuestos y sin conclusión de negocio. En Colombia eso pesa más que un modelo elegante.

---

## 10. Expectativas salariales para el primer empleo

> Rangos de referencia del mercado local 2026, en **COP mensuales**, antes de prestaciones. Varían por ciudad, tamaño de empresa, modalidad y nivel de inglés. Tipo de cambio usado: ~4.000 COP/USD.

| Rol | Junior (0–2 años) | Con inglés B2/C1 | Nota |
|---|---|---|---|
| **Practicante / aprendiz** | 1–2 SMMLV + auxilio | — | La vía más rápida si aplica |
| **Analista de Datos** | 2,5–4,5 M (≈ USD 600–1.100) | 3,5–5,5 M | El rol más abundante |
| **Analista BI** | 3,0–5,0 M (≈ USD 750–1.250) | 4,0–6,0 M | Power BI/Tableau pesan |
| **Analytics Engineer** | 4,5–7,0 M (≈ USD 1.100–1.750) | 5,5–8,5 M | Mejor relación fit/salario |
| **Data Engineer** | 5,0–7,0 M (≈ USD 1.250–1.750) | 6,0–9,0 M | Bogotá/Medellín; remoto nacional suma |
| **Remoto para empresa extranjera (desde Colombia)** | USD 1.200–1.850/mes | USD 1.500–2.200/mes | Contractor; sin prestaciones |

### 10.1 Cómo leer una oferta

- **Salario integral:** incluye prestaciones sociales; el neto es menor de lo que parece.
- **Prestación de servicios (contractor):** no incluye salud, pensión, cesantías, prima ni vacaciones. Compara **compensación total**, no solo el bruto.
- **“Salario + beneficios”:** pregunta por prepaga, auxilio de conectividad, presupuesto de formación y días de vacaciones.
- **Bono variable:** no lo cuentes como fijo.

### 10.2 Guion de negociación

> “Mi expectativa está entre **X e Y** millones, según el alcance del rol y el paquete de beneficios. Con el nivel de inglés y el portafolio que traigo, me ubico en la parte media-alta de ese rango. ¿Cómo se compara con la banda del cargo?”

Reglas:

- Da un **rango**, no un número único.
- No aceptes en la primera llamada; pide la oferta por escrito.
- Negocia formación, modalidad y fecha de inicio si el salario está topado.
- **El primer empleo no define tu salario a 5 años**; define la experiencia que te permite el salto.

---

## 11. Primeros 90 días en el empleo

| Periodo | Objetivo | Acción |
|---|---|---|
| **Días 1–15** | Entender el negocio y los datos | Reunirte con 5 stakeholders; documentar fuentes y métricas |
| **Días 16–30** | Entregar algo visible | Automatizar un reporte o corregir una consulta crítica |
| **Días 31–60** | Ganar confianza técnica | Proponer una mejora de calidad o performance con medición |
| **Días 61–90** | Consolidar el rol | Documentar tu trabajo; pedir feedback formal; definir plan de crecimiento |

**Regla:** en los primeros 90 días, **documenta todo**. Lo que no se ve, no cuenta para la promoción ni para el siguiente empleo.

---

## 12. Riesgos y errores frecuentes

1. **Esperar a “estar listo”.** Nunca lo estarás; aplica desde la semana 9.
2. **Postular solo a “Data Engineer”.** Es el título más competido y el menos junior.
3. **Ignorar Excel y BI.** En banca y retail colombianos siguen siendo el día a día.
4. **Portafolio sin negocio.** Un pipeline técnico sin pregunta de negocio no convence.
5. **No practicar SQL en voz alta.** Saber la respuesta no es saber explicarla.
6. **Inglés declarado sin evidencia.** Te van a probar.
7. **Aplicar solo por portales.** Sin referidos, el embudo se alarga meses.
8. **Aceptar el primer contrato sin leerlo.** Revisa modalidad, prestaciones, horario y cláusula de exclusividad.
9. **No registrar el proceso.** Sin métricas no sabes qué corregir.
10. **Estudiar Spark/Kafka antes de dominar SQL.** Prioridad invertida.

---

## 13. Checklist final

### Antes de aplicar (cierre de la semana 8; postulas desde la 9)

- [ ] Resuelvo 20+ ejercicios SQL sin apuntes.
- [ ] Tengo un dashboard de BI con pregunta de negocio y recomendación.
- [ ] Tengo el capstone con `fact_contrato`, `dim_entidad_scd2` y `dim_fecha` con TRM, README, tests y métricas de impacto.
- [ ] Los 2 artefactos están publicados en el repo público y los enlaces abren en incógnito.
- [ ] Mi CV cabe en 1 página y tiene las keywords del mercado local.
- [ ] Mi LinkedIn está actualizado en español e inglés.
- [ ] Tengo un guion de 90 segundos en español y en inglés.
- [ ] Sé explicar SCD2, idempotencia, star schema y por qué el hecho es a grano contrato en 3 minutos.
- [ ] Tengo una hoja de seguimiento de aplicaciones.

### Durante la búsqueda

- [ ] 10–15 postulaciones personalizadas por semana.
- [ ] 3–5 contactos nuevos por semana.
- [ ] 1 mock interview por semana.
- [ ] 5 h de inglés técnico por semana.
- [ ] Revisión semanal de rechazos y patrones.

### Antes de aceptar

- [ ] Leí el contrato y entiendo la modalidad (empleado vs. contractor).
- [ ] Comparé compensación total, no solo salario bruto.
- [ ] Pregunté por beneficios, formación y modalidad.
- [ ] Tengo claro el plan de los primeros 90 días.
- [ ] La oferta me da **experiencia verificable** en el stack que quiero.

---

## 14. Fuentes y supuestos

- Rangos salariales: benchmarks de mercado colombiano 2026 (HR Oasis, DataPath, Glassdoor, SalariosTech), contrastados con ofertas activas. Son referencias, no garantías.
- Volumen de vacantes: Glassdoor Colombia (data analyst, analytics engineer) y portales locales, consultados en noviembre de 2026.
- Prima salarial por inglés: benchmark Colombia 2026 (30–50% para C1).
- Distribución geográfica: Bogotá ~73%, Medellín ~14%, Cali ~4% de vacantes IT.
- Tipo de cambio asumido: ~4.000 COP/USD.
- **Alcance:** este documento excluye deliberadamente open source y freelance como estrategia de entrada. Se enfoca en empleo formal local (presencial, híbrido o remoto nacional).
- **Revisión:** actualizar cada 3 meses o cuando cambie el mercado objetivo.

---

> **Recordatorio:** el objetivo de este plan no es el empleo perfecto. Es conseguir **experiencia verificable** lo antes posible, con un salario digno, para que el segundo empleo —mejor pagado y más técnico— sea mucho más fácil.
