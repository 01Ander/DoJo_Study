# Ejercicio 02-03: Herencia Compuesta y Constructores con `super()` (Tipo A)

**Objetivo:** Implementar jerarquías de clases donde las subclases extienden la inicialización del padre mediante `super().__init__()` sin duplicación de código (Lore 02 §4).

---

## Contexto (Domain Shifting: Gremio de Exploradores RPG)

En un juego de rol táctico, todos los personajes comparten atributos vitales básicos (`name` y `health`), pero las clases especializadas poseen recursos mágicos o de combate adicionales:

1. **`Character` (Clase Base):**
   - Constructor: Recibe `name: str` y `health: int`.
   - Método `take_damage(self, amount: int)`: Reduce `self.health` por `amount`. Si la vida cae por debajo de 0, queda fijada en 0.
   - Método `is_alive(self) -> bool`: Retorna `True` si `self.health > 0`, de lo contrario `False`.

2. **`Mage` (Subclase de `Character`):**
   - Constructor: Recibe `name: str`, `health: int` y `mana: int`.
   - **Regla:** Debe inicializar `name` y `health` llamando a `super().__init__(name, health)`, y asignar `self.mana = mana`.
   - Método `cast_spell(self, cost: int) -> bool`: Si `self.mana >= cost`, resta `cost` a `self.mana` y retorna `True`. Si no alcanza, retorna `False` sin descontar maná.

3. **`Warrior` (Subclase de `Character`):**
   - Constructor: Recibe `name: str`, `health: int` y `shield: int`.
   - **Regla:** Debe inicializar `name` y `health` llamando a `super().__init__(name, health)`, y asignar `self.shield = shield`.
   - Sobrescritura de `take_damage(self, amount: int)`: El daño impacta primero al escudo (`self.shield`). Si el daño supera el escudo, el remanente reduce la vida llamando a `super().take_damage(remanente)`, y el escudo queda en 0.

---

## Tu Tarea (Carril A - Operador)

Edita el archivo [`rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py) completando las clases `Character`, `Mage` y `Warrior` según las especificaciones.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest quests/02-entities/test_rpg_character.py -v
```
El ejercicio se considera superado cuando los 4 tests pasen con **`exit code 0`**.
