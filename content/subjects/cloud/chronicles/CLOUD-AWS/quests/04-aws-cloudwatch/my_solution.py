import logging

# Configure your logger here
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        instability = int(event.get('instability', 0))
        dragon_id = event.get('dragon_id', 'Unknown')

        logger.info(f"Processing report for dragon ID: {dragon_id}")

        if instability < 90:
            logger.info("Normal status. Finishing")
            return {'statusCode': 200}

        logger.error(
            f"CRITICAL DANGER! Dragon {dragon_id} about to explode. Level: {instability}")
        raise Exception("Catastrophic instability")
    except Exception as e:
        logger.error(f"Pipeline failure: {str(e)}")
        return {'statusCode': 500}
