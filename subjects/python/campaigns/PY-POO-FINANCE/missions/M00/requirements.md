# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M (Core Architecture)
Campaign Code: PY-POO-FINANCE
Mission Code: M00
Title: Hello, Classes — From Functions to Objects
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** The procedural ETL pipelines built in PY-BASICO (B00/B01) work, but their functions are floating independently with no cohesive "owner". State (file paths, configuration) is passed around as arguments through every function call — a maintenance problem that grows with scale.
**Proposed Solution / Pattern:** Refactor pipeline logic into a single class (`LogAnalyzer`) that encapsulates related functions as methods and holds shared state as instance attributes. This is the simplest meaningful introduction to OOP: a class that replaces a group of related functions.
**Trade-offs:** We intentionally avoid advanced OOP patterns (ABC, inheritance, polymorphism) in this mission. The goal is strictly to internalize `class`, `__init__`, `self`, and the mental shift from "calling functions" to "sending messages to objects". Advanced patterns follow in M01+.

**Modo de trabajo:** Esta misión se ejecuta en **Fase 1 (Tutor)**.
El Tutor proporciona código explicado con Domain Shifting. El Operador reescribe y asimila.
Referencia permitida: código de B01 como base de refactoreo.

---

## Technical Objective
Convert the procedural `etl.py` from PY-BASICO B01 (server log analyser) into an object-oriented `LogAnalyzer` class. The resulting class must encapsulate all pipeline steps as methods, hold configuration as instance attributes, and produce identical output to the original procedural version.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: `LogAnalyzer` can be instantiated with valid file paths, and its attributes (`input_path`, `output_path`, `log_path`) are correctly stored.
- [ ] Test Case 2: `LogAnalyzer.run()` processes a mock dirty CSV and produces a valid `summary_report.json` identical to the procedural pipeline output.
- [ ] Test Case 3: Calling a private method directly (e.g., `analyzer._load_logs()`) returns the expected `list[str]` — demonstrating that helper methods are encapsulated within the object.

---

## Execution Steps (Implementation Plan)
1. **Create project structure:** Set up `src/log_analyzer.py` and `tests/test_log_analyzer.py` with `pyproject.toml`.
2. **Write failing tests:** Define 3 tests covering instantiation, full pipeline run, and private method access.
3. **Define the class skeleton:** Write `class LogAnalyzer` with `__init__` accepting three paths as parameters. Store them as `self.input_path`, `self.output_path`, `self.log_path`.
4. **Migrate functions to methods:** Convert each procedural function from B01 (`load_logs`, `process_logs`, `aggregation_logs`, `export_report`) into methods of the class. Public orchestrator method: `run()`. Private helpers: `_load_logs()`, `_process_logs()`, `_aggregate()`, `_export()`.
5. **Verify equivalence:** Run the class pipeline against the same mock data from B01 and assert output matches.

---

## Key Concepts to Internalize

| Concept | What it means | Procedural equivalent |
|---|---|---|
| `class LogAnalyzer:` | A blueprint for creating objects | A module/file grouping related functions |
| `__init__(self, ...)` | The constructor — runs when you create an object | Setup code at the top of a script |
| `self` | Reference to "this specific object" | Passing config as function arguments |
| `self.input_path` | Instance attribute — data owned by the object | Global variable or repeated parameter |
| `def run(self)` | Instance method — behavior of the object | A function that calls other functions |
| `def _load_logs(self)` | Private method (convention) — internal detail | Helper function with `_` prefix |
| `analyzer = LogAnalyzer(...)` | Instantiation — creating a real object from the blueprint | Calling `run_pipeline(args)` |
| `analyzer.run()` | Sending a message to the object | `run_pipeline(input, output, log)` |

---

## Completion Criteria & Definition of Done (DoD)
- [ ] A `LogAnalyzer` class exists with `__init__`, `run()`, and at least 4 private methods.
- [ ] Tests execute correctly (`pytest`) — minimum 3 tests covering instantiation, run, and method access.
- [ ] The class produces **identical output** to the procedural B01 pipeline given the same input data.
- [ ] No `abc`, no inheritance, no `@property` — pure basic class with methods. Keep it simple.
- [ ] **English Friendly:** Naming (variables, methods, classes) MUST remain in professional English. Documentation (docstrings, comments) can be Hybrid-English or simplified English. Exception logs can be bilingual (Spanish/English).
- [ ] Comprehensive Docstrings for the class and each public method.

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
