# Ejercicio 06-02: Test Exceptions (Tipo B - Nivel 2)

**Objetivo:** Testear que una excepción se lanza correctamente usando pytest.

## Tu Tarea
Observa el código y complétalo en `test_payments.py` en esta misma carpeta.

```python
import pytest
# from payments import PaymentProcessor, ExpiredCardError

def test_charge_raises_error_for_old_cards():
    processor = PaymentProcessor()
    
    # GIVEN / WHEN / THEN: Queremos asegurar que se lanza ExpiredCardError
    with pytest._______(ExpiredCardError):
        processor.charge(2020)
```

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
import pytest
from payments import PaymentProcessor, ExpiredCardError

def test_charge_raises_error_for_old_cards():
    processor = PaymentProcessor()
    
    with pytest.raises(ExpiredCardError):
        processor.charge(2020)
```
</details>
