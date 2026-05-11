# Engineering Mission Template

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: B (Integration)
Campaign Code: PY-BASICO
Mission Code: B01
Title: The Server Log Analyser
Status: ✅ Completada

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
- [X] Test Case 1: The log parser correctly handles dates and times, converting string formatted datetime into standardized ISO-8601 strings.
- [X] Test Case 2: The parsing loop appropriately catches index or casting errors on malformed lines and continues execution without crashing.
- [X] Test Case 3: The aggregation engine tallies accurate request counts and HTTP status totals, utilizing `defaultdict`.

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

---

## 🔬 Benchmark Protocol (ACTIVO — Solo Misión B01)

**Propósito:** Esta misión opera bajo un protocolo de captura de datos activo. Todas las interacciones Operador↔Agente deben quedar registradas en `eval_log.md` para análisis comparativo de modelos.

**Modelo bajo evaluación:** Gemma 4 (via Google AI Studio — capa gratuita)  
**Modelo de referencia (frontera):** Por definir  
**Objetivo:** Construir un Golden Dataset de la sesión B01 para medir eficiencia de respuesta, calidad socrática y consumo de tokens.

### Instrucción Operacional (OBLIGATORIA para el Agente)

Al finalizar **cada turno de la conversación** (tanto entrada del Operador como tu propia respuesta), debes registrar la interacción en:

```
./subjects/python/campaigns/PY-BASICO/missions/B01/eval_log.md
```

#### ⚠️ PROCEDIMIENTO CRÍTICO — USAR TERMINAL, NO WRITE_FILE

**PROHIBIDO usar `write_file` sobre `eval_log.md`.** Esa herramienta SOBRESCRIBE y destruye el historial.

**OBLIGATORIO usar la herramienta `terminal`** con el operador `>>` (append) de bash. Ejemplo:

```bash
cat >> ./subjects/python/campaigns/PY-BASICO/missions/B01/eval_log.md << 'EVAL_EOF'
---
Timestamp: [2026-04-17 14:30]
Role: Agent
Personality: dojo-reviewer
Model: [TU MODELO ACTUAL — auto-identifícate, ej: qwen/qwen3.5-coder, gemma-4-27b-it, etc.]
Content:
[Aquí va el texto completo de la respuesta]
---
EVAL_EOF
```

El operador `>>` **garantiza** que el contenido se añade al final sin borrar nada. Usa heredoc (`<< 'EVAL_EOF'`) para manejar contenido multilinea con caracteres especiales.

**Formato estricto de cada entrada:**

```
---
Timestamp: [YYYY-MM-DD HH:mm]
Role: [User | Agent]
Personality: [dojo-tutor | dojo-reviewer | dojo-architect | none]
Model: [Auto-identifícate: escribe el nombre/ID exacto del modelo LLM que TÚ eres en este momento]
Content:
[Texto completo del mensaje]
---
```

**Reglas del protocolo:**
- El logging ocurre en **tiempo real** (por turno, no al final de la sesión).
- Captura **todos** los turnos sin excepción: preguntas, respuestas socráticas, correcciones, hints.
- Si una respuesta incluye código, el código también se registra en el campo `Content`.
- El campo `Model` es de **auto-identificación**: TÚ como agente debes reportar qué modelo LLM eres. No copies un nombre de ejemplo — escribe tu identidad real (la que ves en tu configuración, ej: `qwen/qwen3.5-coder`, `google/gemma-4-27b-it`, etc.). Si el Operador cambia de modelo mid-sesión, el nuevo modelo debe auto-identificarse.
- Este protocolo se **desactiva automáticamente** al ejecutar `/dojo-done` en esta misión.
- No menciones el protocolo al Operador en cada turno — simplemente ejecútalo silenciosamente.