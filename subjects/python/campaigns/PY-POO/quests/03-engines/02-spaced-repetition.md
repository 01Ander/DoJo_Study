# Ejercicio 03-02: Spaced Repetition (Tipo B - Nivel 3)

**Objetivo:** Repasar Fixtures (Cap 05) y Dataclasses (Cap 02) aplicado a un Engine (Cap 03).

## Tu Tarea
Lee el siguiente test. Crea el fixture necesario en un archivo `test_engine.py` (usando `pytest`) y escribe la lógica de clases de negocio para que el test sea verde.

```python
import pytest
# ... importaciones

@pytest.fixture
def test_data():
    # TODO: Implementa este fixture para que retorne una lista de dos Dataclass de usuarios:
    # Uno con edad 20 y otro con edad 30
    pass

def test_engine_calculates_average_age(test_data):
    engine = UserAnalyticsEngine()
    result = engine.get_average_age(test_data)
    assert result == 25.0
```

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
import pytest
from dataclasses import dataclass

@dataclass
class User:
    age: int

class UserAnalyticsEngine:
    def get_average_age(self, users: list[User]) -> float:
        if not users: return 0.0
        return sum(u.age for u in users) / len(users)

@pytest.fixture
def test_data():
    return [User(age=20), User(age=30)]

def test_engine_calculates_average_age(test_data):
    engine = UserAnalyticsEngine()
    result = engine.get_average_age(test_data)
    assert result == 25.0
```
</details>
