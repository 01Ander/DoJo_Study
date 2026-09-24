import os
import psycopg2
from dotenv import load_dotenv

def consultar_estado(dragon_id: int):
    """
    Se conecta a PostgreSQL en RDS de forma segura y devuelve el nivel de 
    inestabilidad del dragón consultado. Garantiza el cierre de la conexión.
    """
    load_dotenv()
    
    host = os.environ.get('DB_HOST')
    database = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    
    conn = None
    try:
        # Abrimos túnel TCP a RDS
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432"
        )
        # Creamos cursor
        cur = conn.cursor()
        
        # Armamos el query con parámetros seguros para evitar SQL Injection
        query = "SELECT nivel_inestabilidad FROM dragones_salud WHERE dragon_id = %s"
        cur.execute(query, (dragon_id,))
        
        # Traemos la primera fila (fetchone devuelve una tupla o None)
        resultado = cur.fetchone()
        
        # Cerramos cursor inmediatamente
        cur.close()
        
        if resultado:
            return int(resultado[0])
        else:
            return None
            
    except Exception:
        # Cualquier error de contraseña, red, o SQL explota y cae aquí.
        return None
        
    finally:
        # Bloque vital: si conn existe, cerramos la conexión para no dejar zombies
        if conn is not None:
            conn.close()
