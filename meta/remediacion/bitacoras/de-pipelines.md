# Bitácora Táctica de Remediación — `04-de-pipelines`

> **Documento Rector:** [README.md](../README.md) — índice de la remediación (Ola 1)  
> **Directorio Canónico:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/)  
> **Python / Venv:** `content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/python3`  
> **Estado:** En Preparación (Ola 1)

---

## 0. Veredicto Histórico sobre las Quests de DE-PIPELINES

> [!NOTE]
> **Resolución Epistémica Definitiva:**  
> La auditoría inicial reportó erróneamente que el generador entregó las quests pre-resueltas (`PROTO-OBS-03`). Tras auditar el historial de commits de Git (`af2c0b4` vs `3e87956` y `084aa63`), se demostró que el generador entregó **plantillas vacías con directivas `# 🎯 YOUR TURN:`**, y que el Operador programó, resolvió y commiteó personalmente cada archivo `test_NN_*.py` en septiembre de 2026. En la auditoría técnica consolidada, los 13 tests pasaron limpios sin fallas.  
> **Decisión:** El Operador **NO tiene que rehacer ninguna de las 6 quests**. Su labor de estudio queda enfocada exclusivamente en los claims reales del Rite y Lore (`DE-001`, `DE-002`, `DE-003`).

---

## 1. Carril B: Higiene del Material (Ejecución de Arquitecto / Asistente)

### DE-008: Reconciliación Inversa en `chronicle.md`
- **Diagnóstico:** El temario no declaraba la biblioteca de mocking HTTP `responses`, a pesar de ser la herramienta fundamental explicada y evaluada en el Capítulo 01.
- **Sonda Inicial:**
  ```bash
  grep -c "responses" content/subjects/data_engineering/chronicles/DE-PIPELINES/chronicle.md
  ```
  *Resultado:* `0` (exit 1).
- **Acción:** Declarar formalmente `responses` en el Capítulo 01 del syllabus.
- **Sonda Final:**
  ```bash
  grep "responses" content/subjects/data_engineering/chronicles/DE-PIPELINES/chronicle.md
  ```
  *Resultado:* `- **Capítulo 01:** Extracción Automatizada (APIs REST, Auth tokens, Paginación, librería requests, mocking de APIs con responses).` (exit 0).

### DE-003: Mito 3 — Efecto del Flag `-O` sobre `assert` en Python (Lore 03)
- **Archivo:** [`lore/03-data-quality.md:L49-L55`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/03-data-quality.md#L49-L55)
- **Concepto:** Cuando Python se ejecuta con el flag de optimización `-O` (o `-OO`), el compilador de bytecode **elimina por completo todas las sentencias `assert`** (NOP). Un pipeline de datos productivo que confíe en `assert` para validar esquemas o nulidad dejará pasar datos corruptos sin alertar a nadie.
- **Acción (Antigravity):** Inclusión de advertencia arquitectónica formal en la prosa de Lore 03 explicando el riesgo y documentando que en pipelines de producción se deben emitir excepciones de dominio explícitas.
- **Sonda de Comprobación:**
  ```bash
  python3 -O -c "assert False, 'falla'"
  ```
  *Resultado:* Termina silenciosamente con `exit code 0` sin detonar el `AssertionError`, demostrando la nulidad de `assert` bajo optimización.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

### DE-001: Resiliencia de Ingesta y Endpoints de Desarrollo
- **Archivo a modificar:** [`rite/src/pipeline.py:L20`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/pipeline.py#L20) o [`rite/src/config.py:L1`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/config.py#L1) / [`rite/src/extract.py:L15-L25`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/extract.py#L15-L25)
- **Concepto:** En entornos locales de desarrollo y pipelines batch, una URL ficticia no enrutable (`api.dark_market.fake`) provoca un fallo inmediato por `ConnectionError`. Un pipeline profesional debe contar con un mecanismo de fallback a fixture local (e.g. `tests/fixtures/market_catalog.json`) cuando la red no está disponible, para que el punto de entrada principal (`pipeline.py`) pueda completar una ejecución autónoma de principio a fin (`exit code 0`).
- **Domain Shifting (Recepción de Cargas del Gremio de Comerciantes):**
  ```python
  # Si el puerto marítimo está cerrado por niebla, el sistema debe usar el almacén local:
  def get_market_data(url: str, fallback_path: str = "data/fixtures/market.json"):
      try:
          response = requests.get(url, timeout=2)
          response.raise_for_status()
          return response.json()
      except requests.RequestException:
          logger.warning("Fallo al conectar con %s. Usando fixture local.", url)
          with open(fallback_path, "r", encoding="utf-8") as f:
              return json.load(f)
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  cd content/subjects/data_engineering/chronicles/DE-PIPELINES/rite && ../.venv/bin/python3 -m src.pipeline
  ```
  *Resultado:* `ConnectionError: Failed to resolve 'api.dark_market.fake'` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  cd content/subjects/data_engineering/chronicles/DE-PIPELINES/rite && ../.venv/bin/python3 -m src.pipeline
  ```
  *Criterio:* Ejecución autónoma completa con `exit code 0`.

---

### DE-002: Data Quality Defensivo con Excepciones de Dominio vs `assert`
- **Archivo a modificar:** [`rite/src/quality.py:L26, L31`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/quality.py#L26-L33) y [`rite/tests/test_pipeline.py:L130, L138`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/tests/test_pipeline.py#L128-L141)
- **Concepto:** La palabra clave `assert` está reservada para suites de testing (`pytest`). En código de producción (Quality Gates, pipelines ETL), las validaciones de negocio **deben lanzar excepciones estructuradas** (`DataQualityError` o subclases de `Exception`). Si se utiliza `assert`, cualquier optimización del intérprete (`-O`) anula la validación.
- **Domain Shifting (Control de Pureza de Elixires):**
  ```python
  class PurezaError(Exception):
      """Excepción de dominio cuando un lote no cumple los estándares."""
      pass

  def validar_lote(datos: list):
      if len(datos) < 10:
          raise PurezaError("Lote incompleto: menos de 10 viales.")
  ```
- **Sonda Inicial:**
  ```bash
  grep -n "assert " content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/quality.py
  ```
  *Resultado:* Muestra sentencias `assert` en código productivo (L26 y L31).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  cd content/subjects/data_engineering/chronicles/DE-PIPELINES/rite && ../.venv/bin/pytest tests/test_pipeline.py
  ```
  *Criterio:* Toda la suite de 20 tests pasa validando el lanzamiento de `DataQualityError` con `exit code 0`.

---

## 3. Log de Mutaciones y Verificación

| ID | Fecha | Carril | Responsable | Sonda Inicial (Salida) | Sonda Final (Salida) | Estado |
|---|---|---|---|---|---|---|
| DE-008 | 2026-10-13 | B | Antigravity | `responses` no declarado (exit 1) | Declarado formalmente en Cap 01 (exit 0) | ✅ Completado |
| DE-003 | 2026-10-13 | B | Antigravity | Mito en Lore 03 (afirma detención con assert) | Advertencia arquitectónica de flag `-O` (exit 0) | ✅ Completado |
| DE-001 | 2026-10-13 | A | Operador | `ConnectionError` en pipeline (exit 1) | Flujo autónomo completo exitoso (exit 0) | ✅ Completado |
| DE-002 | 2026-10-13 | A | Operador | `assert` en código productivo L26, L31 | 0 asserts, RateError activo, 20/20 tests OK (exit 0) | ✅ Completado |
