# Rite Requirements — `BI-BASICO`

> **Instrucción para el Operador:** Este es tu proyecto final (Rito de Paso). Integra todos los conceptos aprendidos en la Chronicle. Debes implementar cada fase de manera progresiva en Power BI Desktop / Power BI Service y registrar tus avances en `journal.md`.
>
> ⚠️ **Zero Surprise Syntax:** Solo puedes emplear herramientas, funciones M, DAX y SQL que estén documentadas en la `matriz-trazabilidad.md` de esta Chronicle.

---

## 🎯 Business Context

**Problema de Negocio:**
> La red de logística y paquetería **RutaExpress** opera envíos nacionales a través de múltiples centros de distribución (*hubs*). Actualmente, la gerencia recibe exportaciones CSV crudas con nombres de columnas inconsistentes, espacios sucios, envíos anulados y registros sin identificador, y las analiza en hojas de cálculo planas sin reconciliación contra la base de datos. Esto impide conocer con exactitud el costo operativo por peso, la evolución interanual (`YoY`) y la participación por hub, además de exponer datos de todas las regiones a gerentes locales sin aislamiento de seguridad.

**ROI (Return of Investment):**
> Construir un modelo semántico en estrella `1:N` auditable con ingesta reproducible en Power Query (`query.pq`), 8 medidas DAX reconciliadas contra SQL, un tablero ejecutivo de 1 página y seguridad RLS estática reduce a cero los errores de doble conteo, estandariza la toma de decisiones comerciales y protege la visibilidad regional de los datos.

---

## 🛠️ Arquitectura Esperada

- **Inputs:** Archivos planos CSV o tablas PostgreSQL crudas de envíos (`raw_shipments`) y centros de distribución (`raw_hubs`) de *RutaExpress*.
- **Procesamiento:** Ingesta y limpieza reproducible en Power Query (M), modelado en estrella (`1:N` unidireccional con `dim_date` marcada), capa semántica de 8 medidas DAX reconciliadas con SQL y rol RLS estático.
- **Outputs:** Archivo `.pbix` auditable, script `query.pq`, script SQL de reconciliación, evidencias de dashboard/refresh/RLS (`View as`) y defensa oral de 5 minutos.
- **Domain Shifting:** Este proyecto ocurre en el dominio de **Logística y Envíos de Paquetería (*RutaExpress*)**, por lo que debes traducir lógicamente los conceptos aprendidos en el Lore (*Tostadora El Roble*) y en las Quests (*Librería El Faro*) a este entorno.

---

## 📄 Data Contract (*RutaExpress*)

### Payload Raw (Ejemplo de fuente cruda de envíos)

```json
{
  "id_envio": "SHP-90421",
  "fecha_envio": "2026-03-14",
  "codigo_hub": "HUB-BOG-01",
  "nombre_hub": "  bogota centro ",
  "region": "Andina",
  "ciudad": "Bogotá",
  "ingreso_cop": 85000,
  "peso_kg": 4.5,
  "tarifa_por_kg": 11000,
  "estado_envio": "delivered"
}
```

> **Reglas del upstream:** Pueden llegar filas con `id_envio` nulo/vacío, `estado_envio = "cancelled"` y espacios o minúsculas inconsistentes en `nombre_hub`. Estos registros deben depurarse exclusivamente en Power Query sin modificar el archivo/tabla origen.

### Schema Semántico Destino (Star Schema)

```sql
-- Fact table (grain: 1 row per valid shipment_id)
CREATE TABLE fact_shipments (
    shipment_id   TEXT PRIMARY KEY,
    shipment_date DATE NOT NULL,
    hub_id        TEXT NOT NULL,
    revenue_cop   NUMERIC NOT NULL,
    weight_kg     NUMERIC NOT NULL CHECK (weight_kg > 0),
    rate_per_kg   NUMERIC NOT NULL CHECK (rate_per_kg > 0),
    status        TEXT NOT NULL
);

-- Hub dimension
CREATE TABLE dim_hub (
    hub_id   TEXT PRIMARY KEY,
    hub_name TEXT NOT NULL,
    region   TEXT NOT NULL,
    city     TEXT NOT NULL
);

-- Continuous date dimension (marked as date table in Power BI)
CREATE TABLE dim_date (
    date_key     DATE PRIMARY KEY,
    year         INT  NOT NULL,
    month_number INT  NOT NULL,
    month_name   TEXT NOT NULL,
    year_month   TEXT NOT NULL
);
```

---

## 🚀 Fases Desbloqueables

### Fase 1: Ingesta Reproducible y Modelo Semántico (Referencia: Cap 00 y Cap 01)
Construir la base de datos limpia y el Star Schema sin ambigüedades antes de escribir métricas.

**Criterios de Aceptación (DoD):**
- [ ] Conectar Power Query a las fuentes crudas de *RutaExpress* (CSV o PostgreSQL) aplicando ≥5 pasos reproducibles: lectura de fuente, promoción de encabezados (si es CSV), renombrado de columnas a inglés, tipado explícito, filtrado de nulos/anulados en sintaxis M (`each [shipment_id] <> null and [shipment_id] <> "" and [status] <> "cancelled"`) y limpieza de texto (`Text.Trim`, `Text.Upper`).
- [ ] Exportar el código M completo desde *Advanced Editor* en `query.pq`.
- [ ] Construir el Star Schema con `fact_shipments`, `dim_hub` y `dim_date` (continua y marcada con *Mark as date table*).
- [ ] Configurar relaciones `1:N` con dirección de filtro única (`Single`) y ocultar llaves técnicas en `fact_shipments`.
- [ ] Verificar cero llaves huérfanas con consulta SQL de control.
- [ ] Registrar avances de la fase en `journal.md`.

### Fase 2: Capa de Métricas DAX y Reconciliación SQL (Referencia: Cap 02 y Cap 03)
Implementar la lógica de negocio como medidas explícitas auditables contra SQL.

**Criterios de Aceptación (DoD):**
- [ ] Implementar **8 medidas DAX explícitas** (cero columnas calculadas para ratios):
  1. `Total Revenue` (`SUM` de `revenue_cop`)
  2. `Total Shipments` (`COUNTROWS` de `fact_shipments`)
  3. `Avg Ticket` (`DIVIDE` seguro con fallback `0`)
  4. `Total Cost` (`SUMX(fact_shipments, fact_shipments[weight_kg] * fact_shipments[rate_per_kg])`)
  5. `% of Total` (`DIVIDE` con `CALCULATE` + `ALL(dim_hub)`)
  6. `YoY %` (`VAR ... RETURN`, `CALCULATE`, `SAMEPERIODLASTYEAR`, `NOT ISBLANK`, `BLANK()`)
  7. `YTD Revenue` (`TOTALYTD`)
  8. `MoM %` (`VAR ... RETURN`, `CALCULATE`, `DATEADD(..., -1, MONTH)`, `NOT ISBLANK`, `BLANK()`)
- [ ] Escribir un script SQL equivalente (con CTEs y Window Functions `SUM(...) OVER` / `LAG(...) OVER`) y demostrar reconciliación exacta (diferencia `0` o tolerancia de redondeo de 2 decimales) entre DAX y SQL.
- [ ] Registrar avances de la fase en `journal.md`.

### Fase 3: Storytelling Ejecutivo, Gobernanza y Defensa Oral (Referencia: Cap 04 y Cap 05)
Entregar el producto analítico completo listo para gerencia y auditable en entrevista.

**Criterios de Aceptación (DoD):**
- [ ] Diseñar un dashboard ejecutivo de **1 página** con jerarquía en Z: título de negocio, subtítulo dinámico (`SELECTEDVALUE`), *slicers* desde dimensiones (`dim_date[year]`, `dim_hub[city]`), **5 métricas principales** en tarjetas KPI (`Total Revenue`, `Total Shipments`, `Avg Ticket`, `YoY %`, `YTD Revenue`), gráfico de tendencia mensual y gráfico de barras ordenado por hub.
- [ ] Documentar **3 hallazgos cuantificados** y **1 recomendación accionable** derivada de los datos.
- [ ] Configurar **1 rol RLS estático** sobre `dim_hub` (ej. filtrado por región o ciudad) y validar aislamiento con **View as** (ciclo AAA + captura).
- [ ] Documentar el flujo de publicación y *Refresh* en Power BI Service (incluyendo la restricción de PostgreSQL local sin *On-Premises Data Gateway*).
- [ ] Ejecutar la **defensa oral de 5 minutos** explicando el grano de `fact_shipments`, las relaciones `1:N` y el contexto de filtro de `CALCULATE` + `ALL`.
- [ ] Completar la retrospectiva final en `journal.md`.

---

## ✅ Criterios de Aprobación Final (Gate 5)
Para que el DM certifique que has superado esta Chronicle:
1. El proyecto `.pbix` se actualiza limpiamente con `query.pq` sin edición manual de datos crudos.
2. Las 8 medidas DAX están reconciliadas al centavo (o tolerancia de redondeo documentada) contra SQL.
3. No existen relaciones `N:N` ni bidireccionales por defecto, y el RLS estático está validado sobre `dim_hub`.
4. El `journal.md` está completamente documentado y la defensa oral de 5 minutos supera la auditoría `/scry`.
