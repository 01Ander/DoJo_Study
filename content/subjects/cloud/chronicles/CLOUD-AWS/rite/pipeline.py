import os
import json
import logging
import boto3
import psycopg2
from extract_s3 import extraction_from_s3
from rds import load_to_rds


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Starting pipeline for s3://{bucket}/{key}")

        result = extraction_from_s3(bucket=bucket, key=key)

        warehouse_id = result.get('warehouse_id')
        item_id = result.get('item_id')
        quantity = result.get('quantity')

        if not warehouse_id or not item_id or quantity is None or quantity <= 0:
            logger.error("VALIDATION_FAILED: Payload corrupt or invalid")
            raise ValueError("VALIDATION_FAILED: Payload corrupt or invalid")

        load_to_rds(result)

    except Exception as e:
        logger.error(f"❌ Critical failure in E2E pipeline: {str(e)}")
        raise e
