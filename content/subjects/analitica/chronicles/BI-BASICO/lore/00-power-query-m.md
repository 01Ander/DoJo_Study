# Capítulo 00: Power Query (M) e Ingesta Reproducible

En la cadena de cafeterías **Tostadora El Roble**, cada sucursal exporta diariamente sus ventas en archivos CSV o las registra en una base de datos PostgreSQL. Si un analista abre esos archivos en una hoja de cálculo y borra filas o corrige mayúsculas a mano cada lunes, el proceso no es auditable ni repetible. **Power Query** (y su motor de lenguaje **M**) resuelve este problema actuando como una **receta de transformación automatizada**: cada limpieza queda grabada como un paso reproducible que se ejecuta de nuevo cada vez que llegan datos frescos.

---

## 1. Conexión a Fuentes de Datos (CSV y PostgreSQL) (Qué y Por qué)

**Qué es:** Es el punto de entrada mediante el cual Power BI Desktop se conecta a un origen externo (como un archivo plano `CSV` o una base relacional `PostgreSQL`) para extraer datos sin modificar el archivo o tabla original.

**Por qué importa:** Si copias y pegas datos manualmente en Excel antes de cargarlos a Power BI, rompes el linaje del dato (*data lineage*). Cuando llegue la actualización de la próxima semana, tendrás que repetir todo el trabajo manual y correrás el riesgo de olvidar un filtro o alterar un valor por accidente. Conectarte directamente desde Power Query garantiza que la extracción sea **reproducible** y **solo de lectura** sobre la fuente.

---

## 2. El Editor de Power Query, Applied Steps y Lenguaje M (Qué y Por qué)

**Qué es:**
- **Editor de Power Query:** La interfaz visual de Power BI Desktop donde inspeccionas las columnas, aplicas filtros y limpias datos antes de cargarlos al modelo.
- **Applied Steps (Pasos Aplicados):** La lista cronológica en el panel derecho del editor que registra cada transformación (renombrar, filtrar, cambiar tipo) como una instrucción secuencial.
- **Lenguaje M:** El lenguaje funcional subyacente que Power Query genera automáticamente detrás de cada clic en la interfaz, estructurado en bloques `let ... in`.

**Por qué importa:** Cada clic en Power Query escribe código M. Entender la estructura `let ... in` te permite auditar qué pasó con tus datos, detectar pasos redundantes que hacen lenta la carga y exportar el script (`query.pq`) para versionarlo en Git o revisarlo en equipo.

> **Analogías (*Tostadora El Roble*):**
> 1. **La receta del barista maestro:** Un barista no improvisa la temperatura ni los gramos de café cada mañana; sigue una receta escrita paso a paso (moler 18 g → preinfusión 5 s → extracción 28 s). Los *Applied Steps* son esa receta: garantizan que el espresso (tu tabla limpia) salga idéntico hoy y dentro de seis meses.
> 2. **La línea de empaque en la tostaduría:** Los sacos de café verde entran por una banda transportadora, pasan por una zaranda que retira piedras (filtro de nulos), luego por la tostadora (tipado) y finalmente por la etiquetadora (renombrado de columnas). Si cambia la cosecha de la semana siguiente, no reconstruyes la fábrica: solo enciendes la misma banda.

---

## 3. Setup Inicial (Zero Assumption)

Para ejecutar los ejemplos y las prácticas de este capítulo necesitas **Power BI Desktop** operativo:

1. **Entorno en macOS / Windows:** Power BI Desktop solo corre de forma nativa en Windows. Si trabajas en macOS, inicia tu máquina virtual Windows (UTM, Parallels o Windows 365) con el snapshot preparado previamente.
2. **Abrir Power Query Editor:**
   - Inicia **Power BI Desktop**.
   - En la cinta superior (**Home**), haz clic en **Get data** → **Text/CSV** (para archivos locales) o **More... → Database → PostgreSQL database** (para tablas en PostgreSQL).
   - Una vez seleccionada la fuente, en la ventana de previsualización **NO** hagas clic en *Load* directamente; haz clic en **Transform Data** para abrir el **Power Query Editor**.
3. **Abrir el Editor Avanzado (código M):**
   - Dentro del Power Query Editor, ve a la pestaña **Home** (o **View**) y haz clic en **Advanced Editor**. Allí verás el código M generado y podrás copiarlo para guardarlo en un archivo `query.pq`.

---

## 4. Implementación: Ingesta y Limpieza Reproducible (Cómo)

### El Camino Frágil (Limpieza manual en origen y tipos implícitos)

**🎯 Objetivo de Negocio:** Cargar el archivo de ventas diarias de *Tostadora El Roble* (`roble_sales_raw.csv`) asegurando que no entren pedidos anulados ni espacios sucios antes de calcular ingresos.

Un enfoque frágil consiste en abrir el CSV en una hoja de cálculo, borrar manualmente las filas con estado `"cancelled"`, editar nombres de sucursal a mano y cargar el resultado en Power BI dejando que la herramienta "adivine" los tipos de columna sin registrar pasos explícitos:

```powerquery
// FRAGILE: Relies on manual pre-cleaning outside Power Query and lacks explicit typing or null filtering
let
    Source = Csv.Document(
        File.Contents("C:\data\roble_sales_manually_edited.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    PromotedHeaders
```

**Por qué falla este camino:**
- Si mañana llega un nuevo archivo `roble_sales_raw.csv`, la limpieza manual se perdió y volverán a entrar filas nulas o canceladas.
- Al no declarar tipos de datos explícitos (`Table.TransformColumnTypes`), Power BI puede interpretar un código de sucursal `"001"` como número `1` o una fecha `"2026-03-01"` como texto.

---

### El Camino Robusto (Pipeline reproducible en M con 5+ pasos)

**🎯 Objetivo de Negocio:** Cargar `roble_sales_raw.csv` (o una tabla PostgreSQL equivalente) mediante una secuencia auditable de pasos en Power Query que renombre columnas al estándar en inglés, asigne tipos explícitos, filtre nulos y órdenes canceladas, y normalice el texto de las sucursales.

```powerquery
// ROBUST: Reproducible ingestion pipeline for Tostadora El Roble
let
    // Step 1: Extract raw CSV file without modifying source
    Source = Csv.Document(
        File.Contents("C:\data\roble_sales_raw.csv"),
        [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),

    // Step 2: Promote first row as column headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // Step 3: Rename columns to clean English snake_case standard
    RenamedColumns = Table.RenameColumns(
        PromotedHeaders,
        {
            {"id_venta", "sale_id"},
            {"fecha_venta", "sale_date"},
            {"sucursal", "branch_name"},
            {"monto_cop", "amount_cop"},
            {"estado", "order_status"}
        }
    ),

    // Step 4: Enforce explicit data types
    TypedTable = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {"sale_id", type text},
            {"sale_date", type date},
            {"branch_name", type text},
            {"amount_cop", Int64.Type},
            {"order_status", type text}
        }
    ),

    // Step 5: Filter out null keys and cancelled orders
    FilteredRows = Table.SelectRows(
        TypedTable,
        each [sale_id] <> null and [sale_id] <> "" and [order_status] <> "cancelled"
    ),

    // Step 6: Trim whitespace and standardize branch_name to uppercase
    CleanedText = Table.TransformColumns(
        FilteredRows,
        {
            {"branch_name", each Text.Upper(Text.Trim(_)), type text}
        }
    )
in
    CleanedText
```

#### Desglose de Sintaxis (Zero Surprise Syntax)

| Instrucción / Operador | Qué hace | Por qué se eligió | Cómo funciona internamente |
|---|---|---|---|
| `let ... in` | Define un bloque de variables secuenciales (`let`) y declara cuál se devuelve como resultado final (`in`). | Es la estructura obligatoria de todo script en lenguaje M. | Cada línea dentro de `let` evalúa una expresión y la asigna a un identificador (un *Applied Step*), pasando el resultado de un paso como primer argumento del siguiente. |
| `Csv.Document(File.Contents(...), [...])` | Lee los bytes de un archivo local y los interpreta como tabla CSV. | Permite apuntar directamente al archivo crudo sin abrirlo manualmente; `QuoteStyle.Csv` elimina comillas dobles delimitadoras de campos de texto. | `File.Contents` carga el flujo binario del archivo y `Csv.Document` lo divide usando `Delimiter`, codificación UTF-8 (`Encoding = 65001`) y manejo estándar de comillas (`QuoteStyle.Csv`). |
| `Table.PromoteHeaders(tabla, [PromoteAllScalars = true])` | Convierte la primera fila de datos en los nombres de las columnas. | Al leer un CSV, Power Query nombra las columnas como `Column1`, `Column2`, etc. | Toma la fila 0, convierte sus valores a texto (`PromoteAllScalars = true`) y los asigna como encabezados, eliminando esa primera fila del cuerpo de la tabla. |
| `Table.RenameColumns(tabla, {{"old", "new"}})` | Cambia el nombre de las columnas según pares `{nombre_actual, nombre_nuevo}`. | Estandariza columnas heterogéneas del origen al formato `snake_case` en inglés. | Recorre la lista de pares y reemplaza los metadatos del encabezado sin copiar los datos de las filas. |
| `Table.TransformColumnTypes(tabla, {{"col", tipo}})` | Convierte explícitamente cada columna al tipo indicado (`type text`, `type date`, `Int64.Type`). | Evita errores silenciosos de cálculo o agrupación por inferencia automática. | Evalúa cada celda de la columna e intenta convertirla al tipo destino (`Int64.Type` = entero de 64 bits; `type date` = fecha sin hora). |
| `Table.SelectRows(tabla, each <condición>)` | Conserva solo las filas donde la condición evalúa a `true`. | Elimina registros corruptos (`null`) o anulados (`"cancelled"`) desde la ingesta. | La palabra clave `each` crea una función anónima que recibe cada fila de la tabla; `[columna]` accede al valor de esa columna en la fila actual, y `<>` significa "distinto de". |
| `Table.TransformColumns(tabla, {{"col", fn, tipo}})` | Aplica una función de transformación sobre cada valor de la columna indicada. | Limpia espacios sobrantes y unifica mayúsculas para evitar que `" Chapinero "` y `"chapinero"` se cuenten como dos sucursales distintas. | `_` representa el valor actual de la celda dentro de `each`; primero `Text.Trim(_)` quita espacios al inicio y al final, y luego `Text.Upper(...)` lo convierte a mayúsculas. |

#### Conexión equivalente a PostgreSQL

**🎯 Objetivo de Negocio:** Conectarse a la tabla `raw_sales` en PostgreSQL local en lugar de un archivo CSV, manteniendo intactos los pasos de limpieza posteriores.

```powerquery
// ROBUST: PostgreSQL source connection (replaces Csv.Document + PromoteHeaders)
let
    Source = PostgreSQL.Database("localhost:5432", "roble_analytics"),
    RawSales = Source{[Schema = "public", Item = "raw_sales"]}[Data],
    RenamedColumns = Table.RenameColumns(
        RawSales,
        {
            {"id_venta", "sale_id"},
            {"fecha_venta", "sale_date"},
            {"sucursal", "branch_name"},
            {"monto_cop", "amount_cop"},
            {"estado", "order_status"}
        }
    )
in
    RenamedColumns
```

- `PostgreSQL.Database("host:puerto", "nombre_bd")`: Abre una conexión de solo lectura al servidor PostgreSQL y devuelve un catálogo de tablas y vistas disponibles.
- `{[Schema = "public", Item = "raw_sales"]}[Data]`: Filtra ese catálogo por esquema (`public`) y nombre de tabla (`raw_sales`) y extrae su contenido tabular (`[Data]`).

---

## 5. Exportación del Script `query.pq` (Qué, Cómo y Por qué)

**Qué es:** Guardar el bloque `let ... in` completo del *Advanced Editor* en un archivo de texto plano con extensión `.pq` (por ejemplo, `query.pq`).

**Cómo se hace:** En Power Query Editor → **Home** → **Advanced Editor** → selecciona todo (`Ctrl+A`), copia (`Ctrl+C`) y pégalo en un archivo `query.pq` dentro de tu carpeta de trabajo.

**Por qué importa:** Un archivo `.pbix` es un binario opaco para Git; si solo guardas el `.pbix`, nadie puede revisar tus transformaciones en un Pull Request sin abrir Power BI Desktop. El archivo `query.pq` hace tu ingesta **auditable y versionable**.

---

## 6. Conexión con Testing y Validación (Regla Crítica)

En `BI-BASICO` no ejecutamos `pytest` sobre archivos `.pbix`, pero aplicamos exactamente el mismo rigor del **ciclo AAA (Arrange → Act → Assert)** para verificar que nuestra ingesta en Power Query no pierde ni duplica datos:

1. **Arrange (Preparar escenario de prueba):** Toma un archivo CSV o tabla de prueba con casos conocidos: 1 fila con `sale_id` nulo, 1 fila con `order_status = "cancelled"`, 1 sucursal con espacios `"  chapinero "` y 3 ventas válidas.
2. **Act (Ejecutar la transformación):** Haz clic en **Refresh Preview** (o **Close & Apply**) en Power Query Editor ejecutando tu `query.pq`.
3. **Assert (Validar resultados y reconciliar contra SQL):**
   - Verifica en el perfil de columna (*Column Quality* en la pestaña **View**) que `sale_id` tenga **0% Empty** y **0% Error**.
   - Verifica que el conteo de filas resultante sea exactamente `3` (las 2 filas inválidas fueron filtradas) y que `branch_name` aparezca como `"CHAPINERO"`.
   - Si tu fuente es PostgreSQL, ejecuta esta consulta de control para confirmar que el número de filas válidas coincide exactamente con el resultado de Power Query:

```sql
-- Control query to assert row count and total amount after Power Query filtering
SELECT
    COUNT(*) AS valid_row_count,
    SUM(monto_cop) AS valid_total_cop
FROM public.raw_sales
WHERE id_venta IS NOT NULL
  AND id_venta <> ''
  AND estado <> 'cancelled';
```

---

## 7. Mapa de Ejercicios

Dirígete a `quests/00-power-query-m/` y completa la práctica deliberada **BI-00**:

```text
quests/00-power-query-m/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```

*(Recuerda: en `BI-BASICO` la validación se realiza mediante artefacto reproducible `query.pq` + captura de pasos + defensa oral).*
