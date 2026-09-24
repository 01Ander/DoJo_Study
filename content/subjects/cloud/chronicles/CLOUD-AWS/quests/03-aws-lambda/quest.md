# Quest 03: AWS Lambda (Serverless & Event-Driven)

Es hora de crear nuestro primer servicio que responda dinámicamente a eventos sin necesidad de servidores encendidos 24/7. 

## 🎯 Objetivo de Negocio
Escribir la función principal (handler) que AWS Lambda invocará automáticamente cada vez que alguien (o el script de tu Quest 01) suba un nuevo archivo JSON al bucket de S3.

## 📝 Instrucciones

1. **Crear la función `lambda_handler(event, context)`:**
   - **Propósito:** AWS te pasará un diccionario gigante llamado `event`. Tu función debe navegar ese diccionario, extraer el nombre del bucket y el nombre del archivo (`key`), y retornar un mensaje de éxito con formato estándar HTTP.
   - **Entrada:** `event` (dict) y `context` (objeto, puedes ignorarlo en el código).
   - **Salida Exitosa:** Debe retornar exactamente un diccionario como este:
     ```python
     {
         'statusCode': 200,
         'body': 'Archivo dragon_42.json subido a mi-bucket-test'
     }
     ```
   - **Manejo de Errores:** Si el evento viene con un formato extraño que tu código no espera (KeyError, IndexError), tu función debe atrapar el error mediante `try/except` y retornar este diccionario:
     ```python
     {
         'statusCode': 500,
         'body': 'Error'
     }
     ```

> **Scaffolding Nivel 4:** Estás casi solo. El archivo de pruebas inyectará eventos de mentira, simulando lo que haría AWS en la vida real. Tu trabajo es construir el handler y explorar la estructura interna del Payload de S3 tal como se mostró en el Capítulo 03.
