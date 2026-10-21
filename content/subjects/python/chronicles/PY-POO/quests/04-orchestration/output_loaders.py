"""
Módulo output_loaders.py — Quest 04-03: Patrón Output Loaders y Orquestación ETL

Completa la clase abstracta BaseOutputLoader, los cargadores concretos
ConsoleOutputLoader y JsonFileOutputLoader, y el orquestador ManagedDataPipeline.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import json


class BaseOutputLoader(ABC):
    """Interfaz abstracta que define el contrato de persistencia/emisión de salida."""

    @abstractmethod
    def load(self, records: List[Dict[str, Any]], destination: str) -> int:
        """
        Persiste o emite los registros procesados al destino especificado.
        Retorna el número de registros cargados.
        """
        pass


class ConsoleOutputLoader(BaseOutputLoader):
    """Cargador concreto que emite registros a la consola estándar."""

    def load(self, records: List[Dict[str, Any]], destination: str = "console") -> int:
        # TODO: Iterar sobre records e imprimir cada uno precedido por f"[CONSOLE:{destination}] {record}"
        # TODO: Retornar el número de registros cargados (len(records))
        pass


class JsonFileOutputLoader(BaseOutputLoader):
    """Cargador concreto que serializa y persiste registros en un archivo JSON."""

    def load(self, records: List[Dict[str, Any]], destination: str) -> int:
        # TODO: Abrir destination en modo escritura con UTF-8
        # TODO: Serializar records usando json.dump(records, f, indent=2)
        # TODO: Retornar el número de registros cargados (len(records))
        pass


class ManagedDataPipeline:
    """Orquestador ETL que coordina extracción, transformación y carga desacoplada."""

    def __init__(self, extractor: Any, engine: Any, loader: BaseOutputLoader):
        # TODO: Almacenar extractor, engine y loader inyectados
        pass

    def run(self, source_path: str, destination_path: str) -> int:
        # TODO: 1. Extraer registros usando self.extractor.extract(source_path)
        # TODO: 2. Procesar registros usando self.engine.process(raw_records)
        # TODO: 3. Cargar registros usando self.loader.load(processed_records, destination_path)
        # TODO: 4. Retornar el conteo obtenido del loader
        pass
