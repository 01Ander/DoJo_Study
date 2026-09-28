import os
import boto3
from dotenv import load_dotenv

def verify_identity():
    """
    Connects to AWS IAM using credentials injected via environment variables,
    and returns the username (UserName). If it fails, returns "Authentication failed".
    """
    # 1. Load environment variables
    load_dotenv()
    
    try:
        # 2. Create IAM client
        iam_client = boto3.client('iam')
        
        # 3. Retrieve user and extract username
        response = iam_client.get_user()
        username = response['User']['UserName']
        
        return username
        
    except Exception:
        # 4. Catch any cryptographic or network error
        return "Authentication failed"
