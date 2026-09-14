# Quest 00: Arquitecturas y Zonas de Datos

**Nivel de Scaffolding: 1 (Leer un test y explicar qué valida)**

En este nivel, los tests (TDD) ya están escritos al 100% por el Arquitecto. Tu trabajo como Operador es **leer los tests** para entender qué se espera, y luego implementar la lógica de negocio en las funciones vacías (`pass`) para que los tests pasen a color verde.

## Objetivos
1. Implementa `load_to_bronze()` asegurando la inmutabilidad de la zona.
2. Implementa `process_to_silver()` para limpiar la basura y estandarizar datos.
3. Implementa `aggregate_to_gold()` para totalizar las cantidades por ingrediente.

## Comandos
```bash
pytest test_00_zonas.py
```
