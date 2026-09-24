import pytest
from unittest.mock import patch, MagicMock
from solution import consultar_estado

@patch('solution.psycopg2.connect')
def test_consultar_estado_exitoso(mock_connect):
    """Valida que la consulta sea parametrizada, retorne el dato y se cierre la conexión."""
    
    # Creamos simulacros para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Simulamos que fetchone() nos trae una tupla como lo haría PostgreSQL
    mock_cur.fetchone.return_value = (89,)
    
    resultado = consultar_estado(42)
    
    # Verificaciones de lógica
    assert resultado == 89, "Debería retornar 89 convertido a entero"
    
    # Verificaciones de seguridad SQL
    mock_cur.execute.assert_called_once()
    args_execute = mock_cur.execute.call_args[0]
    # Comprobar que no se usó f-strings para inyectar el ID, sino tuplas
    assert args_execute[1] == (42,), "El dragon_id debe pasarse como parámetro seguro a execute()"
    
    # Verificaciones de limpieza de recursos
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('solution.psycopg2.connect')
def test_consultar_estado_error_limpieza(mock_connect):
    """Valida que incluso si ocurre un error a mitad de camino, la conexión se cierra."""
    
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Simulamos que la tabla no existe y falla el execute
    mock_cur.execute.side_effect = Exception("Relation dragones_salud does not exist")
    
    resultado = consultar_estado(99)
    
    assert resultado is None, "Debería retornar None si hay error"
    
    # Lo más importante: se lanzó error en execute, pero close() en la conexión DEBE haber sido llamado
    mock_conn.close.assert_called_once()
