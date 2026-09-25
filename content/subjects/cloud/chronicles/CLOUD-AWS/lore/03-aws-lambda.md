# Capítulo 03: AWS Lambda (Serverless Compute)

Hasta ahora hemos almacenado datos en S3 y consultado en RDS. Pero necesitamos "código vivo" que procese esos datos automáticamente. La forma antigua era mantener un servidor encendido 24/7. La forma moderna de ingeniería de datos es **AWS Lambda**.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** AWS Lambda es un servicio de cómputo *Serverless* (sin servidor). Ejecuta código Python sin tener que aprovisionar ni mantener servidores. Levanta un contenedor cuando hay trabajo, y lo apaga en milisegundos.
**POR QUÉ importa:** Elimina costos de servidores inactivos. Además, escala automáticamente: si llegan 1000 archivos de golpe, AWS levanta 1000 copias de tu código en paralelo, sin que tú hagas nada.

> **Densidad (Arquitectura Orientada a Eventos):**
> En un sistema *Event-Driven*, los componentes duermen y reaccionan a eventos.
> *Analogía del Gremio:* Un diseño ineficiente (*polling*) es salir a revisar el buzón bajo la lluvia cada 5 minutos por si llegó correo del Gremio. Un diseño *Event-Driven* es ponerle un timbre al buzón para que el cartero lo toque **solo** cuando deja una carta. Así puedes dormir el resto del día. 

## 2. Setup Inicial (Zero Assumption)

Para usar AWS Lambda, tu código base no requiere instalación de frameworks. Solo necesitas tener configurado tu script con una función de punto de entrada obligatoria (el `handler`). Además, deberás adjuntarle un **Execution Role** (IAM) en la consola de AWS para que tenga permiso de tocar otros servicios como S3.

## 3. Implementación (Cómo)

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
        
        # 3. Retornamos una respuesta estándar dictada por AWS
        return {
            'statusCode': 200,
            'body': json.dumps('Dieta procesada exitosamente.')
        }
        
    except Exception as e:
        print(f"❌ Error catastrófico: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error procesando la dieta.')
        }
```

*Zero Surprise Syntax:*
- `def lambda_handler(event, context)`: La firma técnica obligatoria de AWS. `event` es un diccionario gigante de Python que contiene los datos del detonante. `context` provee metadatos técnicos (ej. tiempo restante).
- `event['Records'][0]['s3']...`: Estructura estándar de un evento S3. AWS inyecta estos diccionarios anidados diciéndonos *exactamente* qué archivo detonó la Lambda.
- `return {'statusCode': 200, ...}`: Convención estricta que simula una respuesta de red HTTP. `200` es OK, `500` es Error.

## 4. Conexión con Testing (Test-Driven Lore)

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
    
    # 3. Verificamos que nuestro código haya reaccionado correctamente
    assert respuesta['statusCode'] == 200
```

## 5. Mapa de Ejercicios

Dirígete a `quests/03-aws-lambda/` y pon a prueba tus habilidades armando tu primer Handler serverless.
