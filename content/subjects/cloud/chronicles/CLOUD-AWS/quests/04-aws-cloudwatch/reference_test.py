import pytest
import logging
from solution import lambda_handler

def test_lambda_handler_estado_normal(caplog):
    """Valida que un dragón estable loguee correctamente INFO y retorne 200 sin lanzar excepciones."""
    caplog.set_level(logging.INFO)
    
    evento = {"dragon_id": 10, "inestabilidad": 50}
    resultado = lambda_handler(evento, {})
    
    assert resultado['statusCode'] == 200, "Debe retornar 200 si la inestabilidad es < 90"
    
    # Verificamos los logs inyectados a CloudWatch
    mensajes = [record.message for record in caplog.records]
    assert "Procesando reporte del dragón ID: 10" in mensajes
    assert "Estado normal. Finalizando." in mensajes

def test_lambda_handler_estado_critico(caplog):
    """Valida que un dragón inestable loguee ERROR con la frase exacta y retorne 500."""
    caplog.set_level(logging.INFO)
    
    evento = {"dragon_id": 99, "inestabilidad": 95}
    resultado = lambda_handler(evento, {})
    
    assert resultado['statusCode'] == 500, "La excepción catastrófica debió ser atrapada y retornar 500."
    
    mensajes_error = [record.message for record in caplog.records if record.levelname == 'ERROR']
    
    # La frase debe ser idéntica para que el Metric Filter del Gremio funcione
    frase_esperada = "¡PELIGRO CRÍTICO! Dragón 99 a punto de explotar. Nivel: 95"
    assert frase_esperada in mensajes_error, f"Falta el log de error crítico exacto para CloudWatch. Esperado: {frase_esperada}"
    
    # Validamos que el try/except global también logueó el fallo final
    assert any("Fallo en el pipeline: Inestabilidad catastrófica" in m for m in mensajes_error), "No se logueó la excepción final."
