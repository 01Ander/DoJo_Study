# Capítulo 04: Amazon CloudWatch & Observabilidad

Cuando mueves tu código a la nube usando herramientas Serverless como Lambda (Capítulo 03), pierdes el acceso directo a la consola para ver qué está pasando. Si la Lambda falla, ¿dónde ves el mensaje de error? ¿Cómo sabes que falló en primer lugar? La respuesta de AWS es **Amazon CloudWatch**.

## 1. Monitoreo vs Observabilidad

**QUÉ es:** El monitoreo es el acto de recolectar datos predefinidos sobre tu sistema (ej. "Uso de CPU al 80%"). La **Observabilidad** es una propiedad del sistema que te permite entender *por qué* está pasando algo adentro, basándote únicamente en sus salidas externas (logs, métricas y trazas).
**CÓMO se usa:** En AWS, la observabilidad se logra escribiendo buenos Logs (registros) en tu código Python, los cuales son absorbidos automáticamente por Amazon CloudWatch.
**POR QUÉ importa:** En sistemas distribuidos, un error en S3 puede hacer que falle una Lambda, lo que deja la tabla de RDS vacía. Sin observabilidad, pasarás días adivinando qué falló.

*Analogía 1 (El Carruaje de Patricio Vetinari)*: Monitoreo es mirar el tablero del carruaje y ver que vas a 10 km/h. Observabilidad es poder escuchar el crujido de la madera, sentir la temperatura del eje y cruzarlo con el peso de los pasajeros para deducir *por qué* la rueda derecha está a punto de romperse antes de que suceda.

## 2. El Ecosistema CloudWatch: Log Groups y Log Streams

**QUÉ es:** Amazon CloudWatch es el servicio unificado de AWS para logs (texto) y métricas (números). Todo servicio de AWS (como Lambda) escupe sus registros aquí de forma jerárquica:
1. **Log Group:** El contenedor lógico para una aplicación entera (ej. todos los logs de nuestra Lambda `ProcesarNacimientos`).
2. **Log Stream:** Una secuencia específica de eventos de log que comparten la misma fuente, típicamente una instancia física del contenedor que corrió la función.
**CÓMO se usa:** Cuando usas `print()` o el módulo `logging` en Python dentro de una Lambda, AWS automáticamente envía ese texto al Log Stream correspondiente en CloudWatch.
**POR QUÉ importa:** Organiza el caos. Si 500 Lambdas corrieron simultáneamente, CloudWatch permite buscar la palabra clave "ERROR" entre todas ellas en un solo lugar centralizado.

*Analogía 2 (El Archivo del Gremio)*: Un *Log Group* es el cuarto gigante donde se guardan los registros históricos de las explosiones de los dragones de pantano. Un *Log Stream* es el libro individual de bitácora que llenó un solo cuidador durante su turno de guardia del martes en la noche.

## 3. Ejemplo Progresivo: Retención de Logs

Cuando los cuidadores reportan niveles de inestabilidad, los logs se envían a CloudWatch.

### ❌ El Mal Camino (Logs Infinitos)

Si solo dejas que las Lambdas impriman registros y no configuras nada, AWS CloudWatch tiene un comportamiento por defecto peligroso: **Retención infinita (Never Expire)**.

🎯 **Objetivo de Negocio:** Registrar el estado del dragón.

```python
def lambda_handler(event, context):
    print("Dragón estable. Nivel de inestabilidad: 45%.")
    # Si la función corre 10,000 veces al día, generas miles de megabytes de logs.
    # Por defecto, AWS guardará este "print" para siempre y te cobrará por gigabyte
    # almacenado por el resto de la eternidad.
    return {"statusCode": 200}
```

**Por qué es malo:** Te arruinará financieramente. Los logs de depuración (debug) o de rutinas normales pierden todo su valor pasados unos días o semanas. Pagar por almacenar un log de hace 3 años que dice "Dragón estable" es tirar dinero.

### ✅ El Buen Camino (Políticas de Retención y Alertas)

La observabilidad proactiva significa configurar AWS (vía consola o Terraform) para que los Log Groups tengan una política de retención (ej. "Borrar todo lo más viejo a 14 días") y crear un **CloudWatch Alarm**.

🎯 **Objetivo de Negocio:** Registrar información de negocio útil y disparar una alarma crítica si el nivel de inestabilidad supera un umbral, sin almacenar logs inútiles para siempre.

```python
import json
import logging

# 1. En aplicaciones profesionales, abandonamos print() y usamos el módulo 'logging'.
# Permite categorizar el nivel de urgencia (INFO, WARNING, ERROR).
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Simulamos recibir la inestabilidad desde el evento de S3 (Cap 03)
        inestabilidad = int(event.get('inestabilidad', 50))
        dragon_id = event.get('dragon_id', 'Desconocido')
        
        # 2. Logs estructurados. Esto va a CloudWatch (Log Stream)
        logger.info(f"Procesando reporte del dragón ID: {dragon_id}")
        
        if inestabilidad >= 90:
            # 3. Un logger.error es fácil de buscar en CloudWatch.
            logger.error(f"¡PELIGRO CRÍTICO! Dragón {dragon_id} a punto de explotar. Nivel: {inestabilidad}")
            
            # En AWS CloudWatch, podemos crear un "Metric Filter" que busque la 
            # palabra "PELIGRO CRÍTICO" en este Log Group y dispare una alarma
            # que nos envíe un email (usando Amazon SNS).
            
            raise Exception("Inestabilidad catastrófica")
            
        logger.info("Estado normal. Finalizando.")
        return {'statusCode': 200, 'body': 'OK'}
        
    except Exception as e:
        logger.error(f"Fallo en el pipeline: {str(e)}")
        return {'statusCode': 500, 'body': 'Error'}
```

*Zero Surprise Syntax:*
- `logging.getLogger()` y `logger.setLevel(logging.INFO)`: Crea un objeto oficial de registro que intercepta todos nuestros mensajes. Configurar el nivel a `INFO` asegura que no imprimamos basura oculta (como registros de `DEBUG` muy verbosos de librerías de terceros).
- `logger.info()` y `logger.error()`: A diferencia de un simple `print()`, estas funciones adjuntan automáticamente metadatos valiosos (como la hora exacta, el módulo y la severidad) antes de enviarlos al *Log Stream* de CloudWatch.
- *Metric Filter (Concepto Cloud)*: No es código de Python, es una regla que configuras en la consola de AWS. Escanea los textos de los logs en tiempo real; si encuentra un patrón (como la palabra "PELIGRO CRÍTICO"), aumenta un contador matemático, detonando alertas y correos de emergencia.
