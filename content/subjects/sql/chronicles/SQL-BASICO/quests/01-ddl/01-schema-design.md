# Ejercicio 01-01: Schema Design & Constraints (Tipo A)

**Objetivo:** Diseñar un esquema relacional normalizado en 3NF con llaves primarias, llaves foráneas y restricciones de integridad.

---

## Contexto de Negocio (Domain Shifting: Gestión de Flotas de Camiones)

Una empresa de logística de transporte necesita modelar sus camiones y los mantenimientos mecánicos preventivos que se les realizan.

---

## Instrucciones

1. Habilita las llaves foráneas en SQLite: `PRAGMA foreign_keys = ON;`.
2. Diseña la tabla `trucks`:
   - `id`: Entero, Clave Primaria Autoincremental.
   - `license_plate`: Texto, Único, No Nulo.
   - `model_year`: Entero, debe ser mayor o igual a 2010 (Constraint `CHECK`).
   - `status`: Texto con valor por defecto `'Active'`.
3. Diseña la tabla `maintenance_logs` (Relación 1:N con `trucks`):
   - `id`: Entero, Clave Primaria.
   - `truck_id`: Entero, Llave Foránea hacia `trucks(id)` con `ON DELETE CASCADE`.
   - `log_date`: Texto, No Nulo.
   - `description`: Texto, No Nulo.
   - `cost_usd`: Decimal, debe ser mayor que 0 (Constraint `CHECK`).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE trucks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_plate TEXT NOT NULL UNIQUE,
    model_year INTEGER CHECK(model_year >= 2010),
    status TEXT DEFAULT 'Active'
);

CREATE TABLE maintenance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    truck_id INTEGER NOT NULL,
    log_date TEXT NOT NULL,
    description TEXT NOT NULL,
    cost_usd REAL CHECK(cost_usd > 0),
    FOREIGN KEY (truck_id) REFERENCES trucks(id) ON DELETE CASCADE
);
```
</details>
