# Ejercicio 00-02: Test Reading (Tipo B - Nivel 1)

**Objetivo:** Acostumbrar al ojo a leer la sintaxis de `pytest` (GIVEN/WHEN/THEN) sin la carga cognitiva de escribirlo desde cero.

## Tu Tarea
Observa el siguiente test unitario diseñado para una clase `BankAccount`. Tu tarea es leerlo, deducir qué hace la clase y **escribir la implementación de la clase para que el test pase**.

### El Test:
```python
def test_bank_account_deposit_and_withdraw():
    # GIVEN
    account = BankAccount(owner="Ander", initial_balance=100.0)
    
    # WHEN
    account.deposit(50.0)
    success = account.withdraw(30.0)
    failed = account.withdraw(500.0) # Insufficient funds
    
    # THEN
    assert success is True
    assert failed is False
    assert account.balance == 120.0
```

Crea el archivo `bank_account.py` en esta carpeta e implementa la clase `BankAccount` con los métodos deducidos. No es necesario ejecutar pytest, solo comprobar lógicamente.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner
        self.balance = initial_balance
        
    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
            
    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
```
</details>
