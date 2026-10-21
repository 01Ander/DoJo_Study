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
| **`PY-014`** | `02-py-poo` | Extractor desacoplado CSV/JSON | [`quests/01-abstractions/data_extractors.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py) | `pytest quests/01-abstractions/test_data_extractors.py` | 🟢 **COMPLETADO** |
| **`PY-020`** | `02-py-poo` | Ciclo TDD Red-Green-Refactor | [`quests/05-testing/billing_service.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py) | `pytest quests/05-testing/test_billing_service.py` | 🟡 **ACTIVA (Tu turno - Cierre PY)** |

---

## 2. 🚀 MISIÓN ACTIVA: `PY-020` — Ciclo TDD Red-Green-Refactor (Cierre de PY-POO)

* **Materia:** `02-py-poo` (Última misión antes de pasar a `03-sql-basico`)  
* **Archivo a editar por el Operador:** [`content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py)  
* **Enunciado de la Quest:** [`content/subjects/python/chronicles/PY-POO/quests/05-testing/04-tdd-red-green-refactor.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/04-tdd-red-green-refactor.md)  
* **Teoría de Respaldo:** [`content/subjects/python/chronicles/PY-POO/lore/05-testing-with-pytest.md` (§6)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/05-testing-with-pytest.md)

### 📋 El Contrato que debes cumplir:

Implementa en [`billing_service.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py) el método:
```python
def calculate_invoice(self, gigabytes: float, is_enterprise: bool = False) -> float:
```

1. **Validación de Integridad:**
   * Si `gigabytes < 0`, lanzar `ValueError("Storage consumption cannot be negative")`.
2. **Consumo Cero:**
   * Si `gigabytes == 0.0`, retorna `0.0`.
3. **Nivel 1 (Estándar):**
   * Si `gigabytes <= self.TIER_1_LIMIT` (100.0), el subtotal es `gigabytes * self.TIER_1_RATE` (0.02).
4. **Nivel 2 (Excedente escalonado):**
   * Si `gigabytes > self.TIER_1_LIMIT`:
     * Los primeros 100 GB se cobran a `self.TIER_1_RATE` (`100.0 * 0.02 = 2.00`).
     * Los GB excedentes (`gigabytes - 100.0`) se cobran a `self.TIER_2_RATE` (0.015).
5. **Descuento Enterprise:**
   * Si `is_enterprise is True`, aplica un 10% de descuento sobre el subtotal (`subtotal * (1.0 - self.ENTERPRISE_DISCOUNT)`).
6. **Retorno:**
   * Retorna el monto final como `float`.

---

### 🔄 Fases TDD:

1. **🔴 RED:** Ejecuta el comando de test y confirma que los 5 tests fallan.
2. **🟢 GREEN:** Escribe la lógica en `billing_service.py` hasta que los 5 tests pasen.
3. **🔵 REFACTOR:** Limpia el código usando las constantes de clase y manteniendo los tests verdes.

---

### 💡 Ejemplo con Domain Shifting (Monitor de Calidad del Aire):

```python
# 🎯 Objetivo de Negocio: Clasificar índice de partículas y validar rangos físicos en TDD.

class AirQualityMonitor:
    HEALTHY_THRESHOLD: float = 50.0
    MODERATE_THRESHOLD: float = 150.0

    def classify_pm25(self, concentration: float) -> str:
        if concentration < 0:
            raise ValueError("Particulate concentration cannot be negative")
        if concentration <= self.HEALTHY_THRESHOLD:
            return "HEALTHY"
        elif concentration <= self.MODERATE_THRESHOLD:
            return "MODERATE"
        return "HAZARDOUS"
```

---

### 🧪 Comando de Verificación Binaria (Sonda Final):
Ejecuta en tu terminal desde la raíz del repositorio:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/python/chronicles/PY-POO/quests/05-testing/test_billing_service.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/python/chronicles/PY-POO/quests/01-abstractions/data_extractors.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`4/4 passed`, exit code 0). Cierre formal de la brecha `PY-014`.**
* `content/subjects/python/chronicles/PY-POO/lore/05-testing-with-pytest.md`:
  * *Cambio:* Añadida Sección 6 sobre el Ciclo Virtuoso TDD (Red-Green-Refactor) con dos analogías, ciclo paso a paso, Domain Shifting y ciclo AAA.
* `content/subjects/python/chronicles/PY-POO/quests/05-testing/04-tdd-red-green-refactor.md`:
  * *Cambio:* Enunciado didáctico de la Quest 05-04 (`PY-020`).
* `content/subjects/python/chronicles/PY-POO/quests/05-testing/billing_service.py`:
  * *Cambio:* Plantilla inicial para el Operador con `pass` y firmas de método.
* `content/subjects/python/chronicles/PY-POO/quests/05-testing/test_billing_service.py`:
  * *Cambio:* Suite evaluadora automatizada con 5 tests unitarios cubriendo casos límite y escalonados.






