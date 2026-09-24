import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

def guardar_dieta(dragon_id: int, dieta_lista: list):
    """
    Empaqueta los datos en JSON, calcula la ruta particionada por fecha actual
    y sube el payload a Amazon S3.
    """
    # 1. Aseguramos entorno cargado (del Cap 00)
    load_dotenv()
    
    # 2. Armar el diccionario
    reporte = {
        "dragon_id": dragon_id,
        "dieta": dieta_lista
    }
    
    # 3. Convertir a string JSON
    payload_json = json.dumps(reporte)
    
    # 4. Obtener fecha actual y formatearla
    hoy = datetime.now()
    year = hoy.strftime('%Y')
    month = hoy.strftime('%m')
    day = hoy.strftime('%d')
    
    # 5. Construir la ruta (key) particionada
    s3_key = f"raw/dietas/{year}/{month}/{day}/dragon_{dragon_id}.json"
    bucket_name = 'alimento-dragones-pantano-prod'
    
    try:
        # 6. Conectar a S3 y subir el archivo
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=payload_json
        )
        return s3_key
        
    except Exception:
        # Si falla S3 o la red, retornamos None
        return None
