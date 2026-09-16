# Ejercicio 01-02: ER Diagram Interpretation (Tipo B)

**Objetivo:** Interpretar un diagrama entidad-relación expresado en texto y traducir una relación N:M a una tabla intermedia con DDL.

---

## Diagrama ER

```text
  ┌──────────────┐                       ┌──────────────┐
  │   courses    │ 1                   N │  enrollments │ N                   1 ┌──────────────┐
  ├──────────────┤                       ├──────────────┤                       │   students   │
  │ id (PK)      │───────────────────────│ course_id(FK)│───────────────────────├──────────────┤
  │ title        │                       │ student_id(FK│                       │ id (PK)      │
  └──────────────┘                       │ grade        │                       │ name         │
                                         └──────────────┘                       └──────────────┘
```

---

## Tu Tarea

Escribe las sentencias DDL completas para crear las 3 tablas de este diagrama, asegurando que la combinación de `course_id` y `student_id` dentro de `enrollments` sea **ÚNICA** (para impedir que un estudiante se inscriba dos veces al mismo curso).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    grade REAL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    UNIQUE(course_id, student_id)
);
```
</details>
