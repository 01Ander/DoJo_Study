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
| **`PY-011.2`** | `02-py-poo` | Validadores de Negocio y Excepciones | [`quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py) | `pytest quests/06-logging/test_transaction_schema.py` | 🟡 **ACTIVA (Tu turno)** |
| **`PY-013`** | `02-py-poo` | Patrón Output Loaders | *Próximamente en quests/04-orchestration/* | — | ⏳ En espera |
| **`PY-014`** | `02-py-poo` | Extractor desacoplado | *Próximamente en quests/01-abstractions/* | — | ⏳ En espera |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green | *Próximamente en quests/05-testing/* | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-011.2` — Validadores de Negocio y Excepciones de Dominio

* **Materia:** `02-py-poo`  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/06-logging/04-pydantic-domain-exceptions.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/06-logging/04-pydantic-domain-exceptions.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md` (§4.3, §5, §6 y §7)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md)

### 📋 El Contrato que debes cumplir:

1. **`InvalidTransactionDataError(Exception)`:**
   * Excepción de dominio personalizada para errores de validación en transacciones (hereda de `Exception`).

2. **`TransactionPayload(BaseModel)`:**
   * Hereda de `BaseModel` de Pydantic.
   * Campos y restricciones requeridas:
     * `transaction_id: str`: Longitud mínima de 3 caracteres (`Field(min_length=3)`).
     * `account_id: int`: Estrictamente positivo (`Field(gt=0)`).
     * `amount: float`: Estrictamente positivo (`Field(gt=0.0)`).
     * `currency: str`: Por defecto `"USD"`.
   * Validador personalizado (`@field_validator("currency")` como `@classmethod`):
     * Convierte el valor recibido a mayúsculas (`v.upper()`).
     * Verifica que esté en el conjunto permitido: `{"USD", "EUR", "GBP", "COP"}`.
     * Si no pertenece, lanza un `ValueError(f"Moneda '{v}' no soportada")`.

3. **Función `validate_and_create_transaction(data: dict) -> TransactionPayload`:**
   * Recibe un diccionario crudo no tipado.
   * Intenta instanciar `TransactionPayload(**data)`.
   * Si Pydantic arroja `pydantic.ValidationError`, **captura la excepción** y levanta un `InvalidTransactionDataError(str(e))`.
   * Si es válido, retorna la instancia construida de `TransactionPayload`.

---

### 💡 Ejemplo con Domain Shifting (Telemetría Satelital):
*Observa cómo la frontera captura el error técnico de Pydantic y lo transforma en una excepción de dominio con logging (ver ejemplo completo en Lore 06B §6):*

```python
# 🎯 Objetivo de Negocio: Validar un payload de telemetría y atrapar errores de esquema en la frontera perimetral.

from pydantic import BaseModel, Field, field_validator, ValidationError

class CorruptedTelemetryPacketError(Exception):
    pass

class SatelliteTelemetry(BaseModel):
    sensor_id: str = Field(min_length=3)
    battery_pct: float = Field(ge=0.0, le=100.0)
    band: str = "UHF"

    @field_validator("band")
    @classmethod
    def check_band(cls, v: str) -> str:
        clean_band = v.strip().upper()
        if clean_band not in {"UHF", "VHF", "S-BAND"}:
            raise ValueError(f"Banda '{v}' no autorizada")
        return clean_band

def ingest_packet(raw_data: dict) -> SatelliteTelemetry:
    try:
        return SatelliteTelemetry(**raw_data)
    except ValidationError as err:
        raise CorruptedTelemetryPacketError(f"Rechazo en frontera: {err}")
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

Registro de archivos nuevos o actualizados en el sistema según las reglas de `09-generation-protocol.md`:

* `content/subjects/python/chronicles/PY-POO/lore/06b-pydantic-and-data-contracts.md`:
  * *Cambio:* Reescritura exhaustiva bajo el protocolo de generación (Zero Assumption con setup pip, Zero Surprise Syntax, 2 analogías del mundo real, `🎯 Objetivo de Negocio:`, English First en código, Ejemplo End-to-End completo en §6 y suite de testing bajo ciclo AAA en §7).
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/user_account_schema.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`5/5 passed`, exit code 0).**
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/transaction_schema.py`:
  * *Cambio:* Plantilla para el Operador con `pass` para la misión activa `PY-011.2`.
* `content/subjects/python/chronicles/PY-POO/quests/06-logging/test_transaction_schema.py`:
  * *Cambio:* Suite evaluadora automatizada con 6 tests unitarios.



