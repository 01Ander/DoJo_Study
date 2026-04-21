# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M (Core Architecture)
Campaign Code: PY-POO-FINANCE
Mission Code: M01
Title: Abstract Extractors and Interface Segregation
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** Hardcoding a CSV parser inside the main pipeline violates the Open-Closed Principle. If tomorrow we need to parse financial records from a JSON file or an API, we would have to rewrite the core logic.
**Proposed Solution / Pattern:** Implement an Abstract Base Class (ABC) named `AbstractExtractor` dictating a strict contract (e.g., must implement an `extract_data` method). Then, create concrete classes like `CSVExtractor` that inherit from this interface. 
**Trade-offs:** Introduces minor boilerplate overhead initially, but guarantees that any future data source will seamlessly plug into the pipeline without breaking downstream components.

---

## Technical Objective
Develop the extraction layer of the ETL pipeline avoiding procedural scripting. Rely heavily on the `abc` library in Python to lock class definitions. Build the first concrete implementation for reading static CSV files yielding raw dictionaries.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: Instantiating `AbstractExtractor` directly raises a `TypeError` (enforcing abstract behavior).
- [ ] Test Case 2: A poorly defined concrete class missing the `extract_data` implementation throws a `TypeError` upon instantiation.
- [ ] Test Case 3: `CSVExtractor.extract_data()` correctly returns a structurally valid `List[dict]` given a valid mock CSV file.

---

## Execution Steps (Implementation Plan)
1. Write the Pytest suite in `tests/test_extractors.py` strictly checking the aforementioned cases. 
2. Create the `abstract_extractor.py` interface.
3. Develop the `csv_extractor.py` class handling context managers (`with open...`) safely.
4. Assure typing hints return exactly `List[Dict[str, Any]]`.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Code passes static analysis (`mypy` yields zero typing issues).
- [ ] Tests execute correctly (`pytest` is all green).
- [ ] Logic respects SOLID principles (specifically OCP: Open to extension by new formats, closed to internal modification).
- [ ] **English Grace Period:** Naming (variables, methods, classes) MUST remain in professional English. Documentation (docstrings, comments) can be Hybrid-English. Exception logs can be bilingual (Spanish/English).
- [ ] **Specialization Flexibility:** Do not aim for aesthetic perfection; choose between a strong Data Quality focus (strict schema assertions) or a DevOps/Automation focus (CI/CD readiness, CLI arguments).

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
