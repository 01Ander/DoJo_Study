# Ejercicio 09-04: Modelado Dimensional Star Schema y SCD Tipo 2 (Nivel 4)

**Objetivo:** Implementar una dimensión con Slowly Changing Dimensions Tipo 2 (SCD Tipo 2), modelar la transición de atributos históricos preservando vigencias y construir vistas analíticas temporales Point-in-Time cruzadas con tablas de hechos (Lore 09 §6).

---

## Contexto de Negocio (Domain Shifting: Procesamiento de Liquidaciones Fintech)

La pasarela de pagos B2B **NovaPay Settlements** procesa liquidaciones financieras diarias para comercios asociados. En el Data Warehouse analítico, los comercios están modelados en la dimensión `dim_merchants`, la cual debe registrar auditoría histórica completa de cambios en el nivel de riesgo (`risk_tier`) y tasa de comisión (`fee_rate`).

* Si un comercio cambia de tasa en julio de 2025, las liquidaciones procesadas en marzo de 2025 deben seguir calculándose con la tasa que el comercio tenía en marzo (precisión histórica *Point-in-Time*).
* Si sobreescribiéramos los datos con un simple `UPDATE` (SCD Tipo 1), falsearíamos los estados financieros de meses anteriores.

---

## Archivo de Trabajo

Edita el archivo [`scd_type2_dim.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql).

El archivo ya contiene la estructura DDL de `dim_merchants` y `fact_settlements`, junto con los datos semilla iniciales. Tu misión consiste en completar los 3 desafíos:

### 1. Desafío 1: Transición SCD Tipo 2 (Evolución de la Dimensión)
El 1 de julio de 2025 (`'2025-07-01'`), debido a un incremento en su tasa de disputas, el comercio `'MKT-101'` (`Solaris Market`) es reclasificado:
* Su `risk_tier` cambia de `'LOW'` a `'HIGH'`.
* Su `fee_rate` sube de `0.020` (2.0%) a `0.050` (5.0%).

Debes escribir el bloque DML atómico (dentro de `BEGIN TRANSACTION` y `COMMIT`):
1. **Expirar la versión vigente:** Actualiza la fila activa actual (`is_current = 1`) de `'MKT-101'`, asignando `valid_to = '2025-07-01'` e `is_current = 0`.
2. **Insertar la nueva versión activa:** Inserta una nueva fila para `'MKT-101'` con:
   * `merchant_name = 'Solaris Market'`
   * `risk_tier = 'HIGH'`
   * `fee_rate = 0.050`
   * `valid_from = '2025-07-01'`
   * `valid_to = NULL`
   * `is_current = 1`

### 2. Desafío 2: Vista Analítica Temporal Point-in-Time (`v_settlement_reporting`)
Crea o reemplaza la vista `v_settlement_reporting` uniendo `fact_settlements` con `dim_merchants`. 

La unión debe ser temporalmente precisa: cada liquidación (`settlement_date`) debe cruzarse con la versión de la dimensión que estaba vigente en esa fecha exacta:
* **Condición de Join:**
  ```sql
  ON f.merchant_id = d.merchant_id
 AND f.settlement_date >= d.valid_from
 AND (f.settlement_date < d.valid_to OR d.valid_to IS NULL)
  ```
* **Columnas proyectadas:**
  1. `settlement_id`: ID de la liquidación.
  2. `settlement_date`: Fecha de la liquidación.
  3. `merchant_id`: Código de negocio del comercio.
  4. `merchant_name`: Nombre del comercio.
  5. `risk_tier`: Nivel de riesgo histórico que aplicaba en la fecha de liquidación.
  6. `gross_volume_usd`: Monto bruto liquidado.
  7. `fee_rate`: Tasa porcentual histórica que aplicaba en la fecha.
  8. `fee_amount_usd`: Monto de la comisión en USD, redondeado a 2 decimales:
     `ROUND(f.gross_volume_usd * d.fee_rate, 2)`
* Ordena por `settlement_id ASC`.

### 3. Desafío 3: Vista de Estado Actual de la Dimensión (`v_current_merchants`)
Crea o reemplaza la vista `v_current_merchants` para dashboards operacionales que necesitan consultar únicamente la versión actual y vigente de cada comercio:
* Filtra exclusivamente filas con `is_current = 1`.
* **Columnas proyectadas:** `merchant_id`, `merchant_name`, `risk_tier`, `fee_rate`, `valid_from`.
* Ordena por `merchant_id ASC`.

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas unitarias automatizada:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_scd_type2_dim.py -v
```
*(Criterio de éxito: 3 passed con exit code 0).*

También puedes verificar la validez sintáctica de SQLite con el runner agnóstico:
```bash
python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql
```

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```sql
-- Desafío 1: Transición SCD Tipo 2
BEGIN TRANSACTION;
UPDATE dim_merchants
SET valid_to = '2025-07-01',
    is_current = 0
WHERE merchant_id = 'MKT-101' AND is_current = 1;

INSERT INTO dim_merchants (merchant_id, merchant_name, risk_tier, fee_rate, valid_from, valid_to, is_current)
VALUES ('MKT-101', 'Solaris Market', 'HIGH', 0.050, '2025-07-01', NULL, 1);
COMMIT;

-- Desafío 2: Vista Analítica Point-in-Time
DROP VIEW IF EXISTS v_settlement_reporting;
CREATE VIEW v_settlement_reporting AS
SELECT 
    f.settlement_id,
    f.settlement_date,
    f.merchant_id,
    d.merchant_name,
    d.risk_tier,
    f.gross_volume_usd,
    d.fee_rate,
    ROUND(f.gross_volume_usd * d.fee_rate, 2) AS fee_amount_usd
FROM fact_settlements f
JOIN dim_merchants d
  ON f.merchant_id = d.merchant_id
 AND f.settlement_date >= d.valid_from
 AND (f.settlement_date < d.valid_to OR d.valid_to IS NULL)
ORDER BY f.settlement_id ASC;

-- Desafío 3: Vista de Estado Actual
DROP VIEW IF EXISTS v_current_merchants;
CREATE VIEW v_current_merchants AS
SELECT 
    merchant_id,
    merchant_name,
    risk_tier,
    fee_rate,
    valid_from
FROM dim_merchants
WHERE is_current = 1
ORDER BY merchant_id ASC;
```
</details>
