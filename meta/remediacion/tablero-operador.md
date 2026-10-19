# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-19  
> **Materia Activa:** `02-py-poo` (Python Orientado a Objetos & TDD)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

| Tarea ID | Materia | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|
| **`PY-010`** | `02-py-poo` | Constructores con `super()` | [`quests/02-entities/rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py) | `pytest quests/02-entities/test_rpg_character.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-011`** | `02-py-poo` | Validación con Pydantic | *Próximamente en quests/06-logging/* | — | ⏳ En espera |
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | *Próximamente en quests/04-orchestration/* | — | ⏳ En espera |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado | *Próximamente en quests/01-abstractions/* | — | ⏳ En espera |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-010` — Constructores con `super()`

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/02-entities/03-inheritance-super.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/03-inheritance-super.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/02-domain-entities-and-dataclasses.md` (Sección 4)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/02-domain-entities-and-dataclasses.md)

### 📋 El Contrato que debes cumplir:
1. **`Character` (Clase Base):**
   * `__init__(self, name: str, health: int)`: Inicializa `self.name` y `self.health`.
   * `take_damage(self, amount: int) -> None`: Reduce la vida en `amount`. Si la vida cae por debajo de 0, queda en `0`.
   * `is_alive(self) -> bool`: Retorna `True` si `self.health > 0`, sino `False`.
2. **`Mage` (Hereda de `Character`):**
   * `__init__(self, name: str, health: int, mana: int)`: **Debe llamar a `super().__init__(name, health)`** e inicializar `self.mana = mana`.
   * `cast_spell(self, cost: int) -> bool`: Si `self.mana >= cost`, descuenta `cost` del maná y retorna `True`. Si no alcanza, retorna `False` sin descontar maná.
3. **`Warrior` (Hereda de `Character`):**
   * `__init__(self, name: str, health: int, shield: int)`: **Debe llamar a `super().__init__(name, health)`** e inicializar `self.shield = shield`.
   * `take_damage(self, amount: int) -> None`: El daño impacta primero al escudo (`self.shield`). Si el daño supera el escudo, el remanente reduce la vida llamando a `super().take_damage(remanente)` y el escudo queda en `0`.

---

### 💡 Ejemplo con Domain Shifting (Flota Espacial):
*Observa cómo la subclase delega la inicialización base al padre y cómo reutiliza su comportamiento:*

```python
class Spaceship:
    def __init__(self, code: str, hull_integrity: int):
        self.code = code
        self.hull_integrity = hull_integrity

    def take_hit(self, damage: int) -> None:
        self.hull_integrity = max(0, self.hull_integrity - damage)

class StealthCorvette(Spaceship):
    def __init__(self, code: str, hull_integrity: int, cloak_energy: int):
        # 1. Delegamos al constructor del ancestro:
        super().__init__(code=code, hull_integrity=hull_integrity)
        # 2. Inicializamos lo exclusivo de la subclase:
        self.cloak_energy = cloak_energy

    def activate_cloak(self) -> bool:
        if self.cloak_energy >= 15:
            self.cloak_energy -= 15
            return True
        return False
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/02-entities/test_rpg_character.py -v
```
*(Criterio de éxito: 3 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema para que sepas exactamente qué ha cambiado:

* `content/subjects/python/chronicles/PY-POO/lore/02-domain-entities-and-dataclasses.md`:
  * *Cambio:* Añadida la Sección 4 sobre Herencia Compuesta y uso correcto de `super().__init__()`.
* `content/subjects/python/chronicles/PY-POO/quests/02-entities/03-inheritance-super.md`:
  * *Cambio:* Enunciado didáctico de la Quest 02-03.
* `content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de método.
* `content/subjects/python/chronicles/PY-POO/quests/02-entities/test_rpg_character.py`:
  * *Cambio:* Suite evaluadora automatizada con 3 tests unitarios.
