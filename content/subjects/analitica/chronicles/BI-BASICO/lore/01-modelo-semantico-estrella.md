# Capítulo 01: Modelo Semántico en Estrella (Star Schema)

Cuando **Tostadora El Roble** empezó a analizar sus ventas, alguien exportó una sola tabla gigante con 40 columnas repetitivas (nombre de la sucursal, dirección, ciudad, nombre del café, categoría, fecha, día de la semana, monto). Ese archivo funcionaba para una tabla rápida, pero en Power BI se volvió lento, confuso y propenso a errores de conteo. Un **Modelo Semántico en Estrella (*Star Schema*)** organiza los datos separando los eventos medibles (hechos) de su contexto descriptivo (dimensiones), creando una estructura rápida, limpia y auditable.

---

## 1. Tabla Plana vs. Modelo en Estrella (Qué y Por qué)

**Qué es:**
- **Tabla Plana (*Flat Table*):** Una única tabla desnormalizada donde cada fila repite todos los atributos descriptivos (ciudad, categoría, mes, proveedor) junto con las métricas numéricas.
- **Modelo en Estrella (*Star Schema*):** Arquitectura analítica compuesta por una tabla central de **hechos** (*Fact Table*) conectada mediante relaciones a múltiples tablas de **dimensiones** (*Dimension Tables*), formando visualmente una estrella.

**Por qué importa:**
1. **Compresión y velocidad:** El motor tabular de Power BI (*VertiPaq*) comprime mucho mejor columnas con pocos valores repetidos en dimensiones separadas que textos repetidos millones de veces en una tabla plana.
2. **Sin ambigüedad en cálculos:** En tablas planas con distintos niveles de detalle (ej. metas mensuales mezcladas con ventas diarias), sumar columnas produce doble conteo silencioso.

> **Analogías (*Tostadora El Roble*):**
> 1. **El ticket de caja vs. el catálogo de la tienda:** El ticket de venta (*hecho*) solo imprime el código del producto, la fecha y el total pagado (`SKU-04`, `2026-03-10`, `$18,000`); no imprime la historia completa de la finca cafetera ni la dirección de la sucursal en cada línea. Esa información vive una sola vez en el catálogo (*dimensión*).
> 2. **La ficha médica y el directorio de sucursales:** Si la sucursal *Chapinero* cambia de gerente o de zona comercial, actualizas **una sola fila** en la tabla de sucursales (*dimensión*), no 500,000 recibos históricos (*hechos*).

---

## 2. Tabla de Hechos (*Fact Table*) y Grano (Qué y Por qué)

**Qué es:** Una **tabla de hechos** almacena eventos cuantitativos del negocio (ventas, transacciones, consumos). Su **grano (*grain*)** define exactamente qué representa **una fila** en esa tabla (por ejemplo: *una fila por ítem vendido en un ticket*).

**Por qué importa:** Si no defines el grano de forma explícita, puedes mezclar filas de distinto nivel (un resumen diario junto con tickets individuales) o provocar multiplicación de filas al cruzar tablas. Toda medida DAX que escribas depende de que el grano sea único y consistente.

---

## 3. Tablas de Dimensiones (*Dimension Tables*) (Qué y Por qué)

**Qué es:** Tablas descriptivas que responden el **quién, qué, dónde y cuándo** de cada hecho (por ejemplo: `dim_branch`, `dim_product`, `dim_date`). Contienen una clave primaria única (*Primary Key*) y atributos textuales o categóricos usados para filtrar y agrupar.

**Por qué importa:** Las dimensiones actúan como los "filtros oficiales" del modelo. Cuando un usuario hace clic en una región o en un mes dentro de un gráfico, el filtro nace en la dimensión y viaja hacia la tabla de hechos.

---

## 4. Cardinalidad `1:N` y Dirección de Filtro Única (Qué y Por qué)

**Qué es:**
- **Cardinalidad `1:N` (Uno a Muchos):** Significa que cada clave en la tabla de dimensión aparece **una sola vez** (lado `1`), mientras que en la tabla de hechos puede aparecer **muchas veces** (lado `*` o `N`).
- **Dirección de Filtro Única (Unidireccional):** Significa que los filtros fluyen estrictamente desde la dimensión hacia la tabla de hechos (`dim_branch` → `fact_coffee_sales`), **nunca** en sentido contrario ni en ambas direcciones (*Both*).

**Por qué importa:** Activar filtros bidireccionales (*Both*) por defecto es una de las trampas más peligrosas en Power BI: crea ambigüedad en los caminos de filtro, degrada el rendimiento y puede hacer que una dimensión filtre accidentalmente a otra dimensión a través de la tabla de hechos, generando números engañosos.

---

## 5. Ocultamiento de Llaves Técnicas y Tabla de Fechas Marcada (Qué y Por qué)

**Qué es:**
- **Ocultamiento de llaves técnicas (*Hide in report view*):** Ocultar las columnas de clave foránea (`branch_id`, `sale_date`) en la tabla de hechos y las claves internas en las dimensiones para que no aparezcan en la vista de creación de gráficos.
- **Tabla de fechas marcada (*Mark as date table*):** Designar explícitamente una dimensión calendario continua (`dim_date`) como la tabla oficial de fechas del modelo indicando su columna de fecha única.

**Por qué importa:**
1. Si dejas visibles las llaves técnicas en `fact_coffee_sales`, un usuario o tú mismo podría arrastrar `fact_coffee_sales[branch_id]` a un gráfico en lugar de `dim_branch[branch_name]`, rompiendo la lógica del filtro.
2. Sin una tabla de fechas marcada y continua (sin saltos de días), las funciones de inteligencia de tiempo de DAX (`YoY`, `YTD`, `MoM`) fallan o devuelven resultados en blanco.

---

## 6. Implementación en Power BI Desktop (Cómo)

### Setup Inicial (Vista de Modelo)

1. Carga tus tablas limpias desde Power Query (`fact_coffee_sales`, `dim_branch`, `dim_date`).
2. En el menú lateral izquierdo de Power BI Desktop, haz clic en el ícono de **Model view** (el tercer ícono, con forma de diagrama de relaciones).

### El Camino Frágil (Tabla plana o relación bidireccional)

**🎯 Objetivo de Negocio:** Conectar las ventas de *Tostadora El Roble* con sus sucursales para analizar ingresos por ciudad.

Un modelo frágil deja que Power BI cree relaciones automáticas bidireccionales (`Both`) o con cardinalidad `N:N` por tener sucursales duplicadas en `dim_branch`, y usa la fecha automática oculta de Power BI (*Auto Date/Time*) en lugar de una `dim_date` explícita.

```text
[dim_branch] * <---> * [fact_coffee_sales]   (FRAGILE: N:N and Bidirectional filter)
```

### El Camino Robusto (Star Schema `1:N` unidireccional + `dim_date` marcada)

**🎯 Objetivo de Negocio:** Construir un modelo semántico limpio donde `dim_branch` y `dim_date` filtren a `fact_coffee_sales` sin ambigüedad y con tabla de fechas oficial.

1. **Crear relaciones `1:N` unidireccionales:**
   - Arrastra `dim_branch[branch_id]` hacia `fact_coffee_sales[branch_id]`.
   - Haz doble clic en la línea de relación y verifica:
     - **Cardinality:** `One to many (1:*)` (lado `1` en `dim_branch`, lado `*` en `fact_coffee_sales`).
     - **Cross filter direction:** `Single` (flecha apuntando desde `dim_branch` hacia `fact_coffee_sales`).
   - Repite el mismo proceso entre `dim_date[Date]` (`1`) y `fact_coffee_sales[sale_date]` (`*`) con dirección `Single`.
2. **Ocultar llaves técnicas:**
   - En `fact_coffee_sales`, haz clic derecho sobre `branch_id` y `sale_date` → **Hide in report view**.
   - En `dim_branch`, oculta `branch_id` si es una clave técnica sin significado para el usuario final.
3. **Generar y marcar la tabla de fechas (`dim_date`):**
   - Si no tienes una `dim_date` cargada desde SQL/CSV, puedes crear una tabla calculada en **Table view → New table**:

```dax
-- ROBUST: Continuous calendar table for Tostadora El Roble
dim_date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2024, 1, 1 ), DATE ( 2026, 12, 31 ) ),
    "year", YEAR ( [Date] ),
    "month_number", MONTH ( [Date] ),
    "month_name", FORMAT ( [Date], "MMM" ),
    "year_month", FORMAT ( [Date], "YYYY-MM" )
)
```

> **Convención de capas:** la tabla creada con `CALENDAR` expone la columna `[Date]`; en DAX se referencia como `dim_date[Date]` (`SAMEPERIODLASTYEAR`, `TOTALYTD`, `DATEADD`). En las tablas PostgreSQL y en el DDL del Rite esa misma columna se llama `date_key`; si tu `dim_date` viene de SQL, usa `dim_date[date_key]` en DAX.

#### Desglose de Sintaxis (Zero Surprise Syntax)

| Función / Cláusula DAX | Qué hace | Por qué se eligió | Cómo funciona internamente |
|---|---|---|---|
| `CALENDAR(start_date, end_date)` | Genera una tabla de una sola columna llamada `[Date]` con todas las fechas continuas entre inicio y fin. | Garantiza que no falten días (fines de semana o festivos), requisito obligatorio para Time Intelligence. | Crea una secuencia diaria ininterrumpida desde `DATE(2024, 1, 1)` hasta `DATE(2026, 12, 31)`. |
| `DATE(year, month, day)` | Construye un valor de tipo fecha válido a partir de año, mes y día numéricos. | Evita ambigüedades regionales (`DD/MM/YYYY` vs `MM/DD/YYYY`). | Retorna un escalar `datetime` exacto. |
| `ADDCOLUMNS(table, name, expr, ...)` | Toma una tabla existente y le agrega columnas calculadas evaluadas fila por fila. | Permite enriquecer `CALENDAR(...)` con año, mes y etiqueta `YYYY-MM` en una sola expresión. | Itera sobre cada fila de `[Date]` y evalúa `YEAR([Date])`, `MONTH([Date])` y `FORMAT(...)`. |
| `FORMAT(value, format_string)` | Convierte una fecha o número a texto con el formato especificado (`"MMM"`, `"YYYY-MM"`). | Facilita ejes legibles en gráficos (`2026-03`) ordenables cronológicamente. | Aplica la máscara de formato sobre `[Date]` y devuelve tipo `text`. |

4. **Marcar como tabla de fechas:**
   - Selecciona `dim_date` en el panel derecho → pestaña **Table tools** → **Mark as date table** → elige la columna `[Date]`.

---

## 7. Conexión con Testing y Validación (Regla Crítica)

Un modelo estrella roto no lanza un error visible en pantalla: simplemente muestra totales repetidos en todas las filas de una tabla visual. Valida tu modelo aplicando el ciclo **AAA**:

1. **Arrange (Preparar prueba de relación):** Crea una tabla visual temporal en Power BI con `dim_branch[city]` como fila y un conteo de filas de `fact_coffee_sales`.
2. **Act (Ejecutar el filtro):** Observa el diagrama de **Model view** y la tabla visual resultante.
3. **Assert (Verificar integridad del modelo):**
   - **Aserción de cardinalidad:** Ninguna relación muestra `Many to many (*:*)` ni flecha doble (`Both`).
   - **Aserción de filtrado:** Los valores por ciudad en la tabla visual son distintos entre sí (si todas las ciudades muestran exactamente el mismo total global, la relación está inactiva o en dirección incorrecta).
   - **Aserción de integridad referencial (sin huérfanos):** Ejecuta en SQL la siguiente consulta de control para asegurar que ninguna venta en `fact_coffee_sales` apunta a una sucursal inexistente en `dim_branch`:

```sql
-- Control query to assert zero orphan foreign keys in fact_coffee_sales
SELECT COUNT(*) AS orphan_sales_count
FROM fact_coffee_sales f
LEFT JOIN dim_branch b ON f.branch_id = b.branch_id
WHERE b.branch_id IS NULL;
```

El resultado esperado es estrictamente `0`.

---

## 8. Mapa de Ejercicios

Dirígete a `quests/01-modelo-semantico-estrella/` y completa la práctica deliberada **BI-01**:

```text
quests/01-modelo-semantico-estrella/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```
