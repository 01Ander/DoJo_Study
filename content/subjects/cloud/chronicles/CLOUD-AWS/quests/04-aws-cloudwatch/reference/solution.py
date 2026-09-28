import logging

# 1. Observability: Initialized globally for Lambda container reuse
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Receives the event, processes business rules, and sends the corresponding
    structured logs to Amazon CloudWatch.
    """
    try:
        # Extract business information
        dragon_id = event.get('dragon_id')
        instability = int(event.get('instability', 0))
        
        # Normal log to CloudWatch Log Stream
        logger.info(f"Processing report for dragon ID: {dragon_id}")
        
        # Alarm rule
        if instability >= 90:
            # This exact text triggers the Metric Filter in AWS
            logger.error(f"CRITICAL DANGER! Dragon {dragon_id} about to explode. Level: {instability}")
            # Break the flow so Lambda is marked as Failed in invocation metrics
            raise Exception("Catastrophic instability")
            
        logger.info("Normal status. Finishing.")
        return {'statusCode': 200}
        
    except Exception as e:
        logger.error(f"Pipeline failure: {str(e)}")
        return {'statusCode': 500}
