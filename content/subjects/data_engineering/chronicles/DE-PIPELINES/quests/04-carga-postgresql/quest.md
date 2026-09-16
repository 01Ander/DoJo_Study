# Quest 04: Carga a PostgreSQL (SQLAlchemy)

**Nivel de Scaffolding: 5 (Escribir un test completo desde cero)**

¡Estás solo! Debes escribir tanto la lógica de negocio como los tests desde cero. 

## Objetivos
En el archivo `test_04_carga.py`:
1. Crea la función `load_gold_inventory(df, engine)` que reciba un DataFrame y un motor de base de datos.
2. La función debe guardar el DataFrame en la tabla `potion_stock` usando `to_sql`, sin guardar el índice, y con `if_exists='append'`.
3. Crea el fixture `test_engine` que devuelva `create_engine('sqlite:///:memory:')`.
4. Crea un test `test_load_inventory_successfully(test_engine)` que simule un DataFrame, llame a tu función, y luego use SQLAlchemy Core (`text()`, `connect()`, `execute()`, `fetchall()`) para verificar que los registros llegaron a la tabla.

## Comandos
```bash
pytest test_04_carga.py
```
