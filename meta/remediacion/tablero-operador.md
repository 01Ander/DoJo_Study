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
| **`SQL-013`** | `03-sql-basico` | Cap 02: Filtros | Semántica 3VL de `NULL`, trampa de `NOT IN` y `COALESCE` | [`quests/02-filtering/null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql) | `pytest quests/02-filtering/test_null_semantics.py` | 🟢 **COMPLETADO** |
| **`SQL-006`** | `03-sql-basico` | Cap 03: Agregaciones | Agregaciones condicionales `SUM(CASE WHEN...)` | [`quests/03-functions/conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql) | `pytest quests/03-functions/test_conditional_aggregations.py` | 🟢 **COMPLETADO** |
| **`SQL-005`** | `03-sql-basico` | Cap 09: Transacciones | Transacciones explícitas, `ROLLBACK`, `SAVEPOINT` y ACID | [`quests/09-integrity/transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql) | `pytest quests/09-integrity/test_transactions_acid.py` | 🟡 **ACTIVA (Tu turno)** |
| **`MKT-SQL-002`**| `03-sql-basico` | Cap 09: Modelado | SCD Tipo 2 en Star Schema dimensional | `quests/09-integrity/scd_type2_dim.sql` | — | ⏳ Próximo Subject |

---

## 2. 🚀 MISIÓN ACTIVA: `SQL-005` — Transacciones Explícitas, ROLLBACK y ACID (VaultCustodian)

* **Materia:** `03-sql-basico` (Capítulo 09: Views, Indexes & Transactions)  
* **Archivo a editar por el Operador:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql)  
* **Enunciado de la Quest:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/03-transactions-acid-rollback.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/03-transactions-acid-rollback.md)  
* **Teoría de Respaldo:** [`content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md` (§5)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md#5-transacciones-explícitas-rollback-y-principios-acid)

### 📋 El Contrato que debes cumplir:

Reemplaza los bloques `TODO` en [`transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql) con las 3 transacciones explícitas:

1. **Transacción 1: Transferencia Atómica Confirmada (`COMMIT`)**
   * Inicia con `BEGIN TRANSACTION;`.
   * Resta `300.0` del `balance_usd` de `'VAULT-001'`.
   * Suma `300.0` al `balance_usd` de `'VAULT-002'`.
   * Inserta una fila en `transfer_logs` con `sender_account = 'VAULT-001'`, `receiver_account = 'VAULT-002'`, `amount = 300.0` y `status = 'CONFIRMED'`.
   * Confirma permanentemente con `COMMIT;`.
   * *Estado esperado:* `VAULT-001` pasa de 1000 a 700; `VAULT-002` pasa de 500 a 800.

2. **Transacción 2: Retiro Abortado con Reversión Total (`ROLLBACK`)**
   * Inicia con `BEGIN TRANSACTION;`.
   * Intenta debitar `500.0` de `'VAULT-003'` (saldo actual: 200.0).
   * Aborta de inmediato con `ROLLBACK;`.
   * *Estado esperado:* Gracias a `ROLLBACK`, el saldo de `'VAULT-003'` permanece intacto en `200.0`.

3. **Transacción 3: Savepoint y Reversión Parcial (`SAVEPOINT` & `ROLLBACK TO`)**
   * Inicia con `BEGIN TRANSACTION;`.
   * Transfiere `100.0` restándolos de `'VAULT-001'` y sumándolos a `'VAULT-003'`.
   * Crea un punto de guardado: `SAVEPOINT fee_step;`.
   * Intenta aplicar un recargo debitando `50.0` adicionales de `'VAULT-001'`.
   * Revierte únicamente el recargo con `ROLLBACK TO fee_step;`.
   * Libera el marcador: `RELEASE SAVEPOINT fee_step;`.
   * Confirma la operación principal con `COMMIT;`.
   * *Saldos finales:* `VAULT-001 = 600.0` (1000 - 300 - 100, recargo de 50 revertido), `VAULT-002 = 800.0`, `VAULT-003 = 300.0` (200 + 100).

---

### 💡 Ejemplo con Domain Shifting (Sistema Hospitalario - Asignación de Camas):

```sql
-- 🎯 Objetivo de Negocio: Reasignar cama de UCI, revertir cargo de ambulancia opcional si se cancela.

BEGIN TRANSACTION;
-- Operación principal: Reasignar recurso
UPDATE hospital_rooms SET occupied_beds = occupied_beds - 1 WHERE room_code = 'ICU-A';
UPDATE hospital_rooms SET occupied_beds = occupied_beds + 1 WHERE room_code = 'ICU-B';

-- Punto de control intermedio
SAVEPOINT transport_addon;

-- Cargo opcional de traslado en ambulancia
INSERT INTO billing_records (patient_id, concept, amount) VALUES (42, 'AMBULANCE_TRANSFER', 150.0);

-- El traslado se cancela por mal tiempo: revertir SOLO el cargo
ROLLBACK TO transport_addon;
RELEASE SAVEPOINT transport_addon;

-- Confirmar la reasignación de cama
COMMIT;
```

---

### 🧪 Comandos de Verificación Binaria:

1. **Validación Funcional y de Integridad (Pytest):**
   ```bash
   /Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_transactions_acid.py -v
   ```
   *(Criterio de éxito: 2 passed con exit code 0).*

2. **Validación Sintáctica del Script SQL Completo (Runner del DoJo):**
   ```bash
   python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql
   ```

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql`:
  * *Cambio:* **Implementado y aprobado por el Operador (`2/2 passed`, exit code 0). Cierre formal de la brecha `SQL-006`.**
* `content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md`:
  * *Cambio:* Sección 5 añadida con teoría profunda de Transacciones Explícitas, `ROLLBACK`, `SAVEPOINT` y Principios ACID.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/03-transactions-acid-rollback.md`:
  * *Cambio:* Enunciado didáctico de la Quest 09-03 (`SQL-005`).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql`:
  * *Cambio:* Plantilla inicial para el Operador con esquema de bóveda financiera, seed data y bloques transaccionales `TODO`.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_transactions_acid.py`:
  * *Cambio:* Suite evaluadora automatizada con 2 tests unitarios validando atomicidad, reversión de sobregiros y aislamiento de savepoints.








