# Capítulo 03: AWS Lambda (Serverless Compute)

Hasta ahora hemos almacenado datos en S3 y consultado en RDS. Pero necesitamos "código vivo" que procese esos datos automáticamente. La forma antigua era mantener un servidor encendido 24/7. La forma moderna de ingeniería de datos es **AWS Lambda**.

## 1. Computación Serverless

**QUÉ es:** AWS Lambda es un servicio de cómputo *Serverless* (sin servidor). Ejecuta código Python sin que tengas que aprovisionar ni mantener servidores. AWS se encarga de todo: levanta un contenedor cuando hay trabajo, y lo apaga en milisegundos cuando termina.
**POR QUÉ importa:** Elimina costos de servidores inactivos. Además, escala automáticamente de forma infinita: si llegan 1000 archivos de golpe, AWS levanta 1000 copias de tu código en paralelo. AWS te cobra fraccionado por el milisegundo exacto de ejecución, en lugar de cobrarte una tarifa plana mensual por un servidor encendido que no hace nada.

## 2. Arquitectura Orientada a Eventos (Triggers y Contratos de Ejecución)

En un sistema *Event-Driven* (Orientado a Eventos), los componentes duermen y reaccionan a eventos o *Triggers* automáticos, en lugar de preguntar constantemente si hay trabajo (lo cual se conoce como *Polling*).
Cuando S3 recibe un archivo, dispara un evento que activa a Lambda automáticamente. Aunque el origen (S3) no se quede esperando en una conexión HTTP síncrona tradicional, en AWS Lambda es **estándar de la industria y buena práctica** que la función `lambda_handler` devuelva un **contrato de respuesta estructurado** (un diccionario con `statusCode` y `body`). Este formato permite a herramientas de orquestación, suites de testing (`pytest`) y servicios de observabilidad verificar si la ejecución concluyó con éxito (`200`) o si ocurrió un error controlado (`500`).

*Analogía del Gremio:* Un diseño ineficiente de *Polling* continuo es salir a revisar el buzón bajo la lluvia cada 5 minutos por si llegó correo. Desperdicias energía. Un diseño *Event-Driven* es cuando el cartero toca el timbre y deposita el paquete. Aunque el cartero siga su camino, en la bitácora de la entrada sellas un comprobante con el estado del paquete (`statusCode: 200` o `statusCode: 500`) para que el gremio pueda auditar qué pasó.

## 3. Execution Role (El Gafete)

**QUÉ es:** Una función Lambda vive en la nube, pero por el principio de seguridad de AWS, es "ciega". No puede tocar ningún otro servicio, ni siquiera escribir sus propios logs, a menos que tenga permisos. El **Execution Role** es un IAM Role (Cap 00) que se le asigna a la función Lambda como su identidad.
**POR QUÉ importa:** Si tu Lambda necesita descargar un archivo de S3, debes crear un Execution Role con la política `s3:GetObject` y ponérselo a la Lambda. Sin él, el código de Python lanzaría un error criptográfico de `AccessDenied` inmediatamente.

## 4. Setup Inicial (Zero Assumption): Variables de Entorno Nativas

Para usar AWS Lambda, tu código base no requiere instalación de frameworks. Solo necesitas tener configurado tu script con una función de punto de entrada obligatoria (el `handler`) y adjuntarle tu **Execution Role** en la consola de AWS.

**Cuidado con `.env`:** En tu computadora, simulabas el entorno usando `python-dotenv` para leer tu archivo `.env`. En AWS Lambda, **ese archivo `.env` no existe ni debe subirse jamás**. Subir un archivo con contraseñas junto a tu código anula toda la seguridad. 
En Lambda, las variables de entorno se configuran directamente en la consola web de AWS. Python las lee usando `os.environ` de manera nativa, sin necesidad de usar `load_dotenv()`.

## 5. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Detectar nacimientos de dragones en la base y asignarles dieta.

```python
import time

def inefficient_polling_loop():
    # Infinite loop blocking the server indefinitely (Polling)
    while True:
        new_dragons = check_new_dragons() 
        if new_dragons:
            assign_base_diet(new_dragons)
            
        # Paying 24 hours of server at month-end even if only one dragon is born per week.
        time.sleep(300) 
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Un pipeline serverless que reaccione exactamente en el momento en que un JSON de nacimiento cae en el bucket de S3 y retorne un estado de ejecución estructurado.

```python
import json

# In AWS Lambda, this function is the mandatory entry point.
def lambda_handler(event, context):
    try:
        # 1. Inspect the "event" that triggered this Lambda.
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        
        print(f"✅ Event detected! New birth in {s3_bucket}/{s3_key}")
        
        # 2. (Transformation logic would go here)
        
        # 3. Return standard structured response (statusCode and body)
        return {
            'statusCode': 200,
            'body': f'File {s3_key} uploaded to {s3_bucket}'
        }
        
    except Exception as e:
        print(f"❌ Catastrophic error: {str(e)}")
        # Catch errors to respond with a controlled status
        return {
            'statusCode': 500,
            'body': 'Error'
        }
```

*Zero Surprise Syntax:*
- `def lambda_handler(event, context)`: La firma técnica obligatoria de AWS. `event` es un diccionario gigante de Python que contiene los datos del detonante. `context` provee metadatos técnicos (ej. tiempo restante).
- `event['Records'][0]['s3']...`: Estructura estándar de un evento S3. AWS inyecta estos diccionarios anidados diciéndonos *exactamente* qué archivo detonó la Lambda.
- `{'statusCode': 200, 'body': ...}`: Diccionario de respuesta estándar. Permite indicar numéricamente si la ejecución fue exitosa (`200`) o falló (`500`), facilitando la validación en pruebas automáticas y la integración con otros servicios de AWS.

## 6. Conexión con Testing (Test-Driven Lore)

¿Cómo testeas funciones Serverless localmente si no tienes AWS corriendo en tu máquina? ¡Simplemente llamándolas con diccionarios de Python convencionales!

Para probar un `lambda_handler`, no necesitas simular servidores. Simplemente construyes un diccionario que imite la estructura exacta del evento que AWS enviaría, y se lo pasas como argumento a tu función:

```python
from my_solution import lambda_handler

def test_local_handler_success():
    # 1. Mock the dictionary that AWS would build after an S3 event
    mock_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "test-bucket"},
                    "object": {"key": "reports/birth_42.json"}
                }
            }
        ]
    }
    
    # 2. Call our Python function directly (context does not matter here)
    response = lambda_handler(mock_event, {})
    
    # 3. Verify that our code returns the expected dictionary
    assert isinstance(response, dict)
    assert response['statusCode'] == 200
    assert "birth_42.json" in response['body']

def test_local_handler_error():
    # Mock an invalid payload to verify fault tolerance
    invalid_event = {"invalid_format": True}
    response = lambda_handler(invalid_event, {})
    
    assert isinstance(response, dict)
    assert response['statusCode'] == 500
    assert response['body'] == "Error"
```

## 7. Mapa de Ejercicios

Dirígete a `quests/03-aws-lambda/` y pon a prueba tus habilidades armando tu primer Handler serverless.
