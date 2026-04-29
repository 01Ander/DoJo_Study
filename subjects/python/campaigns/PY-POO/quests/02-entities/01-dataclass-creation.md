# Ejercicio 02-01: Dataclass Creation (Tipo A)

**Objetivo:** Usar `@dataclass` para crear entidades de dominio seguras.

## Contexto (Domain Shifting: RPG Inventory)
Tienes que modelar ítems en un inventario de un videojuego.

## Tu Tarea
Dentro de esta carpeta (`quests/02-entities/`), crea `inventory.py`:

1. Importa `dataclass`.
2. Crea una dataclass `Weapon` con: `name` (str), `damage` (int), `durability` (float).
3. Crea una dataclass `Potion` con: `name` (str), `healing_power` (int).

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from dataclasses import dataclass

@dataclass
class Weapon:
    name: str
    damage: int
    durability: float

@dataclass
class Potion:
    name: str
    healing_power: int
```
</details>
