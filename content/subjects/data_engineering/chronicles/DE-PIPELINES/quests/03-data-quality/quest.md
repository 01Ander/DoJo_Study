# Quest 03: Data Quality (DQ)

**Nivel de Scaffolding: 4 (Escribir desde descripción)**

En este nivel, debes crear los tests basándote únicamente en descripciones escritas. 

## Objetivos
En el archivo `test_03_quality.py`:
1. Completa la implementación de `certify_inventory_quality()`.
2. Escribe el cuerpo de `test_certify_removes_duplicates(dirty_inventory)` comprobando que el DataFrame devuelto pase de 4 filas a 3, y que solo existan 3 códigos únicos.
3. Escribe el cuerpo de `test_certify_fails_on_nulls(invalid_inventory)` usando `pytest.raises(AssertionError)` para atrapar el error.

## Comandos
```bash
pytest test_03_quality.py
```
