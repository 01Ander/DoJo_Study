# Chronicle: `BI-BASICO` — Business Intelligence con Power BI

## General Information
**Chronicle Name:** Business Intelligence Básico con Power BI (Power Query, Star Schema, DAX y Publicación)  
**Chronicle Code:** `BI-BASICO`  
**Version:** 1.0  
**Chronicle Type:** CORE-SUBTEMA  
**Área:** `analitica`  
**Prerrequisitos:** `SQL-BASICO` (Star Schema y agregaciones SQL para reconciliación) + entorno Power BI Desktop (VM Windows con snapshot en macOS).  
**Presupuesto de tiempo:** 20–24 horas (máximo 180 minutos por quest).

---

## 🎯 Business Context & ROI

**Business Context:**
> En el mercado laboral de analítica en Colombia (Analista de Datos / Analytics Engineer junior), construir tablas limpias en PostgreSQL o dbt es solo la mitad del trabajo: la toma de decisiones ocurre en la capa semántica y visual. Sin embargo, muchos perfiles técnicos cometen el error de conectar tablas planas gigantes a Power BI, usar filtros bidireccionales por defecto, mezclar columnas calculadas costosas con medidas dinámicas y presentar gráficos sin reconciliación numérica contra la base de datos ni una recomendación accionable.

**ROI Estimado:**
> Un analista que domina Power Query reproducible, modelado en estrella `1:N` con tabla de fechas marcada, DAX con contexto de filtro (`CALCULATE`, `DIVIDE`, `SUMX`, Time Intelligence) y validación cruzada contra SQL reduce en más de un 50% los errores de doble conteo en reportes ejecutivos y entrega dashboards auditables y defendibles en entrevistas técnicas.

---

## 🎭 Domain Shifting Rule

- **Dominio del Lore (Teoría y ejemplos):** Cadena de Cafeterías y Tostaduría Artesanal (*Tostadora El Roble* — sucursales, bebidas/bolsas de café, ventas diarias).
- **Dominio del Rite (Proyecto Final):** Red de Logística y Envíos de Paquetería (*RutaExpress* — envíos, centros de distribución/hubs, rutas y tarifas).

> Ambos dominios son completamente distintos entre sí y distintos al proyecto de portafolio (`PORT-CAPSTONE` / SECOP II) para forzar la transferencia real de conocimiento.

---

## 🛠️ Technical Objective

> Construir de principio a fin una solución de Business Intelligence en Power BI Desktop y Power BI Service: ingesta reproducible con Power Query (M), modelo semántico en estrella (`1:N` unidireccional con tabla de fechas marcada), medidas DAX reconciliadas contra SQL (incluyendo `CALCULATE`, `DIVIDE`, `SUMX` e inteligencia de tiempo `YoY`/`YTD`/`MoM`), dashboard ejecutivo de 1 página con storytelling cuantificado y publicación con refresh documentado y seguridad a nivel de fila (RLS).

---

## 📚 Syllabus (Course Structure)

### Lore (Capítulos Teóricos — 6 Capítulos alineados 1:1 con las Quests)

- **Cap 00: Power Query (M) e Ingesta Reproducible** — Conexión a fuentes (CSV / PostgreSQL), editor de Power Query, lenguaje M básico, pasos aplicados (*Applied Steps*), renombrado de columnas, tipado explícito, filtrado de nulos/anulados, limpieza de texto reproducible sin edición manual y exportación del script `query.pq`.
- **Cap 01: Modelo Semántico en Estrella (Star Schema)** — Diferencia entre tabla plana y modelo en estrella (1 tabla de hechos + dimensiones), cardinalidad `1:N`, dirección de filtro única (unidireccional vs bidireccional), ocultamiento de llaves técnicas, creación y marcado de la tabla de fechas (*Mark as date table*).
- **Cap 02: DAX I — Medidas, Columnas Calculadas y Contexto de Filtro** — Contexto de fila vs contexto de filtro, cuándo usar medidas vs columnas calculadas, funciones agregadoras e iteradoras (`SUM`, `COUNTROWS`, `SUMX`), división segura (`DIVIDE`), modificación y remoción de filtros con `CALCULATE` y `ALL`, y reconciliación de medidas contra SQL.
- **Cap 03: DAX II — Inteligencia de Tiempo (Time Intelligence)** — Requisitos de la tabla de fechas continua, cálculo interanual (`YoY` con `SAMEPERIODLASTYEAR`), acumulado del año (`YTD` con `TOTALYTD`), variación mensual (`MoM` con `DATEADD`) y validación numérica contra consultas SQL equivalentes.
- **Cap 04: Visualización Ejecutiva y Storytelling de Negocio** — Selección de gráficos según pregunta de negocio, jerarquía visual en dashboard de 1 página con 5 métricas clave y segmentadores (*slicers*), KPIs con contexto, redacción de 3 hallazgos cuantificados y formulación de 1 recomendación accionable + estructura de guion de defensa de 5 minutos.
- **Cap 05: Publicación, Refresh y Seguridad a Nivel de Fila (RLS)** — Publicación en Power BI Service, arquitectura de actualización (*Refresh* manual vs programado y limitación de PostgreSQL local sin gateway on-premises), creación y prueba (*View as*) de roles de seguridad a nivel de fila (**RLS** estático).

---

### Quests (Laboratorios Prácticos — 6 Quests: `BI-00` a `BI-05`)

Cada capítulo teórico tiene una quest homóloga en `quests/00-...` a `quests/05-...`:

| ID | Quest | Foco Técnico | Criterio de Aceptación |
|---|---|---|---|
| **BI-00** | Power Query | Conectar a fuente (PostgreSQL o CSV), ≥5 pasos documentados (renombrado, tipado, filtrado de nulos, limpieza de texto), cero limpieza manual | `query.pq` reproducible + captura de pasos |
| **BI-01** | Modelo semántico | Star schema: 1 hecho + 2 dimensiones, relaciones `1:N`, filtro unidireccional, tabla de fechas marcada | Diagrama del modelo + validación de cardinalidad |
| **BI-02** | DAX I | Medidas vs columnas calculadas, `CALCULATE`, `ALL`, `DIVIDE`, `SUMX` | 5 medidas con resultado reconciliado contra SQL |
| **BI-03** | DAX II | Inteligencia de tiempo: `YoY`, `YTD`, variación mensual (`MoM`) | 3 medidas de tiempo sobre tabla de fechas marcada |
| **BI-04** | Visualización y storytelling | Dashboard de 1 página con 5 métricas, segmentadores (*slicers*), 3 hallazgos cuantificados, 1 recomendación | Dashboard de 1 página + guion de defensa de 5 min |
| **BI-05** | Publicación y seguridad | Refresh programado o manual documentado + 1 rol RLS de demo | Evidencia de refresh + captura de RLS (`View as`) |

> [!IMPORTANT]
> **Excepción Declarada de Verificación (Artefacto + Defensa Oral):**
> A diferencia de las chronicles de Python/SQL, las 6 quests de `BI-BASICO` **no se validan con `pytest`** — no existe una forma razonable de ejecutar pruebas unitarias automatizadas sobre un archivo binario `.pbix`. Se validan mediante **artefactos reproducibles** (`.pbix`, `query.pq`, consultas SQL de reconciliación, capturas de modelo/refresh/RLS) + **defensa oral de 3–5 minutos** explicando el modelo semántico y una medida DAX.

---

### Rite (Proyecto Final — Rito de Paso)

**Dominio:** Red de Logística y Envíos de Paquetería (*RutaExpress*).  
**Descripción:**
> Construir desde cero un tablero gerencial completo para *RutaExpress* partiendo de archivos/tablas crudas de envíos y centros de distribución (*hubs*), entregando un `.pbix` auditable, sus scripts de Power Query y SQL de reconciliación, y una defensa oral de 5 minutos.

**Data Contract Mínimo (*RutaExpress*):**
- `fact_shipments` (grano: 1 fila por `shipment_id`): `shipment_id` (text, PK), `shipment_date` (date, FK → `dim_date`), `hub_id` (text, FK → `dim_hub`), `revenue_cop` (numeric), `weight_kg` (numeric > 0), `rate_per_kg` (numeric > 0), `status` (text).
- `dim_hub`: `hub_id` (text, PK), `hub_name` (text), `region` (text), `city` (text).
- `dim_date` (grano: 1 fila por fecha, continua sin huecos): `date_key` (date, PK), `year` (int), `month_number` (int), `month_name` (text), `year_month` (text).

**Fases Desbloqueables y Requerimientos Técnicos (Rite-Driven Design):**
1. **Fase 1: Ingesta Reproducible y Modelo Semántico** *(Mapea a Cap 00 y Cap 01)*
   - Conectar Power Query a las fuentes crudas de *RutaExpress* (CSV o PostgreSQL) aplicando ≥5 pasos de transformación reproducible (renombrado de columnas, tipado explícito, filtrado de nulos/anulados, limpieza de texto) y exportar el código M en `query.pq`.
   - Construir un Star Schema con 1 tabla de hechos (`fact_shipments`) y 2 dimensiones (`dim_hub`, `dim_date`), con relaciones `1:N`, dirección de filtro única, llaves técnicas ocultas y `dim_date` marcada como tabla de fechas.
2. **Fase 2: Capa de Métricas DAX y Reconciliación SQL** *(Mapea a Cap 02 y Cap 03)*
   - Implementar **8 medidas DAX explícitas**: ingresos totales (`Total Revenue`), conteo de envíos (`Total Shipments`), ticket promedio (`Avg Ticket` con `DIVIDE`), costo operativo (`Total Cost` con `SUMX(fact_shipments, fact_shipments[weight_kg] * fact_shipments[rate_per_kg])`), participación porcentual (`% of Total` con `CALCULATE` + `ALL`), variación interanual (`YoY %`), acumulado del año (`YTD Revenue`) y variación mensual (`MoM %`).
   - Escribir un script SQL equivalente y demostrar reconciliación exacta (diferencia `0` o tolerancia de redondeo documentada) entre las medidas DAX y los resultados SQL.
3. **Fase 3: Storytelling Ejecutivo, Gobernanza y Defensa Oral** *(Mapea a Cap 04 y Cap 05)*
   - Diseñar un dashboard ejecutivo de 1 página con las 5 métricas principales, segmentadores (*slicers*), 3 hallazgos cuantificados y 1 recomendación accionable.
   - Configurar 1 rol RLS estático (ej. filtrado por región/hub) validado con *View as* y documentar el flujo de refresh.
   - Documentar el guion y ejecutar la defensa oral de 5 minutos explicando el grano de `fact_shipments`, las relaciones `1:N` y el contexto de filtro de al menos una medida `CALCULATE`.

---

## 🎓 Domain Criteria (Definition of Done)

- Puede construir flujos de ingesta y limpieza reproducibles en Power Query (M) sin edición manual en origen, documentando el script `query.pq`.
- Puede diseñar un modelo semántico en estrella (`1:N`, filtro unidireccional, tabla de fechas marcada) evitando tablas planas y relaciones bidireccionales por defecto.
- Puede distinguir entre contexto de fila y contexto de filtro para escribir medidas DAX (`CALCULATE`, `DIVIDE`, `SUMX`) en lugar de abusar de columnas calculadas.
- Puede implementar métricas de inteligencia de tiempo (`YoY`, `YTD`, `MoM`) sobre una tabla de fechas continua y reconciliar sus resultados contra SQL.
- Puede diseñar un dashboard ejecutivo de 1 página con jerarquía visual clara, 3 hallazgos cuantificados y 1 recomendación de negocio defendible en 5 minutos.
- Puede documentar el proceso de publicación/refresh en Power BI Service y configurar un rol de seguridad a nivel de fila (RLS) estático verificado.

> Nota: Los Domain Criteria se validan formalmente mediante las 6 quests, el Rite y la auditoría final del DM (`/scry`).

---

## 🚀 Derived Future Chronicles

- `PORT-CAPSTONE`: Aplicación directa del modelo semántico `1:N`, medidas DAX (reconciliadas contra SQL) y storytelling sobre el pipeline E2E de datos de Colombia (`fact_contrato` + `dim_entidad_scd2` + `dim_fecha`).
- **Fase 2 (Post-Empleo):** Microsoft Fabric, Power BI Premium, RLS dinámico corporativo y optimización con DAX Studio / Tabular Editor.
