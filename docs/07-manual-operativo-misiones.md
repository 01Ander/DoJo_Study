# 07 - Manual Operativo Misiones

Este manual es tu estándar operativo cuando entras al bloque de **Deep Work**. Su estricto cumplimiento garantiza calidad de software, trazabilidad profesional, y fluidez en tu Inmersión Lingüística (Inglés).

---

## 1. Reglas Sagradas de Operación

1. **English-Only Zone:** Dentro de tu IDE, consola, y documentación técnica, el español no existe. Variables, Commits, Readmes y logs se escriben obligatoriamente en inglés.
2. **Code Comes Last (Architecture First):** Prohibido abrir archivos de código `.py` sin antes haber llenado la sección de `Mini-RFC` en tu plantilla de misión y definido el diseño lógico.
3. **Test-Driven:** Prohibido escribir la lógica de negocio sin que primero falle su prueba unitaria en `pytest` (Red-Green-Refactor).

---

## 2. Flujo Completo del Operador (Deep Work Loop)

Un bloque típico de Deep Work de 90 minutos se debe ver así:

### Fase A: Onboarding y Diseño (20 mins)
1. Has completado el "English Commando" (Busuu/Leyendo). Tu cerebro está en modo técnico.
2. Vas a tu carpeta de campaña (`subjects/python/campaigns/.../missions`) y creas/abres el archivo de la misión (ej. `M01.md`).
3. **Business Value Check (ROI):** Antes de la arquitectura, define en una oración el problema de negocio y el impacto esperado (ROI). **"No Business Context = No Code"**.
4. **Drafting the Mini-RFC:** Escribes un párrafo documentando la arquitectura. ¿Usarás una Abstract Base Class? ¿Inyectarás dependencias?
5. Defines explícitamente cuáles son los Tests que deberán pasar y el **Social DoD** (README legible para HR/PMs) si es una misión Boss.

### Fase B: TDD (Test-Driven Development) (30 mins)
1. Abres VS Code. Creas tu archivo `test_module.py`.
2. Escribes los Unit Tests básicos basados en tu Mini-RFC.
3. Ejecutas `pytest`. Los tests **deben fallar** (porque aún no has escrito el código real).

### Fase C: Ejecución y Refactor (40 mins)
1. Vas al archivo madre (ej. `extractor.py`). Escribes la lógica mínima para que el test pase.
2. Ejecutas `pytest`. Si está en verde (Green), refactorizas el código para hacerlo más legible o aplicar tipado fuerte (`typing`).
3. Escribes los Docstrings y comentarios clarificadores (todo en Inglés).

### Fase D: Commit y Cierre
1. Emites un git commit semántico: `feat: add abstract extractor interface`.
2. Vas a tu `daily-log-template.md` y marcas tu bloque de **Deep Work** completado. Reportas fricciones si las hubo.

---

## 3. ¿Qué hacer en un Estancamiento ("Muro Técnico")?

Estar en inmersión no significa sufrir horas seguidas un TypeError de Python o mirar una pantalla en blanco sin saber cómo empezar.

### A. Estancamiento Teórico (Antes de codear)
Si intentas redactar tu Mini-RFC (Fase A) y te das cuenta de que no dominas la teoría necesaria para proponer una solución:
- **Detén el Deep Work** inmediatamente. Tu objetivo pasa de "Terminar la Misión" a "Cerrar la Brecha Teórica".
- **Invoca al Instructor:** Cambia el chat a `/mode main` y pídele que te explique el patrón, te dé ejemplos agnósticos o pseudocódigo. No intentes programar (ni usar `/mode work`) hasta que la teoría esté clara.

### B. Estancamiento Práctico (Codiando)
Si llevas 25 minutos trabado en el mismo error de código y tu Friction Level sube a 7 o más:
- Invoca el **[Protocolo Yellow](../docs/08-protocol-yellow.md)**: Utiliza sus palancas (De-abstracción, Mocking, Español) para aislar la lógica o bajar la carga cognitiva. Usa `/mode work` para pedir pistas Socráticas.
- Si esto no funciona o la frustración continúa, asume un **Rest Day** inminente y sal de la pantalla. El cerebro reestructurará el problema mientras descansas.
