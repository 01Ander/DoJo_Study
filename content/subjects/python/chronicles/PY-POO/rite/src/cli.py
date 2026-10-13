import sys
from pathlib import Path

# Asegurar que el directorio raíz de rite esté en sys.path para soportar ejecución directa y modular
_rite_root = Path(__file__).resolve().parent.parent
if str(_rite_root) not in sys.path:
    sys.path.insert(0, str(_rite_root))

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
