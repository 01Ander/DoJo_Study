# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-19  
> **Materia Activa:** `02-py-poo` (Python Orientado a Objetos & TDD)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

| Tarea ID | Materia | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|
| **`PY-010`** | `02-py-poo` | Constructores con `super()` | [`quests/02-entities/rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py) | `pytest quests/02-entities/test_rpg_character.py` | 🟢 **COMPLETADO** |
| **`PY-011.1`** | `02-py-poo` | De Dataclass a Pydantic con `Field` | [`quests/06-logging/user_account_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py) | `pytest quests/06-logging/test_user_account_schema.py` | 🟢 **COMPLETADO** |
| **`PY-011.2`** | `02-py-poo` | Validadores de Negocio y Excepciones | [`quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) | `pytest quests/06-logging/test_transaction_schema.py` | 🟢 **COMPLETADO** |
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | [`quests/04-orchestration/output_loaders.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py) | `pytest quests/04-orchestration/test_output_loaders.py` | 🟢 **COMPLETADO** |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado CSV/JSON | [`quests/01-abstractions/data_extractors.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py) | `pytest quests/01-abstractions/test_data_extractors.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-014` — Extractor Desacoplado CSV y JSON

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/01-abstractions/03-decoupled-json-extractor.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/01-abstractions/03-decoupled-json-extractor.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/01-abstract-classes-and-interfaces.md` (§5)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/01-abstract-classes-and-interfaces.md)

### 📋 El Contrato que debes cumplir:

1. **`AbstractDataExtractor` (Clase Base Abstracta):**
   * Hereda de `abc.ABC`.
   * Define el método `@abstractmethod def extract(self, file_path: str) -> List[Dict[str, Any]]`.
   * Debe impedir instanciación directa.

2. **`CSVDataExtractor` (Subclase de `AbstractDataExtractor`):**
   * Implementa `extract(self, file_path: str) -> List[Dict[str, Any]]`:
     * Abre `file_path` con UTF-8 (`with open(file_path, "r", encoding="utf-8") as f:`).
     * Lee con `csv.DictReader(f)` y retorna `[dict(row) for row in reader]`.

3. **`JSONDataExtractor` (Subclase de `AbstractDataExtractor`):**
   * Implementa `extract(self, file_path: str) -> List[Dict[str, Any]]`:
     * Abre `file_path` con UTF-8 (`with open(file_path, "r", encoding="utf-8") as f:`).
     * Parsea el contenido con `json.load(f)`.
     * Si el contenido es una lista (`isinstance(data, list)`), la retorna directamente.
     * Si es un diccionario único, lo retorna envuelto en una lista `[data]`.

---

### 💡 Ejemplo con Domain Shifting (Observatorio Meteorológico):
*Observa cómo la interfaz abstracta homogeniza la lectura de distintos formatos:*

```python
# 🎯 Objetivo de Negocio: Extraer observaciones meteorológicas multiformato de forma intercambiable.

from abc import ABC, abstractmethod
import csv
import json

class AbstractClimateExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> list[dict]:
        pass

class CSVClimateExtractor(AbstractClimateExtractor):
    def extract(self, file_path: str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            return [dict(row) for row in csv.DictReader(f)]

class JSONClimateExtractor(AbstractClimateExtractor):
    def extract(self, file_path: str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/01-abstractions/test_data_extractors.py -v
```
*(Criterio de éxito: 4 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`5/5 passed`, exit code 0). Cierre formal de la brecha `PY-013`.**
* `content/subjects/python/chronicles/PY-POO/lore/01-abstract-classes-and-interfaces.md`:
  * *Cambio:* Añadida Sección 5 sobre Extracción Polimórfica Desacoplada (AbstractExtractor, CSV y JSON) con Domain Shifting y ciclo AAA.
* `content/subjects/python/chronicles/PY-POO/quests/01-abstractions/03-decoupled-json-extractor.md`:
  * *Cambio:* Enunciado didáctico de la Quest 01-03 (`PY-014`).
* `content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de método.
* `content/subjects/python/chronicles/PY-POO/quests/01-abstractions/test_data_extractors.py`:
  * *Cambio:* Suite evaluadora automatizada con 4 tests unitarios.





