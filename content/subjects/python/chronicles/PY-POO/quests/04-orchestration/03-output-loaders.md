# Ejercicio 04-03: Patrón Output Loaders y Orquestación ETL (Tipo A)

**Objetivo:** Implementar una jerarquía polimórfica de cargadores de salida (`BaseOutputLoader`, `ConsoleOutputLoader`, `JsonFileOutputLoader`) e integrarla en un orquestador mediante Inyección de Dependencias (Lore 04 §4 y §5).

---

## Contexto: Emisión Multicanal en Pipelines de Datos

En un pipeline de datos profesional, el resultado procesado por un motor de cálculo debe poder emitirse a múltiples destinos (la consola para monitoreo local, o un archivo persistente en disco para auditoría) sin alterar el código del orquestador.

Para lograr este desacoplamiento construirás:

1. **`BaseOutputLoader` (Clase Base Abstracta):**
   * Debe heredar de `abc.ABC`.
   * Método abstracto `@abstractmethod def load(self, records: list[dict], destination: str) -> int`:
     * Define el contrato que toda clase cargadora debe implementar.
     * Recibe la lista de diccionarios `records` y el destino `destination`.
     * Retorna el número entero de registros procesados/cargados.

2. **`ConsoleOutputLoader` (Subclase Concreta de `BaseOutputLoader`):**
   * Implementa `load(self, records: list[dict], destination: str = "console") -> int`:
     * Itera sobre `records` e imprime cada registro precedido por `f"[CONSOLE:{destination}] {record}"`.
     * Retorna `len(records)`.

3. **`JsonFileOutputLoader` (Subclase Concreta de `BaseOutputLoader`):**
   * Implementa `load(self, records: list[dict], destination: str) -> int`:
     * Abre el archivo en la ruta `destination` en modo escritura con codificación UTF-8.
     * Serializa `records` en formato JSON con indentación de 2 espacios (`json.dump(records, file, indent=2)`).
     * Retorna `len(records)`.

4. **`ManagedDataPipeline` (Orquestador ETL):**
   * Constructor `__init__(self, extractor, engine, loader: BaseOutputLoader)`:
     * Inyecta y almacena `self.extractor`, `self.engine` y `self.loader`.
   * Método `run(self, source_path: str, destination_path: str) -> int`:
     * Ejecuta el ciclo ETL coordinado:
       1. Extrae: `raw_records = self.extractor.extract(source_path)`
       2. Transforma: `processed_records = self.engine.process(raw_records)`
       3. Carga: `count = self.loader.load(processed_records, destination_path)`
       4. Retorna el conteo `count`.

---

## Tu Tarea (Carril A - Operador)

Edita el archivo [`output_loaders.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py) completando la clase abstracta `BaseOutputLoader`, las implementaciones `ConsoleOutputLoader` y `JsonFileOutputLoader`, y el orquestador `ManagedDataPipeline`.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/04-orchestration/test_output_loaders.py -v
```
El ejercicio se considera superado cuando los 5 tests pasen con **`exit code 0`**.
