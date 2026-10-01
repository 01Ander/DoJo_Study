import os
import logging
import psycopg2

logger = logging.getLogger()


def load_to_rds(data: dict) -> None:
    conn = None
    try:
        db_host = os.environ['DB_HOST']
        db_name = os.environ['DB_NAME']
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASSWORD']

        conn = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_pass)
        cur = conn.cursor()

        warehouse_id = data.get('warehouse_id')
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        cur.execute("INSERT INTO inventory_logs (warehouse_id, item_id, quantity) VALUES (%s, %s, %s)",
                    (warehouse_id, item_id, quantity))
        conn.commit()
        logger.info(f"Data insertion done for: {warehouse_id}, {item_id}")

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"❌ Critical failure in E2E pipeline: {str(e)}")
        raise e

    finally:
        if conn:
            conn.close()
            logger.info("RDS connection safely closed.")
