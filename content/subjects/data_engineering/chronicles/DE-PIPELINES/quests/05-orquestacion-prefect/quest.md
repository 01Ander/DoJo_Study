# Quest 05: Orquestación con Prefect

**Nivel de Scaffolding: 5 (Escribir un test completo desde cero)**

¡Última misión! Demuestra que dominas la sintaxis de los decoradores de Prefect escribiendo todo desde cero.

## Objetivos
En el archivo `test_05_prefect.py`:
1. Crea la función `extract_resources()` decorada como una tarea (`@task`) que simule devolver un diccionario. Configúrala con 2 reintentos (`retries=2`).
2. Crea la función `load_to_vault(data)` decorada como una tarea (`@task`). Esta función simula recibir los datos extraídos y guardarlos; basta con que retorne `True` para indicar éxito.
3. Crea la función `orchestrate_day()` decorada como el flujo principal (`@flow`) con el nombre `"Alchemical_Logistics_Pipeline"`. Esta función debe llamar a las dos anteriores en secuencia, pasando el resultado de `extract_resources()` como argumento a `load_to_vault()`.
4. Escribe 3 tests (`test_extract_is_task`, `test_load_is_task`, `test_orchestrate_is_flow`) que utilicen la función nativa de Python `hasattr()` para comprobar que tus funciones tienen los atributos inyectados por los decoradores de Prefect. Los decoradores `@task` y `@flow` inyectan atributos accesibles directamente en la función (ej. `mi_funcion.retries`, `mi_funcion.name`). Usa esto para verificar que `extract_resources` tiene `retries == 2`, que `load_to_vault` tiene el atributo `name`, y que `orchestrate_day` tiene `name == "Alchemical_Logistics_Pipeline"`.

## Comandos
```bash
pytest test_05_prefect.py
```
