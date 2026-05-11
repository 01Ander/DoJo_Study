# Boss: Financial ETL Pipeline CLI

**Estado:** 🔒 Bloqueado (Requiere autorización del DM en `grimoire.md`)

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
- **Testing Mínimo:** Validar que `AbstractExtractor` no se puede instanciar y que `CSVExtractor` retorna los datos correctos.

### Fase 2: Domain Entities (Ref: Cap 02)
*Los diccionarios no son seguros. Mapeemos los datos a objetos formales con Polimorfismo.*
- Crear una clase abstracta `Transaction` con propiedades `amount` y `date`.
- Crear subclases `Income` y `Expense`.
- Sobrescribir el método de representación para imprimir formatos limpios.
- **Testing Mínimo:** Validar instanciación polimórfica (asegurar que Income suma al neto y Expense resta, o que sus tipos son correctos).

### Fase 3: Transformation Engine (Ref: Cap 03)
*El núcleo de procesamiento lógico, separado de la entrada/salida.*
- Implementar `AnalyticsEngine` (stateless).
- Debe tener un método `calculate_report(transactions: list[Transaction]) -> dict` que use `collections.defaultdict` para agregar totales por categoría.
- **Testing Mínimo:** Validar la agregación usando objetos `Transaction` mockeados en el test.

### Fase 4: Orchestration & CLI (Ref: Cap 04 + 07)
*La interfaz de usuario y el ensamblaje final.*
- Implementar `PipelineOrchestrator` que reciba inyectados el Extractor y el Engine.
- Usar `Typer` o `Click` en un archivo `cli.py` para invocar el pipeline pasando el archivo de entrada como flag: `--input-file`.
- **Testing Mínimo:** Validar invocación de CLI usando `CliRunner` (Exit code 0).

---

## 🛠️ Diagnóstico Quirúrgico (En caso de atasco)
Si fallas al implementar una fase o los tests se vuelven un muro infranqueable (Friction > 8), acude al **Reviewer Socrático**. Si el Reviewer detecta una falla fundamental en el concepto, te indicará pausar el Boss y regresar a repasar el capítulo asociado (ej. "Vuelve a leer el Cap 02 de Lore y repite la Quest B").
