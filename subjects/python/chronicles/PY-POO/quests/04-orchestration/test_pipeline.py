from unittest.mock import Mock
from pipeline import RecipePipeline


def test_pipeline_calories():
    mock_reader = Mock()
    mock_reader.reader.reader_recipes = ["Pizza"]

    mock_calculator = Mock()
    mock_calculator.calculator.calculate = 1500

    pipeline = RecipePipeline(reader=mock_reader, calculator=mock_calculator)
    result = pipeline.run('data.txt')

    assert result == 1500

    mock_reader.reader_recipes.assert_called_once_with('data.txt')
    mock_calculator.calculate.assert_called_once_with("Pizza")
