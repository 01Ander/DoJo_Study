# 🏗️ Sesión Architect — 18 Abril 2026 (DoJo v4.2)

> **Contexto para el Agente:** Este documento fue preparado por Opus 4.6 como blueprint detallado para una sesión de Arquitecto. Contiene las tareas a ejecutar, en orden de prioridad, con rutas exactas, templates y criterios de verificación. Ejecuta cada tarea secuencialmente y marca el checkbox cuando esté completa.

> **Versión objetivo:** DoJo Study v4.2 — "The On-Demand Automation Update"

---

## Tareas a ejecutar (Sesión 1 — Quick Wins)

- [ ] **Tarea 1:** Crear skill `/dojo-idea` (buzón Fire-and-Forget)
- [ ] **Tarea 2:** Crear template estructurado de Mini-RFC
- [ ] **Tarea 3:** Protocolo de Triaje en guía de operaciones
- [ ] **Tarea 4:** Bidireccionalidad de Meta-Documentos en `/dojo-start`
- [ ] **Tarea 5:** Estandarización de `/dojo-log` (template + WakaTime)

---

## Pre-requisitos antes de empezar

1. Leer `.hermes.md` en `~/Documents/DoJo/DoJo_Study/.hermes.md` — es la Constitución del sistema.
2. Leer `guia-operaciones-v4.md` en `~/Documents/DoJo/DoJo_Study/docs/guia-operaciones-v4.md` — explica el flujo operativo.
3. Tener claro que los skills se guardan en: `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/`
4. Cada skill es una **carpeta** con un archivo `SKILL.md` dentro.
5. Las templates se guardan en: `~/Documents/DoJo/DoJo_Study/templates/`

### Archivos de referencia (skills existentes que sirven como template de formato)

Estudiar estos dos archivos ANTES de crear cualquier skill nuevo:

- **session-start:** `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-start/SKILL.md`
- **journal-log:** `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/journal-log/SKILL.md`

Ambos siguen el mismo formato YAML frontmatter + Markdown. Los nuevos skills deben seguir la MISMA estructura.

---

## Tarea 1: Crear skill `/dojo-idea` (Buzón Fire-and-Forget)

### Qué es y por qué
Durante las sesiones de deep work, el Operador tiene ráfagas de ideas sobre el sistema o features futuras. Actualmente, abrir `ideas-in-live.md` y editarlo manualmente **rompe la inmersión** y genera fuga de contexto. Este skill permite vaciar la idea en un solo comando sin salir del flujo.

### Ruta del nuevo skill
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/idea-capture/SKILL.md
```

> **NOTA:** La carpeta `idea-capture` NO existe. Crearla.

### Contenido exacto de `idea-capture/SKILL.md`

```markdown
---
name: dojo-idea
description: Captura rápida de ideas y features sin romper la inmersión del deep work
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, ideas, capture, fire-and-forget]
    category: dojo
    requires_toolsets: [file]
---

# DoJo Idea Capture (Fire-and-Forget)

## When to Use
Cuando el Operador tiene una idea, feature request, o reflexión sobre el sistema DoJo durante una sesión de deep work y quiere registrarla SIN romper su flujo de estudio.

## Usage
```
/dojo-idea [descripción de la idea]
```
Ejemplo: `/dojo-idea Crear un dashboard web que muestre el skills tracker con niveles unseen/exposed/practicing/assimilated`

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Capturar la idea.** El texto después de `/dojo-idea` es el contenido completo. No pidas aclaraciones ni hagas preguntas — este skill es atómico y no-interactivo.

2. **Clasificar automáticamente** el tipo de idea basándote en palabras clave:
   - Si menciona "agente", "skill", "hermes", "comando" → `Feature para el Agente`
   - Si menciona "sistema", "docs", "guía", "protocolo" → `Feature para el Sistema`
   - Si menciona "template", "plantilla" → `Feature para Templates`
   - Si no se puede clasificar → `Idea General`

3. **Escribir en `ideas-in-live.md`** usando `write_file` (append) al final de la sección `## ⏳ Pendiente (Features Futuras)`:
   
   Ruta: `~/Documents/DoJo/DoJo_Study/ideas/ideas-in-live.md`
   
   Formato de la nueva línea:
   ```
   - **[INBOX | YYYY-MM-DD] {Clasificación}:** {texto de la idea del Operador}
   ```

4. **Confirmar al Operador** con un mensaje mínimo (no verboso):
   ```
   [Sistema] 💡 Idea registrada en ideas-in-live.md
   ```
   **NO** hagas seguimiento, NO preguntes "¿quieres ampliar?", NO ofrezcas desarrollar la idea. El Operador debe volver inmediatamente a su deep work.

## Pitfalls
- **Este skill es ATÓMICO.** Un comando, una acción, un mensaje de confirmación. Nada más.
- Requiere que el Operador pase el texto de la idea como argumento. Si ejecuta `/dojo-idea` sin texto, pedir: `[Sistema] Uso: /dojo-idea [tu idea aquí]`
- **NO ejecutes scripts Python ni búsquedas globales.**
- La idea se inserta al final de la sección "Pendiente", ANTES de la sección "🔍 Evaluación Pendiente".
- Si `ideas-in-live.md` no existe, crearlo con la sección header.

## Verification
- `ideas-in-live.md` contiene la nueva entrada con prefijo `[INBOX | fecha]`
- El agente NO hizo preguntas de seguimiento
- El Operador puede continuar trabajando inmediatamente
```

### Verificación de Tarea 1
- [ ] Existe `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/idea-capture/SKILL.md`
- [ ] El archivo tiene frontmatter YAML válido con `name: dojo-idea`
- [ ] El procedure escribe al archivo `ideas-in-live.md` existente
- [ ] El skill es explícitamente atómico (no-interactivo)

---

## Tarea 2: Crear template estructurado de Mini-RFC

### Qué es y por qué
La skill `/mini-rfc` ya existe y referencia `templates/mini-rfc-template.md`, pero **ese archivo NO existe**. El template de misión (`mission-template.md`) tiene una sección de Mini-RFC pero es solo un skeleton con placeholders. El Operador enfrenta la "página en blanco" cada vez que debe diseñar una misión. Este template con preguntas guía y estructura predefinida elimina esa fricción.

### Ruta del nuevo archivo
```
~/Documents/DoJo/DoJo_Study/templates/mini-rfc-template.md
```

> **NOTA:** Este archivo NO existe. Crearlo.

### Contenido exacto de `mini-rfc-template.md`

```markdown
# Mini-RFC: [Título del Módulo / Feature]

> **Instrucción:** Completa cada sección respondiendo las preguntas guía. No elimines las preguntas — respóndelas debajo. El Reviewer validará este documento antes de dar luz verde para codear.

---

## 1. Business Context (¿Por qué existe esto?)

**¿Qué problema del mundo real resuelve este código?**
> [Tu respuesta aquí]

**¿Quién se beneficia y cómo lo usaría?**
> [Tu respuesta aquí]

**ROI estimado** (ej: "Elimina X horas semanales de trabajo manual", "Reduce errores de Y tipo en Z%"):
> [Tu respuesta aquí]

---

## 2. Technical Scope (¿Qué hace exactamente?)

**Input:** ¿Qué recibe? (formato de archivo, tipo de datos, fuente)
> [Tu respuesta aquí]

**Output:** ¿Qué produce? (formato, destino, estructura)
> [Tu respuesta aquí]

**Funciones principales** (máximo 8 — si necesitas más, el scope es demasiado grande):

| # | Función | Responsabilidad (1 oración) | Input → Output |
|---|---------|----------------------------|----------------|
| 1 | `nombre_funcion()` | | → |
| 2 | | | → |
| 3 | | | → |

---

## 3. Architecture Decision (¿Cómo y por qué así?)

**Patrón elegido** (ej: Pipeline secuencial, Event-driven, Repository, etc.):
> [Tu respuesta aquí]

**¿Por qué este patrón y NO otro?** (Trade-offs explícitos):
> [Tu respuesta aquí]

**Diagrama de flujo de datos** (ASCII o descripción textual):
```
[Input] → [Paso 1] → [Paso 2] → [Output]
                ↓ (error)
          [Error Handler]
```

**Dependencias** (solo stdlib permitida en PY-BASICO):
> [Listar módulos: csv, json, datetime, collections, etc.]

---

## 4. Edge Cases & Error Strategy

**¿Qué puede salir mal?** Lista al menos 3 escenarios:

| # | Escenario | Estrategia |
|---|-----------|------------|
| 1 | | |
| 2 | | |
| 3 | | |

**Política de errores:** ¿Fallar rápido (raise) o fallar suave (log + continuar)?
> [Tu respuesta aquí]

---

## 5. Testing Strategy (TDD-First)

**¿Qué test escribo PRIMERO?** (el más simple que demuestre que la función core funciona):
> [Tu respuesta aquí]

**Tests mínimos requeridos** (al menos 3):

| # | Test | Qué valida | Tipo |
|---|------|-----------|------|
| 1 | `test_nombre()` | | Happy path |
| 2 | `test_nombre()` | | Edge case |
| 3 | `test_nombre()` | | Error handling |

---

## 6. Checklist de Aprobación (para el Reviewer)

- [ ] Business Context está definido y es concreto (no genérico)
- [ ] Funciones ≤ 8 y cada una tiene una sola responsabilidad
- [ ] Trade-offs están explicitados (no solo "es mejor así")
- [ ] Al menos 3 edge cases identificados con estrategia
- [ ] Test #1 definido (se puede escribir AHORA sin más diseño)
- [ ] Zero third-party libs (si aplica por campaña)

> **Reviewer:** Si todas las cajas están marcadas → 🟢 Luz verde para TDD.
> Si falta alguna → 🔴 Devolver al Operador con preguntas específicas.
```

### Actualizar el skill `/mini-rfc` existente

#### Archivo a modificar
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/mini-rfc/SKILL.md
```

#### Cambio requerido
En la línea 30 (`Ver templates/mini-rfc-template.md para el template completo.`), el skill ya referencia este archivo. **No necesita cambios** si el archivo se crea con el nombre correcto. Solo verificar que la referencia es correcta.

### Verificación de Tarea 2
- [ ] Existe `~/Documents/DoJo/DoJo_Study/templates/mini-rfc-template.md`
- [ ] El template tiene las 6 secciones: Business Context, Technical Scope, Architecture Decision, Edge Cases, Testing Strategy, Checklist
- [ ] Cada sección tiene preguntas guía concretas (no placeholders vacíos)
- [ ] El skill `/mini-rfc` existente ya referencia este archivo correctamente (verificar)

---

## Tarea 3: Protocolo de Triaje en Guía de Operaciones

### Qué es y por qué
Durante las sesiones de B01, el Operador detectó bugs del sistema (eval_log, personality routing) que lo sacaron del deep work. No existe un protocolo formal para decidir cuándo "parchear en vivo" y cuándo "registrar y diferir". Este protocolo establece un árbol de decisión binario de 2 preguntas.

### Archivo a modificar
```
~/Documents/DoJo/DoJo_Study/docs/guia-operaciones-v4.md
```

### Cambio requerido
**Agregar una nueva sección DESPUÉS de la sección `## 🔄 Flujo típico de un día de estudio` (después de la línea 230) y ANTES de `## ❓ Troubleshooting rápido` (línea 234).** Insertar:

```markdown

---

## 🚑 Protocolo de Triaje en Vivo

> Cuando detectas un bug o carencia del sistema DoJo DURANTE una sesión de deep work, usa este árbol de decisión. **NO abras "dos frentes" de trabajo.**

```
¿El bug me BLOQUEA continuar mi misión actual?
│
├── SÍ → ¿Lo puedo parchear en < 5 minutos?
│         │
│         ├── SÍ → ⚡ Parchea en vivo. Registra con /dojo-log "Hotfix: [qué hice]"
│         │
│         └── NO → 🛑 STOP. Registra con /dojo-idea "BUG BLOQUEANTE: [descripción]"
│                   Usa workaround temporal y sigue. Agenda para próxima ventana Architect.
│
└── NO → 💡 Registra con /dojo-idea "[descripción]" y SIGUE TRABAJANDO.
          No abras el archivo. No investigues. Vuelve a tu misión.
```

### Reglas del Triaje
1. **Si no bloquea, no lo toques.** `/dojo-idea` y sigue.
2. **Si bloquea pero es complejo, busca workaround.** El workaround te desbloquea; la solución real va a la ventana Architect.
3. **Nunca dediques más de 5 minutos a un parche en vivo.** Si pasan 5 minutos y no está resuelto, aplica regla 2.
4. **Los bugs del sistema NO son tu misión.** Tu misión es aprender a codear. El sistema es infraestructura.
```

### Verificación de Tarea 3
- [ ] La sección `## 🚑 Protocolo de Triaje en Vivo` existe en `guia-operaciones-v4.md`
- [ ] El árbol de decisión tiene solo 2 preguntas binarias (sí/no)
- [ ] Referencia `/dojo-idea` como mecanismo de registro
- [ ] La sección está ubicada ANTES de Troubleshooting

---

## Tarea 4: Bidireccionalidad de Meta-Documentos en `/dojo-start`

### Qué es y por qué
Actualmente, `/dojo-done` ya actualiza `Status: ✅ Completada` en `requirements.md`. Pero `/dojo-start` NO actualiza `Status: 🟢 Ready` → `Status: 🔵 En Ejecución` al arrancar. Esto deja el meta-dato inconsistente. La corrección es agregar un paso al procedure de `session-start`.

### Archivo a modificar
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-start/SKILL.md
```

### Cambio requerido

**Agregar un paso 2.5 entre el paso 2 actual (Leer requirements.md) y el paso 3 actual (Leer journal.md).** Insertar después del paso 2:

```markdown

2.5. **Actualizar Status en `requirements.md`** (Bidireccionalidad):
   - Leer la línea que contiene `Status:` en la sección `## Identification`
   - Si el valor actual es `🟢 Ready`, cambiarlo a `🔵 En Ejecución`
   - Si ya es `🔵 En Ejecución` o `✅ Completada`, NO cambiar nada
   - Usar `write_file` para hacer la modificación. No tocar ninguna otra línea del archivo.
   - **NOTA:** Solo ejecutar este paso cuando el Operador confirma que va a trabajar en esta misión (después del paso 0 de detección de sesión pausada, si aplica).
```

### Verificación de Tarea 4
- [ ] `session-start/SKILL.md` tiene el nuevo paso 2.5
- [ ] El paso solo actúa sobre misiones con Status `🟢 Ready` (no sobrescribe misiones ya en ejecución o completadas)
- [ ] El paso modifica SOLO la línea `Status:`, nada más

---

## Tarea 5: Estandarización de `/dojo-log` (Template + WakaTime)

### Qué es y por qué
El journal-log actual (46 líneas) es minimal: no estandariza la estructura de las entradas ni registra qué modelo LLM se usó durante el bloque. Además, el Operador reporta manualmente los tiempos de WakaTime. Esta actualización fuerza un template estructurado y agrega la inyección best-effort de WakaTime.

### Archivo a modificar
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/journal-log/SKILL.md
```

### Contenido completo de reemplazo para `journal-log/SKILL.md`

**Sobrescribir** el archivo completo con:

```markdown
---
name: dojo-log
description: Registra una entrada estructurada en la bitácora (journal.md) de la misión activa
version: 2.0.0
metadata:
  hermes:
    tags: [dojo, journal, logging]
    category: dojo
    requires_toolsets: [file, terminal]
---

# DoJo Journal Log

## When to Use
Cuando el Operador quiere registrar un avance, reflexión, error o duda en la bitácora de la misión activa. Este skill también se usa internamente por `/stop-sesion` y `/dojo-done` para entradas de sistema.

## Usage
```
/dojo-log [mensaje]
```
Ejemplo: `/dojo-log Completé el primer test unitario. Descubrí que decimal.Decimal es mejor que float para finanzas.`

### Modo resumen de bloque (al pausar o cerrar)
```
/dojo-log --summary
```
Genera una entrada de resumen del bloque con métricas de WakaTime (si disponibles).

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Identificar la misión activa.** Si el usuario ya usó `/dojo-start` en esta sesión, ya sabes la campaña y misión. Si no, pregúntale.

2. **Construir la ruta del journal:**
   `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/journal.md`

3. **Determinar tipo de entrada:**

   **Si es una entrada normal** (sin `--summary`):
   
   Agregar al final de `journal.md` usando `write_file` (append). Formato:
   ```
   - **[User | YYYY-MM-DD HH:MM]:** {mensaje del usuario}
   ```

   **Si es un resumen de bloque** (con `--summary`):
   
   a. **Auto-identificar modelo LLM:** Reportar el nombre/ID del modelo que TÚ eres actualmente.
   
   b. **Intentar obtener métricas de WakaTime** (best-effort):
      - Leer la API key desde `~/.wakatime.cfg` (campo `api_key` bajo `[settings]`)
      - Si la key existe, ejecutar via `terminal`:
        ```bash
        curl -s -H "Authorization: Basic $(echo -n '{API_KEY}' | base64)" \
          "https://wakatime.com/api/v1/users/current/summaries?start=$(date +%Y-%m-%d)&end=$(date +%Y-%m-%d)" \
          | python3 -c "import sys,json; d=json.load(sys.stdin)['data'][0]; print(f\"Coding: {d['grand_total']['text']}\")"
        ```
      - Si falla (key no existe, API caída, error de red): usar `WakaTime: ⚠️ no disponible` y continuar sin bloquear.
   
   c. Agregar entrada de resumen al final de `journal.md`:
      ```
      ---
      
      ### 📊 Resumen de Bloque {N} — YYYY-MM-DD
      - **Modelo LLM:** {modelo auto-identificado}
      - **WakaTime:** {tiempo de coding | ⚠️ no disponible}
      - **Avance general:** {resumen breve del trabajo realizado durante este bloque — inferir del contexto de conversación}
      - **Siguiente paso:** {lo que indicó el Operador o inferir del estado actual}
      ```

4. **Confirmar** al Operador que la entrada fue registrada.

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- Si no hay misión activa, indica al usuario que use `/dojo-start` primero.
- **NO ejecutes scripts Python ni búsquedas globales.** Usa `write_file` directamente para el journal.
- La integración WakaTime es **best-effort**. Si falla, anota `⚠️ no disponible` y SIGUE. Nunca bloquees el log por WakaTime.
- El campo "Modelo LLM" es de **auto-identificación**: reporta tu propio modelo, no copies un ejemplo.
- Usa `terminal` solo para la llamada a WakaTime. El journal se escribe con `write_file`.

## Verification
- El archivo journal.md contiene la nueva entrada con timestamp correcto.
- Las entradas normales usan formato de una línea.
- Las entradas de resumen usan el template estructurado con separador `---`.
- Si WakaTime falló, la entrada dice `⚠️ no disponible` (no se bloqueó).
```

### Verificación de Tarea 5
- [ ] `journal-log/SKILL.md` fue actualizado a versión 2.0.0
- [ ] El skill ahora acepta modo `--summary`
- [ ] El template de resumen incluye campo de Modelo LLM (auto-identificación)
- [ ] WakaTime es best-effort con fallback graceful (`⚠️ no disponible`)
- [ ] `requires_toolsets` ahora incluye `[file, terminal]`

---

## Post-tareas: Actualizar documentación

Después de completar las 5 tareas, actualizar estos archivos:

### 1. Actualizar `.hermes.md`

En la sección **"Skills Disponibles"** (línea 83-91), agregar:

```markdown
- `/dojo-idea [idea]` — Captura rápida de ideas sin romper el deep work
```

### 2. Actualizar `guia-operaciones-v4.md`

En la sección **"⚡ Comandos rápidos (cheat sheet)"**, agregar un nuevo bloque:

```markdown
#### Capturar idea rápida (funciona con CUALQUIER personalidad):
```
/dojo-idea Automatizar la carga de datos crudos con un script CLI
```
```

En la sección **"📁 Dónde vive todo"**, agregar al árbol de skills:

```
│   ├── idea-capture/             ← /dojo-idea
```

### 3. Actualizar `CHANGELOG.md`

Agregar al inicio del archivo (antes de `## [4.1.2]`):

```markdown
## [4.2.0] - 2026-04-18

### 🏗️ "The On-Demand Automation Update"

### Added
- **Idea Capture Skill:** Created `/dojo-idea` for atomic, fire-and-forget idea registration during deep work sessions.
- **Mini-RFC Template:** Created `templates/mini-rfc-template.md` with guided questions across 6 sections (Business Context, Technical Scope, Architecture Decision, Edge Cases, Testing Strategy, Approval Checklist).
- **Triage Protocol:** Formalized a binary decision tree in `guia-operaciones-v4.md` for handling bugs detected during deep work (patch vs defer).
- **WakaTime Integration:** `/dojo-log --summary` now attempts to inject coding time from the local WakaTime API (best-effort with graceful fallback).

### Changed
- **Bidirectional Meta-Documents:** `/dojo-start` now updates mission Status from `🟢 Ready` to `🔵 En Ejecución` when starting work.
- **Journal Log v2:** Upgraded `/dojo-log` to v2.0.0 with structured summary templates, LLM model auto-identification, and `--summary` mode.

---
```

### 4. Actualizar `ideas-in-live.md`

Mover las ideas implementadas de la sección `## ⏳ Pendiente` **eliminando** las líneas correspondientes a las features que se acaban de implementar. Las líneas a eliminar son:

- La línea 2 (Protocolo de Triaje) → Implementada en Tarea 3
- La línea 4 (Actualización bidireccional) → Implementada en Tarea 4
- La línea 7 (`[PRIORITARIO] Template Mini-RFC`) → Implementada en Tarea 2
- La línea 8 (Reglas para `/dojo-log`) → Implementada en Tarea 5

**NO eliminar** las líneas 3 (Inyección personalidad), 5 (`/dojo-test`), ni 6 (WakaTime API standalone) — esas quedan para la Sesión 2 (v4.3).

---

## Verificación Final (Sesión 1)

- [ ] Tarea 1 completada: `/dojo-idea` skill existe y es válido
- [ ] Tarea 2 completada: `mini-rfc-template.md` existe con 6 secciones
- [ ] Tarea 3 completada: Protocolo de Triaje agregado a `guia-operaciones-v4.md`
- [ ] Tarea 4 completada: `/dojo-start` ahora actualiza Status a `🔵 En Ejecución`
- [ ] Tarea 5 completada: `/dojo-log` actualizado a v2.0.0 con `--summary`
- [ ] `.hermes.md` actualizada con `/dojo-idea`
- [ ] `guia-operaciones-v4.md` actualizada con cheat sheet de `/dojo-idea`
- [ ] `CHANGELOG.md` actualizado con entrada de v4.2.0
- [ ] `ideas-in-live.md` limpiado (4 ítems removidos)
- [ ] No se tocó ningún archivo de código del Operador (src/, tests/)

---

## Sesión 2 — Features Pesadas (DIFERIDA a próxima ventana Architect)

> ⚠️ **NO ejecutar en esta sesión.** Estas tareas requieren investigación previa y tienen dependencias no resueltas.

### Tarea 6 (Diferida): `/dojo-test` — Verificador TDD On-Demand
**Bloqueada por:**
1. Necesita convención de naming estricta (test function ↔ checkbox en requirements.md)
2. Requiere verificar que Hermes soporta `requires_toolsets: [file, terminal]` con acceso al .venv
3. Necesita actualizar `mission-template.md` con la convención de naming ANTES

### Tarea 7 (Diferida): Formalización Fase 1/Fase 2
**Decisión pendiente:** ¿Dónde vive la regla? Opciones:
- a) Inyectar en `.hermes.md` (riesgo: inflar la constitución >130 líneas, pérdida de adherencia del LLM)
- b) Agregar campo `phase: 1|2` a `.dojo-session.json` y que las personalidades lean ese campo
- c) Crear un skill `/dojo-phase` que controle la transición

### Tarea 8 (Diferida): Inyección Transparente de Personalidades
**Bloqueada por:** Investigar si Hermes expone API para ejecutar `/personality X` programáticamente desde una skill. Si no lo soporta, la solución es solo UX mejorado (banner más prominente al retomar sesión).
