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
    print("Dragón estable. Nivel de inestabilidad: 45%.")
    # PELIGRO: AWS retiene logs por defecto PARA SIEMPRE (Never Expire).
    # Generarás costos infinitos por prints inútiles viejos.
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

## 6. Conexión con Testing (Test-Driven Lore)

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
    
    from my_solution import lambda_handler
    
    # Act & Assert: Ejecutamos nuestra Lambda asegurando que explota hacia arriba (raises Exception)
    with pytest.raises(Exception, match="AWS Network Down"):
        lambda_handler({}, {})
        
    # Y usamos assert para validar que antes de explotar, dejó un log en CloudWatch
    assert "AWS Network Down" in caplog.text
```

## 7. Mapa de Ejercicios

Es momento de la Quest 04 (`quests/04-aws-cloudwatch/`). Escribe logs estructurados que puedan salvar el pipeline en plena madrugada.
