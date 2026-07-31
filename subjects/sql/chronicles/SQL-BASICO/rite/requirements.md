# Rite: Public Library Management System (SQL-BASICO)

**Estado:** 🔒 Bloqueado (Requiere aprobación de auditoría `/scry SQL-BASICO` por el DM).

Este es el proyecto integrador de la chronicle **`SQL-BASICO`**. Aquí aplicarás de forma autónoma todos los conceptos aprendidos en los 10 capítulos de teoría (`lore/`) y laboratorios (`quests/`), sin andamiaje.

---

## 💼 Contexto de Negocio & ROI

La Red de Bibliotecas Públicas Municipales está migrando su operación desde archivos desorganizados de Excel hacia un sistema relacional centralizado en SQLite. La dirección necesita garantizar la integridad de los préstamos, calcular multas acumuladas por retraso en devoluciones, generar reportes analíticos de lecturas por categoría y disponer de un mecanismo seguro para realizar préstamos y devoluciones atómicas sin riesgos de inconsistencia de datos.

---

## 🏗️ Fases de Despliegue (Desbloqueables)

Desarrolla el Rite ejecutando las sentencias SQL correspondientes a cada fase dentro de scripts `.sql` organizados. Documenta las decisiones de diseño y trade-offs en tu `rite/journal.md`.

---

### Fase 1: Schema Design & Modeling (Ref: Cap 00 + 01)
*Diseñar el esquema relacional en 3NF con restricciones de integridad infalibles.*

- Habilitar soporte para llaves foráneas (`PRAGMA foreign_keys = ON;`).
- Crear la tabla `authors` (`id`, `full_name`, `country`).
- Crear la tabla `categories` (`id`, `name` UNIQUE).
- Crear la tabla `books` (`id`, `isbn` UNIQUE, `title`, `publication_year`, `category_id` FK).
- Crear la tabla intermedia `book_authors` (Relación N:M entre `books` y `authors`).
- Crear la tabla `members` (`id`, `full_name`, `email` UNIQUE, `join_date`, `status` DEFAULT `'Active'`).
- Crear la tabla `loans` (`id`, `book_id` FK, `member_id` FK, `loan_date`, `due_date`, `return_date` NULLABLE, `fine_amount` DEFAULT 0.0).

**Criterio de Validación:** La inserción de un préstamo con un `member_id` o `book_id` inexistente debe ser rechazada por el motor con un error de Foreign Key.

---

### Fase 2: Data Ingestion & Sanitization (Ref: Cap 02 + 03)
*Poblar el sistema con datos de prueba realistas y aplicar funciones escalares y limpieza.*

- Poblar el esquema con al menos:
  - 5 Categorías, 8 Autores, 12 Libros, 10 Miembros y 15 Registros de préstamos (incluyendo préstamos activos, devueltos y con retraso).
- Escribir una consulta de sanitización que seleccione los miembros ordenados por fecha de registro, mostrando su nombre limpio (`UPPER(TRIM(full_name))`), su email estandarizado (`LOWER(email)`), y una categoría calculada con `CASE WHEN` (`'Senior Member'` si se registró hace más de 365 días, `'Standard Member'` de lo contrario).

---

### Fase 3: Core Analytics (Ref: Cap 04 + 05)
*Producir reportes analíticos clave combinando tablas y agregando métricas.*

- **Reporte 1 (JOIN Multi-tabla):** Consultar todos los préstamos activos mostrando: Título del Libro, Nombre del Autor principal, Nombre del Miembro, Fecha de Préstamo y Días de Préstamo transcurridos.
- **Reporte 2 (Agregación & HAVING):** Obtener el Top de Categorías de libros más prestadas, mostrando el nombre de la categoría, el recuento total de préstamos y el promedio de días de retención por libro. Filtrar con `HAVING` para mostrar únicamente categorías con más de 2 préstamos registrados.

---

### Fase 4: Advanced Engineering & Windowing (Ref: Cap 06 + 07)
*Implementar lógica compleja con CTEs y Funciones de Ventana.*

- **Reporte 3 (CTEs & Deduplicación):** Construir una CTE que elimine registros duplicados de préstamos basados en la clave natural (`book_id`, `member_id`, `loan_date`), reteniendo únicamente la entrada con el `id` más alto (`ROW_NUMBER() OVER(...)`).
- **Reporte 4 (Window Functions Analytics):** Calcular el ranking de los libros más leídos por categoría usando `DENSE_RANK() OVER(PARTITION BY category_id ORDER BY COUNT(l.id) DESC)`, mostrando también la diferencia de lecturas en comparación con el libro inmediatamente anterior (`LAG`).

---

### Fase 5: Production & Optimization (Ref: Cap 08 + 09)
*Preparar la base de datos para producción con Vistas, Índices y Transacciones ACID.*

- **Vista Reutilizable:** Crear la vista `v_active_fines` que liste a todos los miembros con multas pendientes de pago (`fine_amount > 0`).
- **Indexación & Inspección:** Crear un índice en `loans(member_id, status)` y ejecutar `EXPLAIN QUERY PLAN` para confirmar que las búsquedas por historial de miembros utilizan `SEARCH TABLE` mediante índice en lugar de `SCAN TABLE`.
- **Transacción Atómica de Préstamo (ACID):** Escribir un bloque transaccional (`BEGIN TRANSACTION ... COMMIT`) que registre el préstamo de un libro, verifique que el miembro no tenga más de 3 préstamos activos y actualice el estado correspondientemente. Si alguna validación falla, ejecutar `ROLLBACK`.

---

## 🛠️ Diagnóstico Quirúrgico (En caso de atasco)

Si durante el desarrollo del Rite encuentras una falla o bloqueo conceptual (Fricción > 8):
1. Invoca a la **Reviewer Socrática** (`/personality witch`).
2. Si la Reviewer detecta una laguna en el paradigma (ej: confusión en la sintaxis de `ROW_NUMBER` o `JOIN`), te indicará pausar el Rite y regresar a repasar el Capítulo de Lore y Quest correspondiente.
