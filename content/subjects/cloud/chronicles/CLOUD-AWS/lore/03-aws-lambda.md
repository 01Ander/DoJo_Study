# Capítulo 03: AWS Lambda (Serverless Compute)

Hasta ahora hemos almacenado datos en S3 y consultado en RDS. Pero necesitamos "código vivo" que procese esos datos automáticamente. La forma antigua era mantener un servidor encendido 24/7. La forma moderna de ingeniería de datos es **AWS Lambda**.

## 1. Computación Serverless

**QUÉ es:** AWS Lambda es un servicio de cómputo *Serverless* (sin servidor). Ejecuta código Python sin que tengas que aprovisionar ni mantener servidores. AWS se encarga de todo: levanta un contenedor cuando hay trabajo, y lo apaga en milisegundos cuando termina.
**POR QUÉ importa:** Elimina costos de servidores inactivos. Además, escala automáticamente de forma infinita: si llegan 1000 archivos de golpe, AWS levanta 1000 copias de tu código en paralelo. AWS te cobra fraccionado por el milisegundo exacto de ejecución, en lugar de cobrarte una tarifa plana mensual por un servidor encendido que no hace nada.

## 2. Arquitectura Orientada a Eventos (Triggers y Contratos de Ejecución)

En un sistema *Event-Driven* (Orientado a Eventos), los componentes duermen y reaccionan a eventos o *Triggers* automáticos, en lugar de preguntar constantemente si hay trabajo (lo cual se conoce como *Polling*).
Cuando S3 recibe un archivo, dispara un evento que activa a Lambda automáticamente.

> ⚠️ **Invocación Síncrona vs Asíncrona (El Mito del `statusCode` en eventos de S3):**  
> Cuando una Lambda se expone como un endpoint HTTP síncrono (por ejemplo, a través de Amazon API Gateway), la función debe retornar un contrato de respuesta estructurado (`{'statusCode': 200/500, 'body': ...}`) para que el cliente web reciba la respuesta.  
> **Sin embargo, en arquitecturas Event-Driven disparadas por S3 (`s3:ObjectCreated:*`), la invocación es estrictamente Asíncrona.** AWS dispara la función en segundo plano y **descarta por completo cualquier valor de retorno del diccionario**.  
> **El peligro de silenciar errores:** Si capturas un error y retornas `{'statusCode': 500, 'body': 'Error'}`, para el runtime de AWS la invocación terminó como un éxito (`Exit 0`). Esto provoca que CloudWatch Metrics registre `Invocations: 1, Errors: 0`, impidiendo que se disparen las alarmas de monitoreo y desactivando las colas de reintentos automáticos o Dead Letter Queues (DLQ).  
> **Regla de Producción:** En Lambdas asíncronas de datos (como las disparadas por S3), ante un error irrecuperable debes **propagar la excepción (`raise`)**, de modo que AWS marque la invocación como fallida, registre el error en CloudWatch y active los mecanismos de reintento o DLQ. *(En las Quests de este capítulo usamos el diccionario estructurado para facilitar el testing unitario local con pytest, pero ten siempre presente esta distinción crítica para entornos productivos y para el Rite)*.

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
- `{'statusCode': 200, 'body': ...}`: Diccionario de respuesta estándar usado en invocaciones síncronas (API Gateway) y en pruebas unitarias. En pipelines asíncronos reales (S3), el valor retornado se descarta y los errores deben propagarse con `raise` para no silenciar las fallas ante AWS.

---

## 5.1 Empaquetado `.zip` y Despliegue Programático con `create_function` (`AWS-008`)

Para desplegar una función Lambda en AWS sin usar la interfaz web, debemos cumplir dos pasos programáticos:
1. **Empaquetar el archivo `.py` dentro de un archivo comprimido `.zip` en memoria** usando las librerías estándar `io.BytesIO` y `zipfile.ZipFile`.
2. **Invocar `lambda_client.create_function(...)`** pasándole el nombre de la función, el runtime (`"python3.12"`), el **ARN del Rol IAM** (creado en el Cap 00), el punto de entrada (`"handler.lambda_handler"`), los bytes del `.zip` (`Code={"ZipFile": zip_bytes}`) y las **variables de entorno nativas de AWS** (`Environment={"Variables": {...}}`).

```python
import io
import zipfile
from typing import Any

# 🎯 Objetivo de Negocio: Empaquetar código Python en un .zip en RAM y desplegar la función Lambda.

def build_lambda_zip(source_code: str, filename: str = "handler.py") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, source_code)
    return buffer.getvalue()


def deploy_serverless_worker(
    lambda_client: Any,
    function_name: str,
    role_arn: str,
    zip_bytes: bytes,
    env_vars: dict[str, str],
) -> str:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.12",
        Role=role_arn,
        Handler="handler.lambda_handler",
        Code={"ZipFile": zip_bytes},
        Environment={"Variables": env_vars},
        Timeout=60,
        MemorySize=256,
    )
    return response["FunctionArn"]
```

> **Zero Surprise Syntax:**
> * **`with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:`:** Abre un archivo `.zip` directamente sobre nuestro buffer de memoria RAM (`io.BytesIO()`).
> * **`zf.writestr(filename, source_code)`:** Escribe el texto de nuestro código Python dentro del `.zip` bajo el nombre `handler.py` sin necesidad de crear archivos en el disco duro.
> * **`Handler="handler.lambda_handler"`:** Tiene el formato `<nombre_archivo_sin_py>.<nombre_funcion>`. Si el archivo dentro del `.zip` se llama `handler.py` y la función es `def lambda_handler(event, context):`, el Handler es `"handler.lambda_handler"`.
> * **`Environment={"Variables": env_vars}`:** Así se inyectan variables de entorno reales en AWS Lambda (nunca subiendo un archivo `.env` dentro del `.zip`).

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
