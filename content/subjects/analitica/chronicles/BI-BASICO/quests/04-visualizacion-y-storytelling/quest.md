# Quest BI-04: Visualización Ejecutiva y Storytelling

> **Objetivo:** Diseñar un dashboard ejecutivo de 1 página con jerarquía en Z, 5 métricas clave, segmentadores (*slicers*), 3 hallazgos cuantificados, 1 recomendación accionable y guion de defensa oral de 5 minutos.
> **Requisitos Previos:** Lore de los Capítulos 00–04 y `BI-03` completada.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
La dirección de **Librería El Faro** necesita un tablero ejecutivo de 1 página para la revisión trimestral Q1 2026 que responda en menos de 30 segundos cuánto se vendió, qué tienda lidera el crecimiento y qué acción comercial tomar en Q2.

---

## 📋 Instrucciones

1. **Diseñar el dashboard de 1 página en tu `.pbix`:**
   - **Cabecera:** Título de negocio + medida DAX dinámica `Active Filter Subtitle` usando `SELECTEDVALUE` y `&` (sobre `dim_date[year]` y `dim_store[city]`).
   - **Segmentadores (*slicers*):** Agrega 2 *slicers* usando columnas de dimensiones (`dim_date[year]` y `dim_store[city]`).
   - **5 métricas clave (tarjetas KPI):** `Total Revenue`, `Total Orders`, `Avg Ticket`, `YoY %`, `YTD Revenue`.
   - **Visuales de análisis:**
     - 1 gráfico de líneas (`Line chart`) con `dim_date[year_month]` vs `[Total Revenue]`.
     - 1 gráfico de barras horizontales (`Clustered bar chart`) ordenado de mayor a menor con `dim_store[store_name]` vs `[Total Revenue]` (o `[% of Total Revenue]`).
2. **Redactar el storytelling y guion de defensa (`my_storytelling.md`):**
   - Escribe **3 hallazgos cuantificados** (con cifra exacta y comparación) basados en los datos de *Librería El Faro*.
   - Formula **1 recomendación accionable** derivada de esos hallazgos.
   - Redacta tu **guion de defensa oral de 5 minutos** cubriendo los 4 bloques: (1) problema y grano, (2) modelo `1:N` y reconciliación SQL, (3) 3 hallazgos cuantificados, (4) 1 recomendación y límites.

---

## 🧪 Validación (Andamiaje Nivel 5 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Selecciona `year = 2026` y `city = Bogotá` en los *slicers*.
2. **Act:** Observa las 5 tarjetas KPI, ambos gráficos y el subtítulo dinámico.
3. **Assert:**
   - El subtítulo muestra `"Selected Year: 2026 | City: Bogotá"`.
   - Todos los KPIs y gráficos se filtran coherentemente (`Total Revenue = 410,000`, `Total Orders = 3`, suma de barras `CENTRO + NORTE = 410,000`).
   - El tablero no usa gráficos de torta ni columnas de llaves técnicas.

---

## 💡 Restricciones y Entrega
- Prohibido usar gráficos de torta o conectar *slicers* a columnas de `fact_book_sales`.
- **Entregables:** `.pbix` actualizado + `my_storytelling.md` + captura del dashboard de 1 página + defensa oral de 5 min.
