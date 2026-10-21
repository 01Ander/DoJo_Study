# Ejercicio 06-03: De Dataclass a Pydantic BaseModel (Tipo A)

**Objetivo:** Migrar una entidad basada en `@dataclass` vulnerable a un modelo Pydantic V2 (`BaseModel`) utilizando restricciones declarativas con `Field` (Lore 06B §2 y §3).

---

## Contexto: Blindaje de Cuentas de Usuario

En el sistema heredado, la entidad de cuenta de usuario estaba definida como una `@dataclass` sin validación en tiempo de ejecución:

```python
# ❌ Modelo vulnerable: acepta datos corruptos sin protestar
from dataclasses import dataclass

@dataclass
class UserAccount:
    username: str
    age: int
    balance: float
    is_active: bool = True
```

Si una API externa envía `username=""`, `age=-5` o `balance=-1000.0`, la `@dataclass` lo acepta silenciosamente.

---

## Tu Tarea (Carril A - Operador)

En [`user_account_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py):

1. Sustituye la `@dataclass` haciendo que `UserAccount` herede de `pydantic.BaseModel`.
2. Aplica las restricciones declarativas con `Field`:
   * `username: str`: Debe tener al menos 3 caracteres (`min_length=3`).
   * `age: int`: Debe ser mayor o igual a 18 años (`ge=18`).
   * `balance: float`: No puede ser negativo; debe ser mayor o igual a 0.0 (`ge=0.0`).
   * `is_active: bool`: Debe tener valor por defecto `True`.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/06-logging/test_user_account_schema.py -v
```
El ejercicio se considera superado cuando los 5 tests pasen con **`exit code 0`**.
