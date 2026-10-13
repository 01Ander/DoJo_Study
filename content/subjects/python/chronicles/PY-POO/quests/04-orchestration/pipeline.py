class RecipePipeline:
    def __init__(self, reader, calculator):
        self.reader = reader
        self.calculator = calculator

    def execute(self, file_path: str):
        recipes = self.reader.read_recipes(file_path)
        total_calories = self.calculator.calculate(recipes)
        return total_calories
