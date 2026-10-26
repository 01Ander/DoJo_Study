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
| **`SQL-006`** | `03-sql-basico` | Cap 03: Agregaciones | Agregaciones condicionales `SUM(CASE WHEN...)` | [`quests/03-functions/conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql) | `pytest quests/03-functions/test_conditional_aggregations.py` | 🟡 **ACTIVA (Tu turno)** |
| **`SQL-005`** | `03-sql-basico` | Cap 08: Transacciones | Transacciones explícitas, `ROLLBACK` y ACID | `quests/08-set-ops/transactions_acid.sql` | — | ⏳ En espera |
| **`MKT-SQL-002`**| `03-sql-basico` | Cap 09: Modelado | SCD Tipo 2 en Star Schema dimensional | `quests/09-integrity/scd_type2_dim.sql` | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `SQL-006` — Agregaciones Condicionales con CASE WHEN (Pivoteo Analítico)

* **Materia:** `03-sql-basico` (Capítulo 03: Scalar Functions, CASE WHEN & Data Types)  
* **Archivo a editar por el Operador:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql)  
* **Enunciado de la Quest:** [`content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/03-conditional-aggregations.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/03-conditional-aggregations.md)  
* **Teoría de Respaldo:** [`content/subjects/sql/chronicles/SQL-BASICO/lore/03-functions-and-expressions.md` (§7)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/lore/03-functions-and-expressions.md#7-agregaciones-condicionales-con-case-when-pivoteo-analítico)

### 📋 El Contrato que debes cumplir:

Reemplaza los `SELECT` dummy dentro de las 2 vistas analíticas en [`conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql):

1. **`v_merchant_status_pivot` (Desafío 1 - Pivoteo de Estados y Montos):**
   * Agrupa por `merchant_id` y calcula en una sola pasada:
     * `merchant_id`: ID del comercio.
     * `total_orders`: Total general de órdenes (`COUNT(*)`).
     * `completed_orders`: Órdenes con `order_status = 'COMPLETED'` (`SUM(CASE WHEN order_status = 'COMPLETED' THEN 1 ELSE 0 END)`).
     * `failed_orders`: Órdenes con `order_status = 'FAILED'`.
     * `refunded_orders`: Órdenes con `order_status = 'REFUNDED'`.
     * `total_completed_amount`: Suma del `amount` **únicamente** para órdenes `COMPLETED` (`SUM(CASE WHEN order_status = 'COMPLETED' THEN amount ELSE 0.0 END)`).
   * Ordena por `merchant_id ASC`.

2. **`v_merchant_payment_breakdown` (Desafío 2 - Métricas de Canal y Tasa de Éxito):**
   * Agrupa por `merchant_id` y calcula:
     * `merchant_id`: ID del comercio.
     * `credit_card_orders`: Órdenes pagadas con `'CREDIT_CARD'`.
     * `crypto_orders`: Órdenes pagadas con `'CRYPTO'`.
     * `success_rate_pct`: Porcentaje de éxito de órdenes completadas sobre el total, redondeado a 1 decimal:
       $$\text{ROUND}\left(\frac{\sum (\text{COMPLETED})}{\text{total}} \times 100.0, 1\right)$$
       *(⚠️ Recuerda forzar punto flotante usando `1.0` o `100.0` para evitar división entera a cero).*
   * Ordena por `merchant_id ASC`.

---

### 💡 Ejemplo con Domain Shifting (Sistema Universitario):

```sql
-- 🎯 Objetivo de Negocio: Pivotear notas aprobadas, reprobadas y calcular tasa de aprobación en una pasada.

SELECT 
    course_code,
    COUNT(*) AS total_students,
    SUM(CASE WHEN numeric_score >= 60.0 THEN 1 ELSE 0 END) AS passed_students,
    SUM(CASE WHEN numeric_score < 60.0 THEN 1 ELSE 0 END) AS failed_students,
    ROUND(
        SUM(CASE WHEN numeric_score >= 60.0 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 
        1
    ) AS pass_rate_pct
FROM grades
GROUP BY course_code
ORDER BY course_code ASC;
```

---

### 🧪 Comandos de Verificación Binaria:

1. **Validación Funcional y de Lógica de Negocio (Pytest):**
   ```bash
   /Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/test_conditional_aggregations.py -v
   ```
   *(Criterio de éxito: 2 passed con exit code 0).*

2. **Validación Sintáctica de SQLite en Memoria (Runner del DoJo):**
   ```bash
   python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql
   ```

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql`:
  * *Cambio:* **Implementado y aprobado por el Operador (`3/3 passed`, exit code 0). Cierre formal de la brecha `SQL-013`.**
* `content/subjects/sql/chronicles/SQL-BASICO/lore/03-functions-and-expressions.md`:
  * *Cambio:* Sección 7 añadida sobre Agregaciones Condicionales con `CASE WHEN` (pivoteo de filas a columnas, optimización de escaneo único y ratios porcentuales).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/03-conditional-aggregations.md`:
  * *Cambio:* Enunciado didáctico de la Quest 03-03 (`SQL-006`).
* `content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql`:
  * *Cambio:* Plantilla inicial para el Operador con esquema de órdenes, seed data y vistas analíticas.
* `content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/test_conditional_aggregations.py`:
  * *Cambio:* Suite evaluadora automatizada con 2 tests unitarios evaluando pivoteo y métricas de tasa de éxito.








