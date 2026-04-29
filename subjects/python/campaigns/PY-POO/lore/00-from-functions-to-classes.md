# Capítulo 00: From Functions to Classes

Bienvenido al paradigma Orientado a Objetos (OOP). Hasta ahora, has escrito scripts procedimentales: datos por un lado, funciones por el otro. Las funciones reciben datos, los transforman y los devuelven.

En OOP, **fusionamos el estado (datos) y el comportamiento (funciones)** en una sola entidad llamada "Objeto".

## 1. El Problema de las Funciones Aisladas

Imagina un sistema de reservas de hotel hecho con diccionarios y funciones:

```python
# Estado (Datos)
room_101 = {"number": 101, "is_booked": False, "price": 150.0}

# Comportamiento (Función)
def book_room(room: dict) -> bool:
    if not room["is_booked"]:
        room["is_booked"] = True
        return True
    return False

# Ejecución
book_room(room_101)
```

**Problema:** Cualquier otra parte del código puede modificar `room_101["is_booked"] = "patata"` accidentalmente. No hay protección. No hay garantía de que el diccionario tenga la llave `"price"`.

## 2. La Solución: Clases y Objetos

Una clase es un "molde" o "plano". Define exactamente qué datos debe tener un objeto y qué acciones puede realizar.

```python
class HotelRoom:
    # 1. El Constructor (__init__)
    # Se ejecuta automáticamente al crear un nuevo cuarto
    def __init__(self, number: int, price: float):
        # self representa al objeto individual que se está creando
        self.number = number
        self.price = price
        self.is_booked = False  # Estado por defecto
        
    # 2. Métodos de Instancia
    # Funciones que le pertenecen al objeto
    def book(self) -> bool:
        if not self.is_booked:
            self.is_booked = True
            return True
        return False
```

### ¿Qué es `self`?
`self` es la referencia al objeto específico. Si creamos el cuarto 101 y el cuarto 205, `self` asegura que al llamar a `cuarto_101.book()`, se marque como ocupado el 101 y no el 205. **Siempre** debe ser el primer parámetro de un método de instancia en Python.

### Instanciando (Usando el molde)

```python
# Creamos objetos (Instancias de la clase)
room_101 = HotelRoom(number=101, price=150.0)
room_205 = HotelRoom(number=205, price=300.0)

# Usamos sus métodos
success = room_101.book()
print(f"Room 101 booked: {success}") # True
print(f"Room 205 booked: {room_205.is_booked}") # False
```

## 3. Conexión con Testing (Nivel 1: Leer un test)

En TDD (Test-Driven Development), probamos que el comportamiento de la clase sea exacto.

```python
def test_hotel_room_booking_flow():
    # GIVEN: Un cuarto de hotel disponible (Arrange)
    room = HotelRoom(number=101, price=150.0)
    assert room.is_booked is False
    
    # WHEN: Intentamos reservarlo (Act)
    result = room.book()
    
    # THEN: La reserva es exitosa y el cuarto queda ocupado (Assert)
    assert result is True
    assert room.is_booked is True
```
> Nota cómo instanciamos la clase dentro del test, operamos sobre ella y verificamos su estado interno (`room.is_booked`).

---

## 4. Setup y Ejecución

No requieres dependencias externas para este capítulo. Solo Python puro.
Si vas a correr los tests, asegúrate de tener pytest instalado (lo instalaremos formalmente en el Cap 05).

**Comando de verificación:**
```bash
python --version
# Output esperado: Python 3.10 o superior
```

## 5. Mapa de Ejercicios

Ahora, dirígete a `quests/00-classes/` y completa los ejercicios en orden:

```text
PY-POO/quests/00-classes/
├── 01-concept-modeling.md  (Tipo A: Implementación Base)
└── 02-test-reading.md      (Tipo B: Testing Nivel 1)
```
