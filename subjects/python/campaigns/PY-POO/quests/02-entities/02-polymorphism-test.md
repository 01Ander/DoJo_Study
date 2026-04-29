# Ejercicio 02-02: Polymorphism Test (Tipo B - Nivel 2)

**Objetivo:** Implementar comportamiento polimórfico guiado por un test.

## Tu Tarea
Observa el test para un sistema de empleados.

```python
def test_employee_bonus_calculation():
    dev = Developer(name="Ana", salary=1000)
    manager = Manager(name="Bob", salary=1000)
    
    # Developers get 10% bonus, Managers get 20%
    assert dev.calculate_bonus() == 100.0
    assert manager.calculate_bonus() == 200.0
```

Crea `employee.py` en esta carpeta e implementa la clase base `Employee` (como Abstract Base Class) y las hijas `Developer` y `Manager` para que el test tenga sentido lógico.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
        
    @abstractmethod
    def calculate_bonus(self) -> float:
        pass

class Developer(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.10

class Manager(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.20
```
</details>
