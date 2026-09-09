# Journal de Desarrollo — Rite: Public Library Management System

**Operador:** Andersson
**Chronicle:** SQL-BASICO
**Inicio del Rite:** 2026-08-09
**Estado:** 🔵 En Progreso 

---

## 📓 Bitácora de Registro por Fases

### Fase 1: Schema Design & Modeling
- **Fecha de ejecución:** 2026-09-08
- **Notas de diseño:** (Decisiones sobre tipos de datos, llaves primarias autoincrementales, constraints UNIQUE y CHECK) Se selecciona o se recuerda que las fechas se toman como TEXT para el manejo de ellas con ISO. Se decide manejar el isbn como integer, para facilidad de uso de numeros aleatorios, en dado caso, aunque se entiende que dicho codigo numerico en algunos caso tiene separacion por guiones. 
- **Trade-offs / Desafíos:** Se comprende con uso del Pair Programming, que PRAGMA foreign_keys = 0N; debe ejecutarse en cada interaccion del codigo, para que funcione dicha regla, no como un comando al inicio del archivo que se ejecuta una sola vez y mantiene persistencia. 
- **Comandos de verificación ejecutados:**
```sql
PRAGMA foreign_keys = ON;

INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date)

VALUES (5, 10, '2026-08-01 09:00', '2026-08-30 09:00', '2026-08-30 09:00');
```


---

### Fase 2: Data Ingestion & Sanitization
- **Fecha de ejecución:** 2026-09-08
- **Notas de diseño:** (Uso de funciones escalares de texto, CASE WHEN y formateo de fechas ISO) Se hace uso de JULIANDAY para poder normalizar los dias y hacer el calculo dentro del mismo CASE WHEN y realizar la categoria que se exige.
- **Trade-offs / Desafíos:** El calculo de la fecha se debe realizar dentro del CASE ya este no puede hacer uso de etiquetas directas de la seleccion. 

---

### Fase 3: Core Analytics
- **Fecha de ejecución:** 2026-09-08
- **Notas de diseño:** (Estrategia de JOINs multi-tabla, agregaciones y diferencia de filtrado entre WHERE y HAVING) INNER JOIN para poder hacer los puentes con la tabla intermedia y obtener los datos requeridos dentro de la seleccion. 
- **Trade-offs / Desafíos:** Se 'aclara' que se debe tener en cuenta el orden de ejecucion del codigo SQL, no es secuencial segun se escriba, si no hay un orden especifico dependiendo de los comandos utilizados, por ello, para el reporte dos el 'COUNT(x)' es viable y mas legible por si solo.  

---

### Fase 4: Advanced Engineering & Windowing
- **Fecha de ejecución:** 2026-09-09
- **Notas de diseño:** (Implementación de CTEs con `WITH`, deduplicación con `ROW_NUMBER`, uso de `LAG` y `DENSE_RANK`) Se hace implementacion de CTE con WITH para el reporte 3. SE hace agrupacion de tablas para poder obtener los datos requeridos para el reporte 4, uso de count para la suma de repeticiones sencilla de loans y count para la diferencia de loans entre libros.
- **Trade-offs / Desafíos:** Se particiona los pasos que solicitaba el report 4 de manera que se pudo observar como se iban seleccionado y particionando los datos. Se interioriza mucho mas el uso de JOIN. A la vez se entiende que siempre que exista un group by, toda columna mostrada en el select debe estar en el group o en una funcion de agregacion. 

---

### Fase 5: Production & Optimization
- **Fecha de ejecución:** 2026-09-09
- **Notas de diseño:** (Creación de vistas, análisis del plan de ejecución con `EXPLAIN QUERY PLAN`, índices B-Tree y transacciones ACID `BEGIN/COMMIT/ROLLBACK`) 
- **Trade-offs / Desafíos:** Fallos de diseno dentro del rite, donde se solicito requerimientos que no se vieron dentro del LORE. Por demas, se hace uso de CREATE VIEW con uso de JOIIN WHERE Y GROUP para crear una vista mas compleja como la solicitada. 

---

---

## Nota de la Bruja — Resumen de Pair Programming (08-09 Sep 2026)

*Sesión completa de acompañamiento para desbloquear y ejecutar el Rite completo de SQL-BASICO en una sola jornada de dos días. A continuación, los puntos clave tratados:*

**Fase 1 — Schema:** Se revisó el diseño de la tabla intermedia `book_authors`. El operador tenía un campo `title` extra que sobraba — una tabla N:M solo debe contener las dos FKs mas su PK. Tambien se corrigio el error de `PRAGMA foreign_key = ON` (singular) vs `PRAGMA foreign_keys = ON` (plural), lo que impedía que las FK funcionaran. Se comprendió que el PRAGMA debe ejecutarse en cada conexión, no es persistente.

**Fase 2 — Data Ingestion:** Se generó un CSV con datos semilla (5 categorías, 8 autores, 12 libros, 10 miembros, 15 préstamos). Se implementó la consulta de sanitización con `UPPER(TRIM())`, `LOWER()`, `JULIANDAY()` y `CASE WHEN`. Se entendió la limitación de que los alias de columna no pueden usarse dentro del mismo SELECT.

**Fase 3 — Core Analytics:** Reporte 1 con JOIN multi-tabla usando la cadena `loans → books → book_authors → authors` para llegar al nombre del autor. Se agregó filtro `WHERE return_date IS NULL` para préstamos activos. Reporte 2 con `COUNT(*)`, `AVG`, `GROUP BY` y `HAVING > 2`. Se aclaró la diferencia entre `COUNT(*)` (cuenta filas del grupo) y `COUNT(columna)` (cuenta no-nulos), y se discutió que la convención industrial favorece `COUNT(*)` para contar transacciones.

**Fase 4 — Advanced Engineering:** Reporte 3: CTE con `ROW_NUMBER() PARTITION BY book_id, member_id, loan_date ORDER BY id DESC` para deduplicación. Reporte 4: `DENSE_RANK` particionado por categoría y `LAG` sobre el conteo de préstamos (no sobre el rango). Se corrigió un JOIN innecesario a `book_authors` que inflaba el COUNT. Se profundizó en la regla de GROUP BY: toda columna del SELECT debe estar en GROUP BY o dentro de una función de agregación.

**Fase 5 — Production:** Vista `v_active_fines` con `SUM(COALESCE())` y filtro `HAVING` vs `WHERE`. Índice en `loans(member_id)` con verificación via `EXPLAIN QUERY PLAN`. Transacción ACID con `BEGIN/COMMIT`. Se identificó que la validación de "máximo 3 préstamos activos" requería `TRIGGER + RAISE` (fuera del alcance de SQL-BASICO), por lo que el DM ajustó el requerimiento al patrón básico visto en lore.

**Conceptos clave reforzados:** Orden de ejecucion SQL (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY), normalización de tablas N:M, dependencia funcional, diferencia entre filtrar antes (WHERE) y después (HAVING) de agrupar, y que los alias de columna no existen en tiempo de ejecución del SELECT.
