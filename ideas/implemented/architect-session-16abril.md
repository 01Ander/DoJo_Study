# 🏗️ Sesión Architect — 16 Abril 2026

> **Contexto para el Agente:** Este documento fue preparado por Opus como blueprint detallado para una sesión de Arquitecto. Contiene las 3 tareas a ejecutar, en orden de prioridad, con rutas exactas, templates y criterios de verificación. Ejecuta cada tarea secuencialmente y marca el checkbox cuando esté completa.

---

## Tareas a ejecutar

- [ ] **Tarea 1:** Crear skill `/dojo-done` (cierre formal de misión)
- [ ] **Tarea 2:** Crear skill `/stop_sesion` (pausa de bloque de deep work)
- [ ] **Tarea 3:** Generar `requirements.md` para misión B01

---

## Pre-requisitos antes de empezar

1. Leer `.hermes.md` en `~/Documents/DoJo/DoJo_Study/.hermes.md` — es la Constitución del sistema.
2. Leer `guia-operaciones-v4.md` en `~/Documents/DoJo/DoJo_Study/docs/guia-operaciones-v4.md` — explica el flujo operativo.
3. Tener claro que los skills se guardan en: `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/`
4. Cada skill es una **carpeta** con un archivo `SKILL.md` dentro (y opcionalmente una subcarpeta `scripts/`).

### Archivos de referencia (skills existentes que sirven como template)

Estudiar estos dos archivos ANTES de crear cualquier skill nuevo:

- **session-start:** `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-start/SKILL.md`
- **journal-log:** `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/journal-log/SKILL.md`

Ambos siguen el mismo formato YAML frontmatter + Markdown. Los nuevos skills deben seguir la MISMA estructura.

---

## Tarea 1: Crear skill `/dojo-done` (Cierre formal de misión)

### Qué es y por qué
`.hermes.md` ya menciona `/dojo-done` como skill disponible (línea 86), pero **no existe la carpeta ni el SKILL.md**. Este skill cierra formalmente una misión: actualiza el status en `requirements.md`, escribe una entrada de cierre en `journal.md`, y sugiere la siguiente misión si la hay.

### Ruta del nuevo skill
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/mission-done/SKILL.md
```

> **NOTA:** La carpeta `mission-done` NO existe. Crearla. Ya existe `mission-status/` pero está vacía y es un concepto diferente.

### Contenido exacto de `mission-done/SKILL.md`

```markdown
---
name: dojo-done
description: Cierra formalmente una misión, actualiza su estado y registra la retrospectiva final
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, mission, completion]
    category: dojo
    requires_toolsets: [file]
---

# DoJo Mission Done

## When to Use
Cuando el Operador ha completado todos los Criterios de Aceptación de una misión y quiere cerrarla formalmente.

## Usage
```
/dojo-done
```
No requiere argumentos — usa la misión activa (previamente fijada con `/dojo-start`).

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio. NUNCA hagas búsquedas en `/home`, `/Users` ni en la raíz del sistema.**

1. **Verificar misión activa.** Si no hay misión fijada con `/dojo-start`, pedir al usuario que la fije primero.

2. **Leer `requirements.md`** de la misión activa y verificar el estado de los Criterios de Aceptación (DoD). Listar cuáles están marcados `[X]` y cuáles `[ ]`.

3. **Confirmar cierre con el Operador.** Mostrar un resumen:
   ```
   [Sistema] Cierre de misión: {MISIÓN}
   
   DoD completados: X/Y
   DoD pendientes: (listar si hay)
   
   ¿Confirmas el cierre? (sí/no)
   ```
   Si hay criterios pendientes, advertir pero permitir el cierre si el Operador lo confirma.

4. **Actualizar `requirements.md`:**
   - Buscar la línea `Status:` en la sección `## Identification`
   - Cambiar el valor actual (ej: `🟢 Ready` o `🔵 En Ejecución`) a `✅ Completada`
   - Usar `write_file` para hacer la modificación. No tocar ninguna otra línea del archivo.

5. **Registrar cierre en `journal.md`:**
   - Agregar una entrada con separador y formato de retrospectiva:
   ```
   ---
   
   - **[Sistema | YYYY-MM-DD HH:MM — MISIÓN {CÓDIGO} COMPLETADA]:**
     - **Tests finales:** (preguntar al Operador o leer del journal si ya está)
     - **DoD:** Completo / Parcial
     - **Nota de cierre:** (pedir al Operador un resumen breve)
   ```

6. **Limpiar archivo de sesión pausada:**
   - Si existe `~/Documents/DoJo/DoJo_Study/.dojo-session.json`, **eliminarlo**. La misión está cerrada, no hay sesión que retomar.

7. **Sugerir siguiente paso:**
   - Listar las misiones disponibles en la misma campaña (`missions/` del mismo directorio de campaña)
   - Sugerir: *"¿Quieres fijar la siguiente misión con `/dojo-start {campaña} {siguiente_misión}`?"*

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- **NO ejecutes scripts Python ni búsquedas globales.** Las rutas son conocidas y fijas.
- Solo modifica la línea `Status:` en `requirements.md`. No toques el resto del archivo.
- Si el usuario dice "no" a la confirmación, cancela el proceso.
- Siempre eliminar `.dojo-session.json` al cerrar misión para evitar sesiones fantasma.

## Verification
- `requirements.md` tiene `Status: ✅ Completada`
- `journal.md` tiene la entrada de cierre con timestamp
- `.dojo-session.json` fue eliminado (si existía)
- El agente sugiere la siguiente misión
```

### Verificación de Tarea 1
- [ ] Existe el archivo `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/mission-done/SKILL.md`
- [ ] El archivo tiene frontmatter YAML válido con `name: dojo-done`
- [ ] El procedure referencia rutas correctas dentro de `~/Documents/DoJo/DoJo_Study/`

---

## Tarea 2: Crear skill `/stop_sesion` + Modificar `/dojo-start` (Pausa y reanudación de bloques)

### Qué es y por qué
Durante B00 (15-abril), el Operador trabajó en 3 bloques de deep work y tuvo que hacer `/dojo-start` cada vez para re-fijar el contexto. 

**Restricción crítica:** El Operador SALE de Hermes y SUSPENDE el Mac entre bloques. No mantiene la terminal abierta. Esto significa que el contexto de conversación de Hermes se pierde entre bloques. Por lo tanto, el estado de la sesión debe **persistir a disco** en un archivo JSON.

### Arquitectura de la solución

```
Bloque 1:
  /dojo-start py-basico B01      → trabajo normal
  /stop_sesion                   → Escribe .dojo-session.json + entrada en journal
  (sale de Hermes, suspende Mac)

Bloque 2:
  (abre terminal, lanza hermes)
  /dojo-start                    → Detecta .dojo-session.json, ofrece retomar
  "¿Retomar sesión pausada? PY-BASICO B01, bloque 2"
  → Sí → Carga contexto automáticamente (lee requirements + journal)
  → No → Pide campaña y misión como siempre
```

### Archivo de estado: `.dojo-session.json`

**Ruta:** `~/Documents/DoJo/DoJo_Study/.dojo-session.json`

**Estructura:**
```json
{
  "campaign": "PY-BASICO",
  "mission": "B01",
  "personality": "dojo-reviewer",
  "block_number": 1,
  "paused_at": "2026-04-16T13:45:00",
  "next_step": "Escribir tests de export_report",
  "status": "paused"
}
```

- Este archivo se **CREA/ACTUALIZA** cuando se ejecuta `/stop_sesion`
- Este archivo se **LEE** cuando se ejecuta `/dojo-start` sin argumentos
- Este archivo se **ELIMINA** cuando se ejecuta `/dojo-done` (cierre de misión)

### Parte A: Crear skill `/stop_sesion`

#### Ruta del nuevo skill
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-pause/SKILL.md
```

#### Contenido exacto de `session-pause/SKILL.md`

```markdown
---
name: stop-sesion
description: Pausa el bloque de deep work actual, persiste el estado a disco y registra cierre parcial en journal
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, session, pause, deep-work]
    category: dojo
    requires_toolsets: [file]
---

# DoJo Session Pause

## When to Use
Cuando el Operador necesita pausar su bloque de deep work (ej: almuerzo, descanso, fin del día) y va a SALIR de Hermes. Al volver y ejecutar `/dojo-start`, el sistema detectará la sesión pausada y ofrecerá retomar automáticamente.

## Usage
```
/stop_sesion
```
No requiere argumentos. Opcionalmente puede incluir un mensaje con el siguiente paso:
```
/stop_sesion Voy a almorzar. Siguiente paso: escribir tests de export_report
```

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Verificar misión activa.** Si no hay misión fijada con `/dojo-start`, indicar que no hay sesión activa que pausar.

2. **Escribir archivo de estado** en `~/Documents/DoJo/DoJo_Study/.dojo-session.json`:
   ```json
   {
     "campaign": "{CAMPAÑA}",
     "mission": "{MISIÓN}",
     "personality": "{PERSONALIDAD_ACTIVA o null}",
     "block_number": {N},
     "paused_at": "{ISO_TIMESTAMP}",
     "next_step": "{MENSAJE_DEL_OPERADOR o null}",
     "status": "paused"
   }
   ```
   - Si el archivo ya existe y tiene `status: "paused"`, **incrementar** `block_number` en 1.
   - Si el archivo no existe, usar `block_number: 1`.
   - Usar `write_file` para crear/sobrescribir el archivo.

3. **Registrar pausa en `journal.md`** de la misión activa:
   ```
   - **[Sistema | YYYY-MM-DD HH:MM — Pausa de bloque {N}]:** {mensaje del operador si lo hay, o "Pausa de bloque de deep work."}
   ```

4. **Mostrar resumen al Operador:**
   ```
   [Sistema] ⏸️ Bloque {N} pausado | Campaña: {CAMPAÑA} | Misión: {MISIÓN}
   
   Hora de pausa: HH:MM
   Estado guardado en .dojo-session.json
   
   Cuando vuelvas:
   1. Abre terminal → hermes
   2. Escribe /dojo-start (sin argumentos)
   3. El sistema detectará la sesión pausada y te ofrecerá retomar.
   ```

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- **NO ejecutes scripts Python ni búsquedas globales.**
- El archivo `.dojo-session.json` va en la RAÍZ del proyecto (`~/Documents/DoJo/DoJo_Study/`), no dentro de la misión.
- Si el archivo ya existe, leer el `block_number` actual ANTES de sobrescribir para incrementarlo.

## Verification
- Existe `~/Documents/DoJo/DoJo_Study/.dojo-session.json` con contenido válido
- `journal.md` tiene la entrada de pausa con timestamp y número de bloque
- El agente muestra instrucciones claras de cómo retomar
```

### Parte B: Modificar skill `/dojo-start` para detectar sesiones pausadas

#### Archivo a modificar
```
~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-start/SKILL.md
```

#### Cambios requeridos en `session-start/SKILL.md`

**Agregar un paso 0 ANTES del paso 1 actual.** El nuevo procedure debe empezar así:

```markdown
## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio. NUNCA hagas búsquedas en `/home`, `/Users` ni en la raíz del sistema.**

### Paso 0: Detectar sesión pausada (NUEVO)

Si el usuario ejecuta `/dojo-start` **SIN argumentos** (sin campaña ni misión):

1. Verificar si existe el archivo `~/Documents/DoJo/DoJo_Study/.dojo-session.json`
2. Si existe y tiene `"status": "paused"`:
   - Leer los campos `campaign`, `mission`, `block_number`, `paused_at`, `next_step`
   - Mostrar al Operador:
     ```
     [Sistema] 🔄 Sesión pausada detectada
     Campaña: {campaign} | Misión: {mission}
     Pausada a las: {paused_at}
     Bloque anterior: {block_number}
     Siguiente paso anotado: {next_step o "ninguno"}
     
     ¿Retomar esta sesión? (sí/no)
     ```
   - Si el Operador dice **sí**: Continuar con el paso 1 usando los valores de `campaign` y `mission` del archivo JSON. Registrar en el journal:
     ```
     - **[Sistema | YYYY-MM-DD HH:MM — Inicio de bloque {block_number + 1}]:** Sesión retomada.
     ```
   - Si el Operador dice **no**: Preguntar campaña y misión como normalmente.
3. Si NO existe el archivo: Pedir campaña y misión como normalmente.

Si el usuario ejecuta `/dojo-start` **CON argumentos** (ej: `/dojo-start py-basico B01`):
- Ignorar `.dojo-session.json` y proceder normalmente con los argumentos dados.
- Si existe `.dojo-session.json` de una misión DIFERENTE, advertir: *"Hay una sesión pausada de {otra misión}. ¿Descartarla?"*
```

**El resto del procedure (pasos 1-5 originales) permanece IGUAL.** Solo se agrega este paso 0 al inicio.

**También actualizar la sección Usage para reflejar que ahora acepta invocación sin argumentos:**

```markdown
## Usage
```
/dojo-start [campaña] [misión]
```
Ejemplo: `/dojo-start py-basico B00`

O sin argumentos para retomar una sesión pausada:
```
/dojo-start
```
```

### Verificación de Tarea 2
- [ ] Existe `~/Documents/DoJo/DoJo_Study/dojo_agent/skills/dojo/session-pause/SKILL.md`
- [ ] El archivo tiene frontmatter YAML válido con `name: stop-sesion`
- [ ] El procedure escribe `.dojo-session.json` en la raíz del proyecto
- [ ] `session-start/SKILL.md` fue modificado para incluir Paso 0 (detección de sesión pausada)
- [ ] `/dojo-start` sin argumentos lee `.dojo-session.json` y ofrece retomar
- [ ] `/dojo-start` con argumentos ignora `.dojo-session.json` (pero advierte si hay una sesión diferente pausada)

---

## Tarea 3: Generar `requirements.md` para misión B01

### Qué es y por qué
B01 es una misión de **consolidación/validación** de los conceptos aprendidos en B00. El Operador debe usar predominantemente el modo **Reviewer (socrático)**, NO Tutor. Puede referirse al código de B00 como "documentación", pero el problema debe ser diferente para forzar aplicación, no copia.

### Contexto pedagógico (CRÍTICO — el Agente debe entender esto)

**Conceptos que B00 dejó en estado `exposed` (vistos con Tutor, nunca usados solo):**
- `pytest` (assert, raises, fixtures)
- `datetime.strptime` / `strftime`
- `defaultdict(list)` / `defaultdict(float)`
- Type hints + `Any` (mypy compliance)
- Estructura `src/` + `test/` + `pyproject.toml`
- `csv.DictReader`
- `json.dump`
- `try/except` con `raise`
- Patrón "una función = un trabajo"
- Función supervisora (loop + error logging)
- Reglas de negocio vs limpieza de datos (separación)

**Objetivo de B01:** Mover estos conceptos de `exposed` → `practicing`. El Operador debe usarlos SOLO con Reviewer socrático. Si la fricción sube >7, puede escalar a Tutor como red de seguridad.

### Ruta del nuevo archivo
```
~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01/requirements.md
```

> **NOTA:** La carpeta `B01/` NO existe. Crearla.

### Template y criterios para generar el `requirements.md`

Usar **exactamente el mismo formato** que `B00/requirements.md` (ver archivo de referencia en `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B00/requirements.md`).

**Restricciones de diseño para B01:**

1. **Dominio DIFERENTE a B00:** B00 fue transacciones financieras. B01 debe ser otro dominio. Sugerencia: un **Log Analyzer** — leer archivos de log de servidor (tipo Apache/Nginx), parsear timestamps, extraer métricas (requests por hora, códigos de error, IPs más activas), exportar reporte.

2. **Mismos building blocks:** csv/text parsing, datetime, defaultdict, try/except, type hints, pytest, json output. Esto fuerza al Operador a REUTILIZAR los mismos patrones en un contexto nuevo.

3. **Complejidad similar o ligeramente mayor que B00:** No más funciones (mantener ~6-8), pero el parsing puede ser ligeramente más complejo (regex básico para parsear líneas de log).

4. **Zero third-party libs:** Igual que B00. Solo stdlib.

5. **TDD obligatorio:** Igual que B00. Mínimo 3 test cases definidos.

6. **Debe incluir los mismos criterios DoD de B00** (English naming, zero third-party, Social README, docstrings, mypy).

7. **Campo `Status`:** Debe ser `🟢 Ready`

8. **Agregar una nota de Fase 2 en la sección Architecture:**
   ```
   **Modo de trabajo:** Esta misión se ejecuta en **Fase 2 (Reviewer Socrático)**. 
   El Operador implementa solo. El Reviewer hace preguntas, NO da código. 
   Si la fricción sube >7, escalar a Tutor temporalmente.
   Referencia permitida: código de B00 como documentación.
   ```

9. **Crear también un `journal.md` vacío inicial:**
   ```
   ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01/journal.md
   ```
   Contenido inicial: vacío (el primer entry será del `/dojo-start`).

### Verificación de Tarea 3
- [ ] Existe `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01/requirements.md`
- [ ] Existe `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01/journal.md`
- [ ] El requirements.md sigue el MISMO formato que B00 (YAML-like headers, mismas secciones)
- [ ] El dominio es DIFERENTE a B00 (no transacciones financieras)
- [ ] Los building blocks son los MISMOS que B00 (csv/text, datetime, defaultdict, try/except, type hints, pytest)
- [ ] Incluye nota de Fase 2 (Reviewer socrático)
- [ ] Status es `🟢 Ready`
- [ ] Zero third-party libs

---

## Post-tareas: Actualizar documentación

Después de completar las 3 tareas, actualizar estos archivos:

### 1. Actualizar `guia-operaciones-v4.md`

En la sección **"⚡ Comandos rápidos (cheat sheet)"**, agregar los nuevos skills:

```markdown
#### Pausar bloque de deep work (funciona con CUALQUIER personalidad):
```
/stop_sesion
```

#### Cerrar misión formalmente (funciona con CUALQUIER personalidad):
```
/dojo-done
```
```

En la sección **"📁 Dónde vive todo"**, agregar las carpetas nuevas al árbol:

```
│   ├── session-pause/           ← /stop_sesion
│   ├── mission-done/            ← /dojo-done
```

En la sección **"🔄 Flujo típico de un día de estudio"**, agregar paso de pausa:

```
5.5. Si necesito pausar (almuerzo, descanso):
   /stop_sesion                      ← Guarda estado a disco, registra en journal
   (puedes cerrar Hermes y suspender el Mac)
   Cuando vuelvas: hermes → /dojo-start (sin args) → retoma automáticamente
```

Y cambiar el paso 10:
```
10. Al terminar la misión:
    /dojo-done                       ← Cierre formal
```

### 2. Actualizar `.hermes.md`

En la sección **"Skills Disponibles"** (línea 83-89), agregar:

```markdown
- `/stop_sesion` — Pausar bloque de deep work (persiste estado a disco)
- `/dojo-done` — Cerrar misión formalmente
```

### 3. Ejecutar `/dojo-done` en B00

Una vez creado el skill, ejecutar el cierre formal de B00:
- Cambiar `Status:` en `B00/requirements.md` de `🟢 Ready` a `✅ Completada`
- Esto se puede hacer manualmente con `write_file` — buscar la línea `Status: 🟢 Ready` y reemplazarla por `Status: ✅ Completada`

### 4. Agregar `.dojo-session.json` al `.gitignore`

El archivo `.dojo-session.json` es estado local transitorio (como `.env`). NO debe estar en git.

Verificar si existe `~/Documents/DoJo/DoJo_Study/.gitignore`:
- Si existe: agregar la línea `.dojo-session.json` al final
- Si no existe: crear el archivo con al menos:
  ```
  .dojo-session.json
  __pycache__/
  *.pyc
  .venv/
  ```

---

## Verificación Final

- [ ] Tarea 1 completada: `/dojo-done` skill existe y es válido
- [ ] Tarea 2 completada: `/stop_sesion` skill existe y es válido
- [ ] Tarea 2b completada: `/dojo-start` modificado con Paso 0 (detección de sesión pausada)
- [ ] Tarea 3 completada: B01 requirements + journal existen
- [ ] `guia-operaciones-v4.md` actualizada con nuevos comandos
- [ ] `.hermes.md` actualizada con nuevos skills
- [ ] B00 `requirements.md` tiene `Status: ✅ Completada`
- [ ] `.gitignore` incluye `.dojo-session.json`
- [ ] No se tocó ningún archivo de código del Operador (src/, tests/)

