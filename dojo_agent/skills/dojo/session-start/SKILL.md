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

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio. NUNCA hagas búsquedas en `/home`, `/Users` ni en la raíz del sistema.**

Dado los argumentos `[campaña]` y `[misión]`, sigue estos pasos exactos:

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
