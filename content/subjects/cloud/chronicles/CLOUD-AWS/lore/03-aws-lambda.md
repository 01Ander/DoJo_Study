# Capítulo 03: AWS Lambda (Serverless Compute)

Hasta ahora hemos almacenado datos en S3 y consultado en RDS. Pero necesitamos "código vivo" que procese esos datos automáticamente. La forma antigua era mantener un servidor encendido 24/7. La forma moderna de ingeniería de datos es **AWS Lambda**.

## 1. Computación Serverless

**QUÉ es:** AWS Lambda es un servicio de cómputo *Serverless* (sin servidor). Ejecuta código Python sin que tengas que aprovisionar ni mantener servidores. AWS se encarga de todo: levanta un contenedor cuando hay trabajo, y lo apaga en milisegundos cuando termina.
**POR QUÉ importa:** Elimina costos de servidores inactivos. Además, escala automáticamente de forma infinita: si llegan 1000 archivos de golpe, AWS levanta 1000 copias de tu código en paralelo. AWS te cobra fraccionado por el milisegundo exacto de ejecución, en lugar de cobrarte una tarifa plana mensual por un servidor encendido que no hace nada.

## 2. Arquitectura Orientada a Eventos (Ejecución Asíncrona)

En un sistema *Event-Driven* (Orientado a Eventos), los componentes duermen y reaccionan a eventos o *Triggers* automáticos, en lugar de preguntar constantemente si hay trabajo (lo cual se conoce como *Polling*).
Cuando S3 dispara un evento hacia Lambda, lo hace de forma **asíncrona** (fire-and-forget). S3 suelta el evento en el aire y sigue con su vida; no se queda esperando a ver si la Lambda terminó con éxito ni espera una respuesta web (como un código HTTP 200). Por ende, si tu Lambda retorna un diccionario HTTP, ese retorno simplemente se pierde en el vacío.

*Analogía del Gremio:* Un diseño ineficiente de *Polling* continuo es salir a revisar el buzón bajo la lluvia cada 5 minutos por si llegó correo. Desperdicias energía. Un diseño *Event-Driven asíncrono* es cuando el cartero toca el timbre, tira la carta por la ranura y sigue su camino inmediatamente; no se queda bajo la lluvia esperando a que tú le leas la carta en voz alta.

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

def polling_loop_ineficiente():
    # Un bucle infinito que bloquea el servidor eternamente (Polling)
    while True:
        dragones_nuevos = check_nuevos_dragones() 
        if dragones_nuevos:
            asignar_dieta_base(dragones_nuevos)
            
        # Pagarás 24 horas de servidor a fin de mes, aunque solo nazca un dragón por semana.
        time.sleep(300) 
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Un pipeline serverless que reaccione exactamente en el momento en que un JSON de nacimiento cae en el bucket de S3.

```python
import json

# En AWS Lambda, esta función es el punto de entrada obligatorio.
def lambda_handler(event, context):
    try:
        # 1. Inspeccionamos el "evento" que despertó a esta Lambda.
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        
        print(f"✅ ¡Evento detectado! Nuevo nacimiento en {s3_bucket}/{s3_key}")
        
        # 2. (Lógica de transformación iría aquí)
        
        # 3. Al ser asíncrono, simplemente terminamos la función con éxito
        # sin retornar códigos HTTP inútiles.
        
    except Exception as e:
        print(f"❌ Error catastrófico: {str(e)}")
        # Lanzar de nuevo la excepción para que AWS registre el fallo oficial
        raise e
```

*Zero Surprise Syntax:*
- `def lambda_handler(event, context)`: La firma técnica obligatoria de AWS. `event` es un diccionario gigante de Python que contiene los datos del detonante. `context` provee metadatos técnicos (ej. tiempo restante).
- `event['Records'][0]['s3']...`: Estructura estándar de un evento S3. AWS inyecta estos diccionarios anidados diciéndonos *exactamente* qué archivo detonó la Lambda.
- `raise e`: A diferencia de una API web donde devuelves un HTTP 500, en eventos asíncronos si quieres que AWS se entere de que tu código falló (para reintentar o generar alertas), debes dejar que la excepción "estalle" hacia arriba.

## 6. Conexión con Testing (Test-Driven Lore)

¿Cómo testeas funciones Serverless localmente si no tienes AWS corriendo en tu máquina? ¡Simplemente llamándolas con diccionarios de Python convencionales!

Para probar un `lambda_handler`, no necesitas simular servidores. Simplemente construyes un diccionario que imite la estructura exacta del evento que AWS enviaría, y se lo pasas como argumento a tu función:

```python
from my_solution import lambda_handler

def test_handler_local():
    # 1. Simulamos el diccionario que AWS construiría tras un evento S3
    evento_falso = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "bucket-prueba"},
                    "object": {"key": "archivo.json"}
                }
            }
        ]
    }
    
    # 2. Llamamos directamente a nuestra función de Python (context no importa aquí)
    respuesta = lambda_handler(evento_falso, {})
    
    # 3. Verificamos que nuestro código no lance excepciones
    assert respuesta is None # Al no retornar nada explícitamente, retorna None
```

## 7. Mapa de Ejercicios

Dirígete a `quests/03-aws-lambda/` y pon a prueba tus habilidades armando tu primer Handler serverless.
