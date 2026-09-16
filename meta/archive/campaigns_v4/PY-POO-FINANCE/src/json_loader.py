import json
from src.abstract_loader import AbstractLoader


class JSONLoader(AbstractLoader):
    """
    Concrete implementation that saves data to a JSON file.
    """

    def load_data(self, data, **kwargs) -> None:
        filename = kwargs.get('filename', 'output.json')
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
