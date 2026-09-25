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
        
    except Exception as e:
        # 6. Tolerancia a Fallos
        if conn:
            conn.rollback() # Deshacer datos "a medias"
        logger.error(f"❌ Fallo E2E: {str(e)}")
        raise e # Relanzamos para que CloudWatch marque la Lambda como fallida
        
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

## 6. Conexión con Testing (Test-Driven Lore)

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

## 7. Mapa de Ejercicios

Termina tu aprendizaje en la nube con `quests/05-cloud-integration/`. Construye tu primer Pipeline E2E aplicando toda la tolerancia a fallos necesaria para sobrevivir en un entorno productivo.
