# Capítulo 04: Orchestration & I/O

Ya tienes Extractores (Cap 01), Entidades (Cap 02) y Motores (Cap 03). Ahora necesitamos unirlos. El **Orquestador** es el director de la sinfonía.

## 1. El Orquestador

Un Orquestador es una clase cuyo único propósito es llamar a otras clases en el orden correcto. **No contiene lógica de negocio**, solo flujo.

### Analogía 1: El Director de Orquesta
El director de orquesta no toca el violín ni el piano. Su único trabajo es decirle al violín *cuándo* empezar y al piano *cuándo* detenerse. Si el director empieza a tocar un instrumento él mismo, la orquesta se descoordina. El Orquestador de tu código funciona igual: solo delega tareas a los Engines y Extractores.

### Analogía 2: El Contratista General
Cuando construyes una casa, contratas a un Contratista General. Él no pone ladrillos ni instala tuberías. Él llama al albañil primero, luego al plomero, y luego al electricista. 

## 2. Inyección de Dependencias (DI)

La "Inyección de Dependencias" es un término que asusta, pero el concepto es ridículamente simple: **pasar los objetos que necesitas como parámetros en lugar de crearlos por dentro.**

### Analogía 1: El Taladro en la Obra
Imagina que eres un carpintero que necesita hacer agujeros. 
- **Sin Inyección (Hardcoding):** Llegas a la obra, sacas metal y plástico, y te pones a fabricar un taladro desde cero ahí mismo antes de hacer el agujero.
- **Con Inyección:** Alguien te entrega un taladro ya armado antes de empezar a trabajar. Solo tienes que usarlo.

### Ejemplo de Código: Hardcoding vs Inyección

```python
# ❌ MAL: Hardcoding (Fabricando el taladro en la obra)
class GamePipeline:
    def __init__(self):
        # El pipeline crea sus propias dependencias. ¡Pésimo!
        # Si queremos cambiar a un loader de JSON, toca modificar esta clase.
        self.loader = CSVLoader()
        self.engine = PhysicsEngine()

# ✅ BIEN: Inyección de Dependencias (Recibiendo el taladro)
class GamePipeline:
    def __init__(self, loader: AbstractLoader, engine: GameEngine):
        # Alguien más creó el loader y el engine, nosotros solo los guardamos.
        self.loader = loader
        self.engine = engine
        
    def run(self, filepath: str):
        # 1. Extraer (I/O)
        raw_data = self.loader.load(filepath)
        
        # 2. Transformar / Procesar (Lógica pura)
        result = self.engine.process(raw_data)
        
        # 3. Retornar
        return result
```

¿Por qué inyectar es mejor? Porque si mañana quieres probar tu código, puedes inyectar un "Mock" (un objeto falso) que no toque el disco duro, y tu clase ni se dará cuenta del cambio.

## 3. I/O (Input/Output)

La lectura y escritura de archivos debe estar aislada en clases (como tu Extractor del Cap 01). El orquestador une el mundo exterior "sucio y propenso a errores" (I/O, bases de datos, APIs) con el mundo interior "limpio y testeable" (Motores).

## 4. Conexión con Testing (Nivel 4: Mocking)

Un test unitario **jamás** debe depender de que un archivo exista en el disco duro o de que haya internet. Para testear un Orquestador aislado del mundo real, usamos Mocks. Un Mock es un doble de acción que programamos para dar una respuesta fija.

```python
from unittest.mock import Mock

def test_game_pipeline():
    # Creamos objetos falsos (Mocks) que fingen ser las dependencias
    mock_loader = Mock()
    mock_loader.load.return_value = ["Nivel 1", "Nivel 2"]
    
    mock_engine = Mock()
    mock_engine.process.return_value = "Victoria"
    
    # Inyectamos los mocks en lugar de los objetos reales
    pipeline = GamePipeline(loader=mock_loader, engine=mock_engine)
    result = pipeline.run("dummy.txt")
    
    assert result == "Victoria"
    # Podemos verificar que el pipeline llamó a los mocks correctamente
    mock_loader.load.assert_called_once_with("dummy.txt")
```

## 5. Mapa de Ejercicios

Dirígete a `quests/04-orchestration/`:

- [[01-pipeline-assembly]]
- [[02-mocking-io]]

```text
PY-POO/quests/04-orchestration/
├── [[01-pipeline-assembly]].md      (Tipo A: Inyección de Dependencias)
└── [[02-mocking-io]].md             (Tipo B: Testing con Mocks)
```
