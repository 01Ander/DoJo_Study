---
name: dojo-start
description: Inicia una sesión de estudio fijando Campaña y Misión activa del DoJo
version: 1.1.0
metadata:
  hermes:
    tags: [dojo, session, study]
    category: dojo
    requires_toolsets: [file]
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

1. **Construir la ruta de la misión** (case-insensitive, las campañas en disco usan MAYÚSCULAS):
   - Campañas: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/`
   - Misiones: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/`
   - Ejemplo: si el usuario dice `py-basico B00`, la ruta es:
     `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B00/`

2. **Leer `requirements.md`** de esa ruta usando la herramienta `read_file`. No ejecutes scripts Python ni hagas `find`. Lee el archivo directamente.

3. **Leer `journal.md`** de esa misma ruta (si existe). Solo las últimas 15 líneas.

4. **Presentar el contexto** al Operador con este formato:
   ```
   [Sistema] ¡Contexto Fijado! Campaña: {CAMPAÑA} | Misión: {MISIÓN}
   
   - Estado de la misión (basado en journal.md)
   - Resumen de requirements.md
   - Siguiente paso sugerido
   ```

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
