# Ejercicio 05-01: Fixture Creation (Nivel 3)

**Objetivo:** Crear un fixture para eliminar redundancia de inicialización en múltiples tests.

## Contexto (Domain Shifting: Redes Sociales)
Tienes una clase `UserProfile` que maneja seguidores.

```python
class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.followers = 0
        
    def add_follower(self):
        self.followers += 1
```

## Tu Tarea
Crea un archivo `test_profile.py`.

1. Importa `pytest` y la clase `UserProfile`.
2. Escribe una función fixture llamada `new_profile` decorada con `@pytest.fixture` que devuelva una instancia de `UserProfile("john_doe")`.
3. Completa los dos tests inyectando el fixture como parámetro.

### Código Base a completar:
```python
import pytest
from profile import UserProfile

# 1. Escribe el fixture aquí
________
________
________

# 2. Inyecta el fixture
def test_initial_followers_is_zero(________):
    assert ________.followers == 0

# 3. Inyecta el fixture
def test_add_follower_increases_count(________):
    ________.add_follower()
    assert ________.followers == 1
```

*Instala pytest localmente si no lo has hecho, y corre `pytest test_profile.py -v`.*

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
import pytest
from profile import UserProfile

@pytest.fixture
def new_profile():
    return UserProfile("john_doe")

def test_initial_followers_is_zero(new_profile):
    assert new_profile.followers == 0

def test_add_follower_increases_count(new_profile):
    new_profile.add_follower()
    assert new_profile.followers == 1
```
</details>
