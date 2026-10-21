# Ejercicio 01-03: Extractor Desacoplado CSV y JSON (Tipo A)

**Objetivo:** Implementar la interfaz abstracta `AbstractDataExtractor` y sus dos implementaciones concretas `CSVDataExtractor` y `JSONDataExtractor`, asegurando que cualquier consumidor pueda leer datos multiformato bajo un mismo contrato (Lore 01 §5).

---

## Contexto: Ingesta Multiformato Desacoplada

En pipelines de datos, las fuentes externas envían información en múltiples formatos físicos: archivos CSV delimitados por comas o archivos JSON con estructuras de objetos. El consumidor (o motor de cálculo) no debe preocuparse por cómo abrir o parsear cada formato; solo debe llamar a `.extract(file_path)` y recibir una lista uniforme de diccionarios (`list[dict]`).

Para lograrlo, construirás:

1. **`AbstractDataExtractor` (Clase Base Abstracta):**
   * Debe heredar de `abc.ABC`.
   * Método abstracto `@abstractmethod def extract(self, file_path: str) -> list[dict]`:
     * Define el contrato de extracción obligatorio.
     * No debe permitir instanciación directa.

2. **`CSVDataExtractor` (Subclase Concreta de `AbstractDataExtractor`):**
   * Implementa `extract(self, file_path: str) -> list[dict]`:
     * Abre el archivo en modo lectura con codificación UTF-8.
     * Parsea las filas utilizando `csv.DictReader`.
     * Retorna una lista de diccionarios `[dict(row) for row in reader]`.

3. **`JSONDataExtractor` (Subclase Concreta de `AbstractDataExtractor`):**
   * Implementa `extract(self, file_path: str) -> list[dict]`:
     * Abre el archivo en modo lectura con codificación UTF-8.
     * Parsea el contenido utilizando `json.load`.
     * Si la raíz del JSON es una lista, la retorna directamente. Si es un único diccionario, lo retorna envuelto en una lista de un elemento `[data]`.

---

## Tu Tarea (Carril A - Operador)

Edita el archivo [`data_extractors.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py) completando las tres clases según las especificaciones.

---

## Verificación

Ejecuta el evaluador automatizado en tu terminal:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/01-abstractions/test_data_extractors.py -v
```
El ejercicio se considera superado cuando los 4 tests pasen con **`exit code 0`**.
