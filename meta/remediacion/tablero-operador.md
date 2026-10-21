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
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | [`quests/04-orchestration/output_loaders.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py) | `pytest quests/04-orchestration/test_output_loaders.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado | *Próximamente en quests/01-abstractions/* | — | ⏳ En espera |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-013` — Patrón Output Loaders y Orquestación ETL

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/04-orchestration/03-output-loaders.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/04-orchestration/03-output-loaders.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/04-orchestration-and-io.md` (§3, §4, §5 y §6)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/04-orchestration-and-io.md)

### 📋 El Contrato que debes cumplir:

1. **`BaseOutputLoader` (Clase Base Abstracta):**
   * Hereda de `abc.ABC`.
   * Define el método `@abstractmethod def load(self, records: List[Dict[str, Any]], destination: str) -> int`.
   * No debe poder instanciarse directamente.

2. **`ConsoleOutputLoader` (Subclase de `BaseOutputLoader`):**
   * Implementa `load(self, records: List[Dict[str, Any]], destination: str = "console") -> int`:
     * Itera sobre cada registro en `records` e imprime: `f"[CONSOLE:{destination}] {record}"`.
     * Retorna `len(records)`.

3. **`JsonFileOutputLoader` (Subclase de `BaseOutputLoader`):**
   * Implementa `load(self, records: List[Dict[str, Any]], destination: str) -> int`:
     * Abre el archivo en `destination` en modo escritura con UTF-8 (`with open(...)`).
     * Serializa los registros con `json.dump(records, file_handle, indent=2)`.
     * Retorna `len(records)`.

4. **`ManagedDataPipeline` (Orquestador ETL):**
   * Constructor `__init__(self, extractor: Any, engine: Any, loader: BaseOutputLoader)`:
     * Almacena las dependencias inyectadas: `self.extractor`, `self.engine`, `self.loader`.
   * Método `run(self, source_path: str, destination_path: str) -> int`:
     * Extrae: `raw_records = self.extractor.extract(source_path)`
     * Transforma: `processed_records = self.engine.process(raw_records)`
     * Carga: `count = self.loader.load(processed_records, destination_path)`
     * Retorna `count`.

---

### 💡 Ejemplo con Domain Shifting (Observatorio Astrofísico):
*Observa cómo la interfaz abstracta desacopla la salida del motor y del orquestador:*

```python
# 🎯 Objetivo de Negocio: Desacoplar la persistencia de espectros astronómicos procesados mediante el patrón polimórfico Output Loader.

from abc import ABC, abstractmethod
import json

class BaseSpectralLoader(ABC):
    @abstractmethod
    def load(self, records: list, destination: str) -> int:
        pass

class ConsoleSpectralLoader(BaseSpectralLoader):
    def load(self, records: list, destination: str = "stdout") -> int:
        for r in records:
            print(f"[SPECTRAL:{destination}] {r}")
        return len(records)

class StellarPipeline:
    def __init__(self, extractor, engine, loader: BaseSpectralLoader):
        self.extractor = extractor
        self.engine = engine
        self.loader = loader

    def run(self, src: str, dest: str) -> int:
        data = self.extractor.extract(src)
        processed = self.engine.process(data)
        return self.loader.load(processed, dest)
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/04-orchestration/test_output_loaders.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`6/6 passed`, exit code 0). Cierre formal de la brecha `PY-011`.**
* `content/subjects/python/chronicles/PY-POO/lore/04-orchestration-and-io.md`:
  * *Cambio:* Añadida Sección 4 (Patrón Output Loader), Sección 5 (Ciclo ETL en el Orquestador) y Sección 6 (Testing AAA con Mocks).
* `content/subjects/python/chronicles/PY-POO/quests/04-orchestration/03-output-loaders.md`:
  * *Cambio:* Enunciado didáctico de la Quest 04-03 (`PY-013`).
* `content/subjects/python/chronicles/PY-POO/quests/04-orchestration/output_loaders.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de método.
* `content/subjects/python/chronicles/PY-POO/quests/04-orchestration/test_output_loaders.py`:
  * *Cambio:* Suite evaluadora automatizada con 5 tests unitarios.




