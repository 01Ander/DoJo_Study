# Capítulo 06: Logging y Error Handling

Un pipeline fallará en producción. Archivos corruptos, APIs caídas, datos faltantes. Si usas `print()`, esa información se pierde al cerrar la consola.

## 1. El Módulo Logging

```python
import logging

# Configuración básica (generalmente en el Orquestador o en cli.py)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FileProcessor:
    def process(self, filepath: str):
        logger.info(f"Empezando a procesar: {filepath}")
        # ...
        logger.warning("Campo edad vacío, usando default.")
        # ...
        logger.error("Archivo no encontrado.")
```

## 2. Excepciones Personalizadas (Domain Exceptions)

En vez de atrapar genéricos `ValueError`, creamos excepciones que hablen el idioma de nuestro negocio.

```python
class InvalidTransactionError(Exception):
    pass

class Engine:
    def process(self, amount):
        if amount < 0:
            raise InvalidTransactionError(f"Amount cannot be negative: {amount}")
```

## 3. Manejo en el Orquestador

El orquestador atrapa la excepción de dominio, loggea el error crítico, y decide si el pipeline aborta de forma segura o continúa con el siguiente registro.

```python
    def run(self):
        try:
            self.engine.process(-5)
        except InvalidTransactionError as e:
            logger.error(f"Falla en el pipeline: {e}")
```

## 4. Conexión con Testing (Nivel 2)

```python
import pytest

def test_raises_invalid_transaction():
    engine = Engine()
    with pytest.raises(InvalidTransactionError):
        engine.process(-5)
```

## 5. Mapa de Ejercicios

Dirígete a `quests/06-logging/`:

```text
PY-POO/quests/06-logging/
├── 01-custom-exceptions.md      (Tipo A: Lanzar Errores)
└── 02-test-exceptions.md        (Tipo B: Testing Nivel 2)
```
