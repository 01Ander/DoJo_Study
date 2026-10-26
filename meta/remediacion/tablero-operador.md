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
| **`SQL-005`** | `03-sql-basico` | Cap 09: Transacciones | Transacciones explícitas, `ROLLBACK`, `SAVEPOINT` y ACID | [`quests/09-integrity/transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql) | `pytest quests/09-integrity/test_transactions_acid.py` | 🟢 **COMPLETADO** |
| **`MKT-SQL-002`**| `03-sql-basico` | Cap 09: Modelado | SCD Tipo 2 en Star Schema dimensional | [`quests/09-integrity/scd_type2_dim.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql) | `pytest quests/09-integrity/test_scd_type2_dim.py` | 🟡 **ACTIVA (Tu turno)** |

---

## 2. 🚀 MISIÓN ACTIVA: `MKT-SQL-002` — Slowly Changing Dimensions (SCD Tipo 2) en Modelado Dimensional

* **Materia:** `03-sql-basico` (Capítulo 09: Views, Indexes & Transactions — Extensión Dimensional)  
* **Archivo a editar por el Operador:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql)  
* **Enunciado de la Quest:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/04-scd-type2-dimensional-modeling.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/04-scd-type2-dimensional-modeling.md)  
* **Teoría de Respaldo:** [`content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md` (§6)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md#6-modelado-dimensional-y-slowly-changing-dimensions-scd-tipo-2)

### 📋 El Contrato que debes cumplir:

Edita [`scd_type2_dim.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql) resolviendo los 3 desafíos:

1. **Desafío 1: Transición SCD Tipo 2 (Evolución de Atributos)**
   * El `'2025-07-01'`, el comercio `'MKT-101'` sube a `risk_tier = 'HIGH'` y `fee_rate = 0.050`.
   * Abre `BEGIN TRANSACTION;`.
   * **Expirar versión vigente:**
     ```sql
     UPDATE dim_merchants
     SET valid_to = '2025-07-01', is_current = 0
     WHERE merchant_id = 'MKT-101' AND is_current = 1;
     ```
   * **Insertar nueva versión activa:**
     ```sql
     INSERT INTO dim_merchants (merchant_id, merchant_name, risk_tier, fee_rate, valid_from, valid_to, is_current)
     VALUES ('MKT-101', 'Solaris Market', 'HIGH', 0.050, '2025-07-01', NULL, 1);
     ```
   * Cierra con `COMMIT;`.

2. **Desafío 2: Vista Analítica Point-in-Time (`v_settlement_reporting`)**
   * Une `fact_settlements` con `dim_merchants` usando la cláusula de ventana temporal:
     ```sql
     ON f.merchant_id = d.merchant_id
    AND f.settlement_date >= d.valid_from
    AND (f.settlement_date < d.valid_to OR d.valid_to IS NULL)
     ```
   * Columnas proyectadas: `settlement_id`, `settlement_date`, `merchant_id`, `merchant_name`, `risk_tier`, `gross_volume_usd`, `fee_rate`, y `ROUND(gross_volume_usd * fee_rate, 2) AS fee_amount_usd`.
   * Ordena por `settlement_id ASC`.

3. **Desafío 3: Vista de Estado Actual de la Dimensión (`v_current_merchants`)**
   * Selecciona de `dim_merchants` únicamente los registros con `is_current = 1`.
   * Columnas proyectadas: `merchant_id`, `merchant_name`, `risk_tier`, `fee_rate`, `valid_from`.
   * Ordena por `merchant_id ASC`.

---

### 💡 Ejemplo con Domain Shifting (Suscripciones SaaS - Cambio de Plan):

```sql
-- 🎯 Objetivo de Negocio: Ingestar cambio de plan de 'BASIC' a 'PRO' y reportar consumo histórico con el precio vigente.

-- 1. Transición SCD2
BEGIN TRANSACTION;
UPDATE dim_tenants 
SET valid_to = '2025-05-01', is_current = 0 
WHERE tenant_id = 'TNT-500' AND is_current = 1;

INSERT INTO dim_tenants (tenant_id, tenant_name, plan_name, cost_per_gb, valid_from, valid_to, is_current)
VALUES ('TNT-500', 'Nova Cloud', 'PRO', 0.08, '2025-05-01', NULL, 1);
COMMIT;

-- 2. Reporte Point-in-Time
CREATE VIEW v_usage_billing AS
SELECT 
    u.usage_id,
    u.usage_date,
    t.tenant_name,
    t.plan_name,
    u.gb_consumed,
    ROUND(u.gb_consumed * t.cost_per_gb, 2) AS billed_usd
FROM fact_storage_usage u
JOIN dim_tenants t
  ON u.tenant_id = t.tenant_id
 AND u.usage_date >= t.valid_from
 AND (u.usage_date < t.valid_to OR t.valid_to IS NULL)
ORDER BY u.usage_id ASC;
```

---

### 🧪 Comandos de Verificación Binaria:

1. **Validación Funcional y de Fidelidad Temporal (Pytest):**
   ```bash
   /Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_scd_type2_dim.py -v
   ```
   *(Criterio de éxito: 3 passed con exit code 0).*

2. **Validación Sintáctica de SQLite (Runner del DoJo):**
   ```bash
   python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql
   ```

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql`:
  * *Cambio:* **Implementado y aprobado por el Operador (`2/2 passed`, exit code 0). Cierre formal de la brecha `SQL-005`.**
* `content/subjects/sql/chronicles/SQL-BASICO/lore/09-views-indexes-and-transactions.md`:
  * *Cambio:* Sección 6 añadida sobre Modelado Dimensional (Star Schema) y Slowly Changing Dimensions (SCD Tipo 2).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/04-scd-type2-dimensional-modeling.md`:
  * *Cambio:* Enunciado didáctico de la Quest 09-04 (`MKT-SQL-002`).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql`:
  * *Cambio:* Plantilla inicial para el Operador con esquema Star Schema (`dim_merchants`, `fact_settlements`), seed data y desafíos `TODO`.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_scd_type2_dim.py`:
  * *Cambio:* Suite evaluadora automatizada con 3 tests unitarios validando transición SCD2, joins temporales Point-in-Time y snapshot activo.








