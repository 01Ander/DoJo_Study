import os
import psycopg2
from dotenv import load_dotenv

def check_status(dragon_id: int):
    """
    Connects to PostgreSQL on RDS securely and returns the dragon's
    instability level. Guarantees connection cleanup.
    """
    load_dotenv()
    
    host = os.environ.get('DB_HOST')
    database = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    
    conn = None
    try:
        # Open TCP tunnel to RDS
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432"
        )
        cur = conn.cursor()
        
        # Use parameterized query to avoid SQL Injection
        query = "SELECT instability_level FROM dragons_health WHERE dragon_id = %s"
        cur.execute(query, (dragon_id,))
        
        # Fetch first row (tuple or None)
        result = cur.fetchone()
        cur.close()
        
        if result:
            return int(result[0])
        else:
            return None
            
    except Exception:
        # Handle connection, auth, or query failures
        return None
        
    finally:
        # Guarantee connection cleanup
        if conn is not None:
            conn.close()
