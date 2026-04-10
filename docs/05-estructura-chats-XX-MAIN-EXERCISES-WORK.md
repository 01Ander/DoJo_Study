# 05 - Estructura Chats (XX-MAIN / EXERCISES / WORK)

La triada de chats con IA (ChatGPT u otros LLMs) actúa como tu equipo de Ingeniería e Instructores, delimitando estrictamente sus funciones para mantener el código limpio y el esfuerzo cognitivo enfocado.

---

## English-Only Interfaces
Actualmente, los chats **EXERCISES** y **WORK** deben operarse predominantemente en inglés. Esto entrena la traducción cognitiva y simula interacciones en equipos remotos internacionales.

---

## 1. XX-MAIN — Adquisición Conceptual Profunda

**Rol:** 
- Explicar teoría arquitectónica (ej. "What is Dependency Injection in OOP?").
- Este chat **PUEDE ser bilingüe**. Si un concepto es demasiado denso, puedes recurrir al español para solidificar el conocimiento base.
- **Tiene libertad** para dar ejemplos de código y guías paso a paso si el Operador necesita aprender la teoría desde cero.

## 2. XX-EXERCISES — El "Product Manager" Técnico

**Rol:** 
- Asignarte la estructura de las misiones (M, S, B).
- Define los Acceptance Criteria (DoD) y los casos borde que debes testear.
- Todo requerimiento debe generar un output en inglés (para pegarlo en tus `mission-template.md`).

## 3. XX-WORK — Pair Programming y Code Review

**Rol:** 
- Revisión de Arquitectura: Debe leer tu `Mini-RFC` y ser un crítico implacable sobre patrones SOLID o Clean Code.
- Acompañamiento en el red-green-refactor de TDD bajo el **MÉTODO SOCRÁTICO**. Tiene prohibido dar código directo; debe obligar al Operador a razonar.
- Valida el Contexto de Negocio (ROI) antes de aprobar un bloque técnico.
- *Chat Oficial para invocar la "Degradación Transitoria" en caso de fatiga extrema durante un Deep Work.*

---

**Flujo Diario (The Daily Grind):**
1. *English Commando* (30m) para prender motores.
2. Extraer requerimientos en **EXERCISES** (10m).
3. Escribir Mini-RFC y TDD; si hay fricción de diseño, rebotar en **WORK**.
4. Programar en solitario.
5. Review final con **WORK** antes del *commit*.
