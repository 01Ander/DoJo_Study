# Ejercicio 05-04: El Ciclo TDD Red-Green-Refactor (Nivel 4)

**Objetivo:** Vivir y ejecutar el ciclo completo de Test-Driven Development (Red-Green-Refactor) implementando la lógica de facturación de almacenamiento en la nube a partir de una suite de pruebas predefinida (Lore 05 §6).

---

## Contexto de Negocio (Domain Shifting: Facturación Cloud Multi-Tier)

Una plataforma de almacenamiento en la nube (*Object Storage Service*) factura mensualmente a sus clientes basándose en el volumen total de gigabytes (GB) consumidos, aplicando un modelo de tarifas escalonadas (*tiered pricing*) y descuentos corporativos:

1. **Validación de Integridad:** El consumo no puede ser negativo. Si `gigabytes < 0`, debe lanzar un `ValueError` con el mensaje:
   `"Storage consumption cannot be negative"`.
2. **Consumo Cero:** Si `gigabytes == 0.0`, el costo facturado debe ser exactamente `$0.00`.
3. **Nivel 1 (Estándar):** Los primeros $100$ GB se facturan a una tarifa de `$0.02` por GB.
   - Ejemplo: $50$ GB $\rightarrow 50 \times 0.02 = \$1.00$.
   - Ejemplo: $100$ GB $\rightarrow 100 \times 0.02 = \$2.00$.
4. **Nivel 2 (Excedente):** El consumo superior a $100$ GB se factura a una tarifa con descuento por volumen de `$0.015` por cada GB adicional.
   - Ejemplo: $200$ GB $\rightarrow (100 \times 0.02) + (100 \times 0.015) = 2.00 + 1.50 = \$3.50$.
5. **Descuento Enterprise:** Si la cuenta es de cliente corporativo (`is_enterprise=True`), se aplica un descuento del $10\%$ sobre el subtotal general calculado.
   - Ejemplo: $200$ GB con Enterprise $\rightarrow 3.50 \times 0.90 = \$3.15$.

---

## El Contrato de Código

Edita el archivo [`billing_service.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py) donde encontrarás la estructura inicial de la clase `StorageBillingCalculator`:

```python
class StorageBillingCalculator:
    TIER_1_RATE: float = 0.02
    TIER_2_RATE: float = 0.015
    TIER_1_LIMIT: float = 100.0
    ENTERPRISE_DISCOUNT: float = 0.10

    def calculate_invoice(self, gigabytes: float, is_enterprise: bool = False) -> float:
        ...
```

---

## Las Tres Fases de tu Misión TDD

### Fase 1: 🔴 RED (Confirmar el Fallo)
Ejecuta la suite de pruebas antes de escribir cualquier línea de lógica:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/05-testing/test_billing_service.py -v
```
*Observa cómo los 5 tests fallan.* Estás formalmente en la fase roja de TDD: el contrato existe y define el comportamiento esperado, pero el código aún no lo satisface.

### Fase 2: 🟢 GREEN (Hacer Pasar los Tests)
Abre [`billing_service.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py) e implementa la lógica mínima necesaria en `calculate_invoice` para que los 5 tests pasen a verde.
- Vuelve a ejecutar el comando de pytest.
- Criterio de éxito: `5 passed`.

### Fase 3: 🔵 REFACTOR (Pulir y Perfeccionar)
Revisa tu código en `billing_service.py`:
- ¿Usaste las constantes de clase `self.TIER_1_RATE`, `self.TIER_1_LIMIT`, etc., en lugar de números mágicos dispersos?
- ¿La lógica condicional es clara y concisa?
- Guarda tus cambios y re-ejecuta pytest. Si algo falla, el arnés de seguridad de tus tests te atrapará al instante.

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```python
# 🎯 Objetivo de Negocio: Calcular facturas de almacenamiento cloud con tarifas escalonadas y descuentos corporativos.

class StorageBillingCalculator:
    TIER_1_RATE: float = 0.02
    TIER_2_RATE: float = 0.015
    TIER_1_LIMIT: float = 100.0
    ENTERPRISE_DISCOUNT: float = 0.10

    def calculate_invoice(self, gigabytes: float, is_enterprise: bool = False) -> float:
        if gigabytes < 0:
            raise ValueError("Storage consumption cannot be negative")

        if gigabytes <= self.TIER_1_LIMIT:
            subtotal = gigabytes * self.TIER_1_RATE
        else:
            tier1_cost = self.TIER_1_LIMIT * self.TIER_1_RATE
            overage_cost = (gigabytes - self.TIER_1_LIMIT) * self.TIER_2_RATE
            subtotal = tier1_cost + overage_cost

        if is_enterprise:
            subtotal *= (1.0 - self.ENTERPRISE_DISCOUNT)

        return subtotal
```
</details>
