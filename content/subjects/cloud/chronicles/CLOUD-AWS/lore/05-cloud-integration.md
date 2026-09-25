# Capítulo 05: Integración Cloud End-to-End

Es hora de ensamblar el reloj. Hemos estudiado IAM, S3, RDS, Lambda y CloudWatch de forma aislada. Un pipeline real es la orquestación sofisticada de todos interactuando entre sí, tolerando fallos de red y garantizando atomicidad.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** Un flujo *End-to-End (E2E)* es el viaje técnico automatizado completo: S3 dispara Lambda, Lambda asume un rol IAM, extrae de S3, transforma, se conecta a RDS, y hace `COMMIT`. Si algo falla, CloudWatch es notificado.
**POR QUÉ importa:** Aprender a aislar los servicios es teórico. Orquestarlos de forma tolerante a fallos mediante transacciones ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad) evita tener datos corruptos o duplicados a medias en tu Data Warehouse.

> **Densidad (Analogía del Gremio):**
> - **End-to-End:** No sirve de nada tener granjas (S3) y mataderos (RDS) sin carretas automatizadas (Lambda), guardias verificando permisos (IAM) y auditores (CloudWatch). Todo debe encadenarse.
> - **Transacciones (ROLLBACK):** Si un veterinario inyecta un suero de dos fases, pero el dragón destruye la segunda dosis con fuego, debes extraer la primera fase inmediatamente (un `ROLLBACK`). Dejar cosas a medias provoca mutaciones de datos. El `COMMIT` ocurre solo si ambas fases tuvieron éxito rotundo.

## 2. Setup Inicial (Zero Assumption)

**Las variables de entorno en Lambda:**
En Lambda **está prohibido subir el archivo `.env`**. El sistema operativo de AWS las inyecta de forma segura a través de configuraciones de su consola web. No usarás `load_dotenv()` en la nube, solo leerás directamente desde `os.environ`.

## 3. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Pipeline integral de S3 a RDS.

```python
import psycopg2, boto3

def lambda_handler(event, context):
    # ¡Terrible! Hardcoding en pleno código.
    conn = psycopg2.connect(host="dragones.rds", user="admin", password="123")
    cur = conn.cursor()
    
    # Adivinar archivo ciegamente
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket="mi-bucket", Key="ultimo_reporte.json")
    
    # Si la base de datos rechaza la inserción, el script explota, CloudWatch no dice por qué,
    # y la conexión conn queda colgada por siempre como un zombie consumiendo RAM en RDS.
    cur.execute("INSERT INTO inventario VALUES (...)")
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

# Cliente S3 global (ahorra milisegundos de carga entre invocaciones cálidas)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    conn = None
    try:
        # 1. Integración Event-Driven (S3)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # 2. Extracción y Lectura de JSON crudo
        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))
        
        # 3. Conexión segura usando variables Inyectadas (sin load_dotenv)
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()
        
        # 4. Transformación y Carga ACID
        dragon_id = payload.get('dragon_id')
        kilos = payload.get('kilos_carne', 0)
        
        cur.execute("INSERT INTO consumos (dragon_id, kilos) VALUES (%s, %s)", (dragon_id, kilos))
        
        # 5. Confirmar transacción
        conn.commit()
        logger.info(f"✅ Inserción guardada para dragón {dragon_id}")
        return {'statusCode': 200, 'body': 'ETL Cloud Completado'}

    except Exception as e:
        # 6. Tolerancia a Fallos
        if conn:
            conn.rollback() # Deshacer datos "a medias"
        logger.error(f"❌ Fallo E2E: {str(e)}")
        return {'statusCode': 500, 'body': 'Error ETL'}
        
    finally:
        # 7. Limpieza Absoluta e incondicional
        if conn:
            conn.close()
            logger.info("Conexión RDS cerrada de forma segura.")
```

*Zero Surprise Syntax:*
- `response['Body'].read().decode('utf-8')`: Extrae el flujo binario descargado, lo decodifica a texto y permite que `json.loads` lo parseé.
- `conn.commit()`: Le exige al servidor RDS que consolide los cambios permanentemente en el disco.
- `conn.rollback()`: Si hay un error, le ordena a RDS destruir los cambios temporales, devolviendo la base a su estado inmaculado.
- `finally: conn.close()`: Se ejecuta **siempre**, garantizando la muerte de las conexiones zombie sin importar cómo termine el script.

## 4. Conexión con Testing (Test-Driven Lore)

El testing End-to-End (E2E) simulado requiere orquestar múltiples mocks en la misma función.
En el Cap 05, tendrás que parchear tanto S3 como Postgres para asegurarte de que tu código interactúa con ambos.

- Se pueden apilar múltiples decoradores `@patch`. Se inyectan en los argumentos de abajo hacia arriba (el parche más cercano a la función es el primer argumento).

```python
from unittest.mock import patch, MagicMock

# Apilando múltiples parches (Mocks)
@patch('my_solution.psycopg2.connect') # Entra como mock_connect (argumento 2)
@patch('my_solution.boto3.client')     # Entra como mock_boto (argumento 1)
def test_pipeline_completo(mock_boto, mock_connect):
    
    # 1. Preparamos el mock de S3 para devolver un JSON falso
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {
        'Body': MagicMock(read=lambda: b'{"dragon_id": 42, "kilos_carne": 100}')
    }
    mock_boto.return_value = mock_s3
    
    # 2. Preparamos el mock de RDS 
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    
    # 3. Lanzamos el evento falso
    evento = {"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": "k"}}}]}
    
    # ... ejecutar tu código ...
    
    # 4. Aserciones orquestadas: Validamos que ambos servicios fueron tocados
    mock_s3.get_object.assert_called_once()
    mock_conn.commit.assert_called_once()
```

## 5. Mapa de Ejercicios

Termina tu aprendizaje en la nube con `quests/05-cloud-integration/`. Construye tu primer Pipeline E2E aplicando toda la tolerancia a fallos necesaria para sobrevivir en un entorno productivo.
