import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

def save_diet(dragon_id: int, diet_list: list):
    """
    Packages data into JSON, calculates the date-partitioned path,
    and uploads the payload to Amazon S3.
    """
    # 1. Load environment variables
    load_dotenv()
    
    # 2. Build report dictionary
    report = {
        "dragon_id": dragon_id,
        "diet": diet_list
    }
    
    # 3. Serialize to JSON string
    payload_json = json.dumps(report)
    
    # 4. Get current date and format it
    today = datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    
    # 5. Build date-partitioned key
    s3_key = f"raw/diets/{year}/{month}/{day}/dragon_{dragon_id}.json"
    bucket_name = 'dragon-food-swamp-prod'
    
    try:
        # 6. Connect to S3 and upload object
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=payload_json
        )
        return s3_key
        
    except Exception:
        # Return None if S3 or network fails
        return None
