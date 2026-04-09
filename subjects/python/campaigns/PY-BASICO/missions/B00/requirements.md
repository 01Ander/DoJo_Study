# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/08-protocol-yellow.md))*


## Identification
Type: B (Integration)  
Campaign Code: PY-BASICO  
Mission Code: B00  
Title: The Data Resilience Assessment
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*

**Business Context:** Raw financial data arrives in inconsistent formats and featuring corruption. Manual remediation by analysts consumes 8+ hours per week per dataset. Automating this via a resilient, dependency-free script ensures the business can scale data ingestion without ballooning operational costs.

**ROI & Impact:**
- **Cost Reduction:** Offloads 100% of the manual cleansing task to a sub-second automated script.
- **Auditability:** Provides clear logs of ignored records, reducing financial discrepancy risks.

**Protocol Yellow (Muro de Contención):** This assessment acts as a containment wall. It focuses strictly on brute fundamentals: dictionary manipulation, `for` loops with filtering logic, and simple functions before allowing the user to enter the abstraction of OOP classes in M01. If this assessment presents high cognitive friction (Friction > 7), a 2-week reinforcement pause is automatically suggested.
**Proposed Solution / Pattern:** A pipeline of pure native functions (Extract, Cleanse/Transform, Aggregate, Load) utilizing strictly the Python Standard Library. Data flows through these functions using basic loops and conditionals. Failures are isolated per record instead of crashing the batch.
**Trade-offs:** We trade off the execution speed and sheer convenience of Pandas for granular control over the memory and the flow of iterations, demanding manual schema enforcement and robust exception handling.

---

## Technical Objective
Build a lightweight, bulletproof ETL script that reads a simulated flat file (CSV/JSON) containing dirty financial transactions. The system must normalize formatting (dates, currencies), apply business rules (filter out anomalies like negative amounts), calculate financial aggregations per classification, and gracefully handle all parsing errors without halting execution.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: The date parser successfully normalizes different date formats (e.g., `12-31-2023` and `2023/12/31`) into standard ISO-8601 (`YYYY-MM-DD`).
- [ ] Test Case 2: The type-casting logic raises a specific custom-logged exception when finding an alphanumeric string in a currency field instead of crashing implicitly.
- [ ] Test Case 3: The aggregation engine correctly yields the Total, Mean, and Count for an overlapping Category dict.

---

## Execution Steps (Implementation Plan)
1. **Mock the Data:** Programmatically generate (or manually create) a dirty CSV file featuring missing values, trailing spaces, corrupted numbers, and distinct date formats.
2. **Type Hinting Core:** Define the core functions using strict Type Hinting (e.g., `def clean_currency(raw: str) -> float:`).
3. **The Try/Except Envelope:** Implement the reading loop. Corrupted rows must trigger exceptions that write the raw line alongside an explanatory message to a secondary `ignored_records.log` text file.
4. **Aggregation Logic:** Utilize `collections.defaultdict` to efficiently group the validated records by category.
5. **Output Delivery:** Export the final aggregated report into a structured `summary_report.json` document.

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
