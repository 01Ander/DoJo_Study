import pytest
from my_solution import verificar_permisos
import json
import os

def test_verificar_permisos(tmp_path):
    """Verifica la lógica de parsing de la política simulada."""
    d = tmp_path / "policies"
    d.mkdir()
    p = d / "test_policy.json"
    
    mock_policy = {
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"]
            }
        ]
    }
    p.write_text(json.dumps(mock_policy))
    
    # EJERCICIO: Llama a verificar_permisos con p y "s3:GetObject" y haz un assert de que retorne True
    # Tu código aquí:
    
    pass
