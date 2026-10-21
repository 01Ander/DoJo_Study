# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-19  
> **Materia Activa:** `02-py-poo` (Python Orientado a Objetos & TDD)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

| Tarea ID | Materia | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|
| **`PY-010`** | `02-py-poo` | Constructores con `super()` | [`quests/02-entities/rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py) | `pytest quests/02-entities/test_rpg_character.py` | 🟢 **COMPLETADO** |
| **`PY-011.1`** | `02-py-poo` | De Dataclass a Pydantic con `Field` | [`quests/06-logging/user_account_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py) | `pytest quests/06-logging/test_user_account_schema.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-011.2`** | `02-py-poo` | Validadores de Negocio y Excepciones | [`quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) | `pytest quests/06-logging/test_transaction_schema.py` | ⏳ En espera (Paso 2) |
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | *Próximamente en quests/04-orchestration/* | — | ⏳ En espera |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado | *Próximamente en quests/01-abstractions/* | — | ⏳ En espera |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-011.1` — De Dataclass a Pydantic BaseModel con `Field`

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/03-dataclass-to-pydantic.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/03-dataclass-to-pydantic.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md) (Capítulo completo dedicado)

### 📋 El Contrato que debes cumplir:

1. **`UserAccount(BaseModel)`:**
   * Hereda de `pydantic.BaseModel`.
   * Campos y restricciones requeridas:
     * `username: str`: Longitud mínima de 3 caracteres (`Field(min_length=3)`).
     * `age: int`: Mayor o igual a 18 años (`Field(ge=18)`).
     * `balance: float`: No negativo, mayor o igual a 0.0 (`Field(ge=0.0)`).
     * `is_active: bool`: Valor por defecto `True`.

---

### 💡 Ejemplo con Domain Shifting (Especificación de Naves Espaciales):
*Observa cómo sustituir una dataclass por `BaseModel` con `Field` aplica restricciones declarativas sin necesidad de escribir métodos `__post_init__`:*

```python
from pydantic import BaseModel, Field, ValidationError

class StarshipSpec(BaseModel):
    model_name: str = Field(min_length=2)
    crew_capacity: int = Field(ge=1)
    warp_factor: float = Field(ge=0.0, le=9.9)
    hyperdrive_ready: bool = True

# Coerción exitosa: convierte string "5" en int 5
ship = StarshipSpec(model_name="NX-01", crew_capacity="5", warp_factor=5.2)
assert ship.crew_capacity == 5

# Falla inmediata ante datos fuera de rango:
try:
    bad_ship = StarshipSpec(model_name="X", crew_capacity=0, warp_factor=15.0)
except ValidationError as e:
    print(f"Especificación rechazada: {e.errors()}")
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/06-logging/test_user_account_schema.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema para que sepas exactamente qué ha cambiado:

* `content/subjects/python/chronicles/PY-POO/rite/pyproject.toml` y `requirements.txt`:
  * *Cambio:* Declaradas formalmente las dependencias canónicas del entorno (`pytest`, `pydantic>=2.8.0`, `mypy`).
* `content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md`:
  * *Cambio:* Capítulo teórico completo dedicado a la evolución desde `@dataclass`, explicación detallada de cada módulo de Pydantic V2 y su rol en la frontera del sistema.
* `content/subjects/python/chronicles/PY-POO/lore/06-logging-and-error-handling.md`:
  * *Cambio:* Vinculación al Cap 06B y mapa actualizado de 4 ejercicios.
* `content/subjects/python/chronicles/PY-POO/chronicle.md`:
  * *Cambio:* Enlace directo al nuevo Cap 06B en el índice curricular.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/03-dataclass-to-pydantic.md`:
  * *Cambio:* Enunciado de la Quest 06-03 (Paso 1: Migración a `BaseModel` con `Field`).
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de campos.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/test_user_account_schema.py`:
  * *Cambio:* Suite evaluadora automatizada con 5 tests unitarios para Quest 06-03.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/04-pydantic-domain-exceptions.md` & `test_transaction_schema.py`:
  * *Cambio:* Preparado para el Paso 2 (Validadores `@field_validator` y traducción a excepciones de negocio).


