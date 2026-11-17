# Capítulo 03: DAX II — Inteligencia de Tiempo (Time Intelligence)

En **Tostadora El Roble**, saber que en marzo de 2026 se vendieron \$120 millones COP no dice mucho por sí solo: ¿fue mejor o peor que febrero de 2026? ¿Crecimos frente a marzo de 2025? ¿Cuánto llevamos acumulado en lo que va del año? Las funciones de **Inteligencia de Tiempo (*Time Intelligence*)** en DAX permiten comparar periodos dinámicamente, siempre que estén respaldadas por una tabla de fechas continua y correctamente marcada.

---

## 1. Requisitos de la Tabla de Fechas Continua (Qué y Por qué)

**Qué es:** Es la regla obligatoria según la cual las funciones de tiempo de DAX (`SAMEPERIODLASTYEAR`, `TOTALYTD`, `DATEADD`) requieren una tabla calendario (`dim_date`) que cumpla cuatro condiciones:
1. Contener **todos los días** sin huecos desde el 1 de enero del primer año hasta el 31 de diciembre del último año.
2. Tener una columna de tipo `Date` con **valores únicos** (sin duplicados).
3. Estar relacionada `1:N` con la tabla de hechos (`dim_date[Date]` → `fact_coffee_sales[sale_date]`).
4. Estar marcada explícitamente con **Mark as date table**.

**Por qué importa:** Si intentas calcular `SAMEPERIODLASTYEAR` usando directamente la columna `fact_coffee_sales[sale_date]` (que solo tiene los días en que hubo ventas y omite festivos de cierre), el motor de DAX no puede desplazar el calendario de forma simétrica y devuelve resultados en blanco o erróneos.

> **Analogías (*Tostadora El Roble*):**
> 1. **El calendario de pared vs. el libro de caja:** El libro de caja solo tiene páginas para los días que la cafetería abrió; si cerró un lunes festivo, ese día no aparece. Para saber qué día fue hace exactamente un año o un mes, necesitas el **calendario de pared completo** (los 365 días), no el libro de caja con días saltados.
> 2. **La regla graduada sin marcas faltantes:** Si mides el crecimiento de una planta con una regla a la que le faltan los centímetros 14 y 15, cualquier comparación de distancia será falsa. La `dim_date` continua es esa regla sin marcas faltantes.

---

## 2. Variación Interanual (`YoY` con `SAMEPERIODLASTYEAR`) (Qué y Por qué)

**Qué es:** **YoY (*Year-over-Year*)** compara una métrica en el periodo actual frente al mismo periodo del año inmediatamente anterior (por ejemplo, marzo 2026 vs. marzo 2025). Se implementa desplazando el contexto de fecha con `SAMEPERIODLASTYEAR(dim_date[Date])` dentro de `CALCULATE`.

**Por qué importa:** En el negocio cafetero hay estacionalidad fuerte (diciembre vende más que febrero). Comparar diciembre contra noviembre engaña; comparar diciembre 2026 contra diciembre 2025 aísla el crecimiento real del negocio.

---

## 3. Acumulado del Año (`YTD` con `TOTALYTD`) (Qué y Por qué)

**Qué es:** **YTD (*Year-to-Date*)** calcula el acumulado desde el 1 de enero del año en curso hasta la última fecha visible en el contexto de filtro actual, usando `TOTALYTD(<expresión>, <columna_fecha>)`.

**Por qué importa:** Permite responder en cualquier mes del año "¿cómo vamos frente a la meta anual?" sin sumar manualmente mes por mes.

---

## 4. Variación Mensual (`MoM` con `DATEADD`) (Qué y Por qué)

**Qué es:** **MoM (*Month-over-Month*)** compara el periodo actual contra el mes inmediatamente anterior desplazando el contexto de fechas con `DATEADD(dim_date[Date], -1, MONTH)`.

**Por qué importa:** Detecta caídas abruptas o picos recientes de operación (por ejemplo, el impacto inmediato de abrir una nueva sucursal o subir precios el mes pasado) sin esperar a que termine el año.

---

## 5. Implementación en DAX (Cómo)

### El Camino Frágil (Apuntar a la fecha del hecho y no proteger contra `BLANK()`)

**🎯 Objetivo de Negocio:** Calcular las ventas del año anterior y la variación interanual (`YoY %`) para *Tostadora El Roble*.

```dax
-- FRAGILE: Uses fact table date column (breaks on missing days) and divides without zero/blank guard
Revenue LY Fragile =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(fact_coffee_sales[sale_date])
)

YoY % Fragile =
([Total Revenue] - [Revenue LY Fragile]) / [Revenue LY Fragile]
```

**Por qué falla este camino:**
- `fact_coffee_sales[sale_date]` tiene días duplicados y días faltantes; `SAMEPERIODLASTYEAR` exige una tabla de fechas continua.
- En el primer año de operación (2024), `[Revenue LY Fragile]` es `BLANK()`, por lo que la resta y división directa produce valores confusos o errores si hay un `0`.

---

### El Camino Robusto (`VAR ... RETURN`, `dim_date` marcada y `DIVIDE`)

**🎯 Objetivo de Negocio:** Implementar 3 medidas de inteligencia de tiempo auditables (`YoY %`, `YTD Revenue`, `MoM %`) usando la tabla de fechas marcada `dim_date[Date]`.

```dax
-- 1. Year-over-Year (YoY %) growth using VAR/RETURN and SAMEPERIODLASTYEAR
YoY % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousYearRevenue =
    CALCULATE(
        [Total Revenue],
        SAMEPERIODLASTYEAR(dim_date[Date])
    )
RETURN
IF(
    NOT ISBLANK(PreviousYearRevenue),
    DIVIDE(CurrentRevenue - PreviousYearRevenue, PreviousYearRevenue),
    BLANK()
)

-- 2. Year-to-Date (YTD) cumulative revenue using TOTALYTD
YTD Revenue =
TOTALYTD(
    [Total Revenue],
    dim_date[Date]
)

-- 3. Month-over-Month (MoM %) growth using DATEADD
MoM % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousMonthRevenue =
    CALCULATE(
        [Total Revenue],
        DATEADD(dim_date[Date], -1, MONTH)
    )
RETURN
IF(
    NOT ISBLANK(PreviousMonthRevenue),
    DIVIDE(CurrentRevenue - PreviousMonthRevenue, PreviousMonthRevenue),
    BLANK()
)
```

#### Desglose de Sintaxis (Zero Surprise Syntax)

| Instrucción / Función DAX | Qué hace | Por qué se eligió | Cómo funciona internamente |
|---|---|---|---|
| `VAR <nombre> = <expr> RETURN <resultado>` | Almacena el resultado de una expresión en una variable local reutilizable dentro de la medida. | Evita calcular `[Total Revenue]` o el periodo anterior dos veces (una en el numerador y otra en el denominador) y hace la fórmula legible. | Evalúa cada `VAR` una sola vez en el contexto actual de la medida y sustituye su valor en la expresión `RETURN`. |
| `SAMEPERIODLASTYEAR(dim_date[Date])` | Devuelve una tabla con las fechas desplazadas exactamente 1 año hacia atrás respecto al contexto actual. | Es la forma estándar y optimizada para comparaciones interanuales (`YoY`). | Toma el rango de fechas visible en `dim_date[Date]` (ej. `2026-03-01`..`2026-03-31`) y lo traslada a `2025-03-01`..`2025-03-31`. |
| `TOTALYTD(expr, dim_date[Date])` | Evalúa `expr` acumulando desde el 1 de enero del año del contexto hasta la fecha máxima visible. | Simplifica el cálculo acumulado anual sin escribir filtros manuales de rango de fechas. | Internamente equivale a `CALCULATE(expr, DATESYTD(dim_date[Date]))`. |
| `DATEADD(dim_date[Date], -1, MONTH)` | Desplaza el conjunto de fechas visible hacia atrás (`-1`) o adelante (`+1`) por la unidad indicada (`MONTH`, `DAY`, `YEAR`). | Permite comparar el mes actual contra el mes anterior (`MoM`) respetando cierres de año (enero 2026 → diciembre 2025). | Mueve cada fecha del filtro actual exactamente 1 mes calendario hacia atrás en `dim_date[Date]`. |
| `NOT ISBLANK(valor)` / `BLANK()` | `ISBLANK` verifica si un valor está vacío; `NOT` lo niega; `BLANK()` devuelve un vacío explícito de DAX. | En el primer mes/año histórico no existe periodo previo; devolver `BLANK()` evita mostrar `-100%` o `Infinity` engañosos. | `IF` evalúa la condición y solo ejecuta `DIVIDE` cuando existe un periodo anterior con datos. |

---

## 6. Conexión con Testing y Validación contra SQL (Regla Crítica)

Aplicamos el ciclo **AAA** para reconciliar las 3 medidas temporales contra SQL:

1. **Arrange (Preparar tabla de prueba):** En Power BI, crea una tabla visual con `dim_date[year]` y `dim_date[month_number]`, y agrega `[Total Revenue]`, `[YTD Revenue]`, `[MoM %]` y `[YoY %]`.
2. **Act (Ejecutar SQL equivalente por calendario):** Ejecuta en PostgreSQL la consulta con `SUM() OVER (PARTITION BY year ...)` para `YTD` y `LEFT JOIN` al mes calendario anterior por clave entera (`year * 12 + month_number - 1`) y al año anterior (`year - 1`) para `MoM` y `YoY` (evitando `LAG(..., 1/12)` sobre series dispersas con meses faltantes).
3. **Assert (Verificar paridad):** Confirma que para cada mes de `2025` y `2026`:
   - El `YTD Revenue` de enero coincide exactamente con el `Total Revenue` de enero, y en diciembre coincide con el total anual.
   - `YoY %` y `MoM %` son `NULL` (`BLANK()` en DAX) cuando no existe el mes/año calendario previo y coinciden hasta el segundo decimal con la salida de SQL.

```sql
-- Reconciliation query for YTD, MoM%, and YoY% in PostgreSQL (safe on sparse months)
WITH monthly_sales AS (
    SELECT
        d.year,
        d.month_number,
        SUM(f.amount_cop) AS total_revenue
    FROM fact_coffee_sales f
    JOIN dim_date d ON f.sale_date = d.date_key
    GROUP BY d.year, d.month_number
)
SELECT
    cur.year,
    cur.month_number,
    cur.total_revenue,
    SUM(cur.total_revenue) OVER (
        PARTITION BY cur.year
        ORDER BY cur.month_number
    ) AS ytd_revenue,
    ROUND(
        (cur.total_revenue - prev_m.total_revenue) * 100.0
        / NULLIF(prev_m.total_revenue, 0),
        2
    ) AS mom_pct,
    ROUND(
        (cur.total_revenue - prev_y.total_revenue) * 100.0
        / NULLIF(prev_y.total_revenue, 0),
        2
    ) AS yoy_pct
FROM monthly_sales cur
LEFT JOIN monthly_sales prev_m
    ON prev_m.year * 12 + prev_m.month_number
     = cur.year * 12 + cur.month_number - 1
LEFT JOIN monthly_sales prev_y
    ON prev_y.year = cur.year - 1
   AND prev_y.month_number = cur.month_number
ORDER BY cur.year, cur.month_number;
```

---

## 7. Mapa de Ejercicios

Dirígete a `quests/03-dax-inteligencia-de-tiempo/` y completa la práctica deliberada **BI-03**:

```text
quests/03-dax-inteligencia-de-tiempo/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```
