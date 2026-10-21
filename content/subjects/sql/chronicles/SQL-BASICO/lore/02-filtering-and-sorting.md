# Capítulo 02: Filtering & Sorting — WHERE, ORDER BY & CRUD

Al consultar una base de datos en producción, casi nunca querrás traer todos los registros de una tabla. Las tablas pueden albergar millones de filas, por lo que saber filtrar con precisión, ordenar resultados y realizar modificaciones seguras (**CRUD: Create, Read, Update, Delete**) es esencial para la ingeniería de datos.

En este capítulo aprenderás a dominar la cláusula `WHERE`, los operadores lógicos y relacionales, el ordenamiento con `ORDER BY`, el paginado con `LIMIT`/`OFFSET`, y las operaciones críticas de actualización y eliminación.

---

## 1. Conceptos Fundamentales

### Analogía 1: El Filtro de la Cafetera
Piensa en la cláusula `WHERE` como el filtro de una cafetera. Tú viertes una mezcla completa de agua y grano molido, pero el filtro sólo deja pasar el líquido procesado y retiene los residuos. Del mismo modo, `WHERE` evalúa fila por fila de la tabla; si la condición da como resultado `TRUE` (verdadero), la fila pasa al resultado final; si da `FALSE` o `UNKNOWN` (por un `NULL`), la fila se descarta.

### Analogía 2: La Fila de Espera en Triage Médico
En la sala de emergencias de un hospital, los pacientes no se atienden por orden estricto de llegada, sino por nivel de gravedad (Triage). `ORDER BY` funciona exactamente igual: puedes ordenar los registros por urgencia médica (descendente), luego por hora de llegada (ascendente) y limitar la pantalla a los 5 casos más críticos que el médico debe atender de inmediato (`LIMIT 5`).

---

## 2. Dominio de Ejemplo: Sistema de Turnos Médicos (Domain Shifting)

Modelaremos un **Sistema de Citas y Atención Médica en un Hospital**.

### Setup de Datos para la Terminal

Copia y ejecuta este script en tu terminal interactiva de SQLite (`sqlite3 hospital.db`):

```sql
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    years_experience INTEGER NOT NULL,
    is_available INTEGER DEFAULT 1 -- 1 = Disponible, 0 = No disponible
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL, -- Formato ISO: YYYY-MM-DD HH:MM
    status TEXT NOT NULL,          -- 'Scheduled', 'Completed', 'Cancelled'
    fee REAL,
    notes TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Inserción de datos de prueba
INSERT INTO doctors (name, specialty, years_experience, is_available) VALUES
('Dr. Garcia', 'Cardiologia', 12, 1),
('Dra. Lopez', 'Pediatria', 8, 1),
('Dr. Martinez', 'Neurologia', 15, 0),
('Dra. Rodriguez', 'Cardiologia', 4, 1),
('Dr. Perez', 'Dermatologia', 2, 1);

INSERT INTO appointments (patient_name, doctor_id, appointment_date, status, fee, notes) VALUES
('Carlos Mendoza', 1, '2026-08-01 09:00', 'Completed', 150.0, 'Chequeo general OK'),
('Ana Silva', 2, '2026-08-01 10:00', 'Completed', 120.0, NULL),
('Roberto Gomez', 1, '2026-08-02 11:30', 'Scheduled', 150.0, 'Paciente reporta arritmia'),
('Lucia Fernandez', 3, '2026-08-02 14:00', 'Cancelled', 200.0, 'Cancelado por el paciente'),
('Elena Torres', 4, '2026-08-03 08:30', 'Scheduled', 140.0, NULL),
('David Morales', 2, '2026-08-03 16:00', 'Scheduled', 120.0, 'Control pediatrico');
```

---

## 3. Filtrado de Datos con `WHERE`

### Operadores de Comparación y Lógicos
Puedes combinar condiciones usando `=`, `!=` (o `<>`), `>`, `<`, `>=`, `<=`, `AND`, `OR`, `NOT`.

```sql
-- Doctores de Cardiologia con mas de 5 años de experiencia
SELECT name, specialty, years_experience 
FROM doctors 
WHERE specialty = 'Cardiologia' AND years_experience > 5;
```

### Operadores Especiales: `IN`, `BETWEEN`, `LIKE`

- **`IN (val1, val2, ...)`:** Evalúa si el valor coincide con cualquiera de los elementos de una lista.
- **`BETWEEN min AND max`:** Evalúa si el valor está en un rango inclusivo.
- **`LIKE 'patron'`:** Búsqueda de patrones en texto (`%` representa cero o más caracteres; `_` representa exactamente un caracter).

```sql
-- Citas que cuestan entre 130 y 180 USD
SELECT patient_name, fee 
FROM appointments 
WHERE fee BETWEEN 130.0 AND 180.0;

-- Buscar doctores cuya especialidad termine en 'logia' (Cardiologia, Neurologia, Dermatologia)
SELECT name, specialty 
FROM doctors 
WHERE specialty LIKE '%logia';

-- Doctores de Pediatria o Neurologia usando IN
SELECT name, specialty 
FROM doctors 
WHERE specialty IN ('Pediatria', 'Neurologia');
```

---

## 4. El Manejo de `NULL` y la Lógica Tri-Valor (Three-Valued Logic - 3VL)

En SQL, `NULL` no representa el número cero (`0`), un espacio en blanco (`' '`) ni una cadena vacía (`""`). Representa estrictamente la **ausencia de datos**, un valor desconocido o un hecho no aplicable.

Debido a que `NULL` representa lo desconocido, el motor SQL no opera bajo la lógica booleana clásica binaria (`TRUE` / `FALSE`), sino bajo un sistema formal llamado **Lógica Tri-Valor (Three-Valued Logic o 3VL)**, cuyos tres estados son:
1. `TRUE` (Verdadero)
2. `FALSE` (Falso)
3. **`UNKNOWN` (Desconocido)**

---

### Analogías del Mundo Real

#### Analogía 1: La Caja Sellada de Schrödinger
Si tienes una caja sellada y opaca en las manos y alguien te pregunta: *"¿El contenido pesa más de 10 kilogramos?"*, no puedes responder con rigor ni "Sí" ni "No". Tu única respuesta verídica es: *"No lo sé / Desconocido"* (`UNKNOWN`). 
Si colocas otra caja sellada idéntica al lado y te preguntan: *"¿Ambas cajas contienen exactamente el mismo peso?"*, tampoco puedes responder "Sí". Como desconoces ambos contenidos, la comparación `NULL = NULL` evalúa a `UNKNOWN`, jamás a `TRUE`.

#### Analogía 2: El Veredicto de un Jurado (Juicio Nulo por Falta de Pruebas)
En un juicio penal, si las pruebas clave desaparecieron o nunca fueron recolectadas (`NULL`), el jurado no puede declarar al acusado culpable (`TRUE`) ni inocente con total certeza (`FALSE`). El proceso entra en estado de indeterminación o juicio nulo (`UNKNOWN`). La justicia no puede ejecutar una condena basada en una incógnita.

---

### Tablas de Verdad en Lógica Tri-Valor (3VL)

Cuando combinas condiciones lógicas que involucran `UNKNOWN`, el motor aplica estas reglas formales:

| Expresión | Resultado | Justificación Lógica |
|---|---|---|
| `TRUE AND UNKNOWN` | **`UNKNOWN`** | No podemos confirmar el `AND` hasta que no sepamos qué es la incógnita. |
| `FALSE AND UNKNOWN` | **`FALSE`** | Si una parte ya es falsa, el `AND` es falso sin importar la incógnita. |
| `TRUE OR UNKNOWN` | **`TRUE`** | Si una parte ya es verdadera, el `OR` se satisface de inmediato. |
| `FALSE OR UNKNOWN` | **`UNKNOWN`** | Depende de si la incógnita resulta ser verdadera o falsa. |
| `NOT UNKNOWN` | **`UNKNOWN`** | La negación de algo desconocido sigue siendo desconocido. |

> [!IMPORTANT]
> **La Regla de Oro de la Cláusula WHERE:**  
> Una fila **solo se incluye en el resultado final si la condición del `WHERE` evalúa estrictamente a `TRUE`**. Si la condición evalúa a `FALSE` o a `UNKNOWN`, la fila es descartada silenciosamente.

---

### ❌ La Trampa Mortal de `NOT IN` con `NULL` (The Fatal NULL Trap)

Uno de los bugs más destructivos y silenciosos en producción ocurre al combinar `NOT IN` con listas o subconsultas que contienen al menos un valor `NULL`.

#### ¿Por qué explota?
Internamente, el motor SQL traduce una expresión `x IN (1, 2)` como:
$$(x = 1) \lor (x = 2)$$

Por lo tanto, la negación `x NOT IN (1, 2, NULL)` se traduce por las Leyes de De Morgan como:
$$(x \neq 1) \land (x \neq 2) \land (x \neq \text{NULL})$$

Como cualquier comparación directa con `NULL` arroja `UNKNOWN`:
$$(x \neq 1) \land (x \neq 2) \land \text{UNKNOWN} \implies \text{UNKNOWN}$$

**Consecuencia directa:** ¡La condición NUNCA será `TRUE` para ninguna fila de la tabla! La consulta devolverá **cero filas**, haciendo que reportes críticos de auditoría, fraude o conciliación financiera reporten falsos vacíos.

```sql
-- 🎯 Objetivo de Negocio: Identificar citas cuyos doctores no pertenezcan a la lista de asignación especial.

-- ❌ EL MAL CAMINO: Si la lista de exclusión contiene un NULL, la consulta devuelve CERO filas
SELECT id, patient_name, doctor_id
FROM appointments
WHERE doctor_id NOT IN (1, 2, NULL); -- ⚠️ Retorna vacío (0 filas) debido a 3VL

-- ✅ EL BUEN CAMINO: Filtrar los NULL explícitamente o usar NOT EXISTS
SELECT id, patient_name, doctor_id
FROM appointments
WHERE doctor_id NOT IN (
    SELECT id FROM doctors WHERE id IS NOT NULL AND specialty = 'Pediatria'
);
```

---

### La Función de Contingencia: `COALESCE`

Para realizar cálculos aritméticos o comparaciones seguras sin que un `NULL` "contamine" la operación (recuerda que `100.0 + NULL = NULL`), SQL provee la función estándar `COALESCE`.

* **¿Qué hace?** Evalúa una lista de argumentos en orden de izquierda a derecha y devuelve el **primer valor no nulo**.
* **Sintaxis:** `COALESCE(columna, valor_por_defecto)`

```sql
-- 🎯 Objetivo de Negocio: Calcular el total a pagar garantizando que notas vacías muestren un mensaje por defecto y tarifas nulas no rompan sumatorias.

SELECT 
    patient_name,
    status,
    COALESCE(notes, 'Sin observaciones registradas') AS sanitized_notes,
    COALESCE(fee, 0.0) + 15.0 AS total_with_admin_surcharge
FROM appointments;
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): `IS NULL`, `IS NOT NULL` y `COALESCE`
> * **`columna IS NULL` / `columna IS NOT NULL`:** Son los únicos operadores válidos en SQL para verificar nulidad. `columna = NULL` es un error de diseño porque evalúa a `UNKNOWN` y nunca devolverá filas.
> * **`COALESCE(expr1, expr2, ...)`:** Admite $N$ parámetros. Si `expr1` no es nulo, lo devuelve. Si es nulo, evalúa `expr2`, y así sucesivamente. Si todos son nulos, devuelve `NULL`. Es estándar ANSI SQL y funciona de manera idéntica en SQLite, PostgreSQL, MySQL y DuckDB.

---

## 5. Ordenamiento y Paginación (`ORDER BY`, `LIMIT`, `OFFSET`)

Puedes ordenar los resultados por una o varias columnas con `ORDER BY` en sentido ascendente (`ASC`, por defecto) o descendente (`DESC`).

```sql
-- 🎯 Objetivo de Negocio: Consultar los doctores más experimentados aplicando paginación para interfaces web.

-- Doctores ordenados por años de experiencia (de mayor a menor)
SELECT name, specialty, years_experience 
FROM doctors 
ORDER BY years_experience DESC;

-- Paginación: Obtener el 2do y 3er doctor mas experimentado (LIMIT 2 OFFSET 1)
SELECT name, years_experience 
FROM doctors 
ORDER BY years_experience DESC 
LIMIT 2 OFFSET 1;
```

---

## 6. Operaciones CRUD Seguras (`UPDATE` & `DELETE`)

### ❌ El Mal Camino: Operaciones sin WHERE (Peligro de Nivel Catastrófico)
Si ejecutas `UPDATE` o `DELETE` sin especificar la cláusula `WHERE`, la sentencia se aplicará a **TODAS** las filas de la tabla sin previo aviso.

```sql
-- ❌ PELIGRO CATASTRÓFICO: Cambia la tarifa de TODOS los pacientes de la clínica a 0.0 USD
UPDATE appointments SET fee = 0.0;

-- ❌ PELIGRO CATASTRÓFICO: Elimina TODOS los registros de la tabla de doctores
DELETE FROM doctors;
```

### ✅ El Buen Camino: Operaciones Específicas con WHERE
La regla de oro en ingeniería de datos es ejecutar primero un `SELECT` con el `WHERE` para verificar qué filas van a ser modificadas, y luego ejecutar la actualización o borrado usando la Primary Key.

```sql
-- 🎯 Objetivo de Negocio: Cancelar una cita específica y purgar registros obsoletos usando llaves primarias.

-- 1. Verificamos la cita a cancelar
SELECT id, patient_name, status FROM appointments WHERE id = 3;

-- 2. Modificamos únicamente el estado de esa cita específica
UPDATE appointments 
SET status = 'Cancelled', notes = 'Cancelado por fuerza mayor' 
WHERE id = 3;

-- 3. Eliminamos un doctor en particular asegurando su ID
DELETE FROM doctors WHERE id = 5;
```

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/02-filtering/`:

- [[01-crud-operations.md]] (Tipo A: Consultas de filtrado, actualización y borrado controlado)
- [[02-query-challenges.md]] (Tipo B: Desafíos de lógica de filtrado con operadores lógicos y patrones LIKE)
- [[03-null-semantics-and-three-valued-logic.md]] (Tipo A: Semántica Tri-Valor de NULL, trampa de NOT IN y COALESCE)

```text
subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/
├── 01-crud-operations.md
├── 02-query-challenges.md
└── 03-null-semantics-and-three-valued-logic.md
```

