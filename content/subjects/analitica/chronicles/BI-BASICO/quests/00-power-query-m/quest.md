# Quest BI-00: Ingesta Reproducible con Power Query (M)

> **Objetivo:** Construir un flujo de extracción y limpieza reproducible en Power Query (M) sin editar manualmente el archivo de origen.
> **Requisitos Previos:** Lore del Capítulo 00 (`00-power-query-m.md`). No uses sintaxis o funciones no enseñadas en el Capítulo 00.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
La cadena **Librería El Faro** recibe el archivo crudo `../data/faro_sales_raw.csv` con nombres de columnas en español, espacios sobrantes en los nombres de tienda, una fila sin identificador de venta (`id_venta` vacío) y un pedido anulado (`estado = "cancelled"`). Tu misión es ingestar y limpiar estos datos en Power Query manteniendo intacto el archivo CSV original.

---

## 📋 Instrucciones

1. **Conectar a la fuente:**
   - Abre Power BI Desktop (en tu VM Windows o entorno local) → **Get data → Text/CSV** → selecciona `quests/data/faro_sales_raw.csv` → haz clic en **Transform Data**.
2. **Aplicar mínimo 5 pasos reproducibles en Power Query (M):**
   - **Paso 1–2:** Lectura del CSV (`Csv.Document` + `File.Contents`) y promoción de encabezados (`Table.PromoteHeaders`).
   - **Paso 3 (Renombrado):** Renombra las columnas usando `Table.RenameColumns` al estándar en inglés:
     - `id_venta` → `sale_id`
     - `fecha_venta` → `sale_date`
     - `tienda_id` → `store_id`
     - `tienda_nombre` → `store_name`
     - `unidades` → `units`
     - `precio_unitario` → `unit_price`
     - `costo_unitario` → `unit_cost`
     - `monto_cop` → `amount_cop`
     - `estado` → `order_status`
   - **Paso 4 (Tipado explícito):** Asigna tipos con `Table.TransformColumnTypes`: `sale_id` (`type text`), `sale_date` (`type date`), `store_id` (`type text`), `store_name` (`type text`), `units` (`Int64.Type`), `unit_price` (`Int64.Type`), `unit_cost` (`Int64.Type`), `amount_cop` (`Int64.Type`), `order_status` (`type text`).
   - **Paso 5 (Filtrado de nulos y anulados):** Usa `Table.SelectRows` para conservar solo las filas donde `sale_id <> null`, `sale_id <> ""` y `order_status <> "cancelled"`.
   - **Paso 6 (Limpieza de texto):** Usa `Table.TransformColumns` con `Text.Upper(Text.Trim(_))` sobre `store_name`.
3. **Exportar `query.pq`:**
   - Abre **Advanced Editor**, copia el bloque `let ... in` completo y guárdalo en `my_query.pq` dentro de esta carpeta.
   - Guarda una captura de pantalla del panel **Applied Steps** como evidencia.

---

## 🧪 Validación (Andamiaje Nivel 1 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Verifica que `../data/faro_sales_raw.csv` tiene 9 filas de datos (incluyendo 1 `id_venta` vacío y 1 `cancelled`).
2. **Act:** Ejecuta **Refresh Preview** en Power Query Editor.
3. **Assert:**
   - La tabla resultante tiene exactamente **7 filas** válidas.
   - **Column Quality** muestra `0% Empty` y `0% Error` en `sale_id`.
   - Todos los valores de `store_name` aparecen en mayúsculas y sin espacios sobrantes (`"CENTRO"`, `"NORTE"`, `"SUR"`).

---

## 💡 Restricciones y Entrega
- Solo puedes usar funciones M enseñadas en el Capítulo 00.
- Prohibido editar `faro_sales_raw.csv` manualmente.
- **Entregables:** `my_query.pq` + captura de *Applied Steps* + respuesta de 3 min explicando qué hace tu bloque `let ... in`.
