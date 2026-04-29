# Ejercicio 05-02: Test From Scratch (Nivel 4)

**Objetivo:** Escribir un test unitario completamente desde cero para una clase dada.

## Contexto (Domain Shifting: IoT)
Tienes una clase `Thermostat` que controla la temperatura.

```python
class Thermostat:
    def __init__(self):
        self.temperature = 20.0
        
    def increase(self, amount: float):
        self.temperature += amount
        if self.temperature > 30.0:
            self.temperature = 30.0 # Maximum cap
```

## Tu Tarea
Crea un archivo `test_thermostat.py` en esta carpeta y escribe **DOS tests unitarios desde cero**:

1. `test_thermostat_increases_temperature`: Debe verificar que si el termostato está en 20.0 y le sumas 5.0, el resultado es 25.0.
2. `test_thermostat_respects_maximum_cap`: Debe verificar que si el termostato está en 20.0 y le sumas 50.0, la temperatura no supera 30.0.

*No uses fixtures. Escribe GIVEN/WHEN/THEN (Arrange/Act/Assert) en ambos tests.*

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from thermostat import Thermostat

def test_thermostat_increases_temperature():
    # Arrange
    t = Thermostat()
    
    # Act
    t.increase(5.0)
    
    # Assert
    assert t.temperature == 25.0

def test_thermostat_respects_maximum_cap():
    # Arrange
    t = Thermostat()
    
    # Act
    t.increase(50.0)
    
    # Assert
    assert t.temperature == 30.0
```
</details>
