# Capítulo 04: Orchestration & I/O

Ya tienes Extractores (Cap 01), Entidades (Cap 02) y Motores (Cap 03). Ahora necesitamos unirlos. El **Orquestador** es el director de la sinfonía.

## 1. El Orquestador

Un Orquestador es una clase cuyo único propósito es llamar a otras clases en el orden correcto. **No contiene lógica de negocio**, solo flujo.

```python
class GamePipeline:
    def __init__(self, loader: AbstractLoader, engine: GameEngine):
        # Inyección de Dependencias: recibimos las herramientas ya armadas
        self.loader = loader
        self.engine = engine
        
    def run(self, filepath: str):
        # 1. Extraer (I/O)
        raw_data = self.loader.load(filepath)
        
        # 2. Transformar / Procesar (Lógica pura)
        result = self.engine.process(raw_data)
        
        # 3. Retornar o Guardar
        return result
```

## 2. Inyección de Dependencias (DI)

¿Por qué el Orquestador recibe el `loader` y el `engine` en el `__init__` en vez de instanciarlos él mismo por dentro?
Porque si los instancia por dentro, el Orquestador queda **fuertemente acoplado**. Si los recibe por fuera, podemos pasarle un `MockLoader` durante los tests, haciendo que probar el Orquestador sea rapidísimo y no toque el disco duro.

## 3. I/O (Input/Output)

La lectura y escritura de archivos debe estar aislada en clases (como tu Extractor del Cap 01). El orquestador une el mundo exterior (I/O) con el mundo interior (Motores).

## 4. Conexión con Testing (Nivel 4: Mocking)

```python
from unittest.mock import Mock

def test_game_pipeline():
    # Creamos objetos falsos (Mocks)
    mock_loader = Mock()
    mock_loader.load.return_value = ["Nivel 1", "Nivel 2"]
    
    mock_engine = Mock()
    mock_engine.process.return_value = "Victoria"
    
    # Inyectamos los mocks
    pipeline = GamePipeline(mock_loader, mock_engine)
    result = pipeline.run("dummy.txt")
    
    assert result == "Victoria"
```

## 5. Mapa de Ejercicios

Dirígete a `exercises/04-orchestration/`:

```text
PY-POO/exercises/04-orchestration/
├── 01-pipeline-assembly.md      (Tipo A: Inyección de Dependencias)
└── 02-mocking-io.md             (Tipo B: Testing con Mocks)
```
