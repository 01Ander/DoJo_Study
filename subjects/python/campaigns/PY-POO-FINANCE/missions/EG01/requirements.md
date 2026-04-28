# EG01 — Exit Gate: New Extractor Integration

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../docs/07-protocol-yellow.md))*

## Identification
Type: EG (Exit Gate)
Campaign Code: PY-POO-FINANCE
Mission Code: EG01
Title: New Extractor Integration — POO Assimilation Verification
Status: 🟢 Ready

---

## 🏛️ Design & Architecture (Mini-RFC)
**Problem Context:** La campaña PY-POO-FINANCE ha sido completada. Se necesita verificar que los conceptos de OOP (ABC, herencia, polimorfismo, TDD) fueron asimilados — no solo completados con andamiaje.
**Proposed Solution / Pattern:** Implementar un nuevo extractor concreto (JSONExtractor) que cumpla el contrato de AbstractExtractor, demostrando dominio independiente.
**Trade-offs:** Fase 2 obligatoria — sin código del tutor. El operador debe resolver por su cuenta.

---

## Technical Objective
Implementar un `JSONExtractor` que:
1. Herede de `AbstractExtractor`
2. Lea datos desde un archivo `.json` (array de diccionarios)
3. Retorne `List[Dict[str, Any]]` (mismo contrato que `CSVExtractor`)
4. Se integre al `FinancialPipeline` existente sin modificar el pipeline

---

## Rules (Exit Gate Protocol)
- ⚠️ **Modo Fase 2 obligatorio:** el tutor NO da código. Solo preguntas socráticas.
- El operador DEBE escribir el test ANTES de la implementación (TDD).
- Si el operador se bloquea >15 min en un punto, el tutor puede dar UN hint conceptual (no código).
- Si el operador necesita código directo, el Exit Gate se marca como no aprobado y se genera una misión de refuerzo.

---

## Required Testing (TDD / QA)
- [ ] Test: `JSONExtractor` hereda de `AbstractExtractor` (isinstance check)
- [ ] Test: `JSONExtractor.extract_data()` retorna `List[Dict[str, Any]]` desde un archivo JSON válido
- [ ] Test: Pipeline E2E funciona con `JSONExtractor` como input (sustituyendo `CSVExtractor`)

---

## Concepts Validated
- [ ] ABC / Abstract Base Classes (crear clase que hereda de AbstractExtractor)
- [ ] TDD (test escrito antes de la implementación)
- [ ] Herencia y polimorfismo (el pipeline acepta cualquier AbstractExtractor)
- [ ] Imports correctos (sin path hacking, desde src/ centralizado)
- [ ] Typing y mypy clean

---

## Completion Criteria & Definition of Done (DoD)
- [ ] Tests escritos por el operador SIN código directo del tutor
- [ ] `JSONExtractor` implementado por el operador SIN andamiaje
- [ ] `pytest tests/ -v` pasa todos los tests (existentes + nuevos)
- [ ] `mypy src/` limpio
- [ ] Pipeline E2E funciona con JSONExtractor

---

## Architectural/Friction Notes
*Este es el primer Exit Gate del sistema. Documentar la experiencia para calibrar futuros EGs.*
