# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-19  
> **Materia Activa:** `02-py-poo` (Python Orientado a Objetos & TDD)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

| Tarea ID | Materia | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|
| **`PY-010`** | `02-py-poo` | Constructores con `super()` | [`quests/02-entities/rpg_character.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py) | `pytest quests/02-entities/test_rpg_character.py` | 🟢 **COMPLETADO** |
| **`PY-011`** | `02-py-poo` | Validación con Pydantic | [`quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) | `pytest quests/06-logging/test_transaction_schema.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | *Próximamente en quests/04-orchestration/* | — | ⏳ En espera |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado | *Próximamente en quests/01-abstractions/* | — | ⏳ En espera |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-011` — Validación con Pydantic V2

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/03-pydantic-validation.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/03-pydantic-validation.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/06-logging-and-error-handling.md` (Sección 5)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/06-logging-and-error-handling.md)

### 📋 El Contrato que debes cumplir:

1. **`InvalidTransactionDataError(Exception)`:**
   * Excepción de dominio para errores de validación de transacciones (hereda de `Exception`).

2. **`TransactionPayload(BaseModel)`:**
   * Hereda de `BaseModel` de Pydantic.
   * Campos y restricciones requeridas:
     * `transaction_id: str`: Con longitud mínima de 3 caracteres (`Field(min_length=3)`).
     * `account_id: int`: Estrictamente positivo (`Field(gt=0)`).
     * `amount: float`: Estrictamente positivo (`Field(gt=0.0)`).
     * `currency: str`: Por defecto `"USD"`.
   * Validador personalizado (`@field_validator("currency")` como `@classmethod`):
     * Convierte el valor a mayúsculas (`value.upper()`).
     * Verifica que esté en el conjunto permitido: `{"USD", "EUR", "GBP", "COP"}`.
     * Si no pertenece, lanza un `ValueError(f"Moneda '{value}' no soportada")`.

3. **Función `validate_and_create_transaction(data: dict) -> TransactionPayload`:**
   * Recibe un diccionario crudo no tipado.
   * Intenta instanciar `TransactionPayload(**data)`.
   * Si Pydantic arroja `pydantic.ValidationError`, **captura la excepción** y levanta un `InvalidTransactionDataError(str(e))`.
   * Si es válido, retorna la instancia construida de `TransactionPayload`.

---

### 💡 Ejemplo con Domain Shifting (Telemetría Satelital):
*Observa cómo Pydantic valida tipos y restricciones, y cómo un helper envuelve el error técnico en una excepción del negocio:*

```python
from pydantic import BaseModel, Field, field_validator, ValidationError

class TelemetryError(Exception):
    """Excepción de dominio de telemetría."""
    pass

class SatelliteReading(BaseModel):
    satellite_code: str = Field(min_length=2)
    battery_level: float = Field(gt=0.0, le=100.0)
    transmission_band: str = "UHF"

    @field_validator("transmission_band")
    @classmethod
    def check_band(cls, v: str) -> str:
        valid_bands = {"UHF", "VHF", "S-BAND", "X-BAND"}
        if v.upper() not in valid_bands:
            raise ValueError(f"Banda '{v}' fuera del espectro asignado.")
        return v.upper()

def parse_telemetry_packet(raw_dict: dict) -> SatelliteReading:
    try:
        return SatelliteReading(**raw_dict)
    except ValidationError as err:
        raise TelemetryError(f"Paquete satelital corrupto: {err}")
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/06-logging/test_transaction_schema.py -v
```
*(Criterio de éxito: 6 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema para que sepas exactamente qué ha cambiado:

* `content/subjects/python/chronicles/PY-POO/lore/02-domain-entities-and-dataclasses.md`:
  * *Cambio:* Añadida la Sección 4 sobre Herencia Compuesta y uso correcto de `super().__init__()`.
* `content/subjects/python/chronicles/PY-POO/quests/02-entities/03-inheritance-super.md`:
  * *Cambio:* Enunciado didáctico de la Quest 02-03.
* `content/subjects/python/chronicles/PY-POO/quests/02-entities/rpg_character.py`:
  * *Cambio:* Implementado exitosamente por el Operador (`3/3 passed`).
* `content/subjects/python/chronicles/PY-POO/lore/06-logging-and-error-handling.md`:
  * *Cambio:* Añadida Sección 5 sobre Validación de Contratos Fuertes con Pydantic V2 y actualización del mapa de ejercicios.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/03-pydantic-validation.md`:
  * *Cambio:* Enunciado didáctico de la Quest 06-03 (`PY-011`).
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de método.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/test_transaction_schema.py`:
  * *Cambio:* Suite evaluadora automatizada con 6 tests unitarios.

