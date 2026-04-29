## ⏳ Pendiente (Features Futuras)
- **[INBOX | 2026-04-29] ENG-IMMERSION — Inglés como Campaign Intercalada:** Modelo de interleaving estructurado donde campaigns de inglés (2-3 semanas) se intercalan entre campaigns técnicas, con arquitectura v5.0 completa (lore, quests, boss, grimoire). Ver documento completo: [`ideas/eng-immersion-campaign.md`](eng-immersion-campaign.md).
- **[INBOX | 2026-04-28] Feature para el Agente (Sugerencia de Próxima Misión):** Agregar un vector o un log de rápido acceso al final de una misión donde se tengan enlistadas las misiones y su estatus, para que el LLM pueda rápidamente sugerir el siguiente paso sin tener que leer completamente todo el repositorio.
- Feature para el Agente (Refactorización): Automatizar la recarga de personalidad en Hermes. Actualmente al usar `/dojo-start` para reanudar, el LLM asume el rol leyendo `.dojo-session.json` y le debe recordar manualmente al Operador ejecutar `/personality {role}` para inyectar el archivo de sistema. Evaluar hook, ejecución de macro desde el LLM, o mecanismo nativo en Hermes para hacer este cambio de System Prompt 100% transparente sin intervención.
- **Feature para el Agente: Skill `/dojo-test` (Verificador TDD On-Demand)** — Reemplazar la idea de un *watchdog* constante (que quema tokens y genera bucles de fondo) por una skill explícita a demanda. Cuando el Operador ejecuta `/dojo-test`, el agente lee el código del test, cruza con el `requirements.md`, ejecuta el test vía terminal local, y *solo si aprueba*, modifica retroactivamente los metadatos en el markdown para tildar la caja `[x]` correspondiente. Cero monitoreo en vivo, 100% control discrecional.
- **Feature para el Agente (15-abril): Integración WakaTime API standalone** — Al ejecutar `/stop_sesion` o al cierre de misión (`/dojo-done`), el agente consulta automáticamente la API de WakaTime (`GET /api/v1/users/current/summaries?start=HOY&end=HOY`) usando la API key de `~/.wakatime.cfg`, extrae el tiempo de coding/testing/docs del proyecto activo, y lo inyecta formateado en la entrada del journal. Elimina la necesidad de reportar manualmente "Wakatime: 52 min coding, 6 min writing tests". **Requisito:** API key ya existe en `~/.wakatime.cfg`. Usar autenticación Basic Auth (base64 de la api_key).

- **[INBOX | 2026-04-21] Feature para el Agente:** Verificar si el LLM o Hermes a veces pierden los underscores (`_`) en las respuestas renderizadas. Bug menor inconsistente — en ciertos puntos los dunders o variables con `_` privado aparecen sin los guiones bajos.
- **[INBOX | 2026-04-20] Feature para el Agente:** Banner de confirmación explícito al final de skills con side effects (`/dojo-done`, `/stop-sesion`). Debe mostrar qué archivos se modificaron para que el Operador sepa que la skill se ejecutó formalmente y no solo fue "simulada" por el LLM. Ejemplo: `[Sistema] ✅ Skill /dojo-done completada. Archivos: requirements.md (Status → ✅), journal.md (cierre), .dojo-session.json (eliminado)`.
- **[INBOX | 2026-04-21] Protocolo de Bloques de 90 Minutos (Context Reset Strategy):** Formalizar como `docs/10-protocolo-bloques-90.md` la estrategia de sesión óptima derivada del análisis de costos de M00. Incluye: estructura de sesión `[Bloque 90 min] → /stop-sesion + descanso 10 min → /dojo-start → [Bloque 90 min]`, regla de decisión de pausas (< 20 min: no resetear, 20 min–2h: resetear, overnight: siempre resetear), datos calibrados de ahorro (~$0.39/bloque, ~$0.32/sesión), y la regla de una misión por día. Requiere actualizar `00-index.md`, `03-sistema-energia.md`, `09-guia-operaciones-v4.md` y `.hermes.md` para referenciar el nuevo protocolo. Fuente: análisis en Claude del CSV `openrouter_activity_2026-04-21.csv`.
- **[INBOX | 2026-04-27] Bug de Parseo Hermes (Errno 63):** Verificar el uso de mensajes largos en skills de chat como `/dojo-done` y `/dojo-log`. La actualización reciente de Hermes evalúa los mensajes como rutas de archivo usando `os.path.exists()` antes de procesarlos. Si el mensaje supera los 255 caracteres, provoca un crash en Mac (`[Errno 63] File name too long`). *Acción pendiente:* Arreglar temporalmente hardcodeando los journals largos, y evaluar otras soluciones técnicas (ej. salto de línea obligatorio). Adicionalmente, evaluar estrategias para economizar el consumo excesivo de tokens que ocurre al invocar el cierre de las skills con logs largos.
- **[INBOX | 2026-04-27] Memoria Contextual y Adaptabilidad (Journals):** Buscar la manera de extraer y mantener el contexto emocional/cognitivo de los journals anteriores (o de las métricas de fricción) para que el sistema module automáticamente su comportamiento. *Ejemplo:* En la sesión M03 hubo un bloqueo de 3 días por fricción nivel 7. Al retomar y explicar esto explícitamente, el sistema adoptó una postura complementaria (Tutor compasivo, dando el código directo sin exigir para no sumar frustración). Si el sistema pudiera leer y entender este estado del `journal.md` automáticamente al inicio de la sesión, podría adaptar su nivel de andamiaje (scaffolding) de forma proactiva, sin requerir intervención explícita del operador.

## ✅ Resuelto en v4.3.0 (2026-04-27)
- ~~Alucinación de siguientes misiones en `/dojo-done`~~ → `list_dir` obligatorio + directiva "NO inventes misiones"
- ~~Reforzar Directiva TDD para modelos ligeros~~ → Bloque `⚠️ REGLA TDD OBLIGATORIA` en `/dojo-start` paso 4
- ~~Evaluación de Arquitectura Misiones vs Código Centralizado~~ → Campaign Type CUMULATIVE/ADDITIVE
- ~~Optimización de Búsqueda en `/dojo-start`~~ → Paso 1.5 detecta Campaign Type, rutas directas
- ~~Auditoría y Limpieza de Skills (parcial)~~ → Silos eliminados. Pendiente: validar `socratic-review`

## 🔍 Evaluación Pendiente
- **Rol dual del Tutor en temas nuevos (14-abril):** Tutor asume review light en temas nuevos. Es CORRECTO — cambiar personalidad cada 5 min rompe el flujo. Reviewer separado aplica cuando los conceptos YA están comprendidos. **Estado: Funciona por default, formalizar si se vuelve inconsistente.**

## 🏗️ Diseño: Protocolo de Fase 1 — Andamiaje Activo (14-abril)

### Concepto
No es tutorial hell. Es **aprendizaje situado**: el problema llega primero, la teoría llega convocada por el problema. El Tutor actúa como senior que construye junto al Operador, no como un video de YouTube.

### Flujo de Fase 1 (Tutor con Scaffolding)
1. Operador describe la lógica que necesita ("necesito agrupar por categoría y sumar")
2. Tutor da código funcional con Domain Shifting + explicación línea por línea
3. Operador reescribe el código EN SU ARCHIVO (no copy-paste ciego)
4. ⚡ PAUSA OBLIGATORIA: Tutor ESPERA los comentarios del Operador
   → "¿Qué entiendes que hace cada línea?"
   → "¿Qué parte no te queda clara?"
5. Operador responde con su análisis del código
6. Tutor valida la comprensión o corrige malentendidos
7. Si Tutor confirma comprensión → Concepto marcado como "exposed" en Skills Tracker

### Flujo de Fase 2 (Reviewer Estricto)
1. Operador implementa SOLO, usando conceptos de Fase 1
2. Reviewer hace preguntas socráticas, NO da código
3. Si el Operador resuelve sin ayuda → Concepto pasa a "practicing"
4. Si lo usa correctamente en otro contexto → Concepto pasa a "assimilated"

### Skills Tracker — Ciclo de Vida de un Concepto
unseen → exposed → practicing → assimilated
  │         │          │            │
  │     Fase 1:     Fase 2:     Se usó sin
  │     Tutor dio   Operador    ayuda en otro
  │     código,     lo usó      contexto o
  │     Operador    solo con    misión
  │     lo analizó  Reviewer
  │     y explicó
  │
  Sin contacto previo

### Mecanismo de Transición (Fase 1 → Fase 2)
**¿Cuándo se retira el andamiaje para un concepto específico?**
- Cuando el Operador puede **explicar** el código sin mirarlo (validado por Tutor en paso 6)
- Cuando el Skills Tracker muestra `exposed` para TODOS los conceptos de un bloque funcional
- El Reviewer es la prueba: si el Operador necesita que le den código de vuelta, el concepto vuelve a Fase 1

### Conexión con Protocol Yellow
- **Dificultad Deseable (Bjork):** La fricción con pytest y type hints es señal POSITIVA. No eliminar la incomodidad, preservarla.
- **Zona de Desarrollo Próximo (Vygotsky):** Si Tutor da código que el Operador no puede procesar → fuera de zona. Si da código que ya domina → también fuera. El calibrado es el arte.

### Estado: DISEÑO. Pendiente formalización en v4.5 como `docs/11-fases-aprendizaje.md`.
