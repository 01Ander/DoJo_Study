# Engineering Mission Template

**Friction Level:** [2] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: B (Integration / Boss)
Campaign Code: PY-POO-FINANCE
Mission Code: B01
Title: The Financial Projector Command Line Interface (CLI)
Status: ❌ Descartada

---

## 🏛️ Design & Architecture (Mini-RFC)
*A brief architectural discussion before writing code. Justify your approach.*
**Problem Context:** Running scripts directly using `python main.py` and hardcoding file paths is amateur. Users (or automation cron-jobs) need the ability to point the pipeline iteratively at dynamic datasets flexibly. 
**Proposed Solution / Pattern:** Expose the pipeline through an industrial Command Line Interface (CLI) utilizing a library such as `Typer` or `Click`. This enables passing arguments natively from the terminal shell, accompanied by rich feedback mechanics (e.g., Progress Bars).
**Trade-offs:** Abstracts away the direct invocation. The entrypoint becomes heavily bound to the CLI framework's decorators, removing "vanilla" entry properties.

---

## Technical Objective
Wrap the entire `PipelineOrchestrator` in a formal CLI application. The user must be able to invoke the script passing the `--input_file` path, defining an `--output_format` flag, and receiving dynamic visual feedback concerning processing states straight onto the console.

---

## Required Testing (TDD / QA)
List the unit tests or edge cases that MUST be covered by `pytest` (or equivalent) for this mission to be accepted.
- [ ] Test Case 1: CLI invocation strictly raises a User-Friendly error if `--input_file` points to a nonexistent path, bypassing Python's native ugly internal Tracebacks.
- [ ] Test Case 2: Typer/Click validates that `--output_format` choices are rigidly constrained merely to `['json', 'csv']`.
- [ ] Test Case 3: Utilizing the `CliRunner` module from the chosen framework correctly returns exit status `0` upon a flawless pipeline execution sequence.

---

## Execution Steps (Implementation Plan)
1. Install `typer` (alongside `rich`) or `click`.
2. Construct the single entry point `cli.py`. Wrap the `run()` method in the CLI command properties defining `input`, `output`, and `verbose` arguments.
3. Replace passive print statements inside the execution flow with Framework-specific progress bars measuring parsing iteration loads.
4. Prepare a production-grade `README.md` containing commands and instructions for terminal invocation explicitly directed at the End-User.

---

## Completion Criteria & Definition of Done (DoD)
- [ ] The app responds effectively to native flags like `python cli.py --help` printing documented arguments properly.
- [ ] A dedicated `README_PROJECT.md` exists detailing how to install the tool globally and invoke it.
- [ ] **English Friendly:** Naming (commands, arguments, classes) MUST remain in professional English. CLI `--help` messages and terminal output should be in English. Documentation (docstrings, comments) can be Hybrid-English or simplified English.
- [ ] SOLID: The CLI module holds absolutely NO business logic. It merely acts as a switchboard collecting variables and passing them into the `PipelineOrchestrator`.

---

## Architectural/Friction Notes
*Log any code smells, friction discovered, or future scaling ideas to be picked up by the Architect role.*

[2026-04-29] B01 descartada. Causa: inestabilidad del provider DeepSeek v4-flash
(generó código sin pedirlo — violación de Regla 3). Misión no completada por el
Operador. Se cierra PY-POO v4 y se relanza como beta del sistema v5.
