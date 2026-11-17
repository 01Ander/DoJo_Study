# Capítulo 02: DAX I — Medidas, Columnas Calculadas y Contexto de Filtro

En **Tostadora El Roble**, el gerente quiere saber el ticket promedio de venta, el margen bruto por categoría y qué porcentaje del total representa cada sucursal. Si intentas precalcular esos porcentajes en una columna fija de Excel, cualquier filtro por mes o por ciudad romperá el denominador. **DAX (*Data Analysis Expressions*)** resuelve esto evaluando fórmulas dinámicamente según el **contexto de filtro** activo en cada celda de tu reporte.

---

## 1. Contexto de Fila vs. Contexto de Filtro (Qué y Por qué)

**Qué es:**
- **Contexto de Fila (*Row Context*):** Significa "fila actual". Ocurre cuando DAX evalúa una expresión fila por fila (por ejemplo, multiplicando `quantity * unit_price` en cada línea de un ticket).
- **Contexto de Filtro (*Filter Context*):** Es el conjunto de filtros activos aplicados sobre el modelo antes de evaluar una fórmula (por ejemplo, un segmentador en `year = 2026`, la fila `"Chapinero"` en una tabla visual, o un filtro dentro de `CALCULATE`).

**Por qué importa:** Confundir ambos contextos es la causa número uno de errores en DAX. Una suma simple no necesita saber qué pasa fila por fila, pero una multiplicación de dos columnas (`quantity * unit_price`) sí necesita un iterador que cree contexto de fila antes de sumar. Y un cálculo de `% del Total` necesita modificar el contexto de filtro para ver el total global mientras mantiene el numerador filtrado.

> **Analogías (*Tostadora El Roble*):**
> 1. **El filtro de la cafetera (*Filter Context*) vs. pesar cada bolsa (*Row Context*):** El *contexto de filtro* es seleccionar qué granos entran en la tolva (solo cosecha 2026 de la sucursal Chapinero). El *contexto de fila* es tomar cada bolsa individual dentro de esa tolva y multiplicar su peso por su precio por kilo antes de sumar el valor total del lote.
> 2. **La pizarra dinámica vs. la etiqueta pegada:** Una columna calculada es una etiqueta impresa y pegada en cada bolsa al empacar (no cambia aunque el cliente pida ver solo el fin de semana). Una medida es un cálculo hecho al instante en la caja según los filtros que el gerente acaba de marcar.

---

## 2. Medidas Explícitas vs. Columnas Calculadas (Qué y Por qué)

**Qué es:**
- **Columna Calculada:** Se calcula durante la carga/refresco de datos, fila por fila, y se almacena físicamente en la memoria RAM ocupando espacio. Es útil principalmente para categorizar atributos en dimensiones (ej. `size_tier = IF(weight_g > 500, "Large", "Standard")`).
- **Medida Explícita:** Es una fórmula DAX almacenada como definición lógica (ocupa 0 bytes de datos extra) que se evalúa dinámicamente en tiempo de consulta según el contexto de filtro del reporte.

**Por qué importa:** Nunca debes usar columnas calculadas para calcular ratios (como ticket promedio o `% del total`): un promedio de promedios por fila es matemáticamente incorrecto, y almacenar cálculos pre-agregados desperdicia memoria y rompe la interactividad de los filtros.

---

## 3. Funciones Agregadoras, Iteradoras y División Segura (Qué y Por qué)

**Qué es:**
- **Agregadoras (`SUM`, `COUNTROWS`):** Operan sobre toda una columna o tabla bajo el contexto de filtro actual.
- **Iteradoras (`SUMX`):** Reciben una tabla y una expresión, evalúan la expresión en **contexto de fila** para cada fila, y luego suman los resultados.
- **División segura (`DIVIDE`):** Función que divide numerador entre denominador devolviendo un valor alternativo (o `BLANK()`) cuando el denominador es `0`, evitando errores `Infinity` o `NaN`.

**Por qué importa:** En *Tostadora El Roble*, si `fact_coffee_sales` tiene `quantity` y `unit_price` pero no una columna precalculada `line_total`, `SUM` no puede multiplicar dos columnas; necesitas `SUMX`. Y si una sucursal nueva tuvo `0` órdenes en enero, usar `/` en lugar de `DIVIDE` rompe visualmente las tarjetas del dashboard.

---

## 4. Modificación y Remoción de Filtros: `CALCULATE` y `ALL` (Qué y Por qué)

**Qué es:**
- **`CALCULATE(<expresión>, <filtro1>, ...)`:** Es la función más importante de DAX. Evalúa una medida dentro de un **contexto de filtro modificado** (añadiendo, sobrescribiendo o eliminando filtros).
- **`ALL(<tabla o columna>)`:** Función modificadora que **elimina todos los filtros** aplicados sobre la tabla o columna indicada.

**Por qué importa:** Para calcular qué porcentaje de las ventas totales representa la sucursal *Chapinero*, el numerador debe respetar el filtro de *Chapinero*, pero el denominador debe **ignorar** el filtro de sucursal para obtener el gran total de toda la cadena. Sin `CALCULATE(..., ALL(...))`, dividirías las ventas de Chapinero entre sí mismas y siempre obtendrías `100%`.

---

## 5. Implementación en DAX (Cómo)

### Setup Inicial (Crear Medidas en Power BI Desktop)

1. Crea una tabla vacía dedicada (o selecciona `fact_coffee_sales`) → clic derecho → **New measure**.
2. Escribe siempre nombres de medidas claros en inglés profesional y guarda todas tus métricas como **medidas explícitas** (evita arrastrar columnas numéricas crudas directamente a los gráficos como "medidas implícitas").

### El Camino Frágil (Columnas calculadas y operador `/` sin protección)

**🎯 Objetivo de Negocio:** Calcular el ingreso total, el ticket promedio y el porcentaje de participación por sucursal en *Tostadora El Roble*.

```dax
-- FRAGILE: Division with '/' crashes on zero orders; no ALL() for global denominator
Avg Ticket Fragile = SUM(fact_coffee_sales[amount_cop]) / COUNTROWS(fact_coffee_sales)
```

**Por qué falla este camino:**
- Si un filtro selecciona un día sin ventas (`COUNTROWS = 0`), el operador `/` devuelve `Infinity`, dañando la visualización.
- Si intentas calcular `% del Total` sin `CALCULATE` + `ALL`, el denominador cambia en cada fila de la tabla y siempre da `100%`.

### El Camino Robusto (Medidas explícitas con `SUM`, `COUNTROWS`, `SUMX`, `DIVIDE`, `CALCULATE`, `ALL`)

**🎯 Objetivo de Negocio:** Construir 5 medidas DAX auditables para *Tostadora El Roble*: ingresos totales (`Total Revenue`), conteo de órdenes (`Total Orders`), costo total de granos (`Total Bean Cost`), ticket promedio (`Avg Ticket`) y participación porcentual por sucursal (`% of Total Revenue`).

```dax
-- 1. Total Revenue using SUM
Total Revenue = SUM(fact_coffee_sales[amount_cop])

-- 2. Total Orders using COUNTROWS
Total Orders = COUNTROWS(fact_coffee_sales)

-- 3. Total Bean Cost iterating row-by-row with SUMX
Total Bean Cost =
SUMX(
    fact_coffee_sales,
    fact_coffee_sales[beans_kg] * fact_coffee_sales[cost_per_kg]
)

-- 4. Avg Ticket using safe DIVIDE
Avg Ticket =
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)

-- 5. % of Total Revenue removing branch filters with CALCULATE + ALL
% of Total Revenue =
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL(dim_branch)
    ),
    0
)
```

#### Desglose de Sintaxis (Zero Surprise Syntax)

| Función DAX | Qué hace | Por qué se eligió | Cómo funciona internamente |
|---|---|---|---|
| `SUM(columna)` | Suma todos los valores numéricos de una columna bajo el contexto de filtro actual. | Es la agregación estándar más rápida en el motor tabular VertiPaq. | Lee únicamente los valores visibles tras aplicar las relaciones `1:N` activas y devuelve un escalar. |
| `COUNTROWS(tabla)` | Cuenta el número de filas visibles de una tabla bajo el contexto de filtro actual. | Es más rápido y claro que `COUNT(columna)` cuando el grano de la tabla es 1 fila por orden. | Consulta el diccionario interno de filas filtradas de `fact_coffee_sales` sin escanear valores nulos. |
| `SUMX(tabla, expresión)` | Evalúa `expresión` fila por fila sobre `tabla` y suma los resultados. | `fact_coffee_sales` tiene `beans_kg` y `cost_per_kg` separados; `SUM` no acepta multiplicaciones entre columnas. | Crea un **contexto de fila** temporal sobre `fact_coffee_sales`, multiplica ambos valores en cada fila y acumula la suma final. |
| `DIVIDE(num, den, alt)` | Divide `num` entre `den`; si `den` es `0` o `BLANK()`, retorna `alt` (`0`). | Protege el reporte contra errores de división por cero en días o filtros sin actividad. | Verifica internamente si `den = 0` antes de ejecutar la división; si omites `alt`, devuelve `BLANK()`. |
| `CALCULATE(expr, filtro)` | Reevalúa `expr` modificando el contexto de filtro actual según `filtro`. | Permite cambiar dinámicamente el alcance del denominador sin alterar el numerador. | Clona el contexto de filtro actual, aplica las modificaciones indicadas (`ALL(dim_branch)`) y luego ejecuta `[Total Revenue]`. |
| `ALL(tabla)` | Remueve todos los filtros activos sobre `tabla` (como `dim_branch`). | Necesario dentro de `CALCULATE` para obtener el total de todas las sucursales en el denominador de `% of Total Revenue`. | Ignora cualquier selección hecha en `dim_branch[branch_name]` o `dim_branch[city]` mientras mantiene intactos otros filtros externos (como `dim_date[year]`). |

---

## 6. Conexión con Testing y Reconciliación SQL (Regla Crítica)

Toda medida DAX debe **reconciliarse contra SQL** antes de darse por terminada. Aplicamos el ciclo **AAA**:

1. **Arrange (Preparar filtro conocido):** En Power BI, filtra el año `2026` usando `dim_date[year]` en una tabla visual con `dim_branch[branch_name]` y coloca las 5 medidas (`Total Revenue`, `Total Orders`, `Total Bean Cost`, `Avg Ticket`, `% of Total Revenue`).
2. **Act (Ejecutar consulta SQL equivalente):** Ejecuta en PostgreSQL la consulta analítica que replica exactamente el mismo cálculo y filtro (`year = 2026`).
3. **Assert (Validar paridad exacta):** Compara fila por fila los valores de Power BI contra el resultado SQL. La diferencia debe ser `0` (o dentro de la tolerancia de redondeo de 2 decimales).

```sql
-- Reconciliation query for Tostadora El Roble (2026)
WITH branch_metrics AS (
    SELECT
        b.branch_name,
        SUM(f.amount_cop) AS total_revenue,
        COUNT(*) AS total_orders,
        SUM(f.beans_kg * f.cost_per_kg) AS total_bean_cost,
        ROUND(SUM(f.amount_cop)::numeric / NULLIF(COUNT(*), 0), 2) AS avg_ticket
    FROM fact_coffee_sales f
    JOIN dim_branch b ON f.branch_id = b.branch_id
    JOIN dim_date d ON f.sale_date = d.date_key
    WHERE d.year = 2026
    GROUP BY b.branch_name
)
SELECT
    branch_name,
    total_revenue,
    total_orders,
    total_bean_cost,
    avg_ticket,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) AS pct_of_total_revenue
FROM branch_metrics
ORDER BY total_revenue DESC;
```

---

## 7. Mapa de Ejercicios

Dirígete a `quests/02-dax-medidas-y-contexto/` y completa la práctica deliberada **BI-02**:

```text
quests/02-dax-medidas-y-contexto/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```
