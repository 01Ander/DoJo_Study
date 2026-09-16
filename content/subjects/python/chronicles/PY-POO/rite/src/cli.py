import argparse
from src.pipeline import PipelineOrchestrator
from src.extractors import CSVExtractor
from src.engine import AnalyticsEngine
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description="Pipeline financial")
    parser.add_argument("--input", required=True, help="Filepath")
    args = parser.parse_args()

    extractor = CSVExtractor()
    engine = AnalyticsEngine()
    orchestrator = PipelineOrchestrator(extractor=extractor, engine=engine)

    orchestrator.run(args.input)


if __name__ == "__main__":
    main()
