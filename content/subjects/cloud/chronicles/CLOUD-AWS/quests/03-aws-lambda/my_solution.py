def lambda_handler(event, context):
    try:
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        return {
            'statusCode': 200,
            'body': f"File {s3_key} uploaded to {s3_bucket}"
        }
    except:
        return {
            'statusCode': 500,
            'body': 'Error'
        }
