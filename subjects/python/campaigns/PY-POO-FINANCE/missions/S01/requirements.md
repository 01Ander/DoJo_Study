# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: S (Scaling Refactor)
Campaign Code: PY-POO-FINANCE
Mission Code: S01
Title: Automated TDD Suite & Coverage Validation
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** Having isolated unit tests per module (M01-M04) provides local safety, but we lack an overarching view of how well the code is truly tested, and whether the components integrate smoothly End-to-End (E2E).
**Proposed Solution / Pattern:** Implement a systematic Test Suite using `pytest` alongside the `pytest-cov` plugin to trace module coverage. We will design high-level E2E integration tests verifying the uninterrupted flow from Extractor to Loader. 
**Trade-offs:** Imposes friction by enforcing a strict coverage threshold before any new feature merge. It demands maintaining mock data structures, which costs development time but effectively eradicates regression bugs.

---

## Technical Objective
Elevate the project's quality assurance to industrial standards by consolidating all previous unit tests into a formal suite. Furthermore, establish a hard requirement of >80% code coverage measured mathematically. You must write the missing integration tests to cover the "Glue" code in the Orchestrator.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: E2E Pipeline processes a mocked dirty CSV and successfully triggers the mocked JSON Loader without any intermediate state errors.
- [ ] Test Case 2: The pipeline gracefully handles complete structural failure (e.g., injecting an unreadable format) by capturing the Exception natively without dumping a traceback to the user.
- [ ] Test Case 3: `pytest-cov` strictly reports above an 80% coverage on the `src/` directory.

---

## Execution Steps (Implementation Plan)
1. Install `pytest-cov` in the virtual environment.
2. Structure a dedicated `tests/integration/` directory to separate E2E logic from standard unit variables.
3. Write the `test_pipeline_e2e.py` simulating the exact behavior of the main execution script using memory-resident fixtures (Pytest's `tmp_path`).
4. Execute `pytest --cov=src --cov-report=term-missing` and iterate on uncovered branches until the 80% threshold is cleared.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Output terminal proves minimum 80% Coverage explicitly.
- [ ] A local `.coveragerc` file configures the test suite to ignore non-vital code blocks.
- [ ] **English Friendly:** Naming (test functions, variables) MUST remain in professional English (e.g., `test_pipeline_rejects_invalid_file_format_safely`). Documentation (docstrings, comments) can be Hybrid-English or simplified English.
- [ ] SOLID: Test modules decouple logic correctly using mock objects rather than invoking real databases or disks where possible.

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
