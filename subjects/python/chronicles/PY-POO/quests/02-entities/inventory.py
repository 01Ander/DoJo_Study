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


if __name__ == "__main__":
    sword = Weapon(name="Sting", damage=20, durability=25.5)
    small_potion = Potion(name='Potion Small', healing_power=5)
    sword.nam = "Scalibur"
    print(sword, small_potion)
