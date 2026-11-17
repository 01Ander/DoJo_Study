# Quest BI-01: Modelo Semántico en Estrella (Star Schema)

> **Objetivo:** Diseñar un modelo semántico en estrella (`1:N`, filtro unidireccional, llaves técnicas ocultas y tabla de fechas marcada) a partir de las tablas limpias de *Librería El Faro*.
> **Requisitos Previos:** Lore de los Capítulos 00–01 y `BI-00` completada.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
**Librería El Faro** necesita analizar sus ventas (`fact_book_sales`, salida de `BI-00`) cruzadas por tienda (`dim_store`, cargada desde `../data/faro_stores.csv`) y por tiempo (`dim_date`) sin sufrir doble conteo ni ambigüedad en los filtros.

---

## 📋 Instrucciones

1. **Cargar la tabla de hechos y la dimensión de tiendas:**
   - Renombra tu consulta limpia de `BI-00` a `fact_book_sales`.
   - Carga `quests/data/faro_stores.csv` como `dim_store` (promoviendo encabezados y tipando sus columnas).
2. **Crear la tabla de fechas continua (`dim_date`):**
   - En **Table view → New table**, genera `dim_date` usando `CALENDAR(DATE(2025, 1, 1), DATE(2026, 12, 31))` y `ADDCOLUMNS` para agregar `"year"`, `"month_number"`, `"month_name"` y `"year_month"` (ver `my_dim_date.dax`).
   - En **Table tools → Mark as date table**, marca `dim_date` seleccionando la columna `[Date]`.
3. **Configurar relaciones `1:N` unidireccionales:**
   - En **Model view**, crea la relación `dim_store[store_id]` (`1`) → `fact_book_sales[store_id]` (`*`) con **Cross filter direction = Single**.
   - Crea la relación `dim_date[Date]` (`1`) → `fact_book_sales[sale_date]` (`*`) con **Cross filter direction = Single**.
4. **Ocultar llaves técnicas:**
   - En `fact_book_sales`, oculta (`Hide in report view`) las columnas `store_id` y `sale_date`.

---

## 🧪 Validación (Andamiaje Nivel 2 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Crea una tabla visual temporal con `dim_store[city]` y un conteo de filas de `fact_book_sales`.
2. **Act:** Inspecciona el diagrama en **Model view** y la tabla visual resultante.
3. **Assert:**
   - Todas las relaciones muestran cardinalidad `1:*` y dirección `Single` (flecha hacia `fact_book_sales`).
   - La tabla visual muestra conteos distintos por ciudad (`Bogotá` = 6 filas válidas, `Medellín` = 1 fila válida), no el mismo total repetido.
   - Si cargas los datos a PostgreSQL, la consulta de control en `my_validation.sql` devuelve `orphan_sales_count = 0`.

---

## 💡 Restricciones y Entrega
- Prohibido activar filtros bidireccionales (`Both`) o usar *Auto Date/Time* en lugar de `dim_date`.
- Solo puedes usar sintaxis DAX/SQL enseñada en los Capítulos 00–01.
- **Entregables:** `.pbix` actualizado + `my_dim_date.dax` + captura del diagrama de **Model view**.
