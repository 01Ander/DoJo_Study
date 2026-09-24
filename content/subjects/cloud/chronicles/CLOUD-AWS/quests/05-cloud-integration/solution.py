import os
import json
import logging
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Buena práctica: inicializar clientes fuera del handler para reutilizarlos en invocaciones cálidas
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Pipeline completo de Extracción (S3), Transformación (Python) y Carga (RDS)."""
    conn = None
    try:
        # 1. Extracción del origen
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Iniciando pipeline para s3://{bucket}/{key}")
        
        # 2. Descarga y Parseo
        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))
        
        # 3. Credenciales Nativas (Sin dotenv, extraídas del OS inyectado por AWS)
        db_host = os.environ['DB_HOST']
        db_name = os.environ['DB_NAME']
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASSWORD']
        
        # 4. Conexión a Base de Datos
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
        cur = conn.cursor()
        
        dragon_id = payload.get('dragon_id')
        kilos = payload.get('kilos_carne', 0)
        
        # 5. Inserción con parámetros seguros
        cur.execute("INSERT INTO consumos (dragon_id, kilos) VALUES (%s, %s)", (dragon_id, kilos))
        
        # 6. Transacción ACID exitosa
        conn.commit()
        logger.info(f"✅ Inserción confirmada para el dragón {dragon_id}")
        
        return {'statusCode': 200, 'body': 'ETL Cloud Completado'}

    except Exception as e:
        # 7. Tolerancia a fallos
        if conn:
            conn.rollback()
        logger.error(f"❌ Fallo crítico en el pipeline E2E: {str(e)}")
        return {'statusCode': 500, 'body': 'Error de procesamiento ETL'}
        
    finally:
        # 8. Limpieza incondicional
        if conn:
            conn.close()
            logger.info("Conexión RDS cerrada de forma segura.")
