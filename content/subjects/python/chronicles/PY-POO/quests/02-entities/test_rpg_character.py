import pytest
from rpg_character import Character, Mage, Warrior


def test_character_base_initialization_and_damage():
    hero = Character("Arthur", 100)
    assert hero.name == "Arthur"
    assert hero.health == 100
    assert hero.is_alive() is True

    hero.take_damage(40)
    assert hero.health == 60
    assert hero.is_alive() is True

    hero.take_damage(100)
    assert hero.health == 0
    assert hero.is_alive() is False


def test_mage_uses_super_and_manages_mana():
    mage = Mage("Merlin", 80, 50)
    # Verifica que super().__init__() haya asignado name y health en la clase base
    assert mage.name == "Merlin"
    assert mage.health == 80
    assert mage.mana == 50
    assert isinstance(mage, Character)

    # Lanzamiento exitoso
    assert mage.cast_spell(30) is True
    assert mage.mana == 20

    # Maná insuficiente
    assert mage.cast_spell(30) is False
    assert mage.mana == 20


def test_warrior_uses_super_and_absorbs_damage_with_shield():
    warrior = Warrior("Conan", 120, 30)
    assert warrior.name == "Conan"
    assert warrior.health == 120
    assert warrior.shield == 30
    assert isinstance(warrior, Character)

    # Daño absorbido parcialmente por el escudo
    warrior.take_damage(20)
    assert warrior.shield == 10
    assert warrior.health == 120

    # Daño que rompe el escudo y afecta la vida vía super().take_damage()
    warrior.take_damage(25)  # 10 de escudo + 15 a vida
    assert warrior.shield == 0
    assert warrior.health == 105
