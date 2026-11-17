# Quest BI-02: DAX I — Medidas, Contexto de Filtro y Reconciliación SQL

> **Objetivo:** Implementar 5 medidas DAX explícitas (`SUM`, `COUNTROWS`, `SUMX`, `DIVIDE`, `CALCULATE` + `ALL`) y reconciliarlas contra SQL.
> **Requisitos Previos:** Lore de los Capítulos 00–02 y `BI-01` completada.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
La gerencia de **Librería El Faro** necesita 5 métricas dinámicas por tienda que respondan a los filtros de año sin perder el denominador global en los cálculos de participación.

---

## 📋 Instrucciones

> **Prerrequisito de ejecución:** la reconciliación se ejecuta en PostgreSQL. Si aún no tienes las tablas, corre `reference/faro_schema.sql` y carga `dim_store` y las 7 filas limpias de `fact_book_sales` siguiendo las instrucciones del encabezado del script.

1. **Implementar las 5 medidas explícitas en `my_measures.dax` y en tu `.pbix`:**
   - `Total Revenue`: suma de `fact_book_sales[amount_cop]` usando `SUM`.
   - `Total Orders`: conteo de filas de `fact_book_sales` usando `COUNTROWS`.
   - `Total Cost`: costo total calculado fila por fila como `units * unit_cost` usando `SUMX`.
   - `Avg Ticket`: división segura de `[Total Revenue]` entre `[Total Orders]` usando `DIVIDE` (valor alternativo `0`).
   - `% of Total Revenue`: participación de `[Total Revenue]` sobre el total global sin filtro de tienda usando `DIVIDE`, `CALCULATE` y `ALL(dim_store)`.
2. **Reconciliar contra SQL:**
   - Completa `my_reconciliation.sql` con una consulta SQL usando CTE (`WITH`) y función ventana (`SUM(...) OVER ()`) para calcular las mismas 5 métricas filtradas para `year = 2026` agrupadas por `store_name`.

---

## 🧪 Validación (Andamiaje Nivel 3 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Crea una tabla visual en Power BI con `dim_store[store_name]`, filtrada a `dim_date[year] = 2026`, y agrega las 5 medidas.
2. **Act:** Ejecuta tu consulta de `my_reconciliation.sql` sobre los datos limpios de 2026.
3. **Assert:**
   - Para `2026`: `CENTRO` = `280,000` (`58.33%`), `NORTE` = `130,000` (`27.08%`), `SUR` = `70,000` (`14.58%`).
   - La suma de `% of Total Revenue` en la fila total es `100.00%` y la diferencia entre DAX y SQL es `0` (o tolerancia de redondeo de 2 decimales).

---

## 💡 Restricciones y Entrega
- Prohibido usar columnas calculadas para ratios o el operador `/` sin `DIVIDE`.
- Solo puedes usar sintaxis DAX/SQL enseñada en los Capítulos 00–02.
- **Entregables:** `.pbix` actualizado + `my_measures.dax` + `my_reconciliation.sql` + captura de reconciliación.
