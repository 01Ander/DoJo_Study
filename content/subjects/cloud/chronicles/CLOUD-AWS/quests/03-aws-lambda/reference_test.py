import pytest
from solution import lambda_handler

def test_lambda_handler_exitoso():
    """Valida que el handler sepa extraer las rutas anidadas del evento de S3 y retorne 200."""
    
    # Evento simulado idéntico a los que emite AWS S3 internamente
    evento_s3 = {
        "Records": [
            {
                "eventSource": "aws:s3",
                "s3": {
                    "bucket": {
                        "name": "maternidad-dragones-bucket"
                    },
                    "object": {
                        "key": "reportes/nuevo_nacimiento.json"
                    }
                }
            }
        ]
    }
    
    # Context vacío simulado
    context_simulado = {}
    
    resultado = lambda_handler(evento_s3, context_simulado)
    
    assert type(resultado) is dict, "El handler debe retornar un diccionario."
    assert resultado.get('statusCode') == 200, "Debe retornar statusCode 200 en éxito."
    assert resultado.get('body') == "Archivo reportes/nuevo_nacimiento.json subido a maternidad-dragones-bucket"

def test_lambda_handler_error():
    """Valida que si el evento no tiene formato S3, la Lambda retorne 500 sin explotar."""
    
    evento_invalido = {"alguna_otra_cosa": 123}
    
    resultado = lambda_handler(evento_invalido, {})
    
    assert resultado.get('statusCode') == 500, "Debe retornar 500 si falla la extracción."
    assert resultado.get('body') == "Error"
