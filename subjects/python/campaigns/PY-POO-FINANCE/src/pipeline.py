from src.abstract_extractor import AbstractExtractor
from src.transactions import map_all
from src.analytics_engine import AnalyticsEngine
from src.abstract_loader import AbstractLoader


class FinancialPipeline:
    def __init__(self, extractor, engine, loader):
        if not isinstance(extractor, AbstractExtractor):
            raise TypeError("extractor must be an AbstractExtractor instance")
        if not isinstance(engine, AnalyticsEngine):
            raise TypeError("engine must be an AnalyticsEngine instance")
        if not isinstance(loader, AbstractLoader):
            raise TypeError("loader must be an AbstractLoader instance")

        self.extractor = extractor
        self.engine = engine
        self.loader = loader

    def run(self, output_json: str) -> dict:
        raw = self.extractor.extract_data()
        transactions = map_all(raw)
        report = self.engine.calculate_report(transactions)
        categories = self.engine.aggregate_by_category(transactions)
        result = {**report, "expenses_by_category": categories}
        self.loader.load_data(result, filename=output_json)

        return result
