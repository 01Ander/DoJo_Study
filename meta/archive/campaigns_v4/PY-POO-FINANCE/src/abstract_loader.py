from abc import ABC, abstractmethod
from typing import Any


class AbstractLoader(ABC):
    """
    Abstract base class for data loaders.
    """

    @abstractmethod
    def load_data(self, data: Any, **kwargs) -> None:
        """
        Saves the provided payload to the target destination.
        :param data: The payload to be persisted (usually List[dict]).
        :param kwargs: Optional extra parameters.
        """
        pass
