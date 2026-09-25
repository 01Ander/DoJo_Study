# Capítulo 04: Amazon CloudWatch & Observabilidad

Cuando mueves tu código a la nube usando herramientas Serverless, pierdes la terminal física para ver errores. Si la Lambda falla, ¿dónde ves el mensaje? La respuesta es **Amazon CloudWatch**.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** El servicio unificado de AWS para logs (texto) y métricas (números). Los registros se agrupan en **Log Groups** (aplicación entera) y **Log Streams** (instancia/ejecución específica).
**POR QUÉ importa:** Permite diagnosticar errores en sistemas distribuidos. En lugar de monitoreo ("el servidor está al 80%"), logramos **Observabilidad** ("Entender por qué falló basándonos en sus logs estructurados").

> **Densidad (Analogía del Gremio de Dragones):**
> Monitoreo es ver que el carruaje de reparto va a 10 km/h. Observabilidad es escuchar el crujido de la madera, sentir la temperatura del eje y deducir *por qué* la rueda derecha va a romperse antes de que suceda, gracias a un log detallado. Un *Log Group* es el archivo central de todas las bitácoras; un *Log Stream* es la bitácora de un solo guardia de turno.

## 2. Setup Inicial (Zero Assumption)

No requieres librerías externas. La librería nativa de Python `logging` es interceptada por AWS CloudWatch de manera automática.

## 3. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Registrar el estado del dragón en los logs.

```python
def lambda_handler(event, context):
    print("Dragón estable. Nivel de inestabilidad: 45%.")
    # PELIGRO: AWS retiene logs por defecto PARA SIEMPRE (Never Expire).
    # Si la función corre 10,000 veces al día, pagarás infinito almacenamiento
    # por millones de prints inútiles de hace 5 años.
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
        inestabilidad = int(event.get('inestabilidad', 50))
        dragon_id = event.get('dragon_id', 'Desconocido')
        
        # 2. Logs estructurados
        logger.info(f"Procesando reporte del dragón ID: {dragon_id}")
        
        if inestabilidad >= 90:
            # 3. Emitir ERROR crítico. En AWS podemos crear un "Metric Filter"
            # que lea la palabra "PELIGRO CRÍTICO" en los logs y dispare alarmas.
            logger.error(f"¡PELIGRO CRÍTICO! Dragón {dragon_id} a punto de explotar. Nivel: {inestabilidad}")
            
            # Lanzamos excepción intencional para frenar el flujo.
            raise Exception("Inestabilidad catastrófica")
            
        logger.info("Estado normal. Finalizando.")
        return {'statusCode': 200, 'body': 'OK'}
        
    except Exception as e:
        logger.error(f"Fallo en el pipeline: {str(e)}")
        return {'statusCode': 500, 'body': 'Error'}
```

*Zero Surprise Syntax:*
- `logging.getLogger()` y `logger.setLevel(logging.INFO)`: Crea un interceptor de registros, filtrando la basura (DEBUG).
- `logger.info()` y `logger.error()`: A diferencia de `print()`, adjuntan metadatos (hora, severidad) y son enviados nativamente a CloudWatch.
- *Metric Filter (Concepto)*: Regla en la consola AWS que escanea el texto del log. Si halla un patrón exacto, detona alertas.

## 4. Conexión con Testing (Test-Driven Lore)

Al probar código que depende de enviar alertas u observabilidad bajo fallos catastróficos, debemos forzar esos fallos en los tests.

- **Forzar errores con `side_effect`:** Si tienes un mock de S3 o RDS, puedes ordenarle que *explote* lanzando una excepción de red, y así verificar que tu bloque `except` (y tus `.error()`) se disparen correctamente.
- **Validar logs generados:** Usando el fixture `caplog` de `pytest`, podemos capturar lo que el `logger` intentó enviar a CloudWatch y hacer aserciones sobre ello.

```python
import pytest
import logging
from unittest.mock import patch, MagicMock

@patch('my_solution.boto3.client')
def test_simulacion_fallo(mock_boto, caplog):
    # Forzamos una caída de la "red" en nuestro mock
    mock_s3 = MagicMock()
    mock_s3.get_object.side_effect = Exception("AWS Network Down")
    mock_boto.return_value = mock_s3
    
    # Habilitamos la lectura de logs en el test
    caplog.set_level(logging.ERROR)
    
    # Ejecutamos nuestra Lambda (que atrapará internamente el error)
    # y usamos assert para validar que haya registrado la caída en CloudWatch
    assert "AWS Network Down" in caplog.text
```

## 5. Mapa de Ejercicios

Es momento de la Quest 04 (`quests/04-aws-cloudwatch/`). Escribe logs estructurados que puedan salvar el pipeline en plena madrugada.
