from src.extractors import AbstractExtractor
from src.engine import AnalyticsEngine
from src.transactions import build_transactions
import logging
from src.exceptions import DataSourceNotFoundError

logger = logging.getLogger(__name__)


class PipelineOrchestrator:

    def __init__(self, extractor: AbstractExtractor, engine: AnalyticsEngine):
        self.extractor = extractor
        self.engine = engine

    def run(self, filepath: str) -> dict:
        report = {}
        try:
            logger.info(f"Empezando a procesar: {filepath}")
            raw_data = self.extractor.extract(filepath)
            transactions = build_transactions(raw_data)
            report = self.engine.calculate_report(transactions)
            logger.info(report)
        except DataSourceNotFoundError as e:
            logger.error(f"Data source not found: {e}")

        return report
