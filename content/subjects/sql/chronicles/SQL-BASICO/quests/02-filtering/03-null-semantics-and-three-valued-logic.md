# Ejercicio 02-03: Semántica Tri-Valor de NULL, Trampa de NOT IN y COALESCE (Nivel 4)

**Objetivo:** Dominar la Lógica Tri-Valor (3VL) de SQL (`TRUE`, `FALSE`, `UNKNOWN`), implementar operaciones aritméticas seguras con `COALESCE` y evitar la trampa mortal de `NOT IN` con subconsultas que contienen `NULL` (Lore 02 §4).

---

## Contexto de Negocio (Domain Shifting: Logística de Carga Internacional)

Trabajas como Data Engineer en la plataforma de logística global **GlobalCargoExpress**. El sistema gestiona miles de paquetes internacionales, pero los datos operativos sufren de valores incompletos:
- Algunos paquetes están exentos de aduana o su arancel no ha sido tasado aún (`customs_fee IS NULL`).
- Ciertos paquetes aún no tienen un transportista asignado en la bodega (`carrier_id IS NULL`).
- La tabla de países sancionados (`sanctioned_destinations`) contiene códigos de países bloqueados y un registro `NULL` producto de una migración incompleta.

---

## Archivo de Trabajo

Edita el archivo [`null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql). 

El script ya crea las tablas `shipments` y `sanctioned_destinations` con sus datos de prueba. Tu labor consiste en reemplazar las tres consultas dummy (`SELECT ...`) dentro de las tres vistas analíticas:

### 1. Desafío 1: Tarifa Efectiva con `COALESCE`
Crea la vista `v_effective_customs_fees`:
* **Columnas requeridas:** `tracking_code`, `destination_country`, `effective_customs_fee`.
* **Regla de negocio:** `effective_customs_fee` debe ser igual a `customs_fee` más un recargo administrativo fijo de `$10.0`. Si `customs_fee` es `NULL`, debe tratarse como `$0.0` para que el total sea `$10.0` (evitando que `NULL + 10.0` resulte en `NULL`).
* **Ordenamiento:** `ORDER BY tracking_code ASC`.

### 2. Desafío 2: Envíos No Sancionados (Eludiendo la Trampa de `NOT IN`)
Crea la vista `v_unsanctioned_shipments`:
* **Columnas requeridas:** `tracking_code`, `destination_country`, `weight_kg`.
* **Regla de negocio:** Retornar los paquetes cuyo `destination_country` **NO** esté en la tabla `sanctioned_destinations`.
* ⚠️ **ADVERTENCIA CRÍTICA (3VL Trap):** La tabla `sanctioned_destinations` contiene un registro con valor `NULL`. Si ejecutas `WHERE destination_country NOT IN (SELECT country_code FROM sanctioned_destinations)`, la lógica tri-valor evaluará la condición a `UNKNOWN` y tu consulta retornará **0 filas**. Debes eludir la trampa filtrando `WHERE country_code IS NOT NULL` en la subconsulta (o usando `NOT EXISTS`).
* **Ordenamiento:** `ORDER BY tracking_code ASC`.
* **Filas esperadas:** 5 envíos (`CAN`, `MEX`, `FRA`, `DEU`, `JPN`).

### 3. Desafío 3: Envíos sin Transportista Asignado
Crea la vista `v_unassigned_carriers`:
* **Columnas requeridas:** `tracking_code`, `destination_country`.
* **Regla de negocio:** Obtener los paquetes que aún no han sido asignados a ningún transportista (`carrier_id IS NULL`).
* ⚠️ **Regla:** Nunca uses `= NULL` ni `!= NULL`.
* **Ordenamiento:** `ORDER BY tracking_code ASC`.
* **Filas esperadas:** 2 envíos (`TRK-1003` y `TRK-1005`).

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas automatizadas:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/test_null_semantics.py -v
```
*(Criterio de éxito: 3 passed con exit code 0).*

También puedes verificar la validez sintáctica de todo el script SQL con el runner agnóstico del DoJo:
```bash
python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql
```

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```sql
-- Desafío 1: Tarifa con COALESCE
DROP VIEW IF EXISTS v_effective_customs_fees;
CREATE VIEW v_effective_customs_fees AS
SELECT 
    tracking_code, 
    destination_country, 
    COALESCE(customs_fee, 0.0) + 10.0 AS effective_customs_fee 
FROM shipments
ORDER BY tracking_code ASC;

-- Desafío 2: Envíos no sancionados eludiendo la trampa de NOT IN
DROP VIEW IF EXISTS v_unsanctioned_shipments;
CREATE VIEW v_unsanctioned_shipments AS
SELECT 
    tracking_code, 
    destination_country, 
    weight_kg 
FROM shipments 
WHERE destination_country NOT IN (
    SELECT country_code 
    FROM sanctioned_destinations 
    WHERE country_code IS NOT NULL
)
ORDER BY tracking_code ASC;

-- Desafío 3: Envíos sin transportista
DROP VIEW IF EXISTS v_unassigned_carriers;
CREATE VIEW v_unassigned_carriers AS
SELECT 
    tracking_code, 
    destination_country 
FROM shipments 
WHERE carrier_id IS NULL
ORDER BY tracking_code ASC;
```
</details>
