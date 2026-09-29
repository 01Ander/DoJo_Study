# Build the complete pipeline here from scratch.

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
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))

        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()

        dragon_id = payload.get('dragon_id')
        kg = payload.get('meat_kg', 0)

        cur.execute(
            "INSERT INTO consumptions (dragon_id, kg) VALUES (%s, %s)", (dragon_id, kg))

        conn.commit()
        logger.info(f"Insertion saved for drago {dragon_id}")

        return {'statusCode': 200, 'body': 'Cloud ETL Completed'}

    except Exception as e:

        if conn:
            conn.rollback()
        logger.error(f"E2E Failure: {str(e)}")
        return {'statusCode': 500, 'body': 'ETl processing error'}

    finally:
        if conn:
            conn.close()
            logger.info('RDS connection safely closed.')
