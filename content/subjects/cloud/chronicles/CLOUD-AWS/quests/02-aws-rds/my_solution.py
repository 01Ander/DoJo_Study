import os
import psycopg2
from dotenv import load_dotenv


def check_status(dragon_id: int):
    """
    Connects to PostgreSQL securely and returns the dragon's instability level.
    Guarantees connection cleanup in a finally block.
    """
    # 1. Load environment variables
    load_dotenv()

    # 2. Extract DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

    host = os.environ.get('DB_HOST')
    database = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')

    conn = None

    # 3. try/except/finally block:
    #    - Connect and create cursor
    #    - Execute parameterized query (SELECT instability_level FROM dragons_health WHERE dragon_id = %s)
    #    - Return level (integer) or None on failure
    #    - Always clean up resources
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432"
        )
        cur = conn.cursor()
        query = "SELECT instability_level FROM dragons_health WHERE dragon_id = %s"
        cur.execute(query, (dragon_id,))
        record = cur.fetchone()
        return record[0]
    except:
        return None
    finally:
        if 'cur' in locals():
            cur.close()
        if conn is not None:
            conn.close()
