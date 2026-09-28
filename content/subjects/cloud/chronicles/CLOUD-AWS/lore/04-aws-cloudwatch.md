# Capítulo 04: Amazon CloudWatch & Observabilidad

Cuando mueves tu código a la nube usando herramientas Serverless, pierdes la terminal física para ver errores. Si la Lambda falla, ¿dónde ves el mensaje? La respuesta es **Amazon CloudWatch**.

## 1. Monitoreo vs Observabilidad

**QUÉ es:** El monitoreo recolecta métricas predefinidas (ej. "El servidor usa 80% de CPU"). La **Observabilidad** es entender *por qué* falló el código interno basándote en los logs que emitió.
**POR QUÉ importa:** En sistemas distribuidos, un fallo en S3 arruinará la Lambda, y la base de datos quedará vacía. Sin observabilidad, pasarás días adivinando en qué punto de la cadena de servidores ocurrió el fallo. Necesitas registros ricos.

*Analogía del Gremio:* Monitoreo es ver que el carruaje de reparto va lento. Observabilidad es escuchar el crujido de la madera, sentir la temperatura del eje y deducir *por qué* la rueda derecha va a romperse antes de que suceda.

## 2. Log Groups y Log Streams

Amazon CloudWatch es el servicio unificado de AWS para logs (texto) y métricas (números). Los registros se agrupan siguiendo una taxonomía estricta:
1. **Log Group:** Es el contenedor lógico para una aplicación entera (ej. todos los logs de nuestra Lambda `ProcesarNacimientos`).
2. **Log Stream:** Una secuencia específica de eventos de log que comparten la misma fuente física, típicamente una instancia física del contenedor que corrió la función en un momento dado.
*Analogía del Gremio:* Un *Log Group* es el cuarto gigante con los archivos de todo el gremio. Un *Log Stream* es la bitácora individual que llenó un solo guardia durante su turno del martes.

## 3. Políticas de Retención

Por defecto, AWS CloudWatch guarda los logs generados bajo la política *Never Expire* (Retención infinita).
Esto es extremadamente peligroso financieramente. Si tu Lambda de producción escupe "Proceso OK" 10,000 veces al día, pagarás almacenamiento infinito por prints inútiles de hace 5 años. Debes configurar la retención de los Log Groups a 14 o 30 días para borrar la basura automáticamente.

## 4. Setup Inicial (Zero Assumption)

No requieres librerías externas. La librería nativa de Python `logging` es interceptada por AWS CloudWatch de manera automática cuando se ejecuta en la nube.

## 5. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Registrar el estado del dragón en los logs.

```python
def lambda_handler(event, context):
    print("Stable dragon. Instability level: 45%.")
    # DANGER: AWS retains logs by default FOREVER (Never Expire).
    # You will generate infinite costs for old useless prints.
    return {"statusCode": 200}
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Registrar información de negocio útil categorizada (INFO/ERROR) y disparar una alarma crítica simulada si el nivel supera el umbral, reteniendo solo lo vital.

```python
import logging

# 1. Abandonamos print() y usamos el módulo 'logging' a nivel de INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        instability = int(event.get('instability', 50))
        dragon_id = event.get('dragon_id', 'Unknown')
        
        # 2. Structured logs
        logger.info(f"Processing report for dragon ID: {dragon_id}")
        
        if instability >= 90:
            # 3. Emit critical ERROR. En AWS podemos crear un "Metric Filter"
            # que lea la frase "CRITICAL DANGER" en los logs y dispare alarmas.
            logger.error(f"CRITICAL DANGER! Dragon {dragon_id} about to explode. Level: {instability}")
            
            # Intentional exception to halt flow.
            raise Exception("Catastrophic instability")
            
        logger.info("Normal status. Finishing.")
        return {'statusCode': 200, 'body': 'OK'}
        
    except Exception as e:
        logger.error(f"Pipeline failure: {str(e)}")
        return {'statusCode': 500, 'body': 'Error'}
```

*Zero Surprise Syntax:*
- `logging.getLogger()` y `logger.setLevel(logging.INFO)`: Crea un interceptor de registros, filtrando la basura (DEBUG).
- `logger.info()` y `logger.error()`: A diferencia de `print()`, adjuntan metadatos (hora, severidad) y son enviados nativamente a CloudWatch.
- *Metric Filter (Concepto)*: Regla en la consola AWS que escanea el texto del log. Si halla un patrón exacto, detona alertas.

## 6. Conexión con Testing (Test-Driven Lore)

Al probar código que emite observabilidad y gestiona fallos, debemos verificar tanto los registros de CloudWatch como el estado final devuelto.

- **Capturar y validar logs con `caplog`:** Usando el fixture nativo `caplog` de `pytest`, podemos capturar lo que el `logger` envió a CloudWatch y hacer aserciones sobre el texto y el nivel de severidad (`INFO`, `ERROR`).
- **Verificar el contrato de retorno:** Aseguramos que los eventos normales retornen `statusCode 200` y que las excepciones controladas logueen el error y retornen `statusCode 500`.

```python
import pytest
import logging
from my_solution import lambda_handler

def test_logs_normal_status(caplog):
    # Enable log capture at INFO level
    caplog.set_level(logging.INFO)
    
    event = {"dragon_id": 10, "instability": 50}
    result = lambda_handler(event, {})
    
    # 1. Validate success code
    assert result['statusCode'] == 200
    
    # 2. Validate that CloudWatch received expected info logs
    messages = [record.message for record in caplog.records]
    assert "Processing report for dragon ID: 10" in messages
    assert "Normal status. Finishing." in messages

def test_logs_critical_status(caplog):
    caplog.set_level(logging.INFO)
    
    event = {"dragon_id": 99, "instability": 95}
    result = lambda_handler(event, {})
    
    # 1. Validate that exception was caught and returned 500
    assert result['statusCode'] == 500
    
    # 2. Validate that ERROR log was emitted with the exact phrase for alarm
    error_messages = [record.message for record in caplog.records if record.levelname == 'ERROR']
    assert any("CRITICAL DANGER!" in m for m in error_messages)
    assert any("Pipeline failure:" in m for m in error_messages)
```

## 7. Mapa de Ejercicios

Es momento de la Quest 04 (`quests/04-aws-cloudwatch/`). Escribe logs estructurados que puedan salvar el pipeline en plena madrugada.
