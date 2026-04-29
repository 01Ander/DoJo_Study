# Capítulo 03: Stateless Engines y Composición

Las Entidades de Dominio (Cap 02) guardan estado (datos). Pero las reglas de negocio complejas, las transformaciones masivas y las agregaciones no deben vivir dentro de las entidades.

Para eso usamos **Stateless Engines** (Motores sin estado).

## 1. El Problema de Acoplar Lógica al Estado

Si un `ShoppingCart` también tiene la lógica de calcular impuestos complejos consultando una API externa, la clase "hace demasiado" (Viola el principio de Responsabilidad Única - SRP de SOLID).

## 2. La Solución: Stateless Engines

Un "Engine" o "Service" es una clase que recibe datos, los procesa y devuelve un resultado, pero **no guarda el resultado en su propio `self`**.

```python
class TaxCalculatorEngine:
    # No hay __init__ que guarde estado
    
    def calculate_total_tax(self, cart_items: list, country_code: str) -> float:
        total_tax = 0.0
        for item in cart_items:
            # Lógica pura de transformación
            if country_code == "CO":
                total_tax += item.price * 0.19
            else:
                total_tax += item.price * 0.10
        return total_tax
```
> Si llamas a `calculate_total_tax` mil veces con los mismos parámetros, siempre dará el mismo resultado. No hay efectos secundarios. Es puramente funcional pero encapsulado en OOP.

## 3. Composición (Tiene-Un) vs Herencia (Es-Un)

En lugar de que un Carrito "herede" de una calculadora de impuestos, el Carrito puede *usar* la calculadora pasándola por parámetro, o un Orquestador superior puede llamar a ambos.

## 4. Conexión con Testing (Nivel 3: Fixtures)

Los Stateless Engines son las clases más fáciles de testear. Solo inyectas un fixture de datos falsos y compruebas el output.

```python
def test_tax_calculator_for_colombia(mock_cart_items):
    engine = TaxCalculatorEngine()
    tax = engine.calculate_total_tax(mock_cart_items, "CO")
    assert tax == 19.0 # Suponiendo mock_cart_items vale 100
```

## 5. Setup y Ejecución

Python puro. 

## 6. Mapa de Ejercicios

Dirígete a `quests/03-engines/`:

```text
PY-POO/quests/03-engines/
├── 01-stateless-logic.md      (Tipo A: Implementación Base)
└── 02-spaced-repetition.md    (Tipo B: Spaced Repetition + Testing)
```
