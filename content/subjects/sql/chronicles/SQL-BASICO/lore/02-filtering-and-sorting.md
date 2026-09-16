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

## 4. El Manejo de `NULL`

En SQL, `NULL` representa la **ausencia de datos** o un valor desconocido. `NULL` **no** es igual a cero (`0`) ni a una cadena vacía (`""`).

Para verificar si un campo es o no nulo, se deben usar estrictamente los operadores `IS NULL` o `IS NOT NULL`.

```sql
-- ❌ MAL: Esto NO funcionará como esperas en SQL porque NULL = NULL da UNKNOWN
SELECT patient_name FROM appointments WHERE notes = NULL;

-- ✅ BIEN: Utilizar IS NULL o IS NOT NULL
SELECT patient_name, status 
FROM appointments 
WHERE notes IS NULL;
```

---

## 5. Ordenamiento y Paginación (`ORDER BY`, `LIMIT`, `OFFSET`)

Puedes ordenar los resultados por una o varias columnas con `ORDER BY` en sentido ascendente (`ASC`, por defecto) o descendente (`DESC`).

```sql
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

```text
subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/
├── 01-crud-operations.md
└── 02-query-challenges.md
```
