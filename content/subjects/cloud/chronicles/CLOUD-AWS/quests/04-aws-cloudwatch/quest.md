# Quest 04: Amazon CloudWatch (Observabilidad y Spaced Repetition)

Hasta ahora hemos confiado en que los scripts funcionan. Pero en la nube, si una Lambda falla en silencio, nadie se entera. Vamos a integrar *Observabilidad* estructurada (Cap 04) dentro de una función Lambda orientada a eventos (Cap 03).

## 🎯 Objetivo de Negocio
Construir una Lambda que reciba las métricas vitales de un dragón e imprima logs estructurados hacia CloudWatch. Si un dragón está a punto de explotar, debe generar un log de ERROR con una palabra clave exacta que detonará nuestras alarmas configuradas en AWS.

## 📝 Instrucciones

1. **Configuración Global:** Importa el módulo nativo `logging` de Python y configura un objeto `logger` a nivel `INFO` **afuera** de tu función handler (revisa el Lore del Cap 04).
2. **Crear la función `lambda_handler(event, context)`:**
   - **Propósito:** Leer el diccionario `event`, evaluar el peligro y loguear.
   - **Entrada:** `event` vendrá con un formato simple (ej. `{"dragon_id": 42, "instability": 95}`).
   - **Lógica y Logging:**
     - Apenas inicie, extrae las dos variables e imprime con `.info()` exactamente: `"Processing report for dragon ID: {dragon_id}"`.
     - Si la `instability` es MENOR a 90: Imprime con `.info()` `"Normal status. Finishing."` y retorna `{'statusCode': 200}`.
     - Si la `instability` es MAYOR O IGUAL a 90: Imprime con `.error()` **exactamente** la siguiente cadena (vital para el CloudWatch Metric Filter): `"CRITICAL DANGER! Dragon {dragon_id} about to explode. Level: {instability}"`. Y luego de loguearlo, lanza un error crítico usando `raise Exception("Catastrophic instability")`.
   - **Manejo de Errores Global:** Envuelve la lógica en un `try/except`. Si se atrapa alguna Excepción (como la que tú mismo lanzas en el punto anterior, u otra cualquiera), loguea el error con `.error()` (`f"Pipeline failure: {str(e)}"`) y retorna `{'statusCode': 500}`.

> **Scaffolding Nivel 4:** Escribe el handler en `my_solution.py`. En `test_my_solution.py` completa la captura de logs con `caplog` y las aserciones de alarmas según los comentarios de ejercicio. Ejecuta `pytest test_my_solution.py` para validar.
