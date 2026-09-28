import json
import boto3
from datetime import datetime
from dotenv import load_dotenv


def save_diet(dragon_id: int, diet_list: list) -> str:
    """
    Packages data into JSON, calculates the current date partitioned path,
    and uploads the payload to Amazon S3.
    """
    # 1. Ensure environment variables are loaded
    load_dotenv()

    # 2. Build dictionary with dragon_id and diet
    report = {
        'dragon_id': dragon_id,
        'diet': diet_list
    }
    # 3. Convert to JSON string
    payload = json.dumps(report)

    # 4. Get current date and format (YYYY, MM, DD)
    today = datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    # 5. Build partitioned path and upload object to S3 (use try/except)
    s3_key = f"raw/diets/{year}/{month}/{day}/dragon_{dragon_id}.json"
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(
            Bucket='Feed dragons',
            Key=s3_key,
            Body=payload
        )
        return s3_key
    except:
        return None
