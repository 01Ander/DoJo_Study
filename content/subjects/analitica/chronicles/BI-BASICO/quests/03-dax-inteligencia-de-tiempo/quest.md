# Quest BI-03: DAX II — Inteligencia de Tiempo (Time Intelligence)

> **Objetivo:** Implementar 3 medidas de inteligencia de tiempo (`YoY %`, `YTD Revenue`, `MoM %`) sobre `dim_date` marcada y reconciliarlas contra SQL.
> **Requisitos Previos:** Lore de los Capítulos 00–03 y `BI-02` completada.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
**Librería El Faro** necesita medir su crecimiento interanual (`YoY %`), su acumulado anual (`YTD Revenue`) y su variación mensual (`MoM %`) para evaluar si el desempeño de 2026 supera al de 2025.

---

## 📋 Instrucciones

1. **Implementar las 3 medidas de Time Intelligence en `my_time_measures.dax` y en tu `.pbix`:**
   - `YoY %`: usa `VAR ... RETURN`, `CALCULATE`, `SAMEPERIODLASTYEAR(dim_date[Date])`, `NOT ISBLANK(...)`, `DIVIDE` y `BLANK()` para el primer año sin historia previa.
   - `YTD Revenue`: usa `TOTALYTD([Total Revenue], dim_date[Date])`.
   - `MoM %`: usa `VAR ... RETURN`, `CALCULATE`, `DATEADD(dim_date[Date], -1, MONTH)`, `NOT ISBLANK(...)`, `DIVIDE` y `BLANK()`.
2. **Reconciliar contra SQL:**
   - Reutiliza las tablas `fact_book_sales`, `dim_store` y `dim_date` que cargaste en `BI-02` (ver `../02-dax-medidas-y-contexto/reference/faro_schema.sql`).
   - Escribe en `my_time_reconciliation.sql` una consulta SQL usando `CTE`, `SUM(...) OVER (PARTITION BY cur.year ORDER BY cur.month_number)` para `ytd_revenue`, y `LEFT JOIN` al mes calendario anterior por aritmética entera (`year * 12 + month_number - 1`) y al año anterior (`cur.year - 1`) para calcular `mom_pct` y `yoy_pct` sin depender de filas contiguas en `LAG`.

---

## 🧪 Validación (Andamiaje Nivel 4 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Crea una matriz o tabla visual con `dim_date[year]` y `dim_date[month_number]`, agregando `[Total Revenue]`, `[YTD Revenue]`, `[MoM %]` y `[YoY %]`.
2. **Act:** Ejecuta tu consulta de `my_time_reconciliation.sql`.
3. **Assert:**
   - En `2025`, `YoY %` aparece en blanco (`BLANK()`) porque no existe `2024`.
   - En `2026-01`, `MoM %` aparece en blanco (`BLANK()`) porque no hubo ventas en `2025-12`.
   - En `2026-03` (marzo 2026: `250,000`), `YTD Revenue` acumula `480,000` (`100,000 + 130,000 + 250,000`), `MoM %` es `+92.31%` y `YoY %` es `+108.33%` (frente a `120,000` en marzo 2025).
   - Todos los valores coinciden hasta el segundo decimal con SQL.

---

## 💡 Restricciones y Entrega
- Prohibido usar `fact_book_sales[sale_date]` dentro de `SAMEPERIODLASTYEAR`, `TOTALYTD` o `DATEADD`.
- Solo puedes usar sintaxis DAX/SQL enseñada en los Capítulos 00–03.
- **Entregables:** `.pbix` actualizado + `my_time_measures.dax` + `my_time_reconciliation.sql`.
