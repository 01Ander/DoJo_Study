# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/08-protocol-yellow.md))*


## Identification
Type: B (Integration)  
Campaign Code: PY-BASICO  
Mission Code: B01  
Title: The Server Log Analyser
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*

**Business Context:** A sprawling application generates large web server logs (e.g. Apache/Nginx format) with thousands of requests, but also contains corrupted lines, irregular timestamps, and missing fields. The Ops team needs a daily automated summary of metrics (total requests, requests per endpoint, HTTP status breakdown) without relying on heavyweight tools.

**ROI & Impact:**
- **Cost Reduction:** Replaces manual Log parsing with an autonomous script that handles corrupted data gracefully.
- **Auditability:** Identifies malformed logs and separates them so infrastructure teams can fix the logging sources.

**Protocol Yellow (Muro de Contención):** This assessment continues to solidify brute fundamentals. It focuses on text/CSV parsing, timestamp manipulation, and frequency mapping using basic dictionaries and loops.

**Modo de trabajo:** Esta misión se ejecuta en **Fase 2 (Reviewer Socrático)**. 
El Operador implementa solo. El Reviewer hace preguntas, NO da código. 
Si la fricción sube >7, escalar a Tutor temporalmente.
Referencia permitida: código de B00 como documentación.

**Proposed Solution / Pattern:** A sequential pipeline utilizing the standard library (`csv`, `collections`, `datetime`, `json`). It processes logs lazily, discarding invalid formats, accumulating counters/metrics via `defaultdict`, and finally outputs a clean `summary_report.json`.
**Trade-offs:** We bypass advanced log-parsing engines or Regex libraries in favor of granular manual text manipulation and manual exception handling.

---

## Technical Objective
Build a lightweight, bulletproof ETL script that reads a simulated flat server log file containing both valid and malformed requests. The system must parse complex timestamp strings, group requests by endpoints and HTTP status codes using `defaultdict`, isolate formatting errors using `try/except`, and export a structured JSON aggregate without failing entirely on encountering bad lines.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: The log parser correctly handles dates and times, converting string formatted datetime into standardized ISO-8601 strings.
- [ ] Test Case 2: The parsing loop appropriately catches index or casting errors on malformed lines and continues execution without crashing.
- [ ] Test Case 3: The aggregation engine tallies accurate request counts and HTTP status totals, utilizing `defaultdict`.

---

## Execution Steps (Implementation Plan)
1. **Mock the Data:** Programmatically generate (or manually create) a dirty text/csv file simulating server logs with timestamps, endpoints, status codes, including rows with missing data or strange formats.
2. **Type Hinting Core:** Define core functions using strict Type Hinting (e.g., `def parse_log_line(line: str) -> dict:`).
3. **The Try/Except Envelope:** Implement the processing loop. Lines that fail parsing should trigger controlled exceptions, writing the bad line to `ignored_logs.txt`.
4. **Aggregation Logic:** Utilize `collections.defaultdict` to efficiently group and count HTTP response codes and endpoint traffic.
5. **Output Delivery:** Export the finalized metrics dictionary into a structured `summary_report.json` document.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] **English Grace Period:** Naming (variables, functions, classes) MUST remain in professional English. Documentation (docstrings, technical comments) can be Hybrid-English or simplified English. Console error logs can be bilingual (Spanish/English) for rapid debugging.
- [ ] **Hard Constraint:** Absolutely Zero usage of third-party libraries (`pandas`, `numpy`, etc. are forbidden). Stick to `csv`, `json`, `datetime`, `collections`, `logging`. 
- [ ] **Functional Resilience:** Aesthetic perfection is not demanded. The goal is functionality and data resilience. Intentional sabotage of the input file must not stop the output generation of the clean records.
- [ ] **Specialization Flexibility:** The Operator can implement a Data Quality focus (heavy programmatic validations) or a DevOps focus (Orchestrated CLI tooling/automation).
- [ ] **Social README (Visibility Layer):** Include a `README.md` that explains the project's business impact and architecture for non-technical stakeholders (HR/PMs).
- [ ] Comprehensive Docstrings included for every single function explaining arguments, return types, and potential raised Exceptions.
- [ ] Mypy compliance (No dynamic `Any` usage where types are definitively known).

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*