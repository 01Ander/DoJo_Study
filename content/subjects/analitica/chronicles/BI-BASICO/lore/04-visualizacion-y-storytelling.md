# Capítulo 04: Visualización Ejecutiva y Storytelling de Negocio

En **Tostadora El Roble**, puedes tener un modelo estrella impecable y medidas DAX exactas al centavo, pero si entregas una pantalla saturada con 14 gráficos de torta en 3D sin título claro ni conclusión, la gerencia cerrará el reporte en diez segundos. La **Visualización Ejecutiva y el Storytelling de Negocio** convierten métricas aisladas en una narrativa clara de 1 página que responde qué está pasando, por qué importa y qué acción tomar.

---

## 1. Selección de Visuales según la Pregunta de Negocio (Qué y Por qué)

**Qué es:** Elegir el tipo de gráfico correcto según la relación analítica que quieres mostrar, en lugar de decorar el lienzo por estética.

| Pregunta de Negocio | Visual Recomendado | Qué Evitar |
|---|---|---|
| ¿Cómo evolucionó el indicador en el tiempo? | Gráfico de líneas (*Line chart*) | Gráficos de torta o barras horizontales desordenadas |
| ¿Qué categoría o sucursal aporta más? | Barras horizontales ordenadas (*Clustered bar chart*) | Gráficos de torta con más de 3 categorías |
| ¿Cuál es el valor actual y su variación? | Tarjeta KPI (*Card / New card visual*) | Tablas gigantes para un solo número |
| ¿Cuál es el detalle exacto auditable? | Matriz o tabla limpia con formato condicional | Gráficos circulares múltiples |

**Por qué importa:** El ojo humano compara longitudes sobre un eje común (barras y líneas) con mucha mayor precisión que ángulos o áreas (tortas/anillos). Elegir el visual correcto reduce el esfuerzo cognitivo del decisor.

> **Analogías (*Tostadora El Roble*):**
> 1. **La carta del café vs. la bodega entera:** Cuando un cliente entra a *Tostadora El Roble*, no le entregas el inventario completo de 400 insumos; le das una carta de 1 página ordenada por secciones (Espresso, Filtrados, Bolsas) con los precios claros. Un dashboard de 1 página sigue exactamente la misma regla.
> 2. **El tablero de control de la tostadora:** El maestro tostador solo mira 3 relojes críticos durante el tueste (temperatura del tambor, tiempo y flujo de aire), no 25 sensores secundarios. Si todo grita al mismo tiempo, nada es prioritario.

---

## 2. Jerarquía Visual en Dashboard de 1 Página y 5 Métricas (Qué y Por qué)

**Qué es:** Organizar el lienzo siguiendo el patrón natural de lectura en **Z** (de arriba a abajo, de izquierda a derecha):
1. **Fila superior (Contexto y KPIs):** Título de negocio + **5 métricas clave** en tarjetas KPI (por ejemplo: `Total Revenue`, `Total Orders`, `Avg Ticket`, `YoY %`, `YTD Revenue`).
2. **Fila central (Tendencia y Comparación):** 1 gráfico de tendencia temporal (`Line chart`) + 1 gráfico de comparación por dimensión (`Clustered bar chart` ordenado de mayor a menor).
3. **Fila inferior (Detalle o Mix):** 1 tabla resumen limpia o descomposición porcentual (`% of Total Revenue`).

**Por qué importa:** Limitar el tablero a **1 página y 5 métricas principales** obliga a priorizar lo que mueve la aguja del negocio y evita la "parálisis por análisis".

---

## 3. Segmentadores (*Slicers*) (Qué y Por qué)

**Qué es:** Controles visuales interactivos (*Slicers*) conectados a las columnas de tus dimensiones (`dim_date[year]`, `dim_branch[city]`, `dim_product[category]`) que permiten al usuario filtrar todo el dashboard con un clic.

**Por qué importa:** Sin segmentadores, un dashboard es una foto estática en PDF. Los *slicers* permiten que el gerente explore hipótesis en vivo durante una reunión ("¿qué pasa si miramos solo Bogotá en 2026?"), aprovechando las relaciones `1:N` unidireccionales construidas en el Capítulo 01.

**Cómo configurarlos:**
- Colócalos en una barra superior compacta o en un panel lateral izquierdo limpio (máximo 3–4 segmentadores por página).
- Usa **siempre** columnas de dimensiones (`dim_branch[city]`), nunca columnas de `fact_coffee_sales`.

---

## 4. Tres Hallazgos Cuantificados y Una Recomendación Accionable (Qué y Por qué)

**Qué es:**
- **Hallazgo cuantificado:** Una afirmación respaldada por cifras concretas, comparación y contexto temporal (no "las ventas subieron", sino *"Las ventas de marzo 2026 crecieron +14.2% YoY (\$18.5M COP adicionales), impulsadas en un 68% por la sucursal Chapinero"*).
- **Recomendación accionable:** Una decisión concreta con responsable o palanca clara, derivada de los 3 hallazgos (por ejemplo: *"Replicar el paquete de suscripción de café en grano de Chapinero en las 2 sucursales con menor ticket promedio durante Q2 para capturar +\$9M COP mensuales estimados"*).

**Por qué importa:** Un analista junior muestra gráficos; un analista listo para contratar entrega **3 hallazgos cuantificados y 1 recomendación accionable** que justifican una decisión de negocio.

---

## 5. Guion de Defensa Oral de 5 Minutos (Cómo)

**Qué es:** Una estructura cronometrada de 5 minutos para presentar tu dashboard en una entrevista o revisión gerencial:
1. **Minuto 0–1 (Problema y Grano):** Qué pregunta de negocio responde el tablero y cuál es el grano de la tabla de hechos.
2. **Minuto 1–2 (Modelo y Reconciliación):** Por qué elegiste Star Schema `1:N` unidireccional, tabla de fechas marcada y cómo reconciliaste las medidas DAX contra SQL.
3. **Minuto 2–4 (3 Hallazgos Cuantificados):** Recorrido guiado por los gráficos usando los segmentadores (*slicers*) para demostrar cada cifra.
4. **Minuto 4–5 (1 Recomendación y Límites):** Qué acción recomiendas y qué límite tienen los datos actuales.

### El Camino Frágil vs. El Camino Robusto

**🎯 Objetivo de Negocio:** Presentar el desempeño comercial 2026 de *Tostadora El Roble* en 1 página clara y auditable.

```text
FRAGILE LAYOUT:
- 3 Pie Charts with 12 slices each
- 14 unaligned cards with no YoY comparison
- Slicer pointing to fact_coffee_sales[branch_id]
- Title: "Dashboard Ventas" (No business question, no findings)
```

```text
ROBUST 1-PAGE EXECUTIVE LAYOUT (Tostadora El Roble):
+-----------------------------------------------------------------------+
| TITLE: Tostadora El Roble — 2026 Revenue & Branch Performance         |
| SLICERS: [Year: 2026 v]  [City: All v]  [Product Category: All v]     |
+------------+------------+------------+------------+-------------------+
| Revenue    | Orders     | Avg Ticket | YoY %      | YTD Revenue       |
| $482.0M    | 12,450     | $38,715    | +14.2%     | $482.0M           |
+------------+------------+------------+------------+-------------------+
| LINE CHART: Monthly Revenue & YoY%   | BAR CHART: Revenue by Branch   |
| (dim_date[year_month] -> Revenue)    | (Chapinero, Usaquén, Laureles) |
+--------------------------------------+--------------------------------+
| EXECUTIVE TAKEAWAYS (3 Quantified Findings + 1 Actionable Rec.)       |
| 1. Chapinero drives 42% of total revenue (+18.4% YoY).                |
| 2. Whole-bean bags grew +22% MoM after Q1 subscription launch.        |
| 3. Laureles avg ticket is 19% below chain average ($31.2k vs $38.7k). |
| -> REC: Roll out bean subscription bundle in Laureles for Q2.         |
+-----------------------------------------------------------------------+
```

También puedes crear una medida DAX dinámica para mostrar el subtítulo del filtro activo en la cabecera del reporte:

```dax
-- Dynamic report subtitle reflecting active slicer selection
Active Filter Subtitle =
"Selected Year: " & SELECTEDVALUE(dim_date[year], "All Years") &
" | City: " & SELECTEDVALUE(dim_branch[city], "All Cities")
```

- `SELECTEDVALUE(columna, valor_alternativo)`: Devuelve el único valor seleccionado en un *slicer*; si hay múltiples valores o ninguno seleccionado, devuelve `valor_alternativo` (`"All Years"`).
- `&`: Operador de concatenación de texto en DAX.

---

## 6. Conexión con Testing y Validación (Regla Crítica)

Antes de dar por terminado un dashboard, valida su usabilidad y exactitud con el ciclo **AAA**:

1. **Arrange (Preparar prueba de interacción):** Selecciona un año (`2026`) y una ciudad (`Bogotá`) en los *slicers*.
2. **Act (Ejecutar interacción):** Observa todas las tarjetas KPI, gráficos y el subtítulo dinámico.
3. **Assert (Verificar):**
   - Los 5 KPIs, ambos gráficos y el subtítulo se actualizan coherentemente sin mostrar errores ni `(Blank)` inesperados.
   - La suma de los valores de las barras de sucursales filtradas coincide exactamente con la tarjeta `Total Revenue`.
   - Tu guion de 5 minutos cubre los 4 bloques (grano/pregunta, modelo/DAX, 3 hallazgos cuantificados, 1 recomendación) sin leer código en pantalla.

---

## 7. Mapa de Ejercicios

Dirígete a `quests/04-visualizacion-y-storytelling/` y completa la práctica deliberada **BI-04**:

```text
quests/04-visualizacion-y-storytelling/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```
