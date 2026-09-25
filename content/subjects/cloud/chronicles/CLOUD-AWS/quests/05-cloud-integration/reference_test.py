import pytest
import os
import json
from unittest.mock import patch, MagicMock

# Evento simulado de S3
EVENTO_S3 = {
    "Records": [{"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.json"}}}]
}

@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('solution.psycopg2.connect')
@patch('solution.boto3.client')
def test_pipeline_exitoso(mock_boto, mock_connect):
    """Valida el flujo feliz: S3 -> Python -> RDS -> Commit."""
    from solution import lambda_handler
    
    # Mockeamos S3 devolviendo un archivo JSON válido
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({"dragon_id": 42, "kilos_carne": 100}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    # Mockeamos PostgreSQL
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Ejecutamos el pipeline
    resultado = lambda_handler(EVENTO_S3, {})
    
    assert resultado['statusCode'] == 200, "Debe retornar 200 en éxito."
    
    # Verificaciones S3
    mock_s3.get_object.assert_called_once_with(Bucket="test-bucket", Key="test.json")
    
    # Verificaciones RDS ACID
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()

@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('solution.psycopg2.connect')
@patch('solution.boto3.client')
def test_pipeline_falla_rollback(mock_boto, mock_connect):
    """Valida que si RDS explota durante la inserción, el pipeline hace rollback y cierra."""
    from solution import lambda_handler
    
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({"dragon_id": 99}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Simulamos que el disco de la BD está lleno y explota
    mock_cur.execute.side_effect = Exception("Disk full")
    
    resultado = lambda_handler(EVENTO_S3, {})
    
    assert resultado['statusCode'] == 500, "Debe retornar 500 en fallo."
    
    # Verificaciones de Resiliencia
    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
