# Capítulo 06: Logging y Error Handling

Un pipeline fallará en producción. Archivos corruptos, APIs caídas, datos faltantes. Si usas `print()`, esa información se pierde al cerrar la consola o al rotar los contenedores en la nube. 

## 1. El Módulo Logging

El módulo `logging` es la forma profesional de registrar eventos en un sistema. 

### Analogía: La Caja Negra del Avión
Imagina que vas en un avión y hay turbulencia. 
- **Usar `print()`:** Es como si el piloto abriera la ventana y gritara "¡Hay turbulencia!". Si nadie lo escuchó en ese exacto milisegundo, la información se pierde para siempre.
- **Usar `logging`:** Es la Caja Negra del avión. Registra exactamente la hora, la severidad del problema (INFO, WARNING, ERROR, CRITICAL) y el mensaje. Si el avión aterriza (o se estrella), los ingenieros pueden abrir la caja negra y ver todo el historial de vuelo.

### Ejemplo de Código
```python
# ❌ MAL: print no tiene contexto ni niveles
print("Empezando a procesar el archivo")
print("Error: archivo no encontrado")

# ✅ BIEN: logging
import logging

# Configuración básica (generalmente en el Orquestador o en cli.py)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FileProcessor:
    def process(self, filepath: str):
        logger.info(f"Empezando a procesar: {filepath}")
        # ...
        logger.warning("Campo edad vacío, usando default.")
        # ...
        logger.error("Archivo no encontrado. Abortando operación.")
```

## 2. Excepciones Personalizadas (Domain Exceptions)

En Python existen errores como `ValueError` o `TypeError`. Pero en código empresarial, necesitamos atrapar errores específicos del negocio para saber exactamente qué falló.

### Analogía: Las Luces del Tablero del Auto
Imagina que tu auto se descompone.
- **Sin Excepciones Custom:** Solo se enciende una luz roja gigante que dice "ERROR". Podría ser que no tienes gasolina, o podría ser que el motor explotó. No tienes idea de cómo solucionarlo.
- **Con Excepciones Custom:** El tablero tiene luces específicas: "Presión de Aceite Baja", "Puerta Abierta", "Sin Gasolina". Sabes exactamente cuál es el problema y cómo reaccionar.

### Ejemplo de Código
```python
# Creamos nuestras "luces del tablero" personalizadas
class InvalidTransactionError(Exception):
    pass

class ExpiredCardError(Exception):
    pass

class Engine:
    def process(self, amount, card_year):
        if amount < 0:
            # Encendemos la luz específica
            raise InvalidTransactionError(f"El monto no puede ser negativo: {amount}")
        if card_year < 2024:
            raise ExpiredCardError("La tarjeta está vencida")
```

## 3. Manejo en el Orquestador

El orquestador es quien atrapa estas excepciones de dominio, loggea el error crítico, y decide si el pipeline aborta de forma segura o continúa con el siguiente registro (por ejemplo, ignorar la transacción mala y seguir con la siguiente).

```python
    def run(self):
        try:
            self.engine.process(-5, 2025)
        except InvalidTransactionError as e:
            # Atrapamos la luz de advertencia y la guardamos en la caja negra
            logger.error(f"Falla en el pipeline: {e}")
```

## 4. Conexión con Testing (Nivel 2)

Podemos testear que nuestra clase levante (raise) la excepción correcta cuando debe hacerlo usando `pytest.raises`.

```python
import pytest

def test_raises_invalid_transaction():
    engine = Engine()
    # "Esperamos que este bloque de código arroje un InvalidTransactionError"
    with pytest.raises(InvalidTransactionError):
        engine.process(-5, 2025)
```

## 5. Mapa de Ejercicios

Dirígete a `quests/06-logging/`:

- [[01-custom-exceptions]]
- [[02-test-exceptions]]

```text
PY-POO/quests/06-logging/
├── [[01-custom-exceptions]].md      (Tipo A: Lanzar Errores)
└── [[02-test-exceptions]].md        (Tipo B: Testing Nivel 2)
```
