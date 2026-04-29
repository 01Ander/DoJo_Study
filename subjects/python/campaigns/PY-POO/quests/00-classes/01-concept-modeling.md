# Ejercicio 00-01: Concept Modeling (Tipo A)

**Objetivo:** Transicionar de pensamiento procedimental a mentalidad de Objetos.

## Contexto (Domain Shifting: E-Commerce)
Tienes un fragmento de código legacy (procedimental) que maneja carritos de compras. Tu objetivo es refactorizarlo a una Clase.

### Código Legacy Procedimental:
```python
def create_cart(customer_id: str) -> dict:
    return {"customer": customer_id, "items": [], "total": 0.0}

def add_item(cart: dict, item_name: str, price: float):
    cart["items"].append(item_name)
    cart["total"] += price
```

## Tu Tarea
Crea un archivo `shopping_cart.py` dentro de esta carpeta (`quests/00-classes/`) y diseña la clase `ShoppingCart`.

1. Define el constructor `__init__` que reciba `customer_id`.
2. Inicializa internamente `items` (como lista vacía) y `total` (como 0.0).
3. Implementa el método de instancia `add_item(self, item_name: str, price: float)`.

*Escribe tu código de forma independiente. Pruébalo instanciando la clase al final del archivo.*

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
class ShoppingCart:
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        self.items = []
        self.total = 0.0
        
    def add_item(self, item_name: str, price: float):
        self.items.append(item_name)
        self.total += price

# Ejecución de prueba
if __name__ == "__main__":
    cart = ShoppingCart("cust_991")
    cart.add_item("Laptop", 1200.0)
    cart.add_item("Mouse", 50.0)
    
    print(f"Cart Total: ${cart.total}") # Esperado: $1250.0
```
</details>
