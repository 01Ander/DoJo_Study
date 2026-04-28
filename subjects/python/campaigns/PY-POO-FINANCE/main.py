from src.csv_extractor import CSVExtractor
from src.analytics_engine import AnalyticsEngine
from src.json_loader import JSONLoader
from src.pipeline import FinancialPipeline


def main():
    extractor = CSVExtractor('data.csv')

    engine = AnalyticsEngine()
    loader = JSONLoader()

    pipeline = FinancialPipeline(extractor, engine, loader)

    try:
        result = pipeline.run(output_json='final_report.json')
        print(f"✅ Pipeline completado exitosamente!")
        print(f"📊 Resultados: {result}")
    except Exception as e:
        print(f"❌ Pipeline falló: {e}")


if __name__ == '__main__':
    main()
