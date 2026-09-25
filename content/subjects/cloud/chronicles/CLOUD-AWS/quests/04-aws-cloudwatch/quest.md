# Quest 04: Amazon CloudWatch (Observabilidad y Spaced Repetition)

Hasta ahora hemos confiado en que los scripts funcionan. Pero en la nube, si una Lambda falla en silencio, nadie se entera. Vamos a integrar *Observabilidad* estructurada (Cap 04) dentro de una función Lambda orientada a eventos (Cap 03).

## 🎯 Objetivo de Negocio
Construir una Lambda que reciba las métricas vitales de un dragón e imprima logs estructurados hacia CloudWatch. Si un dragón está a punto de explotar, debe generar un log de ERROR con una palabra clave exacta que detonará nuestras alarmas configuradas en AWS.

## 📝 Instrucciones

1. **Configuración Global:** Importa el módulo nativo `logging` de Python y configura un objeto `logger` a nivel `INFO` **afuera** de tu función handler (revisa el Lore del Cap 04).
2. **Crear la función `lambda_handler(event, context)`:**
   - **Propósito:** Leer el diccionario `event`, evaluar el peligro y loguear.
   - **Entrada:** `event` vendrá con un formato simple (ej. `{"dragon_id": 42, "inestabilidad": 95}`).
   - **Lógica y Logging:**
     - Apenas inicie, extrae las dos variables e imprime con `.info()` exactamente: `"Procesando reporte del dragón ID: {dragon_id}"`.
     - Si la `inestabilidad` es MENOR a 90: Imprime con `.info()` `"Estado normal. Finalizando."` y retorna `{'statusCode': 200}`.
     - Si la `inestabilidad` es MAYOR O IGUAL a 90: Imprime con `.error()` **exactamente** la siguiente cadena (vital para el CloudWatch Metric Filter): `"¡PELIGRO CRÍTICO! Dragón {dragon_id} a punto de explotar. Nivel: {inestabilidad}"`. Y luego de loguearlo, lanza un error crítico usando `raise Exception("Inestabilidad catastrófica")`.
   - **Manejo de Errores Global:** Envuelve la lógica en un `try/except`. Si se atrapa alguna Excepción (como la que tú mismo lanzas en el punto anterior, u otra cualquiera), loguea el error con `.error()` ("Fallo en el pipeline: ...") y retorna `{'statusCode': 500}`.

> **Scaffolding Nivel 5 (Autónomo):** Escribe el script desde cero en `my_solution.py`. Los tests en `test_my_solution.py` están provistos y evaluarán de manera estricta que tus logs hagan match con las alarmas.
