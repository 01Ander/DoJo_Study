# Bitácora Táctica de Remediación — `03-sql-basico`

> **Documento Rector:** [roadmap.md](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/remediacion/roadmap.md)  
> **Directorio Canónico:** [`content/subjects/sql/chronicles/SQL-BASICO/`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/)  
> **Motor de Base de Datos:** `sqlite3` CLI  
> **Estado:** Carril B Completado (5/5) / Carril A En Espera del Operador

---

## 1. Carril B: Higiene del Material (Ejecución de Arquitecto / Antigravity)

### SQL-001: Sintaxis Truncada en `quests/03-functions/case-when.sql`
- **Diagnóstico:** Expresión `CASE WHEN` incompleta, truncada abruptamente en `WHEN projects_completed >= 10 THEN`.
- **Acción:** Completada la sentencia según la solución del ejercicio [02-case-when-practice.md](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/02-case-when-practice.md).
- **Sonda Final (Runner Agnóstico de SQL):**
  ```bash
  python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/case-when.sql
  ```
  *Criterio:* `✅ PASS` con `exit code 0`.

### SQL-002: Terminadores de Sentencia en `quests/06-subqueries/01.sql`
- **Diagnóstico:** Falta de punto y coma `;` al final de la primera consulta `SELECT` (L20), concatenando sintácticamente la segunda consulta y detonando `Parse error near "SELECT"`.
- **Acción:** Agregado el terminador `;` al final de la consulta independiente.
- **Sonda Final (Runner Agnóstico de SQL):**
  ```bash
  python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/06-subqueries/01.sql
  ```
  *Criterio:* `✅ PASS` con `exit code 0`.

### SQL-003: Idempotencia en `rite/rite.sql` (`DROP TABLE loans`)
- **Diagnóstico:** Al final de `rite.sql` existía un bloque de validación experimental residual que ejecutaba `DROP TABLE IF EXISTS loans;`, destruyendo la tabla principal y provocando que consultas a la vista `v_active_fines` fallaran con `Parse error: no such table: main.loans`.
- **Acción:** Removido el bloque destructivo residual al final de `rite.sql`.
- **Sonda Final:**
  ```bash
  rm -f test_check.db && sqlite3 test_check.db < content/subjects/sql/chronicles/SQL-BASICO/rite/rite.sql && sqlite3 test_check.db "SELECT COUNT(*) FROM v_active_fines;" && rm -f test_check.db
  ```
  *Criterio:* Devuelve `COUNT(*): 3` con `exit code 0`.

### SQL-007: Reconciliación Inversa en `chronicle.md`
- **Diagnóstico:** El temario omitía herramientas indispensables de producción explicadas en el curso: `PRAGMA foreign_keys`, `CTAS` (`CREATE TABLE AS SELECT`) y `DENSE_RANK`.
- **Acción:** Declaradas formalmente en los Capítulos 01, 07 y 08 de [chronicle.md](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/chronicle.md).
- **Sonda Final:**
  ```bash
  grep -E "foreign_keys|CTAS|DENSE_RANK" content/subjects/sql/chronicles/SQL-BASICO/chronicle.md
  ```
  *Criterio:* Las tres herramientas presentes con `exit code 0`.

### SQL-004: Mito 2 — Soporte de `RIGHT/FULL OUTER JOIN` en SQLite
- **Archivo:** [`lore/04-joins-and-relationships.md:L216-L220`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/04-joins-and-relationships.md)
- **Diagnóstico:** El texto afirmaba que SQLite no soporta nativamente `RIGHT JOIN` ni `FULL OUTER JOIN`. Esto es obsoleto: desde SQLite 3.39 (2022) ambas cláusulas están soportadas de forma estándar.
- **Acción:** Corregida la nota teórica en Lore 04 aclarando la evolución del motor.
- **Sonda Final:**
  ```bash
  sqlite3 :memory: "CREATE TABLE a(id INT); CREATE TABLE b(id INT); INSERT INTO a VALUES(1); INSERT INTO b VALUES(2); SELECT * FROM a FULL OUTER JOIN b ON a.id = b.id;"
  ```
  *Criterio:* Ejecución nativa sin emulaciones con `exit code 0`.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

> [!TIP]
> **Metodología de Domain Shifting (Regla 5):** Cada tarea cuenta con su código actual, su anclaje al Lore, su analogía de dominio externo y su sonda de verificación.

---

### SQL-008: Resolución de Cardinalidad en Relaciones N:M (Reporte 1 del Rite)
- **Archivo a modificar:** [`rite/rite.sql:L127-L138`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/rite/rite.sql#L127-L138)
- **Referencia en Lore:** [`lore/01-creating-and-modeling.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/01-creating-and-modeling.md) (Relaciones N:M y tablas intermedias) y [`lore/04-joins-and-relationships.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/04-joins-and-relationships.md) (Multi-table JOINs).
- **Diagnóstico (¿Qué está pasando en tu consulta actual?):**
  En `rite.sql` tienes actualmente:
  ```sql
  SELECT
      b.title AS book_title,
      a.full_name AS author_name,
      m.full_name AS member_name,
      l.loan_date,
      CAST(JULIANDAY('now') - JULIANDAY(l.loan_date) AS INTEGER) AS loan_total_days
  FROM loans AS l
  INNER JOIN books AS b ON l.book_id = b.id
  INNER JOIN book_authors AS ba ON l.book_id = ba.book_id
  INNER JOIN authors AS a ON ba.author_id = a.id
  INNER JOIN members AS m ON l.member_id = m.id
  WHERE l.return_date IS NULL;
  ```
  **El problema de cardinalidad:** En la base de datos hay exactamente **9 préstamos activos** (`loans WHERE return_date IS NULL`). Sin embargo, tu consulta arroja **11 filas**. ¿Por qué? Porque libros como *Good Omens* tienen 2 autores en `book_authors` (Terry Pratchett y Neil Gaiman). Hacer un `INNER JOIN` directo a la tabla intermedia `book_authors` y a `authors` multiplica la fila del préstamo por cada autor asociado.
  **El requisito del Rite:** El requerimiento de la Fase 3 pide mostrar el *«Nombre del Autor principal»*. Debes colapsar la relación N:M a un solo autor por libro (por ejemplo, seleccionando el autor de menor ID con una subconsulta/CTE `MIN(author_id)` o agrupando con `GROUP_CONCAT(a.full_name, ', ')`).
- **Domain Shifting (El Archivo de Casos de la Guardia de Ankh-Morpork):**
  ```sql
  -- Si un arresto involucra un caso con múltiples sospechosos (relación N:M):
  -- Antipatrón: JOIN directo duplica el número de arrestos en el reporte.
  -- Canónico: Seleccionar el sospechoso principal agrupando antes del JOIN:
  WITH caso_sospechoso_principal AS (
      SELECT caso_id, MIN(sospechoso_id) AS principal_id
      FROM caso_sospechosos
      GROUP BY caso_id
  )
  SELECT c.titulo, s.nombre AS sospechoso_principal, a.fecha_arresto
  FROM arrestos a
  JOIN casos c ON a.caso_id = c.id
  JOIN caso_sospechoso_principal csp ON c.id = csp.caso_id
  JOIN sospechosos s ON csp.principal_id = s.id;
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  sqlite3 content/subjects/sql/chronicles/SQL-BASICO/rite/rite.db "SELECT COUNT(*) FROM loans AS l INNER JOIN books AS b ON l.book_id = b.id INNER JOIN book_authors AS ba ON l.book_id = ba.book_id INNER JOIN authors AS a ON ba.author_id = a.id INNER JOIN members AS m ON l.member_id = m.id WHERE l.return_date IS NULL;"
  ```
  *Resultado:* Arroja `11` filas (infladas por co-autoría).
- **Sonda Final (Contrato tras solución del Operador):**
  La consulta del Reporte 1 en `rite.sql` debe devolver exactamente los **9 préstamos activos reales**.

---

### SQL-009: Métricas de Retención Temporal con `COALESCE` (Reporte 2 del Rite)
- **Archivo a modificar:** [`rite/rite.sql:L142-L151`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/rite/rite.sql#L142-L151)
- **Referencia en Lore:** [`lore/03-functions-and-expressions.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/03-functions-and-expressions.md) (`COALESCE`, funciones de fecha `JULIANDAY` y valores `NULL`).
- **Diagnóstico (¿Qué está pasando en tu consulta actual?):**
  En `rite.sql` tienes actualmente:
  ```sql
  SELECT
      c.name AS category_name,
      COUNT(*) AS loans_categories_count,
      ROUND(AVG(CAST(JULIANDAY('now') - JULIANDAY(l.loan_date) AS INTEGER)), 2) AS total_avg_loan_days
  FROM loans AS l
  INNER JOIN books AS b ON l.book_id = b.id
  INNER JOIN categories AS c ON b.category_id = c.id
  GROUP BY c.name
  HAVING COUNT(*) > 2
  ORDER BY loans_categories_count DESC;
  ```
  **La distorsión analítica:** Tu cálculo aplica indiscriminadamente `JULIANDAY('now')` a **todos** los préstamos. Si un libro fue prestado en abril y devuelto en mayo (hace 5 meses), la retención real de ese usuario fue de 30 días. Al calcular `now - loan_date`, estás calculando los días transcurridos desde que se prestó hasta hoy, arrojando promedios distorsionados de 100+ días.  
  Para préstamos devueltos (`return_date IS NOT NULL`), los días de retención son `return_date - loan_date`. Solo para préstamos en curso se usa `now`. Esto se modela limpiamente con:
  `COALESCE(l.return_date, DATE('now')) - l.loan_date`.
- **Domain Shifting (Alquiler de Carruajes de Ankh-Morpork):**
  ```sql
  -- Si el carruaje ya se devolvió, su duración es: fecha_devolucion - fecha_inicio
  -- Si sigue en viaje, su duración hasta hoy es: now - fecha_inicio
  SELECT categoria,
         COUNT(*) AS total_viajes,
         ROUND(AVG(JULIANDAY(COALESCE(fecha_devolucion, DATE('now'))) - JULIANDAY(fecha_inicio)), 2) AS promedio_dias_uso
  FROM alquileres
  GROUP BY categoria;
  ```
- **Sonda Inicial (Fallo actual):**
  La consulta actual produce promedios inflados de `111.33` y `103.0` días.
- **Sonda Final (Contrato tras solución del Operador):**
  La consulta en `rite.sql` debe reflejar la duración real de retención de los préstamos combinando devueltos y activos con `COALESCE`.

---

### SQL-010: Funciones de Ventana y Orden Cronológico (`LAG`)
- **Archivo a modificar:** [`quests/07-windows/07_01.sql:L26-L27`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/07-windows/07_01.sql#L26-L27)
- **Referencia en Lore:** [`lore/07-window-functions.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/07-window-functions.md) (Funciones de desplazamiento `LAG`/`LEAD` y la cláusula `ORDER BY`).
- **Diagnóstico (¿Qué está pasando en tu consulta actual?):**
  En `07_01.sql` tienes actualmente:
  ```sql
  SELECT
      branch_office,
      sale_date,
      revenue AS today_revenue,
      LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY revenue) AS yesterday_sales,
      ROUND(revenue - LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY revenue), 2) AS daily_diff
  FROM daily_revenue;
  ```
  **El error de ventana:** La cláusula dice `ORDER BY revenue`. Al ordenar por monto en lugar de fecha, `LAG` busca la venta de menor valor anterior, no del "día de ayer".  
  Para la 'Sede Centro' (Día 01 = $1000, Día 02 = $1200, Día 03 = $1100), ordenar por revenue sitúa los ingresos como: 1000, 1100, 1200. Por ende, para el Día 03 ($1100), `LAG` devuelve $1000 (del día 01) en lugar de $1200 (del día 02).  
  Para obtener la venta de ayer, el desplazamiento debe ordenarse cronológicamente: `ORDER BY sale_date`.
- **Domain Shifting (Consumo de Pociones en la Taberna):**
  ```sql
  -- Para saber cuántas pintas se vendieron ayer, la ventana DEBE ordenarse por fecha, no por cantidad:
  SELECT fecha,
         pintas_hoy,
         LAG(pintas_hoy, 1) OVER (ORDER BY fecha ASC) AS pintas_ayer
  FROM registro_taberna;
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  sqlite3 :memory: ".read content/subjects/sql/chronicles/SQL-BASICO/quests/07-windows/07_01.sql"
  ```
  *Resultado:* Día `2026-07-03` muestra `yesterday_sales: 1000.0` (del día 01).
- **Sonda Final (Contrato tras solución del Operador):**
  Tras cambiar a `ORDER BY sale_date`, el día `2026-07-03` debe mostrar exactamente `yesterday_sales: 1200.0` (del día 02).

---

### SQL-011: Collation en SQLite y Manejo de Tildes
- **Archivo a modificar:** [`quests/02-filtering/01-crud-operations.md:L43, L53`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/01-crud-operations.md#L41-L55)
- **Referencia en Lore:** [`lore/02-filtering-and-sorting.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/02-filtering-and-sorting.md) (Filtros de texto, igualdad de literales y Collation).
- **Diagnóstico (¿Qué está pasando en tu consulta actual?):**
  En `01-crud-operations.md` registraste:
  ```sql
  SELECT category, unit_price FROM inventory WHERE category = 'Electronica' AND unit_price > 50.0;
  DELETE FROM inventory WHERE category = 'Papeleria';
  ```
  En la tabla `inventory`, los datos fueron insertados con tilde: `'Electrónica'` y `'Papelería'`. Por defecto, SQLite compara cadenas de texto en modo binario estricto. `'Electronica' != 'Electrónica'`. Tu consulta retorna `0` filas y el `DELETE` no borra nada.
- **Contrato de Solución:** Asegurar que las consultas sobre datos con acentos respeten el literal exacto o utilicen coincidencia insensible.
- **Sonda Inicial:**
  ```bash
  sqlite3 :memory: "CREATE TABLE inventory (id INT, category TEXT, unit_price REAL); INSERT INTO inventory VALUES (1, 'Electrónica', 85.0); SELECT count(*) FROM inventory WHERE category = 'Electronica' AND unit_price > 50.0;"
  ```
  *Resultado:* Devuelve `0` (fallo de coincidencia).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  sqlite3 :memory: "CREATE TABLE inventory (id INT, category TEXT, unit_price REAL); INSERT INTO inventory VALUES (1, 'Electrónica', 85.0); SELECT count(*) FROM inventory WHERE category = 'Electrónica' AND unit_price > 50.0;"
  ```
  *Criterio:* Devuelve `1` con `exit code 0`.

---

## 3. Log de Mutaciones y Verificación

| ID | Fecha | Carril | Responsable | Sonda Inicial (Salida) | Sonda Final (Salida) | Estado |
|---|---|---|---|---|---|---|
| SQL-001 | 2026-10-13 | B | Antigravity | `Parse error: incomplete input` (exit 1) | `✅ PASS` en runner agnóstico (exit 0) | ✅ Completado |
| SQL-002 | 2026-10-13 | B | Antigravity | `Parse error near "SELECT"` (exit 1) | `✅ PASS` en runner agnóstico (exit 0) | ✅ Completado |
| SQL-003 | 2026-10-13 | B | Antigravity | `no such table: main.loans` (exit 1) | `v_active_fines COUNT(*): 3` (exit 0) | ✅ Completado |
| SQL-007 | 2026-10-13 | B | Antigravity | Herramientas no declaradas (exit 1) | Declaradas formalmente en syllabus (exit 0) | ✅ Completado |
| SQL-004 | 2026-10-13 | B | Antigravity | Mito en Lore 04 (afirma sin soporte nativo) | Corrección en Lore 04 + Sonda FULL JOIN (exit 0) | ✅ Completado |
| SQL-008 | 2026-10-13 | A | Operador | Devuelve 11 préstamos inflados | `Reporte 1 COUNT(*): 9` (exit 0) | ✅ Completado |
| SQL-009 | 2026-10-13 | A | Operador | Retención temporal distorsionada (100+ días) | `COALESCE` real (Fiction: 65.33, Science: 77.33) (exit 0) | ✅ Completado |
| SQL-010 | 2026-10-13 | A | Operador | LAG ordenado por revenue empareja día equivocado | `yesterday_sales: 1200.0`, `daily_diff: -100.0` (exit 0) | ✅ Completado |
| SQL-011 | 2026-10-13 | A | Operador | Coincidencia de acentos retorna 0 filas | `count(*) = 1` en `inventory` con tildes (exit 0) | ✅ Completado |

