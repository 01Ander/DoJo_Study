import os
import boto3
from dotenv import load_dotenv

def verificar_identidad():
    """
    Se conecta al servicio IAM de AWS usando credenciales inyectadas por variables de entorno,
    y retorna el nombre del usuario (UserName). Si falla, retorna "Error de autenticación".
    """
    # 1. Cargar las variables de entorno
    load_dotenv()
    
    try:
        # 2. Crear cliente IAM
        iam_client = boto3.client('iam')
        
        # 3. Obtener el usuario y extraer el nombre
        response = iam_client.get_user()
        usuario = response['User']['UserName']
        
        return usuario
        
    except Exception:
        # 4. Atrapar cualquier error criptográfico o de red
        return "Error de autenticación"
