def lambda_handler(event, context):
    """
    Entry point function for AWS Lambda. Reacts to an S3 Trigger,
    extracts the bucket and key, and returns a 200 success response.
    If the payload is invalid, returns 500.
    """
    try:
        # Extract surgically from the standard S3 payload
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Lambda requires a structure simulating an HTTP response
        return {
            'statusCode': 200,
            'body': f'File {key} uploaded to {bucket}'
        }
    except Exception:
        # If the event does not have the expected format, return a clean 500
        return {
            'statusCode': 500,
            'body': 'Error'
        }
