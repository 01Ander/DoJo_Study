from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractExtractor(ABC):
    """Base class for all data extractors.

    Subclass must implement the extract_data method to return raw records as a list of dictionaries.
    """

    @abstractmethod
    def extract_data(self) -> List[Dict[str, Any]]:
        """ Extract and return raw records as list of dicts.

        Must be implemented by concrete subclasses (CSVExtractor, JSONExtractor, etc...)
        """
        pass
