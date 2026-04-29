# Journal - S01_testing

## Bitácora Cronológica
\n- **[Sistema | 2026-04-28 12:10 — Inicio de sesión]:** Misión S01 de la campaña PY-POO-FINANCE fijada como activa.

- **[User | 2026-04-28 12:10]:** S01 Done. Waka: Coding 9m, Test 1h8m, docs 5m.

- **[Tutor | 2026-04-28 12:10]:** Sesión muy productiva. El Operador demostró comprensión sólida de cobertura de código (coverage), tests E2E vs unitarios, y la diferencia entre validación de tipos en constructor vs errores en tiempo de ejecución. Destacó en la escritura del test E2E con `tmp_path`, validando tanto el valor de retorno como la escritura física del JSON. Tuvo un momento clave de aprendizaje al identificar que `CSVExtractor()` sin argumentos pasaba el test por razones equivocadas — logró corregirlo y entender por qué las líneas 12/14 de pipeline.py seguían sin cubrirse. La asimilación del patrón `.coveragerc` y exclusión de líneas no vitales fue correcta. Área de atención futura: al cerrar la brecha de renderizado de Markdown (`_` y `*` en comandos).

- **[User | 2026-04-28 12:10]:** S01 terminada. Cambio de LLM a Deepseekv4-flash. Gasto de la sesion: $0.24, 2.3M Tokens. Modelo supremamente economico, alineado a la perfeccion con dojo y sus reglas, no se persivieron alucinaciones, buenas explicaciones y claro. Unico punto negativo, muy baja produccion de tokens de salida, demoras de 4-5 minutos en rasonamiento y salida de prompt. Es una desventaja que se puede soportar a la larga por la economia de tokens. En cuanto a la mision. Buena consolidacion de conceptos de test. Muchisimo mejor haber trabajado todo desde el mismo directorio. La friccion bajo increiblemente y se percato internamente que se esta asimilando un poco mas facil los test, sin embargo aun se necesita guia para saber que se pide. Sesion de 1h40m salida un poco de los 90min pero se compensa por las demoras en las respuestas del LLM. Se observo que al trabajar con misiones de cierta manera separada, se fracciono igualmente la logica que se entendia, por eso no se comprendia porque CSVExtractor necesitaba un paramentro interno, hasta ir a ver el codigo y entender por que se hizo asi. Demuestra quizas un poco de desconexion con lo que se habia hecho. Quizas se requiera trabajar eso internamente para estas cumulative campaigns. Se remotaman las buenas sensaciones del incio de la campaing.
---

- **[Sistema | 2026-04-28 12:10 — MISIÓN S01 COMPLETADA]:**
  - **Tests finales:** 22 passed, 0 failed (19 previos + 3 nuevos de validación de tipos en constructor)
  - **Cobertura:** 100% en `src/` (101 statements, 0 missed)
  - **DoD:** Completo — E2E test, failure test, .coveragerc, tests/integration/
  - **Archivos nuevos:** tests/integration/test_pipeline_e2e.py, .coveragerc
  - **WakaTime:** Coding 9m, Test 1h8m, docs 5m (Total: 1h22m)
