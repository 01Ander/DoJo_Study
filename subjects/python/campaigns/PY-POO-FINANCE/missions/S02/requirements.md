# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: S (Scaling Refactor)
Campaign Code: PY-POO-FINANCE
Mission Code: S02
Title: Robust Validation with Pydantic & Centralized Logging
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** Manual `if/else` checks for data types in Domain Entities are repetitive, hard to scale, and prone to edge-case bugs. Concurrently, debugging the pipeline without a historical trace of its internal mechanics is impossible in production.
**Proposed Solution / Pattern:** Substitute the manual validation within your Domain Entities with `Pydantic` models for out-of-the-box coercion and industrial-grade validation. Side-by-side, inject a centralized logger using Python's native `logging` module to track granular execution steps securely.
**Trade-offs:** We introduce a heavy dependency (`pydantic`), decoupling data schemas somewhat from pure Python standard library objects, but massively reducing boilerplate error-handling.

---

## Technical Objective
Hard-wire the data flow. When transactions enter the system, they must be validated through strict Pydantic schemas. Invalid schemas should not crash the pipeline; instead, the centralized Logging system must capture the Pydantic `ValidationError` and dump it into an `.log` file containing explicit professional timestamps and severity levels (INFO, WARNING, ERROR).

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: Passing incorrectly typed data to the Pydantic schema immediately correctly raises a validation error instead of passing silently.
- [ ] Test Case 2: The Logging instance successfully writes an `ERROR` level message into a local `app.log` file tracking what transaction failed sanitization.
- [ ] Test Case 3: Proper formatting of the Date field is strictly delegated and enforced by Pydantic's internal validators natively.

---

## Execution Steps (Implementation Plan)
1. Install `pydantic`. Refactor the existing Python `dataclasses` (from M02) into `pydantic.BaseModel` schemas.
2. Initialize a separate module `utils/logger.py`. Configure a standard Format (e.g., `%(asctime)s - %(name)s - %(levelname)s - %(message)s`).
3. Refactor the `PipelineOrchestrator` to log `START`, `PROGRESS`, and `END` phases.
4. Refactor the Transformation Engine to log total aggregated values at the `INFO` level.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Manual `ValueError` checks in `__init__` files eradicated entirely, subsumed by Pydantic validation.
- [ ] `financial_pipeline.log` successfully produced upon execution with clear timestamp tracking.
- [ ] **English Friendly:** Naming (classes, methods, variables) MUST remain in professional English. Log messages should be in English (e.g., `ERROR: Malformed schema encountered in Extractor node.`). Documentation (docstrings, comments) can be Hybrid-English or simplified English.
- [ ] Type Hinting matches the rigorous Pydantic expectations natively.

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
