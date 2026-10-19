"""
Módulo rpg_character.py — Quest 02-03: Herencia Compuesta y Constructores con super()

Completa las clases Character, Mage y Warrior respetando los contratos y delegación.
"""


class Character:
    """Clase base de personaje."""

    def __init__(self, name: str, health: int):
        # TODO: Asignar name y health
        pass

    def take_damage(self, amount: int) -> None:
        # TODO: Reducir health por amount. No permitir valores negativos (mínimo 0).
        pass

    def is_alive(self) -> bool:
        # TODO: Retornar True si health > 0, False de lo contrario.
        pass


class Mage(Character):
    """Subclase de mago con recurso de maná."""

    def __init__(self, name: str, health: int, mana: int):
        # TODO: Invocar al constructor padre con super().__init__(...)
        # TODO: Inicializar self.mana
        pass

    def cast_spell(self, cost: int) -> bool:
        # TODO: Si mana >= cost, restar cost y retornar True. Sino, retornar False.
        pass


class Warrior(Character):
    """Subclase de guerrero con escudo protector."""

    def __init__(self, name: str, health: int, shield: int):
        # TODO: Invocar al constructor padre con super().__init__(...)
        # TODO: Inicializar self.shield
        pass

    def take_damage(self, amount: int) -> None:
        # TODO: Reducir primero el escudo. Si sobra daño, llamar a super().take_damage(...)
        pass
