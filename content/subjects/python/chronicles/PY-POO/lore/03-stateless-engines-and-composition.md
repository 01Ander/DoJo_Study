# Capítulo 03: Stateless Engines y Composición

Las Entidades de Dominio (Cap 02) guardan estado (datos). Pero las reglas de negocio complejas, las transformaciones masivas y las agregaciones no deben vivir dentro de las entidades.

Para eso usamos **Stateless Engines** (Motores sin estado).

## 1. El Problema de Acoplar Lógica al Estado

Si un `ShoppingCart` también tiene la lógica de calcular impuestos complejos consultando una API externa, la clase "hace demasiado" (Viola el principio de Responsabilidad Única - SRP de SOLID).

### Analogía 1: La Licuadora Limpia
Imagina una licuadora. Tú le metes fruta y hielo, presionas el botón, y sale un batido. La licuadora **no se queda con parte del batido adentro para la siguiente vez**. Cada vez que la usas, el resultado depende solo de lo que le metiste en ese momento. 
Si la licuadora tuviera "estado" y guardara residuos de ayer, un batido de mango hoy sabría a fresa de ayer. 

### Analogía 2: La Calculadora Básica
Si escribes `2 + 2` en una calculadora, siempre dará `4`. La calculadora no "recuerda" que ayer sumaste `10`, por lo que no te da `14`. Esa predictibilidad es lo que buscamos en el código.

## 2. La Solución: Stateless Engines

Un "Engine" o "Service" es una clase que recibe datos, los procesa y devuelve un resultado, pero **no guarda el resultado en su propio `self`**.

### Ejemplo 1: El Mal Camino (Con Estado)
```python
# ❌ Engine CON estado — peligroso y poco predecible
class TaxEngine:
    def __init__(self):
        self.last_tax = 0.0  # Guarda estado interno

    def calculate(self, price):
        self.last_tax = price * 0.19 + self.last_tax  # ¡Se contamina con llamadas pasadas!
        return self.last_tax

engine = TaxEngine()
print(engine.calculate(100))  # → 19.0 ✅
print(engine.calculate(100))  # → 38.0 ❌ ¡¿Qué?! Cada vez da un número distinto.
```

### Ejemplo 2: El Buen Camino (Sin Estado)
```python
# ✅ Engine SIN estado — predecible y seguro
class TaxEngine:
    # No hay __init__ que inicialice variables de estado
    
    def calculate(self, price):
        # La variable vive y muere dentro del método
        return price * 0.19

engine = TaxEngine()
print(engine.calculate(100))  # → 19.0
print(engine.calculate(100))  # → 19.0  ← Siempre igual. Misma entrada = Misma salida.
```

## 3. Composición (Tiene-Un) vs Herencia (Es-Un)

A menudo, los programadores novatos usan Herencia para todo ("Voy a hacer que el Carrito herede de la Calculadora para poder calcular"). Esto es un error de diseño fundamental.

### Analogía 1: El Gerente del Restaurante
Un gerente coordina al chef y al mesero. Pero el gerente no **es** un chef, ni **es** un mesero. Si usamos herencia, estaríamos diciendo "El gerente heredó la capacidad de cocinar". Si usamos Composición, decimos "El gerente **tiene a su disposición** a un chef y le pide que cocine".

### Analogía 2: El Automóvil
Un carro **tiene** un motor. Un carro no **es** un motor. Si haces `class Carro(Motor):`, estás cometiendo un error lógico. Lo correcto es que el Carro tenga un atributo que sea una instancia de Motor.

### Ejemplo de Código: Herencia vs Composición

```python
# ❌ MAL: Herencia forzada (Es-Un)
class ShoppingCart(TaxEngine):
    # ¿Un Carrito ES un motor de impuestos? No tiene sentido.
    pass

# ✅ BIEN: Composición (Tiene-Un)
class OrderPipeline:
    def __init__(self, cart, calculator):
        self.cart = cart              # TIENE un carrito
        self.calculator = calculator  # TIENE una calculadora

    def process(self):
        items = self.cart.items
        # Delega el trabajo a la calculadora en vez de hacerlo él mismo
        tax = self.calculator.calculate(100)  
        return tax
```
La ventaja de la composición es que mañana puedes cambiar el `TaxEngine` por un `TaxEngineEuropa` sin tener que alterar el código del pipeline, simplemente inyectando el nuevo motor.

## 4. Agrupamiento y Acumuladores con `collections.defaultdict`

En un Stateless Engine de procesamiento de datos, una tarea muy común es **agrupar y acumular métricas por categoría** (ej. total de gastos por rubro, stock por producto o reactivos por tipo elemental).

### El Problema del Diccionario Estándar
Con un `dict` nativo, acceder a una clave que no existe lanza un `KeyError`:

```python
# ❌ Frágil y verboso: requiere chequear la clave manualmente
totals = {}
for item in items:
    cat = item["category"]
    if cat not in totals:
        totals[cat] = 0.0
    totals[cat] += item["amount"]
```

### La Solución Elegante: `defaultdict`
El módulo estándar `collections` provee `defaultdict`, que recibe una **fábrica de tipo por defecto** (`float`, `list`, `int`). Cuando se intenta leer o modificar una clave inexistente, `defaultdict` la crea automáticamente llamando a esa fábrica (`float()` devuelve `0.0`, `list()` devuelve `[]`):

```python
from collections import defaultdict

# ✅ Idiomático, limpio y sin boilerplate de comprobación
totals = defaultdict(float)
for item in items:
    totals[item["category"]] += item["amount"]
```

### Ejemplo en un Stateless Engine (Domain Shifting: Alquimia de Transmutación)
```python
from collections import defaultdict

class AlchemicalAnalyticsEngine:
    """Motor sin estado para consolidar inventario de reactivos mágicos."""

    def aggregate_potency_by_element(self, reagents: list[dict]) -> dict[str, float]:
        # Inicializa automáticamente en 0.0 cualquier elemento no registrado
        potency_totals = defaultdict(float)

        for r in reagents:
            potency_totals[r["element"]] += r["potency"]

        # Convertimos a dict nativo antes de retornar para sellar el contrato
        return dict(potency_totals)
```

## 5. Conexión con Testing: Inyección de Datos con `@pytest.fixture`

Los Stateless Engines son las clases más fáciles de testear del mundo porque no tienen estado interno impredecible: **misma entrada siempre genera misma salida**.

Para evitar duplicar la creación de datos de prueba en cada función de test, Pytest ofrece el decorador `@pytest.fixture`. Una fixture es una función auxiliar que prepara el "set de datos" y se inyecta directamente como argumento en los tests:

```python
import pytest
from alchemy_engine import AlchemicalAnalyticsEngine

# 1. Definimos la fixture con los datos de prueba
@pytest.fixture
def sample_reagents():
    return [
        {"element": "fire", "potency": 25.5},
        {"element": "water", "potency": 10.0},
        {"element": "fire", "potency": 14.5},
    ]

# 2. Inyectamos la fixture en el parámetro del test
def test_aggregate_potency_accumulates_correctly(sample_reagents):
    engine = AlchemicalAnalyticsEngine()
    result = engine.aggregate_potency_by_element(sample_reagents)

    assert result["fire"] == 40.0
    assert result["water"] == 10.0
```

---

## 6. Mapa de Ejercicios

Dirígete a `quests/03-engines/`:

- [[01-stateless-logic]]
- [[02-spaced-repetition]]

```text
PY-POO/quests/03-engines/
├── [[01-stateless-logic]].md      (Tipo A: Implementación Base)
└── [[02-spaced-repetition]].md    (Tipo B: Spaced Repetition + Testing con Fixtures)
```
