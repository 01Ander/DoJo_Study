# Ejercicio 06-01: Custom Exceptions (Tipo A)

**Objetivo:** Crear y lanzar una excepción de dominio.

## Contexto (Domain Shifting: Pagos)
Tu procesador de pagos no admite tarjetas expiradas.

## Tu Tarea
En `exercises/06-logging/`, crea `payments.py`:
1. Define una excepción personalizada vacía `ExpiredCardError`.
2. Crea una clase `PaymentProcessor` con un método `charge(self, card_year: int)`.
3. Si `card_year` es menor a 2024, lanza tu `ExpiredCardError`. De lo contrario, retorna `True`.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
class ExpiredCardError(Exception):
    pass

class PaymentProcessor:
    def charge(self, card_year: int):
        if card_year < 2024:
            raise ExpiredCardError("La tarjeta está expirada.")
        return True
```
</details>
