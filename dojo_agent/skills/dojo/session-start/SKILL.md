---
name: dojo-start
description: Inicia una sesión de estudio fijando Campaña y Misión activa del DoJo
version: 1.2.0
metadata:
  hermes:
    tags: [dojo, session, study]
    category: dojo
    requires_toolsets: [file, terminal]
---

# DoJo Session Start

## When to Use
Cuando el Operador quiere comenzar a trabajar en una misión específica de una campaña.

## Usage
```
/dojo-start [campaña] [misión]
```
Ejemplo: `/dojo-start py-basico B00`

O sin argumentos para retomar una sesión pausada:
```
/dojo-start
```

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio. NUNCA hagas búsquedas en `/home`, `/Users` ni en la raíz del sistema.**

### Paso 0: Detectar sesión pausada (NUEVO)

Si el usuario ejecuta `/dojo-start` **SIN argumentos** (sin campaña ni misión):

1. Verificar si existe el archivo `~/Documents/DoJo/DoJo_Study/.dojo-session.json`
2. Si existe y tiene `"status": "paused"`:
   - Leer los campos `campaign`, `mission`, `block_number`, `paused_at`, `next_step` y `personality`.
   - **RETOMA AUTOMÁTICA (ZERO-SHOT):** NO pidas confirmación (`¿Retomar esta sesión?`). Asume directamente que sí.
   - Muestra el resumen al Operador:
     ```
     [Sistema] 🔄 Sesión retomada automáticamente
     Campaña: {campaign} | Misión: {mission}
     Personalidad: {personality o "none"}
     Siguiente paso anotado: {next_step o "ninguno"}
     ```
   - Continúa con la carga de contexto usando los valores de `campaign` y `mission` del archivo JSON. **Debes adoptar inmediatamente la `personality` recuperada del archivo JSON e indicar al Operador si necesita hacer algún ajuste manual.**
   - Registra en el journal de la misión agregando al final del archivo `journal.md`:
     `- **[Sistema | YYYY-MM-DD HH:MM — Inicio de bloque {block_number + 1}]:** Sesión retomada.`
3. Si NO existe el archivo: Pedir campaña y misión como normalmente.

Si el usuario ejecuta `/dojo-start` **CON argumentos** (ej: `/dojo-start py-basico B01`):
- Ignorar `.dojo-session.json` y proceder normalmente con los argumentos dados.
- Si existe `.dojo-session.json` de una misión DIFERENTE, advertir: *"Hay una sesión pausada de {otra misión}. ¿Descartarla?"*

1. **Construir la ruta de la misión** (case-insensitive, las campañas en disco usan MAYÚSCULAS):
   - Campañas: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/`
   - Misiones: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/`
   - Ejemplo: si el usuario dice `py-basico B00`, la ruta es:
     `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B00/`

### Paso 1.5: Detectar Campaign Type
- Leer `campaign.md` de la campaña activa (ruta: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/campaign.md`)
- Buscar el campo `Campaign Type:` en el archivo
- **Si es `CUMULATIVE`:**
  - El código fuente está en `{CAMPAÑA}/src/`, NO en `{CAMPAÑA}/missions/{MISIÓN}/code/src/`
  - Los tests están en `{CAMPAÑA}/tests/`
  - Informar al Operador: "[Sistema] Campaña CUMULATIVE detectada. Código en {CAMPAÑA}/src/"
- **Si es `ADDITIVE` o no está definido:**
  - Comportamiento actual (buscar en `missions/{MISIÓN}/code/`)

2. **Leer `requirements.md`** de esa ruta usando la herramienta `read_file`. No ejecutes scripts Python ni hagas `find`. Lee el archivo directamente.

2.5. **Actualizar Status en `requirements.md`** (Bidireccionalidad):
   - Leer la línea que contiene `Status:` en la sección `## Identification`
   - Si el valor actual es `🟢 Ready`, cambiarlo a `🔵 En Ejecución`
   - Si ya es `🔵 En Ejecución` o `✅ Completada`, NO cambiar nada
   - Usar `write_file` para hacer la modificación. No tocar ninguna otra línea del archivo.
   - **NOTA:** Solo ejecutar este paso cuando el Operador confirma que va a trabajar en esta misión (después del paso 0 de detección de sesión pausada, si aplica).

2.8. **Registrar inicio de sesión en `journal.md`** de la misión:
   - Usa la herramienta `terminal` para hacer un append atómico (`echo >>`) al archivo `journal.md`. Esto aplica tanto si es la primera vez que se inicia como si se retoma sin archivo de pausa.
   ```bash
   echo "\n- **[Sistema | YYYY-MM-DD HH:MM — Inicio de sesión]:** Misión {MISIÓN} de la campaña {CAMPAÑA} fijada como activa." >> ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/journal.md
   ```

3. **Leer `journal.md`** de esa misma ruta (si existe). Solo las últimas 15 líneas.

4. **Presentar el contexto** al Operador con este formato:
   ```
   [Sistema] ¡Contexto Fijado! Campaña: {CAMPAÑA} | Misión: {MISIÓN}
   
   - Estado de la misión (basado en journal.md)
   - Resumen de requirements.md
   - Siguiente paso sugerido

   ⚠️ REGLA TDD OBLIGATORIA: Escribir tests ANTES del código fuente.
   Flujo: 1) Test (Red) → 2) Implementación mínima (Green) → 3) Refactor.
   NO se permite escribir en src/ sin tener al menos un test fallando en tests/.
   ```
   
   **CRÍTICO PARA MODELOS LIGEROS:** El bloque `⚠️ REGLA TDD OBLIGATORIA` DEBE aparecer siempre en la respuesta al Operador. Esta directiva NO es opcional — es la regla más importante del sistema. Si el Operador intenta escribir código en `src/` sin tests existentes, el agente DEBE detenerlo y redirigirlo a `tests/` primero.

5. **Preguntar** con qué personalidad quiere trabajar (`/personality dojo-tutor`, `/personality dojo-reviewer`, `/personality dojo-architect`), solo si no tiene una activa.

## Mapping de nombres comunes
| El usuario escribe | Carpeta en disco |
|---|---|
| `py-basico` | `PY-BASICO` |
| `py-poo-finance` | `PY-POO-FINANCE` |

## Pitfalls
- **NO ejecutes búsquedas globales.** Las rutas son conocidas y fijas.
- Los nombres de campaña y misión son case-insensitive pero las carpetas en disco usan MAYÚSCULAS para campañas.
- Si la misión no existe, lista las carpetas disponibles en `campaigns/` usando `read_file` o `list_dir`, no `find`.

## Verification
- El agente confirma con: "[Sistema] ¡Contexto Fijado! Campaña: X | Misión: Y"
- El contexto de requirements.md aparece en las respuestas posteriores.
