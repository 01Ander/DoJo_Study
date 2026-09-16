# Boss: Financial ETL Pipeline CLI

**Estado:** Aprobado para su realización.

Este es el proyecto integrador. Aquí aplicarás todos los conceptos aprendidos en los capítulos de teoría y ejercicios, sin andamiaje.

## Contexto de Negocio (Business Value)
Los scripts financieros monolíticos actuales son frágiles y difíciles de testear. Necesitamos una arquitectura Orientada a Objetos robusta que ingiera archivos CSV de transacciones, separe Ingresos de Gastos (polimorfismo), calcule agregaciones analíticas (stateless engine) y exponga todo a través de una CLI profesional.

---

## Fases de Despliegue (Desbloqueables)

No intentes hacer todo el Boss de golpe. Sigue las fases en orden. **Aplica TDD en cada fase.**

### Fase 1: Extraction Layer (Ref: Cap 00 + 01)
*El pipeline necesita saber leer de un archivo sin casarse con un formato específico.*
- Implementar una interfaz `AbstractExtractor` (módulo `abc`) con el método `extract(filepath: str) -> list[dict]`.
- Implementar `CSVExtractor` que herede de la interfaz y lea `data/transactions.csv`.
- **Error Handling (Ref: Cap 06):** Si el archivo no existe o la ruta es inválida, lanzar una excepción de dominio `DataSourceNotFoundError` (no usar `FileNotFoundError` genérico).
- **Testing Mínimo:** Validar que `AbstractExtractor` no se puede instanciar y que `CSVExtractor` retorna los datos correctos.

### Fase 2: Domain Entities (Ref: Cap 02)
*Los diccionarios no son seguros. Mapeemos los datos a objetos formales con Polimorfismo.*
- Crear una clase abstracta `Transaction` con propiedades `amount` y `date`.
- Crear subclases `Income` y `Expense`.
- **Testing Mínimo:** Validar que `Income` y `Expense` se instancian correctamente, que ambas son subclases de `Transaction`, y que cada una retorna su `amount` con el signo esperado (positivo para Income, negativo para Expense).

### Fase 3: Transformation Engine (Ref: Cap 03)
*El núcleo de procesamiento lógico, separado de la entrada/salida.*
- Implementar `AnalyticsEngine` (stateless).
- Debe tener un método `calculate_report(transactions: list[Transaction]) -> dict` que agregue totales por categoría.
- **Testing Mínimo (Ref: Cap 05):** Validar la agregación usando un **`@pytest.fixture`** que provea una lista de objetos `Transaction` de prueba.

### Fase 4: Orchestration & CLI (Ref: Cap 04 + 07)
*La interfaz de usuario y el ensamblaje final.*
- Implementar `PipelineOrchestrator` que reciba inyectados el Extractor y el Engine.
- Usar `argparse` (nativo) en un archivo `cli.py` para invocar el pipeline pasando el archivo de entrada como flag: `--input`.
- **Logging & Error Handling (Ref: Cap 06):** El Orquestador debe envolver la ejecución en `try/except`, atrapar excepciones de dominio (como `DataSourceNotFoundError`) y registrarlas con `logger.error()`. Configurar `logging.basicConfig` en `cli.py`.
- **Testing Mínimo (Ref: Cap 05):** Validar el orquestador usando **`unittest.mock.Mock`** para aislar el Extractor y el Engine. Verificar que al ejecutar el pipeline, este llama a `extractor.extract()` y a `engine.calculate_report()` en orden, sin tocar archivos reales.

---

## 🛠️ Diagnóstico Quirúrgico (En caso de atasco)
Si fallas al implementar una fase o los tests se vuelven un muro infranqueable (Friction > 8), acude al **Reviewer Socrático**. Si el Reviewer detecta una falla fundamental en el concepto, te indicará pausar el Boss y regresar a repasar el capítulo asociado (ej. "Vuelve a leer el Cap 02 de Lore y repite la Quest B").
