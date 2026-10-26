# Ejercicio 03-03: Agregaciones Condicionales con `CASE WHEN` (Nivel 4)

**Objetivo:** Dominar el patrón analítico de agregaciones condicionales (`SUM(CASE WHEN...)`) para realizar pivoteo horizontal de estados y cálculo de KPIs de conversión en un solo escaneo lineal de tabla (Lore 03 §7).

---

## Contexto de Negocio (Domain Shifting: Pasarela de Pagos FinTechPay)

La pasarela de pagos **FinTechPay** procesa transacciones para múltiples comercios asociados (*merchants*). El equipo de Finanzas y Analytics necesita reportes ejecutivos consolidados por comercio que muestren cómo se distribuyen las órdenes entre estados y métodos de pago:
- Ciertas órdenes se completan con éxito (`COMPLETED`).
- Otras son rechazadas por fondos insuficientes o fraude (`FAILED`).
- Otras son devueltas por disputas o retracto del cliente (`REFUNDED`).

El requerimiento arquitectónico es calcular todas las métricas en **una sola pasada sobre los datos** (`GROUP BY merchant_id`), sin realizar múltiples subconsultas costosas ni `JOINs` redundantes.

---

## Archivo de Trabajo

Edita el archivo [`conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql).

El script ya crea la tabla `orders` y los datos de prueba iniciales. Debes reemplazar los `SELECT` provisionales de las dos vistas analíticas:

### 1. Desafío 1: Pivoteo Horizontal de Estados (`v_merchant_status_pivot`)
Agrupa por `merchant_id` y calcula:
* `merchant_id`: Identificador del comercio.
* `total_orders`: Total general de órdenes del comercio (`COUNT(*)`).
* `completed_orders`: Conteo de órdenes cuyo estado es `'COMPLETED'` (`SUM(CASE WHEN order_status = 'COMPLETED' THEN 1 ELSE 0 END)`).
* `failed_orders`: Conteo de órdenes cuyo estado es `'FAILED'`.
* `refunded_orders`: Conteo de órdenes cuyo estado es `'REFUNDED'`.
* `total_completed_amount`: Suma del campo `amount` **únicamente** para aquellas órdenes con estado `'COMPLETED'` (`SUM(CASE WHEN order_status = 'COMPLETED' THEN amount ELSE 0.0 END)`).
* **Ordenamiento:** `ORDER BY merchant_id ASC`.

### 2. Desafío 2: Métricas de Canal y Tasa de Éxito (`v_merchant_payment_breakdown`)
Agrupa por `merchant_id` y calcula:
* `merchant_id`: Identificador del comercio.
* `credit_card_orders`: Conteo de órdenes pagadas con tarjeta (`payment_method = 'CREDIT_CARD'`).
* `crypto_orders`: Conteo de órdenes pagadas en cripto (`payment_method = 'CRYPTO'`).
* `success_rate_pct`: Porcentaje de órdenes completadas sobre el total, redondeado a 1 decimal:
  $$\text{success\_rate\_pct} = \text{ROUND}\left( \frac{\sum (\text{COMPLETED})}{\text{total}} \times 100.0, 1 \right)$$
  *(⚠️ Recuerda usar `1.0` en el numerador o multiplicar por `100.0` para forzar aritmética en punto flotante y evitar división entera a cero).*
* **Ordenamiento:** `ORDER BY merchant_id ASC`.

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas unitarias:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/test_conditional_aggregations.py -v
```
*(Criterio de éxito: 2 passed con exit code 0).*

También puedes verificar la validez sintáctica de todo el script SQL con el runner agnóstico del DoJo:
```bash
python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql
```

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```sql
-- Desafío 1: Pivoteo de Estados
DROP VIEW IF EXISTS v_merchant_status_pivot;
CREATE VIEW v_merchant_status_pivot AS
SELECT 
    merchant_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN order_status = 'FAILED' THEN 1 ELSE 0 END) AS failed_orders,
    SUM(CASE WHEN order_status = 'REFUNDED' THEN 1 ELSE 0 END) AS refunded_orders,
    SUM(CASE WHEN order_status = 'COMPLETED' THEN amount ELSE 0.0 END) AS total_completed_amount
FROM orders
GROUP BY merchant_id
ORDER BY merchant_id ASC;

-- Desafío 2: Métricas de Canal y Conversión
DROP VIEW IF EXISTS v_merchant_payment_breakdown;
CREATE VIEW v_merchant_payment_breakdown AS
SELECT 
    merchant_id,
    SUM(CASE WHEN payment_method = 'CREDIT_CARD' THEN 1 ELSE 0 END) AS credit_card_orders,
    SUM(CASE WHEN payment_method = 'CRYPTO' THEN 1 ELSE 0 END) AS crypto_orders,
    ROUND(
        SUM(CASE WHEN order_status = 'COMPLETED' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 
        1
    ) AS success_rate_pct
FROM orders
GROUP BY merchant_id
ORDER BY merchant_id ASC;
```
</details>
