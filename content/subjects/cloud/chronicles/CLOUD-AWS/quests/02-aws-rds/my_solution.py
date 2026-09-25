import os
import psycopg2
from dotenv import load_dotenv

def consultar_estado(dragon_id: int):
    """
    Se conecta a PostgreSQL de forma segura y devuelve el nivel de inestabilidad.
    Garantiza el cierre de la conexión en un bloque finally.
    """
    # 1. Cargar variables de entorno
    
    # 2. Extraer DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    
    # 3. Bloque try/except/finally:
    #    - Conectar y crear cursor
    #    - Ejecutar query parametrizado (SELECT nivel_inestabilidad FROM dragones_salud WHERE dragon_id = %s)
    #    - Retornar nivel (entero) o None si falla
    #    - Cerrar recursos siempre
    
    pass
