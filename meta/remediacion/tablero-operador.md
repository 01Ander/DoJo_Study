# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-21  
> **Materia Activa:** `03-sql-basico` (SQL Básico, Modelado y Transacciones)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

### 🐍 Fase 1: `02-py-poo` (100% COMPLETADO 🟢)
| Tarea ID | Materia | Concepto | Archivo editado | Estado |
|---|---|---|---|---|
| `PY-010` | `02-py-poo` | Constructores con `super()` | `quests/02-entities/rpg_character.py` | 🟢 **COMPLETADO** |
| `PY-011.1` | `02-py-poo` | De Dataclass a Pydantic con `Field` | `quests/06-logging/user_account_schema.py` | 🟢 **COMPLETADO** |
| `PY-011.2` | `02-py-poo` | Validadores de Negocio y Excepciones | `quests/06-logging/transaction_schema.py` | 🟢 **COMPLETADO** |
| `PY-013` | `02-py-poo` | Patrón Output Loaders | `quests/04-orchestration/output_loaders.py` | 🟢 **COMPLETADO** |
| `PY-014` | `02-py-poo` | Extractor desacoplado CSV/JSON | `quests/01-abstractions/data_extractors.py` | 🟢 **COMPLETADO** |
| `PY-020` | `02-py-poo` | Ciclo TDD Red-Green-Refactor | `quests/05-testing/billing_service.py` | 🟢 **COMPLETADO** |

---

### 🗄️ Fase 2: `03-sql-basico` (En Curso)
| Tarea ID | Materia | Ubicación | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|---|
| **`SQL-013`** | `03-sql-basico` | Cap 02: Filtros | Semántica 3VL de `NULL`, trampa de `NOT IN` y `COALESCE` | [`quests/02-filtering/null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql) | `pytest quests/02-filtering/test_null_semantics.py` | 🟡 **ACTIVA (Tu turno)** |
| **`SQL-006`** | `03-sql-basico` | Cap 03: Agregaciones | Agregaciones condicionales `CASE WHEN` | `quests/03-functions/conditional_aggregations.sql` | — | ⏳ En espera |
| **`SQL-005`** | `03-sql-basico` | Cap 08: Transacciones | Transacciones explícitas, `ROLLBACK` y ACID | `quests/08-set-ops/transactions_acid.sql` | — | ⏳ En espera |
| **`MKT-SQL-002`**| `03-sql-basico` | Cap 09: Modelado | SCD Tipo 2 en Star Schema dimensional | `quests/09-integrity/scd_type2_dim.sql` | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `SQL-013` — Semántica Tri-Valor de NULL y Trampa de NOT IN

* **Materia:** `03-sql-basico` (Capítulo 02: Filtering & Sorting)  
* **Archivo a editar por el Operador:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql)  
* **Enunciado de la Quest:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/03-null-semantics-and-three-valued-logic.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/03-null-semantics-and-three-valued-logic.md)  
* **Teoría de Respaldo:** [`content/subjects/sql/chronicles/SQL-BASICO/lore/02-filtering-and-sorting.md` (§4)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/02-filtering-and-sorting.md#4-el-manejo-de-null-y-la-lógica-tri-valor-three-valued-logic---3vl)

### 📋 El Contrato que debes cumplir:

Reemplaza los `SELECT` dummy dentro de las 3 vistas en [`null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql):

1. **`v_effective_customs_fees` (Desafío 1 - Fallback con COALESCE):**
   * Retorna `tracking_code`, `destination_country`, y `effective_customs_fee`.
   * `effective_customs_fee = COALESCE(customs_fee, 0.0) + 10.0` (recargo fijo). Si `customs_fee` es NULL, debe sumar `$0.0 + $10.0 = $10.0`.
   * Ordena por `tracking_code ASC`.

2. **`v_unsanctioned_shipments` (Desafío 2 - Eludir la Trampa de 3VL con NOT IN):**
   * Retorna `tracking_code`, `destination_country`, `weight_kg`.
   * Filtra envíos cuyo `destination_country` **NO** pertenezca a `sanctioned_destinations`.
   * ⚠️ **Trampa 3VL:** `sanctioned_destinations` contiene un registro `NULL`. Si haces `NOT IN (SELECT country_code FROM sanctioned_destinations)` sin filtrar, el motor evaluará `UNKNOWN` y devolverá 0 filas. Debes asegurar `WHERE country_code IS NOT NULL` en la subconsulta (o usar `NOT EXISTS`).
   * Ordena por `tracking_code ASC` (debe retornar 5 filas: `CAN`, `MEX`, `FRA`, `DEU`, `JPN`).

3. **`v_unassigned_carriers` (Desafío 3 - Filtrado con IS NULL):**
   * Retorna `tracking_code`, `destination_country`.
   * Filtra los paquetes sin transportista asignado usando `WHERE carrier_id IS NULL` (nunca `= NULL`).
   * Ordena por `tracking_code ASC` (debe retornar 2 filas: `TRK-1003` y `TRK-1005`).

---

### 💡 Ejemplo con Domain Shifting (Sistema Hospitalario):

```sql
-- 🎯 Objetivo de Negocio: Calcular facturación con tarifa base por defecto y eludir la trampa de 3VL en listas de exclusión.

-- 1. Uso de COALESCE para evitar contaminación de sumas con NULL:
SELECT 
    patient_name,
    COALESCE(fee, 0.0) + 15.0 AS total_billing
FROM appointments;

-- 2. Elusión de la trampa NOT IN al consultar doctores no restringidos:
SELECT id, patient_name, doctor_id
FROM appointments
WHERE doctor_id NOT IN (
    SELECT id FROM restricted_doctors WHERE id IS NOT NULL
);
```

---

### 🧪 Comandos de Verificación Binaria:

1. **Validación Funcional y de Lógica de Negocio (Pytest):**
   ```bash
   /Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/test_null_semantics.py -v
   ```
   *(Criterio de éxito: 3 passed con exit code 0).*

2. **Validación Sintáctica de SQLite en Memoria (Runner del DoJo):**
   ```bash
   python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql
   ```

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`5/5 passed`, exit code 0). Cierre formal de la brecha `PY-020` y de la materia `02-py-poo`.**
* `content/subjects/sql/chronicles/SQL-BASICO/lore/02-filtering-and-sorting.md`:
  * *Cambio:* Sección 4 ampliada con semántica Tri-Valor (3VL), tablas de verdad `TRUE/FALSE/UNKNOWN`, trampa mortal de `NOT IN` con `NULL`, función `COALESCE`, analogías y Zero Surprise Syntax.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/03-null-semantics-and-three-valued-logic.md`:
  * *Cambio:* Enunciado didáctico de la Quest 02-03 (`SQL-013`).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql`:
  * *Cambio:* Plantilla inicial para el Operador con esquema de carga, seed data y vistas dummy.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/test_null_semantics.py`:
  * *Cambio:* Suite evaluadora automatizada con 3 tests unitarios validando 3VL, trampa `NOT IN` y `COALESCE`.







