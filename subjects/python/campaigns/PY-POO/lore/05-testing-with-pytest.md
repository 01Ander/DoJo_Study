# Capítulo 05: Testing with Pytest

El código sin pruebas (tests) es código legacy desde el momento en que se escribe. Pytest es el framework estándar de la industria en Python para asegurar que tu código hace exactamente lo que promete.

## 1. La Anatomía Universal de un Test

No importa el lenguaje, un buen test sigue el patrón de las tres Aes: **Arrange, Act, Assert** (o Given, When, Then).

```python
# class ShoppingCart a testear
class ShoppingCart:
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)

# El Test
def test_cart_adds_items_correctly():
    # 1. ARRANGE (GIVEN): Preparar el mundo
    # (Instanciar clases, crear datos dummy)
    cart = ShoppingCart()
    
    # 2. ACT (WHEN): Ejecutar la acción a probar
    cart.add("Manzana")
    
    # 3. ASSERT (THEN): Afirmar que el estado cambió como esperábamos
    assert len(cart.items) == 1
    assert cart.items[0] == "Manzana"
```

## 2. Fixtures: Evitando Código Repetitivo

Si tienes 5 tests que necesitan un `ShoppingCart` vacío, no instancies el carrito en cada test. Usa `@pytest.fixture`.

Un Fixture es una función que provee "datos/objetos prefabricados" a tus tests.

```python
import pytest

@pytest.fixture
def empty_cart():
    # Esta función inicializa el carrito una vez y lo "entrega"
    return ShoppingCart()

# En lugar de hacer el ARRANGE adentro, pedimos el fixture en los parámetros
def test_cart_is_empty_initially(empty_cart):
    # ACT / ASSERT
    assert len(empty_cart.items) == 0

def test_cart_adds_items_correctly(empty_cart):
    # Ya tenemos el objeto listo gracias a empty_cart
    empty_cart.add("Pera")
    assert "Pera" in empty_cart.items
```

## 3. Mocks: Aislando Componentes

A veces tu clase depende de otra clase externa (ej. una conexión a Base de Datos). **Los Unit Tests no deben depender de sistemas externos.**

Si tienes que testear tu lógica, debes "fingir" (mockear) la respuesta del sistema externo.

```python
from unittest.mock import Mock

def test_database_call_without_database():
    # GIVEN: Un mock que finge ser la base de datos
    mock_db = Mock()
    mock_db.save.return_value = True # Fingimos que guarda exitosamente
    
    # Supongamos que esta clase guarda en DB
    manager = ProductManager(database=mock_db)
    
    # WHEN
    result = manager.save_product("Laptop")
    
    # THEN
    assert result is True
    # Verificamos que el mock realmente fue llamado con "Laptop"
    mock_db.save.assert_called_once_with("Laptop")
```

## 4. Setup del Entorno (CRÍTICO)

Pytest y Mypy NO son nativos. Deben instalarse en un entorno virtual aislado para no contaminar tu sistema.

1. **Crear y activar el Entorno Virtual (venv):**
   ```bash
   # Crear el entorno (hazlo solo una vez en la raíz del proyecto)
   python -m venv .venv
   
   # Activar el entorno (hazlo cada vez que abras una nueva terminal)
   source .venv/bin/activate  # En Mac/Linux
   ```

2. **Instalación de dependencias:** 
   ```bash
   pip install pytest mypy
   ```

3. **Verificación:**
   ```bash
   pytest --version
   mypy --version
   ```

4. **Ejecución de validaciones:**
   Antes de correr los tests, es buena práctica correr `mypy` para validar los tipos estáticos.
   ```bash
   # 1. Chequeo de Tipos:
   mypy tu_archivo.py
   
   # 2. Correr todos los tests en la carpeta actual:
   pytest -v
   # O especificando el archivo:
   pytest test_shopping_cart.py -v
   ```

## 5. Errores Comunes de Pytest

**Error:** `ModuleNotFoundError: No module named 'pytest'`
- **Causa:** No activaste tu entorno virtual o no instalaste pytest.
- **Solución:** Ejecuta `pip install pytest`.

**Error:** `AssertionError: assert False is True`
- **Causa:** Tu test falló. La línea con `assert` esperaba un valor, pero tu código devolvió otro.
- **Solución:** Mira el traceback de pytest para ver exactamente qué devolvió y corrige tu archivo fuente.

---

## 6. Mapa de Ejercicios

Dirígete a `quests/05-testing/` y completa los ejercicios:

- [[01-fixture-creation]]
- [[02-test-from-scratch]]

```text
PY-POO/quests/05-testing/
├── [[01-fixture-creation]].md       (Tipo B: Nivel 3 - Fixtures)
└── [[02-test-from-scratch]].md      (Tipo B: Nivel 4 - Test Completo)
```
