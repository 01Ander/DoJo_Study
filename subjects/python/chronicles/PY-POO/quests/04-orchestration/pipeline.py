class RecipePipeline:
    def __init__(self, reader: Reader, calculator: Calculator):
        self.reader = reader
        self.calculator = calculator

    def execute(self, filepath: str):
        raw_data = self.reader.reader_recipes(filepath)
        result = self.calculator.calculate(raw_data)
        return result
