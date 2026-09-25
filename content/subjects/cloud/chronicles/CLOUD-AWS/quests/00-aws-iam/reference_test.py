import pytest
from unittest.mock import patch, MagicMock
from solution import verificar_identidad

def test_verificar_identidad_exitoso():
    """Valida que la función retorne el nombre de usuario cuando la API de AWS responde exitosamente."""
    
    # Creamos un simulacro (mock) de lo que respondería AWS
    mock_respuesta_aws = {
        'User': {
            'UserName': 'novato-cuidador-dragones'
        }
    }
    
    # Parcheamos (interceptamos) la llamada a boto3.client para que no vaya a internet
    with patch('boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.return_value = mock_respuesta_aws
        mock_boto.return_value = mock_iam
        
        # Ejecutamos la función del Operador
        resultado = verificar_identidad()
        
        assert resultado == 'novato-cuidador-dragones', "La función debe retornar el UserName extraído de la respuesta."

def test_verificar_identidad_error():
    """Valida que la función atrape la excepción y retorne el mensaje de error por defecto."""
    
    # Interceptamos la llamada para forzar un error (simulando credenciales malas)
    with patch('boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.side_effect = Exception("Invalid Access Key")
        mock_boto.return_value = mock_iam
        
        resultado = verificar_identidad()
        
        assert resultado == "Error de autenticación", "La función debe atrapar excepciones y retornar 'Error de autenticación'."
