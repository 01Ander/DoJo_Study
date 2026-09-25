import pytest
import logging
from my_solution import lambda_handler

def test_lambda_handler_estado_normal(caplog):
    caplog.set_level(logging.INFO)
    evento = {"dragon_id": 10, "inestabilidad": 50}
    resultado = lambda_handler(evento, {})
    
    assert resultado is None
    mensajes = [record.message for record in caplog.records]
    assert "Procesando reporte del dragón ID: 10" in mensajes
    assert "Estado normal. Finalizando." in mensajes

def test_lambda_handler_estado_critico(caplog):
    caplog.set_level(logging.INFO)
    evento = {"dragon_id": 99, "inestabilidad": 95}
    with pytest.raises(Exception):
        lambda_handler(evento, {})
    mensajes_error = [record.message for record in caplog.records if record.levelname == 'ERROR']
    frase_esperada = "¡PELIGRO CRÍTICO! Dragón 99 a punto de explotar. Nivel: 95"
    assert frase_esperada in mensajes_error
    assert any("Fallo en el pipeline: Inestabilidad catastrófica" in m for m in mensajes_error)
