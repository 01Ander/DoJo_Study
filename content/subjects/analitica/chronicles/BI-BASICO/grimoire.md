# Grimoire — `BI-BASICO` (Bitácora Feynman)

> **Propósito:** El aprendizaje pasivo no existe. Después de completar cada capítulo del `lore/` y su laboratorio en `quests/`, explica cada concepto con tus propias palabras (Técnica Feynman), sin copiar literalmente el texto del lore.
>
> **Regla:** Solo cuando el Dungeon Master (`/scry`) certifique que este documento refleja comprensión genuina, se autoriza el acceso al `rite/`.

---

## Métricas de Estudio del Operador

| Capítulo / Quest | Fecha | Tiempo invertido (min) | ¿Superó 180 min? (Sí/No) | Estado |
|---|---|---|---|---|
| Cap 00 / BI-00 — Power Query (M) | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |
| Cap 01 / BI-01 — Modelo Semántico en Estrella | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |
| Cap 02 / BI-02 — DAX I (Medidas y Contexto) | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |
| Cap 03 / BI-03 — DAX II (Time Intelligence) | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |
| Cap 04 / BI-04 — Visualización y Storytelling | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |
| Cap 05 / BI-05 — Publicación, Refresh y RLS | _YYYY-MM-DD_ | _0_ | _No_ | _Pendiente_ |

---

## Preguntas Feynman por Capítulo

### Capítulo 00: Power Query (M) e Ingesta Reproducible

1. **¿Por qué es un antipatrón abrir un archivo CSV en una hoja de cálculo para borrar filas anuladas o corregir espacios manualmente antes de cargarlo a Power BI, y cómo resuelve esto el bloque `let ... in` junto con la exportación de `query.pq`?**
   > _Tu respuesta aquí:_

2. **En lenguaje M, explica qué hace `Table.SelectRows` combinado con `each` y `<>`, y por qué debemos aplicar `Table.TransformColumnTypes` de forma explícita en lugar de dejar que Power BI adivine los tipos de columna.**
   > _Tu respuesta aquí:_

---

### Capítulo 01: Modelo Semántico en Estrella (Star Schema)

1. **¿Por qué un Modelo en Estrella (*Star Schema*) supera a una Tabla Plana en compresión y exactitud de conteos, y qué riesgo introduce activar relaciones con dirección de filtro bidireccional (*Both*) por defecto?**
   > _Tu respuesta aquí:_

2. **¿Cómo se construye y configura correctamente una `dim_date` en Power BI (`CALENDAR`, `ADDCOLUMNS`, relación `1:N` y *Mark as date table*), y por qué es obligatorio ocultar las llaves técnicas de la tabla de hechos en la vista de reporte?**
   > _Tu respuesta aquí:_

---

### Capítulo 02: DAX I — Medidas, Columnas Calculadas y Contexto de Filtro

1. **¿Cuál es la diferencia fundamental entre contexto de fila y contexto de filtro, y por qué debes usar una medida con `DIVIDE` o `SUMX` en lugar de una columna calculada para calcular ratios como el ticket promedio?**
   > _Tu respuesta aquí:_

2. **Explica cómo interactúan `CALCULATE` y `ALL` para calcular el porcentaje de participación sobre el total (`% of Total`), y por qué el resultado debe reconciliarse contra una consulta SQL equivalente.**
   > _Tu respuesta aquí:_

---

### Capítulo 03: DAX II — Inteligencia de Tiempo (Time Intelligence)

1. **¿Cuáles son los cuatro requisitos que debe cumplir `dim_date` para que funciones como `SAMEPERIODLASTYEAR`, `TOTALYTD` y `DATEADD` no devuelvan resultados en blanco o erróneos?**
   > _Tu respuesta aquí:_

2. **Explica cómo funcionan `VAR ... RETURN` junto con `NOT ISBLANK(...)` en las medidas `YoY %` y `MoM %`, y por qué en el primer periodo histórico es preferible devolver `BLANK()` en lugar de `-100%` o `0`.**
   > _Tu respuesta aquí:_

---

### Capítulo 04: Visualización Ejecutiva y Storytelling de Negocio

1. **¿Por qué se prefiere un diseño de 1 página con jerarquía en Z (5 métricas clave, gráficos de líneas/barras ordenadas y *slicers* desde dimensiones) frente a múltiples gráficos de torta, y cómo evita `SELECTEDVALUE` que el subtítulo dinámico muestre errores cuando hay varios filtros?**
   > _Tu respuesta aquí:_

2. **¿Qué diferencia a un hallazgo cuantificado + una recomendación accionable de una simple descripción de un gráfico, y qué cuatro bloques debe cubrir tu guion de defensa oral de 5 minutos?**
   > _Tu respuesta aquí:_

---

### Capítulo 05: Publicación, Refresh y Seguridad a Nivel de Fila (RLS)

1. **¿Por qué Power BI Service en la nube no puede refrescar directamente un PostgreSQL en `localhost` sin un *On-Premises Data Gateway*, y qué alternativas operativas tienes cuando trabajas sin gateway permanente?**
   > _Tu respuesta aquí:_

2. **¿Cómo funciona un rol de seguridad a nivel de fila (**RLS** estático) definido sobre una tabla de dimensión (`dim_branch`) a través de una relación `1:N`, y cómo verificas con el ciclo AAA y *View as* que el aislamiento de datos funciona correctamente?**
   > _Tu respuesta aquí:_

---

## Friction Log (Registro de Fricciones)

| Fecha | Capítulo / Quest | Problema o fricción encontrada | Cómo se resolvió | Tiempo perdido (min) |
|---|---|---|---|---|
| _YYYY-MM-DD_ | _Ej. BI-01_ | _Descripción breve_ | _Solución aplicada_ | _0_ |

---

**Auditoría del DM:** [Pendiente]
