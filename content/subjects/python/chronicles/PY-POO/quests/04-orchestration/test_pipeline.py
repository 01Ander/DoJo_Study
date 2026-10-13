from unittest.mock import Mock
from pipeline import RecipePipeline


def test_recipe_pipeline():
    # Arrange
    mock_reader = Mock()
    mock_reader.read_recipes.return_value = ["Pizza"]

    mock_calc = Mock()
    mock_calc.calculate.return_value = 1500

    pipeline = RecipePipeline(reader=mock_reader, calculator=mock_calc)

    # Act
    result = pipeline.execute("data.txt")

    # Assert
    assert result == 1500
    mock_reader.read_recipes.assert_called_once_with("data.txt")
    mock_calc.calculate.assert_called_once_with(["Pizza"])
