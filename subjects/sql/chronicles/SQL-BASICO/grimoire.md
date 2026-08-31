# 📓 Grimoire — SQL-BASICO

Este documento es tu registro académico. Después de leer cada capítulo en `lore/` y completar su laboratorio en `quests/`, debes documentar tu asimilación aquí utilizando la **Técnica Feynman**.

> **⚠️ Regla del DM:** El DoJo Agent (Dungeon Master) auditará este documento (`/scry`). Si detecta que estás copiando y pegando, o que no comprendes el concepto central, **denegará tu acceso al Rite**.

---

## Capítulo 00: Hello, SQL — Introduction to Databases & SQLite
**Fecha de finalización:** [2026-08-24]
**Métricas:**
- Tiempo de lectura: 8min
- Tiempo en ejercicios: 5min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1
- ¿Verifiqué la instalación de `sqlite3` en macOS?: Sí

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué diferencia a SQL (lenguaje declarativo) de un lenguaje como Python (imperativo) al momento de pedir datos?
> La diferencia es que SQL calcula internamente la mejor ruta para llevar a cabo la operacion de pedir datos,  en cambio en Python y lenguajes similares, se debe ser claro en la ruta que se debe seguir para poder obtener dichos datos.

2. ¿Por qué es fundamental definir tipos de datos explícitos en las columnas de una tabla relacional?
> Esta es una medida de seguridad que se debe usar para evitar cometer errores a la hora de ingresar datos a las columnas. Cada columna esta descrita con su tipo de dato preciso y debe coincidir con la entrada que se le de, si no es asi SQL indicara el error y no dejara ingresar el dato.

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 01: DDL & Relational Modeling
**Fecha de finalización:** 2026-08-31
**Métricas:**
- Tiempo de lectura: 7min
- Tiempo en ejercicios: 5min
- Veces que recurrí al Tutor/DM: 3
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué es una Foreign Key (FK) y qué problema concreto de integridad resuelve en una base de datos?
> Es la referencia que apunta a un identificador unico de otra tabla. Esta permite generar conexiones con otras tablas de manera que no existan datos acumulados en una sola celda separados por comas, y a la vez exista un unico registro especifico en cada celda que no exista con anterioridad en una tabla principal o padre. 

2. ¿Cuándo se necesita una tabla intermedia (relación N:M) y por qué no se pueden conectar dos tablas directamente en ese escenario?
> Porque se busca no juntar en una sola celda varios registros separados por coma. Se busca separar registros de manera clara, por esto se requiere una tabla intermedia que haga la conexion de las dos tablas principales. 

**Friction Log (Opcional):**
> No se habia entendido el uso de ON DELETE CASCADE, el DM dio la claridad para este codigo. 

---

## Capítulo 02: Filtering & Sorting — WHERE, ORDER BY & CRUD
**Fecha de finalización:** 2026-08-31
**Métricas:**
- Tiempo de lectura: 5min
- Tiempo en ejercicios: 15min
- Veces que recurrí al Tutor/DM: 3 (Objetivo: ≤ 2)
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué ejecutar `UPDATE` o `DELETE` sin una cláusula `WHERE` es una de las fallas más graves en ingeniería de datos?
> 	Porque va a modificar o eliminar toda la fila entera, no modificaria un registro especifico, seria una falta grave ante toda la base de datos

2. Explica la diferencia conceptual entre `NULL`, un número `0` y una cadena vacía `""` en SQL.
> NULL es ausencia de dato, diferente a 0 que ya es un dato y un numero (que puede significar vacio o ausencia), y diferente a una cadena "" que tambien es un dato, una cadena vacia, pero estos dos ultimos representan ya un dato o una entrada. NULL  no hay dato, no hay nada, ni cadena, ni numero, ni texto, nada!

**Friction Log (Opcional):**
> Duda especifica por el ; y WHERE. 

---

## Capítulo 03: Scalar Functions, CASE WHEN & Data Types
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. ¿En qué escenarios usarías `CASE WHEN` dentro de una consulta `SELECT` en lugar de filtrar filas con `WHERE`?
> [Tu respuesta aquí]

2. ¿Qué problema resuelve la función `COALESCE()` al manipular datos sucios o incompletos provenientes de un ETL?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 04: JOINs & Table Relationships
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. Explica con tus propias palabras la diferencia de resultado entre `INNER JOIN` y `LEFT JOIN`.
> [Tu respuesta aquí]

2. ¿Qué es un producto cartesiano (`CROSS JOIN`) accidental y por qué ocurre cuando se omite la condición `ON`?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 05: Aggregations & Grouping
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué la regla del `GROUP BY` exige que toda columna no agregada en el `SELECT` esté presente en el `GROUP BY`?
> [Tu respuesta aquí]

2. ¿Cuál es la diferencia fundamental entre filtrar con `WHERE` y filtrar con `HAVING`?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 06: Subqueries & Common Table Expressions (CTEs)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Cuál es la ventaja de legibilidad y mantenimiento de usar una CTE (`WITH ... AS`) frente a múltiples subqueries anidadas?
> [Tu respuesta aquí]

2. ¿Qué es una subquery correlacionada y por qué suele ser computacionalmente más costosa que una subquery independiente?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 07: Window Functions — Analytics & Deduplication
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué problema analítico resuelven las Window Functions que un `GROUP BY` tradicional es incapaz de resolver?
> [Tu respuesta aquí]

2. Describe paso a paso cómo usarías `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)` para eliminar registros duplicados en un dataset de staging.
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 08: Set Operations & ETL Patterns
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Cuál es la diferencia técnica entre `UNION` y `UNION ALL`, y por qué `UNION ALL` es más eficiente cuando sabes que no hay duplicados?
> [Tu respuesta aquí]

2. ¿Por qué el patrón `INSERT INTO ... SELECT` es la piedra angular de las transformaciones relacionales en arquitectura ELT?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 09: Views, Indexes & Transactions (ACID)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [min]
- Tiempo en ejercicios: [min]
- Veces que recurrí al Tutor/DM: [N] (Objetivo: ≤ 2)
- Fricción (1-10): [N]

**Feynman Synthesis (Tus propias palabras):**
1. Explica los principios ACID de una transacción usando un ejemplo real de transferencia de fondos o reserva de inventario.
> [Tu respuesta aquí]

2. ¿Qué ocurre internamente cuando creas un índice en una columna y por qué acelerar lecturas puede ralentizar escrituras (`INSERT`/`UPDATE`)?
> [Tu respuesta aquí]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]
