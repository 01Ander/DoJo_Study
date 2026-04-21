# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M (Core Architecture)
Campaign Code: PY-POO-FINANCE
Mission Code: M03
Title: The Transformation and Analytics Engine
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** Logic that aggregates data can quickly clutter domain models or orchestration scripts if not decoupled appropriately.
**Proposed Solution / Pattern:** Construct a stateless `AnalyticsEngine` class whose sole responsibility is to receive a `List[Transaction]` and return aggregated analytical objects. The engine acts purely functionally—no side effects.
**Trade-offs:** We separate algorithm logic from data structure. It might seem like overkill for basic sums, but as currency conversion and probabilistic metrics are added later, a centralized transformation class scales cleanly.

---

## Technical Objective
Develop a calculation layer that ingests normalized Domain Entities (produced in M02) and computes aggregated financial metrics (gross income, total expenses, net balance, and expense grouping per category).

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: Providing an empty list of `Transaction` entities yields zeros across all analytical outputs organically, without crashing.
- [ ] Test Case 2: The `AnalyticsEngine.calculate_net_balance()` correctly subtracts total expenses from total income using parsed Domain Entities.
- [ ] Test Case 3: Given a list of identical categories, `aggregate_by_category()` accurately sums them utilizing `collections.defaultdict`.

---

## Execution Steps (Implementation Plan)
1. Write the tests supplying multiple lists of mock `Income` and `Expense` objects.
2. Build the `AnalyticsEngine` class and its primary public methods.
3. Use the Python Standard Library (`collections` mostly) or safely integrate `Pandas` if the scaling requires vectorized transformations.
4. Ensure the output is returned as standard Python Dictionaries or a newly defined `AnalyticsReport` Dataclass.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Tests execute correctly (`pytest`).
- [ ] Module integrates seamlessly, accepting strictly typed `List[Transaction]`.
- [ ] Logic respects the Single Responsibility Principle (The engine only calculates, it doesn't deal with file I/O).
- [ ] **English Friendly:** Naming (variables, methods, classes) MUST remain in professional English. Documentation (docstrings, comments) can be Hybrid-English or simplified English. Exception logs can be bilingual (Spanish/English).

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
