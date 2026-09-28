import os
import json
import logging
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Complete Extract (S3), Transform (Python), and Load (RDS) pipeline."""
    conn = None
    try:
        # 1. Source extraction
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Starting pipeline for s3://{bucket}/{key}")
        
        # 2. Download and parse
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))
        
        # 3. Native credentials (no dotenv, extracted from OS injected by AWS)
        db_host = os.environ['DB_HOST']
        db_name = os.environ['DB_NAME']
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASSWORD']
        
        # 4. Database connection
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
        cur = conn.cursor()
        
        dragon_id = payload.get('dragon_id')
        kg = payload.get('meat_kg', 0)
        
        # 5. Insertion with safe parameters
        cur.execute("INSERT INTO consumptions (dragon_id, kg) VALUES (%s, %s)", (dragon_id, kg))
        
        # 6. Successful ACID transaction
        conn.commit()
        logger.info(f"✅ Insertion confirmed for dragon {dragon_id}")
        
        return {'statusCode': 200, 'body': 'Cloud ETL Completed'}

    except Exception as e:
        # 7. Fault tolerance
        if conn:
            conn.rollback()
        logger.error(f"❌ Critical failure in E2E pipeline: {str(e)}")
        return {'statusCode': 500, 'body': 'ETL processing error'}
        
    finally:
        # 8. Unconditional cleanup
        if conn:
            conn.close()
            logger.info("RDS connection safely closed.")
