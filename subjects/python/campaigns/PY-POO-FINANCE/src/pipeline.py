from src.abstract_extractor import AbstractExtractor
from src.transactions import map_all
from src.analytics_engine import AnalyticsEngine
from src.abstract_loader import AbstractLoader
from src.utils.logger import setup_logger


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
        self.logger = setup_logger(name='src.pipeline')

    def run(self, output_json: str) -> dict:
        self.logger.info("Pipeline START")

        raw = self.extractor.extract_data()
        self.logger.info(f"PROGRESS: {len(raw)} raw records extracted")

        transactions = map_all(raw)
        self.logger.info(f"PROGRESS: {len(transactions)} transactions mapped")

        report = self.engine.calculate_report(transactions)
        categories = self.engine.aggregate_by_category(transactions)
        result = {**report, "expenses_by_category": categories}

        self.loader.load_data(result, filename=output_json)
        self.logger.info("Pipeline END")
        return result
