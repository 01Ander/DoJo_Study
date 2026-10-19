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
# Ojo: En runtime, una @dataclass estándar usa __dict__ y permite p1.healt = 90 silenciosamente.
# Para forzar la protección estricta contra typos en ejecución, se usa @dataclass(slots=True),
# lo cual elimina __dict__, ahorra memoria y detona AttributeError ante cualquier atributo dinámico.
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

## 4. Herencia Compuesta y Delegación con `super()`

Cuando una subclase hereda de una clase base pero necesita **atributos adicionales propios**, debemos definir su propio método `__init__`.

### El Antipatrón: Duplicar la Inicialización
Un error común de principiante es volver a asignar manualmente los atributos que ya pertenecen a la clase padre:

```python
# ❌ MAL: Viola el principio DRY (Don't Repeat Yourself) y rompe la encapsulación
class ElectronicBook(LibraryItem):
    def __init__(self, title: str, author: str, file_size_mb: float):
        self.title = title          # ❌ Duplicado de la clase base
        self.author = author        # ❌ Duplicado de la clase base
        self.file_size_mb = file_size_mb
```
Si mañana la clase base agrega validaciones (ej. verificar que `title` no esté vacío), la subclase se salta esas reglas y queda desincronizada.

### La Solución Idiomática: Delegar con `super().__init__()`
La función `super()` devuelve un objeto proxy que nos permite invocar los métodos de la clase base. De este modo, delegamos la inicialización común al ancestro y nos enfocamos únicamente en los atributos nuevos:

```python
# ✅ BIEN: Delegación limpia y robusta
class ElectronicBook(LibraryItem):
    def __init__(self, title: str, author: str, file_size_mb: float):
        # 1. Delegamos los atributos heredados al constructor del padre
        super().__init__(title=title, author=author)
        
        # 2. Asignamos exclusivamente lo específico de la subclase
        self.file_size_mb = file_size_mb

    def get_checkout_duration(self) -> int:
        return 21 # 21 días para libros electrónicos
```

### Reglas de Oro con `super()`:
1. **Llamar a `super().__init__()` primero:** Asegura que el estado base del objeto esté completamente inicializado antes de que la subclase ejecute su lógica especializada.
2. **Pasar los argumentos requeridos:** La llamada a `super().__init__(...)` debe satisfacer exactamente la firma que la clase padre espera.

---

## 5. Conexión con Testing (Nivel 2)

Probar polimorfismo y herencia compuesta implica verificar dos cosas:
1. Que los atributos heredados y propios se asignen correctamente.
2. Que cada subclase retorne su valor específico al invocar métodos comunes.

```python
def test_dvd_checkout_duration_is_3_days():
    dvd = DVD()
    assert dvd.get_checkout_duration() == 3

def test_ebook_inherits_and_extends_attributes():
    ebook = ElectronicBook(title="Clean Code", author="Robert Martin", file_size_mb=4.5)
    assert ebook.title == "Clean Code"
    assert ebook.file_size_mb == 4.5
    assert ebook.get_checkout_duration() == 21
```

## 6. Setup y Ejecución

No requieres dependencias externas. El módulo `dataclasses` y la función `super()` vienen incluidos de forma nativa en Python.

## 7. Mapa de Ejercicios

Dirígete a `quests/02-entities/` y completa:

- [[01-dataclass-creation]]
- [[02-polymorphism-test]]
- [[03-inheritance-super]]

```text
PY-POO/quests/02-entities/
├── [[01-dataclass-creation]].md      (Tipo A: Implementación Base)
├── [[02-polymorphism-test]].md       (Tipo B: Testing Nivel 2)
└── [[03-inheritance-super]].md       (Tipo A: Herencia y Constructores super())
```
