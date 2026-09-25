import pytest
import json
from unittest.mock import patch, MagicMock
import datetime

# Nota: Para evitar que el test falle mañana cuando cambie la fecha real, 
# tenemos que "burlarnos" (mock) de datetime.now()
class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

# Reemplazamos la clase datetime.datetime original por nuestro Mock en la solución
@patch('solution.datetime', MockDatetime)
@patch('boto3.client')
def test_guardar_dieta_exitoso(mock_boto):
    """Prueba que el JSON se genere bien, la ruta esté particionada y llame a S3 correctamente."""
    from solution import guardar_dieta
    
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3
    
    # Ejecutamos la función
    dieta = ["azufre", "rocas"]
    resultado = guardar_dieta(42, dieta)
    
    # Verificamos la ruta retornada (esperamos la fecha congelada 2026-09-24)
    key_esperada = "raw/dietas/2026/09/24/dragon_42.json"
    assert resultado == key_esperada, f"La función debía retornar {key_esperada}, pero retornó {resultado}"
    
    # Verificamos qué se le envió a S3
    mock_s3.put_object.assert_called_once()
    args_enviados = mock_s3.put_object.call_args[1]
    
    assert args_enviados['Bucket'] == 'alimento-dragones-pantano-prod', "El bucket incorrecto fue usado."
    assert args_enviados['Key'] == key_esperada, "La Key enviada a S3 no coincide."
    
    # Verificamos que el body sea un JSON válido con la info correcta
    cuerpo_enviado = json.loads(args_enviados['Body'])
    assert cuerpo_enviado['dragon_id'] == 42
    assert "azufre" in cuerpo_enviado['dieta']

@patch('boto3.client')
def test_guardar_dieta_error(mock_boto):
    """Prueba que un error de S3 sea atrapado y retorne None."""
    from solution import guardar_dieta
    
    mock_s3 = MagicMock()
    # Simulamos que S3 explota (ej. no hay permisos)
    mock_s3.put_object.side_effect = Exception("Access Denied")
    mock_boto.return_value = mock_s3
    
    resultado = guardar_dieta(99, ["ensalada"])
    
    assert resultado is None, "Si S3 lanza un error, la función debe retornar None."
