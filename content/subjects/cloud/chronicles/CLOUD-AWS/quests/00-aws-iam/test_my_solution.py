import pytest
from unittest.mock import patch, MagicMock
from my_solution import verificar_identidad

def test_verificar_identidad_exitoso():
    """Valida que la función retorne el nombre de usuario cuando la API de AWS responde exitosamente."""
    mock_respuesta_aws = {'User': {'UserName': 'novato-cuidador-dragones'}}
    
    with patch('my_solution.boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.return_value = mock_respuesta_aws
        mock_boto.return_value = mock_iam
        
        # EJERCICIO: Ejecuta la función verificar_identidad() y haz un assert de que retorne el usuario esperado
        # Tu código aquí:
        
        pass

def test_verificar_identidad_error():
    """Valida que la función atrape la excepción y retorne el mensaje de error por defecto."""
    with patch('my_solution.boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.side_effect = Exception("Invalid Access Key")
        mock_boto.return_value = mock_iam
        
        # EJERCICIO: Ejecuta verificar_identidad() y asegúrate de que atrape el error devolviendo "Error de autenticación"
        # Tu código aquí:
        
        pass
