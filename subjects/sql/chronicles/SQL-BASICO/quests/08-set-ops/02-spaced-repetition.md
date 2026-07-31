# Ejercicio 08-02: Spaced Repetition — Set Difference & Window Review (Tipo B)

**Objetivo:** Combinar la operación `EXCEPT` con la revisión de Window Functions y CTEs.

---

## Setup de Datos

```sql
CREATE TABLE enrolled_2025 (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT
);

CREATE TABLE enrolled_2026 (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT
);

INSERT INTO enrolled_2025 VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO enrolled_2026 VALUES (2, 'Bob'), (4, 'David');
```

---

## Reto

1. Escribe una consulta con `EXCEPT` que encuentre a los estudiantes que estuvieron inscritos en 2025 pero que **NO** se inscribieron en 2026.
2. Escribe una consulta con `UNION` para obtener una lista completa de estudiantes únicos de ambos años, asignándoles un `ROW_NUMBER()` alfabetizado por nombre.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. EXCEPT (Estudiantes de 2025 que no siguen en 2026)
SELECT student_id, student_name FROM enrolled_2025
EXCEPT
SELECT student_id, student_name FROM enrolled_2026;

-- 2. UNION + Window Function
WITH AllStudents AS (
    SELECT student_id, student_name FROM enrolled_2025
    UNION
    SELECT student_id, student_name FROM enrolled_2026
)
SELECT 
    student_id,
    student_name,
    ROW_NUMBER() OVER(ORDER BY student_name ASC) AS global_list_num
FROM AllStudents;
```
</details>
