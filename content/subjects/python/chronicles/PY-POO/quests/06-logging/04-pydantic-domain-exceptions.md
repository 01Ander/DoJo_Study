# Ejercicio 06-04: Validadores de Negocio y Excepciones de Dominio (Tipo A)

**Objetivo:** Implementar validación personalizada con `@field_validator` en Pydantic V2 y traducir errores técnicos (`ValidationError`) en excepciones de dominio contextualizadas en la frontera del sistema (Lore 06B §4 y §5).

---

## Contexto: Procesamiento Seguro de Transacciones Financieras

Una vez dominada la migración básica a `BaseModel` (Quest 06-03), el siguiente paso en ingeniería de datos es aplicar **reglas de negocio personalizadas** y **encapsular los errores en la frontera**:

1. **`InvalidTransactionDataError` (Excepción de Dominio):**
   - Debe heredar de `Exception`.
   - Representa un fallo de contrato en la ingesta de transacciones.

2. **`TransactionPayload` (Modelo Pydantic):**
   - Atributos con restricciones:
     - `transaction_id: str`: Longitud mínima de 3 caracteres (`Field(min_length=3)`).
     - `account_id: int`: Estrictamente positivo (`Field(gt=0)`).
     - `amount: float`: Estrictamente positivo (`Field(gt=0.0)`).
     - `currency: str`: Por defecto `"USD"`.
   - Validador personalizado (`@field_validator("currency")` como `@classmethod`):
     - Convierte la moneda a mayúsculas (`v.upper()`).
     - Debe pertenecer a: `{"USD", "EUR", "GBP", "COP"}`.
     - Si no pertenece, lanza `ValueError(f"Moneda '{v}' no soportada")`.

3. **Función `validate_and_create_transaction(data: dict) -> TransactionPayload`:**
   - Recibe un diccionario `data` crudo.
   - Intenta instanciar `TransactionPayload(**data)`.
   - Si Pydantic arroja `ValidationError`, **captura la excepción** y lanza `InvalidTransactionDataError` con el detalle del error.
   - Si es válido, retorna la instancia construida.

---

## Tu Tarea (Carril A - Operador)

Edita el archivo [`transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) completando la excepción, el modelo y la función de validación.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/06-logging/test_transaction_schema.py -v
```
El ejercicio se considera superado cuando los 6 tests pasen con **`exit code 0`**.
