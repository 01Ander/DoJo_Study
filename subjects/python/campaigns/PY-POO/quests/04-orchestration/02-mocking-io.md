# Ejercicio 04-02: Mocking I/O (Tipo B - Nivel 4)

**Objetivo:** Probar un Orquestador aislando las dependencias con Mocks.

## Tu Tarea
En `quests/04-orchestration/`, asume que tu `RecipePipeline` del ejercicio anterior ya existe.
Crea un test completo en `test_pipeline.py` usando `from unittest.mock import Mock`.

1. Crea un mock para el reader que devuelva `["Pizza"]` al llamar a `read_recipes`.
2. Crea un mock para el calculator que devuelva `1500` al llamar a `calculate`.
3. Inyéctalos en el Pipeline.
4. Verifica que `execute` retorna `1500` y que los métodos de los mocks fueron llamados con los argumentos correctos.

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from unittest.mock import Mock
# from pipeline import RecipePipeline

def test_recipe_pipeline():
    # Arrange
    mock_reader = Mock()
    mock_reader.read_recipes.return_value = ["Pizza"]
    
    mock_calc = Mock()
    mock_calc.calculate.return_value = 1500
    
    pipeline = RecipePipeline(reader=mock_reader, calculator=mock_calc)
    
    # Act
    result = pipeline.execute("dummy.txt")
    
    # Assert
    assert result == 1500
    mock_reader.read_recipes.assert_called_once_with("dummy.txt")
    mock_calc.calculate.assert_called_once_with(["Pizza"])
```
</details>
