# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../docs/08-protocol-yellow.md))*


## Identification
Type: [M (Core) | S (Refactor/Scaling) | B (Integration)]  
Campaign Code: [e.g., PY-POO-FINANCE]  
Mission Code: [e.g., M01]  
Title: [Short, direct technical scope]
Status: [🟢 Ready | 🔵 In Progress]

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** 
**Proposed Solution / Pattern:** (State the design pattern or modular approach).
**Trade-offs:** 

---

## Technical Objective
Describe the precise functionality to be developed and the module's role in the larger system.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1:
- [ ] Test Case 2:

---

## Execution Steps (Implementation Plan)
1.  
2.  
3.  

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Code passes static analysis (e.g., `flake8`, `mypy`).
- [ ] Tests execute correctly (`pytest`).
- [ ] Module integrates with the system output gracefully.
- [ ] Logic respects SOLID principles (specifically...).

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*
