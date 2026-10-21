"""
Módulo data_extractors.py — Quest 01-03: Extractor Desacoplado CSV y JSON

Completa la clase abstracta AbstractDataExtractor y sus implementaciones
concretas CSVDataExtractor y JSONDataExtractor.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import csv
import json


class AbstractDataExtractor(ABC):
    """Contrato abstracto para extracción uniforme de datos desde archivos."""

    @abstractmethod
    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extrae registros desde file_path y retorna una lista de diccionarios.
        """
        pass


class CSVDataExtractor(AbstractDataExtractor):
    """Extractor concreto para archivos delimitados por comas (CSV)."""

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        # TODO: Abrir file_path en modo lectura con encoding="utf-8"
        # TODO: Leer usando csv.DictReader y retornar lista de diccionarios [dict(row) for row in reader]
        with open(file_path, mode="r", encoding="utf-8") as file_handle:
            reader = csv.DictReader(file_handle)
            return [dict(row) for row in reader]


class JSONDataExtractor(AbstractDataExtractor):
    """Extractor concreto para archivos en formato JSON."""

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        # TODO: Abrir file_path en modo lectura con encoding="utf-8"
        # TODO: Parsear con json.load. Si es lista retornar la lista; si es dict retornar [data]
        with open(file_path, mode="r", encoding="utf-8") as file_handle:
            content = json.load(file_handle)
            if isinstance(content, list):
                return content
            return [content]
