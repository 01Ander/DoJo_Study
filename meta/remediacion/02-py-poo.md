# Bitácora Táctica de Remediación — `02-py-poo`

> **Documento Rector:** [roadmap.md](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/remediacion/roadmap.md)  
> **Directorio Canónico:** [`content/subjects/python/chronicles/PY-POO/`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/)  
> **Python / Venv:** `content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3`  
> **Estado:** ✅ Completado (10/10 Claims en Verde)

---

## 1. Carril B: Higiene del Material (Ejecución de Arquitecto / Asistente)

Tareas mecánicas de reparación sintáctica y reconciliación curricular.

### PY-001: Imports Faltantes en `quests/04-orchestration/pipeline.py`
- **Diagnóstico:** `RecipePipeline` utilizaba las anotaciones de tipo `Reader` y `Calculator` sin importarlas ni definirlas, provocando `NameError` al importar la clase en los tests. Además, el test invocaba `run()` mientras la clase definía `execute()`.
- **Sonda Inicial:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/quests/04-orchestration && ../../rite/.venv/bin/python3 -m pytest -q
  ```
  *Resultado inicial:* `NameError: name 'Reader' is not defined` (exit 2).
- **Acción:** Corregir import/definición de interfaces y sincronizar nombre del método orquestador.
- **Sonda Final:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/quests/04-orchestration && ../../rite/.venv/bin/python3 -m pytest -q
  ```
  *Criterio:* `1 passed` con `exit code 0`.

### PY-002: Variable de Comprensión en `quests/03-engines/weather_engine.py`
- **Diagnóstico:** En la comprensión generadora `sum(days.celsius for day in days)`, se accedía a `.celsius` sobre la lista `days` en lugar del elemento iterado `day`.
- **Sonda Inicial:**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -c "from types import SimpleNamespace; import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/03-engines'); from weather_engine import WeatherAnalyticsEngine; w = WeatherAnalyticsEngine(); d = [SimpleNamespace(celsius=20.0), SimpleNamespace(celsius=30.0)]; print(w.get_average_temp(d))"
  ```
  *Resultado inicial:* `AttributeError: 'list' object has no attribute 'celsius'` (exit 1).
- **Acción:** Corregir la variable dentro de la comprensión generadora a `day.celsius`.
- **Sonda Final:**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -c "from types import SimpleNamespace; import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/03-engines'); from weather_engine import WeatherAnalyticsEngine; w = WeatherAnalyticsEngine(); d = [SimpleNamespace(celsius=20.0), SimpleNamespace(celsius=30.0)]; assert w.get_average_temp(d) == 25.0; print('PASS: Average calculation OK')"
  ```
  *Criterio:* `exit code 0`.

### PY-003: Clases No Importadas en `quests/07-cli/cli2.py`
- **Diagnóstico:** `cli2.py` instanciaba `GameLoader`, `PhysicsEngine` y `GameOrchestrator` sin definirlas ni importarlas.
- **Sonda Inicial:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/quests/07-cli && python3 cli2.py --level 1
  ```
  *Resultado inicial:* `NameError: name 'GameLoader' is not defined` (exit 1).
- **Acción:** Proveer definiciones desacopladas / stubs funcionales en `quests/07-cli/game.py` para satisfacer el ejercicio CLI.
- **Sonda Final:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/quests/07-cli && python3 cli2.py --level 1
  ```
  *Criterio:* Ejecución exitosa con `exit code 0`.

### PY-004: Invocación de `rite/src/cli.py`
- **Diagnóstico:** `from src.pipeline import PipelineOrchestrator` falla con `ModuleNotFoundError` al ejecutarse directamente como `python3 src/cli.py` si el directorio raíz no está en `sys.path`.
- **Sonda Inicial:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/rite && python3 src/cli.py --input data/data.csv
  ```
  *Resultado inicial:* `ModuleNotFoundError: No module named 'src'` (exit 1).
- **Acción:** Robustecer resolución de paths o estandarizar punto de entrada modular.
- **Sonda Final:**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/rite && python3 -m src.cli --input data/data.csv
  ```
  *Criterio:* `exit code 0`.

### PY-021/022: Reconciliación Inversa en `chronicle.md`
- **Diagnóstico:** El temario no declaraba formalmente `@dataclass` en el Capítulo 02 ni `argparse` en el Capítulo 07, a pesar de enseñarse en sus respectivas quests y ritos.
- **Sonda Inicial:**
  ```bash
  grep -cE "argparse" content/subjects/python/chronicles/PY-POO/chronicle.md
  ```
  *Resultado inicial:* `0` (en el texto formal del syllabus).
- **Acción:** Declarar formalmente `@dataclass` en Cap 02 y `argparse` en Cap 07.
- **Sonda Final:**
  ```bash
  grep -E "argparse|@dataclass" content/subjects/python/chronicles/PY-POO/chronicle.md
  ```
  *Criterio:* Ambas tecnologías explícitamente declaradas.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

> [!TIP]
> **Metodología de Domain Shifting:** Los siguientes conceptos se explican utilizando analogías de dominios externos (ej. El Servicio Postal de Ankh-Morpork). El Operador debe traducir el principio a su propio código sin soluciones pre-fabricadas.

### PY-005: Propagación de Excepciones en Pipelines de Ingesta
- **Archivo:** `rite/src/pipeline.py:L24-L27`
- **Concepto:** En pipelines batch de producción, capturar una excepción de ingesta solo para imprimir un log y terminar silenciosamente con `exit 0` es un antipatrón crítico. Si el archivo no existe o está corrupto, el proceso debe fallar con código de error no cero (`sys.exit(1)` o relanzando la excepción) para que el orquestador (Airflow, Prefect, Cron) detecte la falla y active alertas/reintentos.
- **Domain Shifting (Oficina Postal de Ankh-Morpork):**
  ```python
  # Si la valija postal de Lancre se pierde en el pantano:
  # Antipatrón: registrar "Valija perdida" y decir que el día terminó con éxito.
  # Canónico:
  try:
      mailbag = courier.fetch_bag("Lancre")
  except BagNotFoundError as err:
      logger.critical("No se pudo recuperar la valija de Lancre: %s", err)
      raise err  # O sys.exit(1): el Patricio debe enterarse de que el correo falló
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/rite'); from src.cli import main; import sys as s; s.argv=['cli.py', '--input', 'archivo_fantasma.csv']; main()"
  ```
  *Resultado:* Termina con `exit 0` silencioso.
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/rite && python3 -m src.cli --input archivo_fantasma.csv
  ```
  *Criterio:* Termina con código no cero (`exit code != 0`).

### PY-006: Mito Técnico en Lore 02 y Protección con `slots=True` en Dataclasses
- **Archivos:** `lore/02-domain-entities-and-dataclasses.md:L30` y `quests/02-entities/inventory.py:L4,L11,L20`
- **Concepto (Doble Dimensión):**
  1. *Dimensión Teórica (Lore 02):* En Lore 02 se afirma que `@dataclass` previene los errores de tipeo de diccionarios ("Muchos IDEs y mypy te avisarán del error aquí"). Sin embargo, en runtime una dataclass estándar sin `slots=True` utiliza `__dict__` y acepta tranquilamente la asignación de atributos inexistentes (`p1.healt = 90`). Se debe desmitificar esta afirmación en el texto.
  2. *Dimensión Práctica (inventory.py):* El ejercicio del Operador replica la falsa seguridad asignando `sword.nam = "Scalibur"`. Al incorporar `@dataclass(slots=True)` en `Weapon` y `Potion`, Python genera un descriptor rígido sin `__dict__`, bloqueando el typo en seco con `AttributeError`.
- **Domain Shifting (Inventario del Gremio de Alquimistas):**
  ```python
  from dataclasses import dataclass

  # Con slots=True, la estructura de la poción es rígida
  @dataclass(slots=True)
  class Potion:
      name: str
      potency: int

  p = Potion("Curación Mayor", 50)
  # p.potenci = 60  <-- Detona AttributeError inmediatamente, previniendo el bug silencioso
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/02-entities'); from inventory import Weapon; w = Weapon('Sting', 20, 25.5); w.nam = 'Scalibur'; print('Pasa silencioso:', w.nam)"
  ```
  *Resultado:* Pasa sin error (`Pasa silencioso: Scalibur`).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/02-entities'); from inventory import Weapon; w = Weapon('Sting', 20, 25.5);
  try:
      w.nam = 'Scalibur'
      exit(1)
  except AttributeError:
      print('PASS: Typo bloqueado por slots=True')
      exit(0)"
  ```
  *Criterio:* `exit code 0`.

### PY-007: Corrección de Mito en Prosa de `lore/01-abstract-classes-and-interfaces.md`
- **Archivo:** `lore/01-abstract-classes-and-interfaces.md:L30`
- **Diagnóstico:** El texto afirmaba que si una subclase olvida un método abstracto, *"Python lanzará un error antes de que el código corra"*. Esto era falso: el AST y la definición de clase ocurren sin error; la validación la ejecuta `ABCMeta` en runtime al instanciar (`TypeError`).
- **Acción:** Corregida la prosa técnica en el archivo de Lore.
- **Sonda Final:**
  ```bash
  python3 -c "from abc import ABC, abstractmethod
  class B(ABC):
      @abstractmethod
      def m(self): pass
  class S(B): pass
  print('Class defined OK')
  try:
      S()
  except TypeError:
      print('TypeError at runtime instantiation only OK')"
  ```
  *Criterio:* `exit code 0` con demostración física de instanciación en runtime.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

> [!TIP]
> **Metodología de Domain Shifting:** Los siguientes conceptos se explican utilizando analogías de dominios externos (ej. El Servicio Postal de Ankh-Morpork). El Operador debe traducir el principio a su propio código en `quests/` y `rite/` sin soluciones pre-fabricadas.

### PY-005: Propagación de Excepciones en Pipelines de Ingesta
- **Archivo:** `rite/src/pipeline.py:L24-L27`
- **Concepto:** En pipelines batch de producción, capturar una excepción de ingesta solo para imprimir un log y terminar silenciosamente con `exit 0` es un antipatrón crítico. Si el archivo no existe o está corrupto, el proceso debe fallar con código de error no cero (`sys.exit(1)` o relanzando la excepción) para que el orquestador (Airflow, Prefect, Cron) detecte la falla y active alertas/reintentos.
- **Domain Shifting (Oficina Postal de Ankh-Morpork):**
  ```python
  # Si la valija postal de Lancre se pierde en el pantano:
  # Antipatrón: registrar "Valija perdida" y decir que el día terminó con éxito.
  # Canónico:
  try:
      mailbag = courier.fetch_bag("Lancre")
  except BagNotFoundError as err:
      logger.critical("No se pudo recuperar la valija de Lancre: %s", err)
      raise err  # O sys.exit(1): el Patricio debe enterarse de que el correo falló
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/rite'); from src.cli import main; import sys as s; s.argv=['cli.py', '--input', 'archivo_fantasma.csv']; main()"
  ```
  *Resultado:* Termina con `exit 0` silencioso.
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  cd content/subjects/python/chronicles/PY-POO/rite && .venv/bin/python3 -m src.cli --input archivo_fantasma.csv
  ```
  *Criterio:* Termina con código no cero (`exit code != 0`).

### PY-006: Dataclasses con `slots=True` en `quests/02-entities/inventory.py`
- **Archivo a modificar por el Operador:** `quests/02-entities/inventory.py:L4,L11,L20`
- *(Nota de Higiene: La aclaración en `lore/02` ya fue incorporada en Carril B)*
- **Concepto:** Por defecto, `@dataclass` utiliza `__dict__` interno y permite agregar atributos dinámicos arbitrarios por error de tipeo (ej. `sword.nam = 'Scalibur'` en vez de `sword.name`). Al declarar `@dataclass(slots=True)` en `Weapon` y `Potion`, Python genera un descriptor rígido de memoria, optimiza el tamaño del objeto y detona `AttributeError` ante cualquier intento de asignar atributos dinámicos.
- **Domain Shifting (Inventario del Gremio de Alquimistas):**
  ```python
  from dataclasses import dataclass

  # Con slots=True, la estructura de la poción es rígida
  @dataclass(slots=True)
  class Potion:
      name: str
      potency: int

  p = Potion("Curación Mayor", 50)
  # p.potenci = 60  <-- Detona AttributeError inmediatamente, previniendo el bug silencioso
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/02-entities'); from inventory import Weapon; w = Weapon('Sting', 20, 25.5); w.nam = 'Scalibur'; print('Pasa silencioso:', w.nam)"
  ```
  *Resultado:* Pasa sin error (`Pasa silencioso: Scalibur`).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -c "import sys; sys.path.insert(0, 'content/subjects/python/chronicles/PY-POO/quests/02-entities'); from inventory import Weapon; w = Weapon('Sting', 20, 25.5);
  try:
      w.nam = 'Scalibur'
      exit(1)
  except AttributeError:
      print('PASS: Typo bloqueado por slots=True')
      exit(0)"
  ```
  *Criterio:* `exit code 0`.

### PY-008: Tipado Estricto en Polimorfismo e Inferencia de Listas (MyPy)
- **Archivo a modificar:** [`rite/src/transactions.py:L16, L21, L26`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/src/transactions.py)
- **Referencia en Lore:** [`lore/01-abstract-classes-and-interfaces.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/01-abstract-classes-and-interfaces.md) (Contratos de clases base) y [`lore/02-domain-entities-and-dataclasses.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/02-domain-entities-and-dataclasses.md) (Polimorfismo).
- **Diagnóstico (¿Qué está pasando en tu código actual?):**
  Al ejecutar MyPy en `transactions.py`, reporta dos fallos:
  1. **Omisión de firma en subclases:** `Transaction` declara `@abstractmethod def get_signed_amount(self) -> float:`, pero `Income` y `Expense` omitieron la anotación de retorno `-> float`.
  2. **Inferencia de lista vacía en polimorfismo:** En la función `build_transactions`, tienes:
     ```python
     transactions = []  # <-- Sin anotación de tipo
     for row in raw_data:
         if row["type"] == "Income":
             transactions.append(Income(...))  # MyPy asume que la lista es list[Income]
         elif row["type"] == "Expense":
             transactions.append(Expense(...)) # MyPy FALLA: espera Income, no Expense
     ```
     En Python, las listas son *invariantes*. Al hacer el primer `append(Income)`, MyPy deduce que la lista es exclusivamente de tipo `list[Income]`. Cuando luego intentas agregar un `Expense`, MyPy lanza:
     `error: Argument 1 to "append" of "list" has incompatible type "Expense"; expected "Income"`.
     Para que una lista acepte subclases distintas que comparten una clase base, debes anotar explícitamente la lista con la clase padre: `transactions: list[Transaction] = []`.
- **Domain Shifting (El Bestiario de la Universidad Invisible):**
  ```python
  from abc import ABC, abstractmethod

  class MagicalCreature(ABC):
      @abstractmethod
      def danger_level(self) -> float:
          pass

  class Dragon(MagicalCreature):
      # Regla 1: La subclase debe preservar la firma exacta -> float
      def danger_level(self) -> float:
          return 95.5

  class Pixie(MagicalCreature):
      def danger_level(self) -> float:
          return 10.0

  def register_cage(creature_data: list[dict]) -> list[MagicalCreature]:
      # Regla 2: Anotar la lista con la clase BASE para permitir polimorfismo
      creatures: list[MagicalCreature] = []
      for item in creature_data:
          if item["type"] == "dragon":
              creatures.append(Dragon())
          else:
              creatures.append(Pixie())
      return creatures
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -m mypy content/subjects/python/chronicles/PY-POO/rite/src/transactions.py
  ```
  *Resultado:* `error: Argument 1 to "append" of "list" has incompatible type "Expense"; expected "Income"` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -m mypy content/subjects/python/chronicles/PY-POO/rite/src/transactions.py
  ```
  *Criterio:* `Success: no issues found` (`exit code 0`).

---

### PY-009: Semántica de Retorno en Constructores `__init__` y Tipado de Atributos
- **Archivo a modificar:** [`quests/00-classes/shopping_cart.py:L3, L5`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/quests/00-classes/shopping_cart.py)
- **Referencia en Lore:** [`lore/00-from-functions-to-classes.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/lore/00-from-functions-to-classes.md) (Sección 2: Clases y el Constructor `__init__`).
- **Diagnóstico (¿Qué está pasando en tu código actual?):**
  En `shopping_cart.py` tienes actualmente:
  ```python
  class cart:
      def __init__(self, customer_id: str) -> dict:  # <-- ERROR: -> dict
          self.customer_id = customer_id
          self.items = []                             # <-- Falta tipo de la lista
          self.total = 0.0
  ```
  MyPy detona tres errores estrictos:
  1. `error: The return type of "__init__" must be None`: En Python, `__init__` es un inicializador de instancia que muta `self`; el lenguaje prohíbe que devuelva valores. Su retorno siempre es implícitamente `None`. Si se anota con `-> dict` o cualquier otro tipo, MyPy lo considera inválido.
  2. `error: Missing return statement`: Como anotaste `-> dict`, MyPy espera un `return {...}`, pero `__init__` no puede retornar diccionarios.
  3. `error: Need type annotation for "items"`: La lista vacía `self.items = []` necesita saber qué contiene (por ejemplo: `self.items: list[str] = []`).
- **Domain Shifting (Mochila del Explorador de Lancre):**
  ```python
  class Backpack:
      # En Python, el constructor __init__ SIEMPRE retorna None (o se omite la anotación de retorno)
      def __init__(self, owner: str) -> None:
          self.owner = owner
          # Si un atributo es una lista vacía, MyPy exige tipar sus elementos:
          self.inventory: list[str] = []
          self.weight: float = 0.0

      def add_gear(self, item: str, weight: float) -> None:
          self.inventory.append(item)
          self.weight += weight
  ```
- **Sonda Inicial (Fallo actual):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -m mypy content/subjects/python/chronicles/PY-POO/quests/00-classes/shopping_cart.py
  ```
  *Resultado:* `error: The return type of '__init__' must be None` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  content/subjects/python/chronicles/PY-POO/rite/.venv/bin/python3 -m mypy content/subjects/python/chronicles/PY-POO/quests/00-classes/shopping_cart.py
  ```
  *Criterio:* `Success: no issues found` (`exit code 0`).

---

## 3. Log de Mutaciones y Verificación

| ID | Fecha | Carril | Responsable | Sonda Inicial (Salida) | Sonda Final (Salida) | Estado |
|---|---|---|---|---|---|---|
| PY-001 | 2026-10-13 | B | Antigravity | `NameError: name 'Reader' is not defined` (exit 2) | `1 passed in 0.02s` (exit 0) | ✅ Completado |
| PY-002 | 2026-10-13 | B | Antigravity | `AttributeError: 'list' object has no attribute 'celsius'` (exit 1) | `PASS: Average calculation OK` (exit 0) | ✅ Completado |
| PY-003 | 2026-10-13 | B | Antigravity | `NameError: name 'GameLoader' is not defined` (exit 1) | `Starting level 1 with physics engine ready` (exit 0) | ✅ Completado |
| PY-004 | 2026-10-13 | B | Antigravity | `ModuleNotFoundError: No module named 'src'` (exit 1) | Procesamiento exitoso modular y directo (exit 0) | ✅ Completado |
| PY-021/022 | 2026-10-13 | B | Antigravity | `argparse` no declarado en temario (exit 1) | Declarados `@dataclass` y `argparse` en syllabus (exit 0) | ✅ Completado |
| PY-007 | 2026-10-13 | B | Antigravity | Prosa incorrecta en Lore 01 | Corrección en Lore 01 + Sonda de runtime (exit 0) | ✅ Completado |
| PY-005 | 2026-10-13 | A | Operador | Silencioso exit 0 ante archivo faltante (exit 0) | `raise e` propaga `DataSourceNotFoundError` (exit 1) | ✅ Completado |
| PY-006 | 2026-10-13 | A/B | Operador / Antigravity | Permite `w.nam = 'Scalibur'` silencioso | `slots=True` bloquea typo con `AttributeError` (exit 0) | ✅ Completado |
| PY-008 | 2026-10-13 | A | Operador | MyPy falla: `incompatible type Expense` (exit 1) | `Success: no issues found in 1 source file` (exit 0) | ✅ Completado |
| PY-009 | 2026-10-13 | A | Operador | `__init__ -> dict` y lista sin tipo en MyPy (exit 1) | `Success: no issues found in 1 source file` (exit 0) | ✅ Completado |
