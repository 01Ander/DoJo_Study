# Capítulo 03: AWS Lambda (Serverless Compute)

Hasta ahora hemos almacenado dietas en S3 (Cap 01) y consultado el estado de salud en RDS (Cap 02). Pero necesitamos "código vivo" que procese esos datos automáticamente para nuestro pipeline. La forma antigua era alquilar un servidor (EC2), mantenerlo encendido 24/7, y correr un script de Python. La forma moderna de ingeniería de datos es **AWS Lambda**.

## 1. ¿Qué es Serverless y AWS Lambda?

**QUÉ es:** AWS Lambda es un servicio de cómputo *Serverless* (sin servidor). Te permite ejecutar código de Python sin tener que aprovisionar, administrar, actualizar ni pagar por ningún servidor en la nube. AWS se encarga de todo: si hay trabajo por hacer, levanta un contenedor con tu código, lo ejecuta y lo apaga en milisegundos.
**CÓMO se usa:** Escribes una función específica en Python llamada `handler`, la subes a AWS (con un IAM Role asociado) y configuras un "evento" que la dispare. AWS te cobra fraccionado por el milisegundo exacto de ejecución.
**POR QUÉ importa:** Elimina por completo los costos de servidores inactivos (*idle*). Si tu pipeline de limpieza de datos corre 5 minutos al día, no tiene sentido técnico ni financiero pagar por las otras 23 horas y 55 minutos. Además, AWS Lambda escala automáticamente de forma horizontal: si llegan 1000 archivos de golpe, AWS levanta 1000 copias de tu código en paralelo, sin que tú cambies una sola línea.

*Analogía 1 (El Chef de Huevos Duros)*: Imagina que quieres comerte un huevo duro a las 3 AM. El modelo tradicional de cómputo (EC2) equivale a comprar una estufa gigante, pagar la tubería de gas, mantener el fuego piloto encendido 24/7 por si acaso, y hervir el huevo tú mismo. El modelo Serverless (AWS Lambda) es como tener un chef fantasma que aparece de la nada en 100 milisegundos cuando chasqueas los dedos, hierve el huevo, te cobra unos centavos solo por los minutos que usó el agua caliente, y desaparece inmediatamente en una nube de humo.

## 2. Arquitectura Orientada a Eventos

**QUÉ es:** En un sistema de software *Event-Driven* (Orientado a Eventos), los distintos componentes no se la pasan preguntándose mutuamente de forma constante si hay trabajo nuevo; en cambio, se duermen y reaccionan de manera instantánea a notificaciones formales (eventos) generadas por otros componentes del sistema.
**CÓMO se usa:** Se configura un "Trigger" (Gatillo) en AWS. Por ejemplo, le decimos a AWS Lambda: "Duerme hasta que alguien suba un archivo JSON a este bucket específico de S3, y ahí ejecútate".
**POR QUÉ importa:** Desacopla radicalmente los sistemas, haciéndolos mucho más robustos y eficientes. Ya no desperdicias CPU de cómputo (ni dinero) verificando estados vacíos en bucles infinitos.

*Analogía 2 (El Cartero y el Buzón)*: Un diseño ineficiente clásico (*polling*) es salir al jardín a revisar el buzón de tu casa cada 5 minutos bajo la lluvia intensa de Ankh-Morpork para ver si llegó una carta del Gremio. Un diseño *Event-Driven* es pedirle al gremio que le ponga un timbre al buzón para que el cartero lo toque **solo** cuando deja una carta real. Así puedes dormir tranquilo frente a la chimenea el resto del día.

## 3. Ejemplo Progresivo: Calculando Dietas Automatizadas

El Gremio de Cuidadores de Dragones necesita un sistema que asigne una dieta específica a cada dragón bebé que nazca y cuyo registro sea ingresado en el sistema por los cuidadores de campo.

### ❌ El Mal Camino (El Script Infinito / Polling)

Imagina un script anticuado corriendo en tu computadora, o peor, en un servidor alquilado 24/7:

🎯 **Objetivo de Negocio:** Detectar registros de crías nuevas en una base de datos y asignarles una dieta base.

```python
import time

def polling_loop_ineficiente():
    # Un bucle infinito atrapa el programa para que nunca termine
    while True:
        # Simulamos preguntar a la base de datos si hay dragones nuevos
        dragones_nuevos = check_nuevos_dragones() 
        
        if dragones_nuevos:
            print("¡Un dragón nació! Asignando dieta...")
            asignar_dieta_base(dragones_nuevos)
            
        # Esperamos 5 minutos para volver a preguntar.
        # Durante este tiempo de inactividad, la CPU está "encendida", bloqueando la terminal
        # y costando dinero a la empresa por no hacer ABSOLUTAMENTE NADA útil.
        time.sleep(300) 
```

**Por qué es un desastre técnico:** Estás pagando por 24 horas ininterrumpidas de servidor a fin de mes, aunque estadísticamente nazca un dragón por semana. Aún peor: si el script sufre un error de memoria (OOM) y se detiene silenciosamente a medianoche, los dragones bebés no comerán hasta que el Operador se despierte, note el problema, y reinicie el servidor al día siguiente.

### ✅ El Buen Camino (AWS Lambda + S3 Event)

En el paradigma Lambda, no existe el `while True`. Solo hay una función controladora llamada `handler` que recibe un objeto `event` (el paquete de datos crudos con la información de lo que acaba de detonarla) y un `context` (metadatos internos de AWS).

🎯 **Objetivo de Negocio:** Un pipeline serverless que reaccione exactamente en el momento en que un archivo de registro de nacimiento crudo (`.json`) cae en el bucket de S3 de la maternidad, calcule su dieta basándose en su especie, guarde el resultado, y el proceso muera ordenadamente.

```python
import json

# En AWS Lambda, esta función es el punto de entrada obligatorio.
def lambda_handler(event, context):
    try:
        # 1. Inspeccionamos el "evento" que despertó a esta Lambda de su letargo.
        # En este caso, configuramos S3 para enviar una lista de registros (Records).
        # Extraemos quirúrgicamente el nombre del bucket y la ruta exacta del archivo (key).
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        
        print(f"✅ ¡Evento detectado por el timbre! Nuevo nacimiento reportado en {s3_bucket}/{s3_key}")
        
        # 2. Aquí iría la lógica de negocio real del ETL
        # (ej. usar boto3 para leer el JSON con s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        # y luego procesarlo con Pandas o escribirlo en RDS como vimos en Cap 02).
        
        # 3. Retornamos una respuesta estándar dictada por AWS, indicando éxito rotundo.
        return {
            'statusCode': 200,
            'body': json.dumps(f'Dieta para el archivo {s3_key} procesada y guardada exitosamente.')
        }
        
    except Exception as e:
        print(f"❌ Error catastrófico durante la extracción: {str(e)}")
        # Avisamos formalmente a AWS que nuestra lógica falló, para que lo registre en logs.
        return {
            'statusCode': 500,
            'body': json.dumps('Error procesando la dieta.')
        }
```

*Zero Surprise Syntax:*
- `def lambda_handler(event, context)`: Esta es la firma técnica obligatoria que los servidores subyacentes de AWS buscan al levantar tu función en Python. El `event` es un diccionario gigante de Python que contiene toda la anatomía del detonante. El `context` provee información técnica (como el tiempo de ejecución restante o la memoria límite asignada), pero rara vez lo usamos directamente en scripts simples de ingeniería de datos.
- `event['Records'][0]['s3']...`: Esta es la estructura estándar documentada por AWS de un payload enviado por un evento de S3. Es un JSON profundamente anidado que nos dice *exactamente* qué archivo fue el que causó que esta Lambda despertara, evitando que tengamos que buscarlo a ciegas en todo el bucket.
- `return {'statusCode': 200, 'body': ...}`: La convención estricta de Lambda dicta que le devuelvas un diccionario simulando una respuesta de red HTTP. El código `200` significa OK/Exitoso, y `500` significa Error Interno de Servidor.

## 4. Execution Role (El Gafete de la Lambda)

**QUÉ es:** Una función Lambda es todopoderosa pero ciega; vive en la nube, pero por el principio de seguridad por defecto, no puede tocar nada. Para que el código Python dentro de tu `lambda_handler` pueda usar `boto3` para leer el archivo del bucket de S3 o conectarse a tu clúster RDS, debes adjuntarle obligatoriamente un IAM Role al momento de crearla en la consola. A este rol específico se le llama **Execution Role**.
**CÓMO se usa:** Se crea un IAM Role normal (como vimos en el Cap 00) con permisos explícitos de `s3:GetObject` en las *Policies*, y se le asigna a la función Lambda como su identidad.
**POR QUÉ importa:** Sin el Execution Role, el código de Python lanzaría instantáneamente un error criptográfico de `AccessDenied`. Es el principio de Mínimo Privilegio de IAM en plena acción: la función Lambda debe probar legalmente su identidad para tocar otras cosas, exactamente al igual que los humanos.
