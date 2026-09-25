import pytest
from my_solution import lambda_handler

def test_lambda_handler_exitoso():
    """Valida que el handler sepa extraer las rutas anidadas del evento de S3 y retorne 200."""
    evento_s3 = {
        "Records": [
            {
                "eventSource": "aws:s3",
                "s3": {
                    "bucket": {"name": "maternidad-dragones-bucket"},
                    "object": {"key": "reportes/nuevo_nacimiento.json"}
                }
            }
        ]
    }
    
    # EJERCICIO: Ejecuta el handler de tu código y evalúa la respuesta.
    # El test está completo sin pistas, tu código debe hacerlo pasar exitosamente.
    resultado = lambda_handler(evento_s3, {})
    
    # En un sistema asíncrono, la función termina exitosamente sin retornar HTTP codes.
    assert resultado is None, "El handler asíncrono no debe retornar diccionarios HTTP."

def test_lambda_handler_error():
    """Valida que si el evento no tiene formato S3, la Lambda estalle hacia arriba."""
    evento_invalido = {"alguna_otra_cosa": 123}
    with pytest.raises(Exception):
        lambda_handler(evento_invalido, {})
