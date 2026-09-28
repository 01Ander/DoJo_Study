# Capítulo 05: Integración Cloud End-to-End

Es hora de ensamblar el reloj. Hemos estudiado IAM, S3, RDS, Lambda y CloudWatch de forma aislada. Un pipeline real es la orquestación sofisticada de todos interactuando entre sí.

## 1. El Flujo de Trabajo E2E

**QUÉ es:** Un flujo *End-to-End (E2E)* es el viaje técnico automatizado completo sin intervención humana.
**CÓMO funciona:** S3 recibe un archivo crudo. Este evento dispara instantáneamente una Lambda. La Lambda asume un rol de IAM (Execution Role) para tener permiso de descargar el archivo. Transforma la data y abre un túnel a RDS para insertarla. Si falla en algún punto, escribe en CloudWatch.
**POR QUÉ importa:** Aprender a aislar los servicios es teórico. Orquestarlos es el núcleo de la ingeniería de datos, convirtiéndote de un Junior a un Ingeniero Mid-Level.

## 2. Transacciones ACID y Rollbacks

**QUÉ es:** Cuando Lambda intenta insertar datos en RDS, algo puede fallar (ej. la red se cae a la mitad, o un dato venía corrupto). Si un proceso muere a la mitad, dejamos "datos a medias".
**POR QUÉ importa:** Las Transacciones aseguran la consistencia. Al usar `psycopg2`, debes hacer `conn.commit()` para confirmar los cambios. Si hubo un error en Python, haces `conn.rollback()` para deshacer la transacción completa y limpiar la base de datos de los datos "a medias".
*Analogía del Gremio:* Si un veterinario inyecta un suero de dos fases, pero el dragón destruye la segunda jeringa con fuego, debes extraer la primera fase inmediatamente (un `ROLLBACK`). Dejar cosas a medias provoca mutaciones de datos.

## 3. Variables de Entorno Nativas

Como aprendimos en la lección de Lambda (Cap 03), en AWS Lambda **el archivo `.env` no existe ni debe subirse jamás**.
Las contraseñas de producción de RDS no se empaquetan en el código fuente. Se inyectan de forma segura directamente desde la configuración de la consola web de AWS. Python las lee usando `os.environ` nativamente.

## 4. Setup Inicial (Zero Assumption)

No usarás `load_dotenv()` en la nube, solo leerás directamente desde `os.environ`. Deberás configurar tu Lambda en AWS con las credenciales de tu RDS antes de ejecutarla.

## 5. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Pipeline integral de S3 a RDS.

```python
import psycopg2, boto3

def lambda_handler(event, context):
    # Fragile! Hardcoded credentials directly in code.
    conn = psycopg2.connect(host="dragons.rds", user="admin", password="123")
    cur = conn.cursor()
    
    # Guessing file blindly
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket="my-bucket", Key="latest_report.json")
    
    # If the database rejects insertion, script crashes, CloudWatch won't say why,
    # and conn hangs forever as a zombie consuming RAM on RDS.
    cur.execute("INSERT INTO inventory VALUES (...)")
    conn.commit()
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Pipeline E2E que atrape fallos asíncronos y preserve transacciones ACID.

```python
import os
import json
import logging
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    conn = None
    try:
        # 1. Event-Driven integration (S3)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # 2. Extract and parse raw JSON
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))
        
        # 3. Secure connection using injected variables (no load_dotenv)
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()
        
        # 4. ACID Transform and Load
        dragon_id = payload.get('dragon_id')
        kg = payload.get('meat_kg', 0)
        
        cur.execute("INSERT INTO consumptions (dragon_id, kg) VALUES (%s, %s)", (dragon_id, kg))
        
        # 5. Commit transaction
        conn.commit()
        logger.info(f"✅ Insertion saved for dragon {dragon_id}")
        return {'statusCode': 200, 'body': 'Cloud ETL Completed'}
        
    except Exception as e:
        # 6. Fault tolerance
        if conn:
            conn.rollback() # Undo half-committed data
        logger.error(f"❌ E2E failure: {str(e)}")
        return {'statusCode': 500, 'body': 'ETL processing error'}
        
    finally:
        # 7. Unconditional cleanup
        if conn:
            conn.close()
            logger.info("RDS connection safely closed.")
```

*Zero Surprise Syntax:*
- `response['Body'].read().decode('utf-8')`: Extrae el flujo binario descargado, lo decodifica a texto y permite que `json.loads` lo parseé.
- `conn.commit()`: Le exige al servidor RDS que consolide los cambios permanentemente en el disco.
- `conn.rollback()`: Si hay un error, le ordena a RDS destruir los cambios temporales, devolviendo la base a su estado inmaculado.
- `finally: conn.close()`: Se ejecuta **siempre**, garantizando la muerte de las conexiones zombie sin importar cómo termine el script.

## 6. Conexión con Testing (Test-Driven Lore)

El testing End-to-End (E2E) simulado requiere orquestar múltiples mocks en la misma función.
En el Cap 05, tendrás que parchear tanto S3 como Postgres, e inyectar variables de entorno falsas para que tu código pueda leerlas sin lanzar `KeyError`.

- **Inyección de variables de entorno con `@patch.dict`:** Como tu código lee directamente de `os.environ` sin archivo `.env`, usamos `@patch.dict(os.environ, {...})` de `unittest.mock` para suministrar valores simulados (`DB_HOST`, `DB_NAME`, etc.) exclusivamente durante la ejecución del test.
- **Apilar múltiples decoradores `@patch`:** Se pueden apilar múltiples decoradores `@patch`. Se inyectan en los argumentos de la función de prueba de abajo hacia arriba (el parche más cercano a la función `def` es el primer argumento).

```python
import os
import pytest
from unittest.mock import patch, MagicMock

# 1. Mock environment variables injection
@patch.dict(os.environ, {
    "DB_HOST": "localhost",
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_PASSWORD": "password"
})
# 2. Stack external infrastructure mocks
@patch('my_solution.psycopg2.connect') # Injected as mock_connect (arg 2)
@patch('my_solution.boto3.client')     # Injected as mock_boto (arg 1)
def test_full_pipeline(mock_boto, mock_connect):
    from my_solution import lambda_handler
    
    # Prepare S3 mock to return simulated JSON
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = b'{"dragon_id": 42, "meat_kg": 100}'
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    # Prepare RDS mock
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Trigger mock event
    mock_event = {"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": "k"}}}]}
    
    # Execute pipeline
    result = lambda_handler(mock_event, {})
    
    # Assertions: Validate return and simulated network calls
    assert result['statusCode'] == 200
    mock_s3.get_object.assert_called_once()
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

# 3. Test Failure and Rollback (ACID Transactions)
@patch.dict(os.environ, {
    "DB_HOST": "localhost",
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_PASSWORD": "password"
})
@patch('my_solution.psycopg2.connect')
@patch('my_solution.boto3.client')
def test_pipeline_failure_rollback(mock_boto, mock_connect):
    from my_solution import lambda_handler
    
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = b'{"dragon_id": 99, "meat_kg": 50}'
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Force DB error during execute to test resilience
    mock_cur.execute.side_effect = Exception("Disk full")
    
    mock_event = {"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": "k"}}}]}
    result = lambda_handler(mock_event, {})
    
    # Assert: Returns 500, rolls back, and closes connection
    assert result['statusCode'] == 500
    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
```

## 7. Mapa de Ejercicios

Termina tu aprendizaje en la nube con `quests/05-cloud-integration/`. Construye tu primer Pipeline E2E aplicando toda la tolerancia a fallos necesaria para sobrevivir en un entorno productivo.
