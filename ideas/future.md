# 🚀 Futuro de DoJo (Roadmap V5+)

Este documento recopila propuestas arquitectónicas, patrones de diseño y protocolos a nivel de meta-framework, ordenados por nivel de prioridad para su futura implementación en el entorno de Hermes Agent.

---

## 🔴 PRIORIDAD ALTA: Sostenibilidad Cognitiva y Fricción

### 1. Protocolo de Expansión ("Fire-and-Forget")
**El Problema:** Durante días de Operador (Deep Work puro) o en *Rest Days* (desconexión total), la mente a menudo genera ráfagas de creatividad o mejoras para el sistema mismo. Esto tienta a entrar en "Modo Expansión", arruinando el foco en la misión activa o saboteando el descanso necesario.

**La Solución (Implementación Propuesta):**
- **Captura sin Fricción (En Terminal):** Un comando específico (ej. `/dojo-idea "usar Docker para B01"`) que actúe como un dump de memoria rápido. El Agente guarda la línea y responde con un acuse de recibo breve.
- **Captura Fuera de la Terminal (Mobile/Offline):** Para ráfagas creativas mientras estás lejos del computador (caminando, en un Rest Day total). Se debe establecer un "Inbox Externo" de cero fricción (ej. un chat contigo mismo en WhatsApp/Telegram, Google Keep o un atajo de iOS). Durante tu ventana oficial de Arquitecto, el agente simplemente digiere todo ese *dump* externo de golpe para unificarlo, evitando que prendas la computadora en tu día de descanso solo para anotar una idea.
- **Bloqueo de Debate:** El sistema (especialmente las personalidades `dojo-tutor` y `dojo-reviewer`) tendrá **PROHIBIDO** desarrollar la idea, hacer preguntas al respecto o debatirlo si se lanza durante una misión activa. Responderá: *"Idea registrada. Volvamos a los Criterios de Aceptación"*.
- **Ventanas Oficiales de Expansión:** El *backlog* con todas las ideas capturadas (interiores y exteriores) queda congelado hasta la sesión pre-agendada de "Arquitecto" (ej. Sábado). Allí `dojo-architect` asimila las notas y comienza la discusión estratégica.

### 2. Conciencia Temporal (Chronobiological Awareness)
Dotar al "Supervisor" de contexto cronológico real (leyendo el reloj del SO) para hacer cumplir el **Modelo Binario de Rendimiento**:
- **Rest Day Enforcement:** Un sistema que, al inicializarse en sábado o domingo, lance una alerta ineludible al iniciar modo `WORK`/`MAIN`: *"Hoy es día de recarga. El DoJo está cerrado para blindar tu empleabilidad a largo plazo"*. Bloqueando idealmente la ejecución.
- **Burnout Alerts:** Scripts en background que midan el "Session Time" de la misión activa. Si el bucle interactivo cruza los 90 minutos ininterrumpidos: *"Friction Threshold rebasado. Llevas 90m de Deep Work. Ejecuta `/dojo-log` y sepárate de la terminal inmediatamente."*

---

## 🟡 PRIORIDAD MEDIA: Arquitectura Autonómica Avanzada

### 3. El Patrón de Auto-Arbitraje (Self-Arbitration Pattern)
Implementar un Motor de Estado (Supervisor) que no actúe solo bajo demanda (prompt), sino que mantenga la coherencia en segundo plano:
- **Inspección Pasiva:** Leer silenciosamente `journal.md`, `requirements.md` y commits.
- **Análisis de Discrepancia:** Evaluar qué se ha hecho contra el manifiesto y el DoD (Definition of Done) para saber el status real de la misión.
- **Tool Use/Function Calling:** El salto definitivo hacia la autonomía. Enseñar al LLM a detonar funciones (ej. `update_mission_status(to="EJECUCION")`) en lugar de depender únicamente de logs narrativos.

### 4. Mutación Controlada (Controlled Mutation)
Si le damos al Scribe/Supervisor el poder de modificar cosas automáticamente basándose en sus auditorías, necesitamos contenedores herméticos para que no arrase con los archivos de sistema:
- **Schema Enforcement:** El agente debe validar esquemas rígidos (ej. la estructura de los Criterios de Aceptación) antes de tocar archivos de misiones.
- **Separación de Contextos (The 3 Buckets):**
  1. *System State:* Ej. `.hermes.md`. Solo lectura. Intocable para sub-agentes automatizados.
  2. *Operational Artifacts:* Ej. Código y Misiones. Área verde para que el Operador mutable escriba, auditado por el Agente.
  3. *Bitácoras:* Área verde para que el Agente y el Usuario añadan datos, pero nunca sobreescribiendo historia pasada.

### 5. Unificación Total del "Brain Dump" (Centralized Ideation)
Como extensión natural del protocolo de expansión, la idea es eliminar documentos fragmentados (como el viejo `ideas-in-live.md`) y que el bot actúe como un canalizador universal. 
Ya sea que la idea venga de `/dojo-idea` en la terminal o copiada de tus notas de Telegram del Rest Day, el agente procesa la intención cruda, la categoriza (Arquitectura, Tooling, Flujo) y autogenera una sola *Single Source of Truth* para el futuro. El desarrollador deja de preocuparse por "dónde" anotar y pasa a delegarle la estructuración de su propio Roadmap al Arquitecto.

### 6. Ecosistema de Skills y Auditoría de Integración
**El Problema:** Hermes Agent soporta *Skills* (herramientas ejecutables), pero aún dependes de tu propio reconocimiento manual para saber qué parte de tu flujo de trabajo repetitivo debería convertirse en una.
**La Solución:**
- **Descubrimiento Activo:** Implementar una heurística/auditoría donde el Architect analice tus bitácoras pasadas para identificar cuellos de botella ("*Noto que pasas mucho tiempo copiando y pegando salidas de pytest*").
- **Catálogo de Uso:** Diseñar un pipeline donde el sistema te proponga directamente qué *Skills* deberías construir para el repositorio (Ej. un `/dojo-test-runner` que ejecute la suite de pytest y alimente los errores automáticamente, o un `/dojo-refactor` automatizado).
- **Justificación de ROI:** Cada propuesta de Skill deberá venir acompañada de su justificación (cuánto tiempo salvará al Operador).