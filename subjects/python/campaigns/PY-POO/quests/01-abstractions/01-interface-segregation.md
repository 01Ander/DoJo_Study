# Ejercicio 01-01: Interface Segregation (Tipo A)

**Objetivo:** Crear una clase abstracta y forzar su cumplimiento.

## Contexto (Domain Shifting: Pagos)
Estás diseñando una pasarela de pagos. Diferentes métodos de pago requieren diferentes lógicas, pero todos deben procesar un monto.

## Tu Tarea
Crea un archivo `payment_gateway.py`.

1. Importa `ABC` y `abstractmethod` del módulo `abc`.
2. Crea una clase abstracta `PaymentProcessor(ABC)` con un método abstracto `process_payment(self, amount: float) -> bool`.
3. Crea dos clases concretas que hereden de `PaymentProcessor`:
   - `CreditCardProcessor`: Su método `process_payment` imprime `"Procesando Tarjeta de Crédito por $X"` y retorna True.
   - `PayPalProcessor`: Su método `process_payment` imprime `"Redirigiendo a PayPal por $X"` y retorna True.
4. Intenta crear una tercera clase `BitcoinProcessor` que herede de la clase abstracta pero **olvida intencionalmente** implementar `process_payment`. Intenta instanciarla y observa el `TypeError`.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Procesando Tarjeta de Crédito por ${amount}")
        return True

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Redirigiendo a PayPal por ${amount}")
        return True

# class BitcoinProcessor(PaymentProcessor):
#     pass
# btc = BitcoinProcessor() # Lanza TypeError
```
</details>
