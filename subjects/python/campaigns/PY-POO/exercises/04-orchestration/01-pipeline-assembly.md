# Ejercicio 04-01: Pipeline Assembly (Tipo A)

**Objetivo:** Crear un Orquestador inyectando dependencias.

## Contexto (Domain Shifting: Recetas)
Tienes un `RecipeReader` y un `CalorieCalculator`.

## Tu Tarea
En `exercises/04-orchestration/`, crea `pipeline.py`:
1. Crea la clase `RecipePipeline`.
2. En el constructor, inyecta los objetos `reader` y `calculator`.
3. Implementa `execute(self, file_path)`. Debe usar el reader para leer el archivo pasándole la ruta, pasar los datos leídos al calculator, y retornar el resultado final.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
class RecipePipeline:
    def __init__(self, reader, calculator):
        self.reader = reader
        self.calculator = calculator
        
    def execute(self, file_path: str):
        recipes = self.reader.read_recipes(file_path)
        total_calories = self.calculator.calculate(recipes)
        return total_calories
```
</details>
