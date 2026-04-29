# Capítulo 02: Domain Entities y Polimorfismo

Cuando construimos software, representamos conceptos del mundo real (Usuarios, Transacciones, Productos). A estos los llamamos **Entidades de Dominio**.

Tradicionalmente, en Python usaríamos diccionarios, pero estos son frágiles. Las clases nos permiten asegurar el tipo y darles comportamiento polimórfico.

## 1. El Problema de los Diccionarios

```python
# Un jugador de RPG
player = {"name": "Ander", "health": 100, "role": "Mage"}
# ¿Qué pasa si hago player["healt"] = 90? (Typo en la llave). Python lo permite silenciosamente.
```

## 2. Domain Entities Clásicas y `@dataclass`

Podemos crear una clase normal con `__init__`, pero cuando solo necesitamos almacenar datos puros, Python nos da una herramienta mágica: `@dataclass`.

```python
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    health: int
    role: str

# El __init__ se genera solo
p1 = Player(name="Ander", health=100, role="Mage")
# p1.healt = 90 # Muchos IDEs y mypy te avisarán del error aquí.
```

## 3. Polimorfismo

El polimorfismo es la capacidad de objetos de diferentes clases de responder al mismo método de forma distinta. Esto es vital para las entidades de dominio.

Imagina un sistema de biblioteca:

```python
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    @abstractmethod
    def get_checkout_duration(self) -> int:
        pass

class Book(LibraryItem):
    def get_checkout_duration(self) -> int:
        return 14 # 14 días para libros

class DVD(LibraryItem):
    def get_checkout_duration(self) -> int:
        return 3 # 3 días para DVDs
```

Si tenemos una lista de `LibraryItem`s, podemos iterar y llamar a `get_checkout_duration()` sin importar qué tipo exacto sea.

## 4. Conexión con Testing (Nivel 2)

Probar polimorfismo implica asegurar que cada subclase retorna su valor específico.

```python
def test_dvd_checkout_duration_is_3_days():
    dvd = DVD()
    assert dvd.get_checkout_duration() == 3
```

## 5. Setup y Ejecución

No requieres dependencias externas. El módulo `dataclasses` viene incluido en Python 3.7+.

## 6. Mapa de Ejercicios

Dirígete a `quests/02-entities/` y completa:

```text
PY-POO/quests/02-entities/
├── 01-dataclass-creation.md      (Tipo A: Implementación Base)
└── 02-polymorphism-test.md       (Tipo B: Testing Nivel 2)
```
