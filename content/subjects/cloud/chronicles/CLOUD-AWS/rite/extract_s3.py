import boto3
import json
import logging

logger = logging.getLogger()
s3_client = boto3.client('s3')


def extraction_from_s3(bucket: str, key: str) -> dict:
    try:

        response = s3_client.get_object(Bucket=bucket, Key=key)
        payload = json.loads(response['Body'].read().decode('utf-8'))

        return payload

    except Exception as e:
        logger.error(f"Fatal error a: {e}")
        raise e
