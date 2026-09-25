import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

def guardar_dieta(dragon_id: int, dieta_lista: list) -> str:
    """
    Empaqueta los datos en JSON, calcula la ruta particionada por fecha actual
    y sube el payload a Amazon S3.
    """
    # 1. Asegura que el entorno esté cargado
    
    # 2. Arma el diccionario con dragon_id y dieta
    
    # 3. Convierte a JSON string
    
    # 4. Obtén la fecha actual y formatea (YYYY, MM, DD)
    
    # 5. Construye la ruta particionada y sube el objeto a S3 (usa try/except)
    
    pass
