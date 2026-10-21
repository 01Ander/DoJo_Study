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

## 3. I/O (Input/Output) y la Separación ETL

En ingeniería de datos, un pipeline completo ejecuta el ciclo clásico **ETL**:
1. **Extract (I/O de Entrada):** Clases Extractoras (`BaseExtractor`) que leen de fuentes externas (CSV, JSON, APIs).
2. **Transform (Lógica Pura):** Clases Motor (`BaseEngine`) que calculan, filtran y transforman entidades sin tocar el disco ni la red.
3. **Load (I/O de Salida):** Clases Cargadoras (**`BaseOutputLoader`**) que persisten o emiten el resultado final al destino elegido.

El Orquestador es la pieza que ensambla este flujo inyectando tanto la entrada como la salida.

---

## 4. El Patrón Output Loader (Capa de Emisión y Persistencia)

### ¿QUÉ es?
Un **Output Loader** es una clase cuya única responsabilidad es recibir los datos ya procesados por el motor y transmitirlos al medio de destino (la consola estándar, un archivo JSON en disco, un bucket S3 o una tabla de base de datos).

### ¿POR QUÉ importa? (Principio Abierto/Cerrado - OCP)
Si el motor o el orquestador escribieran directamente en disco con `open("output.json", "w")`, cambiar el destino a una base de datos obligaría a modificar y arriesgar código que ya funcionaba. Al desacoplar la salida mediante una interfaz abstracta `BaseOutputLoader`, podemos cambiar el destino inyectando una subclase diferente sin alterar una sola línea del orquestador.

### ¿CÓMO se implementa? (Domain Shifting: Observatorio Astrofísico)

```python
# 🎯 Objetivo de Negocio: Desacoplar la persistencia de espectros astronómicos procesados mediante el patrón polimórfico Output Loader.

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseSpectralLoader(ABC):
    """Abstract interface defining the output loading contract."""

    @abstractmethod
    def load(self, records: List[Dict[str, Any]], destination: str) -> int:
        """
        Persists or emits processed records to the specified destination.
        Returns the total count of successfully loaded records.
        """
        pass


class ConsoleSpectralLoader(BaseSpectralLoader):
    """Concrete loader that emits formatted records to standard output."""

    def load(self, records: List[Dict[str, Any]], destination: str = "stdout") -> int:
        for item in records:
            print(f"[SPECTRAL-LOADER:{destination.upper()}] {item}")
        return len(records)


class JsonFileSpectralLoader(BaseSpectralLoader):
    """Concrete loader that serializes records into structured JSON files."""

    def load(self, records: List[Dict[str, Any]], destination: str) -> int:
        with open(destination, "w", encoding="utf-8") as file_handle:
            json.dump(records, file_handle, indent=2)
        return len(records)
```

---

## 5. El Ciclo ETL Completo en el Orquestador

Al ensamblar el pipeline, el Orquestador recibe por constructor todas sus dependencias externas mediante Inversión de Control:

```python
# 🎯 Objetivo de Negocio: Coordinar la extracción de señales estelares, su calibración y su persistencia desacoplada.

from typing import Any, Dict, List


class StellarObservationPipeline:
    """Orchestrator class coordinating extraction, transformation and loading."""

    def __init__(self, extractor: Any, engine: Any, loader: BaseSpectralLoader):
        self.extractor = extractor
        self.engine = engine
        self.loader = loader

    def run(self, source_path: str, output_destination: str) -> int:
        # 1. Extract (I/O de entrada)
        raw_signals = self.extractor.extract(source_path)

        # 2. Transform (Lógica pura y desacoplada)
        calibrated_signals = self.engine.process(raw_signals)

        # 3. Load (I/O de salida polimórfica)
        loaded_count = self.loader.load(calibrated_signals, output_destination)

        return loaded_count
```

---

## 6. Conexión con Testing (Ciclo AAA con Mocks para Orquestadores)

Un test unitario del Orquestador **jamás debe tocar el disco duro ni la red**. Usamos `unittest.mock.Mock` para simular tanto el Extractor como el Loader, verificando que los métodos sean llamados con los parámetros exactos y en el orden estricto.

```python
# 🎯 Objetivo de Negocio: Verificar que el orquestador coordine el ciclo ETL completo sin ejecutar operaciones de I/O reales.

from unittest.mock import Mock


def test_stellar_pipeline_coordinates_etl_flow():
    # Arrange: Configurar dobles de prueba (Mocks) para cada componente
    mock_extractor = Mock()
    mock_extractor.extract.return_value = [{"raw_wavelength": 656.3}]

    mock_engine = Mock()
    mock_engine.process.return_value = [{"calibrated_wavelength": 656.28, "element": "Hydrogen-Alpha"}]

    mock_loader = Mock()
    mock_loader.load.return_value = 1

    # Act: Inyectar dependencias y ejecutar el orquestador
    pipeline = StellarObservationPipeline(
        extractor=mock_extractor,
        engine=mock_engine,
        loader=mock_loader
    )
    result_count = pipeline.run(source_path="telescope_raw.dat", output_destination="spectral_db.json")

    # Assert: Validar retornos y que cada componente fue invocado en orden
    assert result_count == 1
    mock_extractor.extract.assert_called_once_with("telescope_raw.dat")
    mock_engine.process.assert_called_once_with([{"raw_wavelength": 656.3}])
    mock_loader.load.assert_called_once_with(
        [{"calibrated_wavelength": 656.28, "element": "Hydrogen-Alpha"}],
        "spectral_db.json"
    )
```

---

## 7. Mapa de Ejercicios

Dirígete a `quests/04-orchestration/`:

- [[01-pipeline-assembly]]
- [[02-mocking-io]]
- [[03-output-loaders]]

```text
PY-POO/quests/04-orchestration/
├── [[01-pipeline-assembly]].md      (Tipo A: Inyección de Dependencias)
├── [[02-mocking-io]].md             (Tipo B: Testing con Mocks)
└── [[03-output-loaders]].md         (Tipo A: Patrón Output Loaders)
```
