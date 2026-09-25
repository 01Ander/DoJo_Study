import pytest
import json
from unittest.mock import patch, MagicMock
import datetime

class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

# Aplicamos los parches necesarios para simular S3 y congelar el tiempo
@patch('my_solution.datetime', MockDatetime)
@patch('my_solution.boto3.client')
def test_guardar_dieta_exitoso(mock_boto):
    from my_solution import guardar_dieta
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3
    
    dieta = ["azufre", "rocas"]
    
    # EJERCICIO: Llama a guardar_dieta(42, dieta) y verifica con assert que retorne "raw/dietas/2026/09/24/dragon_42.json"
    # Tu código aquí:
    
    pass
