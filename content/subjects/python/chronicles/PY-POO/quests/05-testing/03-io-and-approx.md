# Ejercicio 05-03: Testing I/O con `tmp_path` y Tolerancia con `pytest.approx` (Nivel 4)

**Objetivo:** Aplicar el fixture nativo `tmp_path` para pruebas de archivos aislados y `pytest.approx` para aserciones de punto flotante sin fragilidad aritmética (Lore 05 §4 y §5).

---

## Contexto (Domain Shifting: Tesorería del Gremio de Alquimistas)

El Gremio de Alquimistas maneja transacciones fraccionarias de oro y necesita leer registros desde archivos de texto temporales sin dejar residuos en disco.

Dispones del módulo `treasury.py` con dos componentes:
1. `TreasuryReportReader`: Lee un archivo delimitado por comas (`gold,silver`) y devuelve la suma total de oro como `float`.
2. `GoldLedger`: Suma una lista de micro-transacciones fraccionarias en oro.

```python
# treasury.py
from pathlib import Path

class TreasuryReportReader:
    def parse_total_gold(self, filepath: str) -> float:
        total = 0.0
        with open(filepath, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("gold"):
                    parts = line.split(",")
                    total += float(parts[0])
        return total

class GoldLedger:
    def sum_micro_transactions(self, amounts: list[float]) -> float:
        return sum(amounts)
```

---

## Tu Tarea

Crea el archivo `test_treasury.py` en esta carpeta e implementa dos pruebas unitarias:

1. **`test_reader_parses_gold_file_with_tmp_path(tmp_path)`**:
   - Inyecta el fixture nativo `tmp_path`.
   - Crea un archivo temporal llamado `records.csv` dentro de `tmp_path` con el contenido:
     ```csv
     gold,silver
     100.25,50.00
     200.50,10.00
     ```
   - Instancia `TreasuryReportReader` y pásale `str(archivo_temporal)`.
   - Afirma con `assert` que el total devuelto es exactamente `pytest.approx(300.75)`.

2. **`test_ledger_avoids_floating_point_imprecision()`**:
   - Pasa la lista `[0.1, 0.2, 0.3]` al método `sum_micro_transactions`.
   - Afirma que el resultado es igual a `0.6` usando `pytest.approx(0.6)`.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```python
from pathlib import Path
import pytest
from treasury import TreasuryReportReader, GoldLedger

def test_reader_parses_gold_file_with_tmp_path(tmp_path: Path):
    # 1. Arrange: crear archivo en directorio temporal aislado
    csv_file = tmp_path / "records.csv"
    csv_file.write_text("gold,silver\n100.25,50.00\n200.50,10.00\n", encoding="utf-8")

    # 2. Act
    reader = TreasuryReportReader()
    total = reader.parse_total_gold(str(csv_file))

    # 3. Assert con approx
    assert total == pytest.approx(300.75)

def test_ledger_avoids_floating_point_imprecision():
    # Arrange & Act
    ledger = GoldLedger()
    result = ledger.sum_micro_transactions([0.1, 0.2, 0.3])

    # Assert
    assert result == pytest.approx(0.6)
```
</details>
