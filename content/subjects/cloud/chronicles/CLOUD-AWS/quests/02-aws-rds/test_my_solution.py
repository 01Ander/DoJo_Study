import pytest
from unittest.mock import patch, MagicMock
from my_solution import consultar_estado

@patch('my_solution.psycopg2.connect')
def test_consultar_estado_exitoso(mock_connect):
    """Valida la consulta parametrizada y cierre de conexión."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Simulamos el retorno de fetchone()
    mock_cur.fetchone.return_value = (89,)
    
    # EJERCICIO: Ejecuta la función consultar_estado(42) y haz los assert lógicos
    # Asegúrate de verificar también que se llamó a mock_conn.close()
    # Tu código aquí:
    
    pass
