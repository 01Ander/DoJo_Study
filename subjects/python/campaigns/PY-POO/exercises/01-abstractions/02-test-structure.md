# Ejercicio 01-02: Test Structure (Tipo B - Nivel 2)

**Objetivo:** Transicionar de solo "leer" a "escribir la estructura básica" de un test (Arrange, Act, Assert).

## Contexto
Basándote en las clases `PaymentProcessor` que acabas de construir en el ejercicio 01.

## Tu Tarea
Crea un archivo `test_payment.py`. Tu tarea es llenar las líneas que faltan en la estructura del test para validar que el `CreditCardProcessor` funciona correctamente. 

*Tip: No necesitas importar pytest a menos que uses sus funciones avanzadas (como `pytest.raises`). En Python básico, la palabra reservada `assert` es suficiente para validar un comportamiento.*

### Completa el código:
```python
from payment_gateway import CreditCardProcessor

def test_credit_card_processor_returns_true():
    # 1. ARRANGE (Instanciar la clase)
    processor = ________
    
    # 2. ACT (Llamar al método de pago con monto 100.0)
    result = ________
    
    # 3. ASSERT (Verificar que el resultado sea True)
    assert result ________
```

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from payment_gateway import CreditCardProcessor

def test_credit_card_processor_returns_true():
    # 1. ARRANGE
    processor = CreditCardProcessor()
    
    # 2. ACT
    result = processor.process_payment(100.0)
    
    # 3. ASSERT
    assert result is True
```
</details>
