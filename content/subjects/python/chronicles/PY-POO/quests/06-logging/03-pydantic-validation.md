# Ejercicio 06-03: Validación de Esquemas con Pydantic (Tipo A)

**Objetivo:** Implementar modelos de datos y validación de contratos estrictos con Pydantic V2 (`BaseModel`, `Field`, `@field_validator`, `ValidationError`), integrando la captura de errores técnicos con excepciones de dominio (Lore 06 §5).

---

## Contexto: Procesamiento Seguro de Transacciones Financieras

En un pipeline de pagos o conciliación contable, los datos crudos llegan en formatos no tipados (diccionarios parseados de JSONs o eventos de streaming). Para proteger la integridad del sistema:

1. **`InvalidTransactionDataError` (Excepción de Dominio):**
   - Debe heredar de `Exception`.
   - Representa un fallo de validación de contrato en el dominio de transacciones.

2. **`TransactionPayload` (Modelo Pydantic - `BaseModel`):**
   - Atributos requeridos:
     - `transaction_id: str`: Debe tener longitud mínima de 3 caracteres (`min_length=3`).
     - `account_id: int`: Debe ser estrictamente positivo (`gt=0`).
     - `amount: float`: Debe ser estrictamente positivo (`gt=0.0`).
     - `currency: str`: Por defecto `"USD"`.
   - Validador personalizado (`@field_validator("currency")`):
     - Convierte la moneda a mayúsculas (`value.upper()`).
     - Debe ser una de las monedas soportadas: `{"USD", "EUR", "GBP", "COP"}`.
     - Si la moneda no está en la lista permitida, lanza un `ValueError` con un mensaje explicativo.

3. **Función `validate_and_create_transaction(data: dict) -> TransactionPayload`:**
   - Recibe un diccionario `data` con la carga útil cruda.
   - Intenta construir e instanciar `TransactionPayload(**data)`.
   - Si Pydantic arroja `ValidationError`, la función **debe capturarla** y relanzar una excepción de dominio `InvalidTransactionDataError` preservando el detalle del error en el mensaje.
   - Si los datos son válidos, retorna la instancia construida de `TransactionPayload`.

---

## Tu Tarea (Carril A - Operador)

Edita el archivo [`transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) completando la excepción, el modelo `TransactionPayload` y la función de parsing.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/06-logging/test_transaction_schema.py -v
```
El ejercicio se considera superado cuando los 5 tests pasen con **`exit code 0`**.
