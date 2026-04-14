---
name: dojo-start
description: Inicia una sesión de estudio fijando Campaña y Misión activa del DoJo
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, session, study]
    category: dojo
    requires_toolsets: [terminal, file]
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
1. Ejecuta el script `scripts/start_mission.py` con los argumentos de campaña y misión.
2. El script valida que la campaña y misión existan en `subjects/python/campaigns/`.
3. Si la misión existe, lee `requirements.md` y las últimas 10 líneas de `journal.md`.
4. Presenta el contexto al Operador: qué misión, qué requerimientos, qué hizo la última vez.
5. El agente ahora tiene contexto de misión para todas las interacciones siguientes.

## Pitfalls
- Los nombres de campaña y misión son case-insensitive pero deben existir en el filesystem.
- Si la misión no existe, el script sugiere misiones disponibles en esa campaña.

## Verification
- El agente confirma con: "[Sistema] ¡Contexto Fijado! Campaña: X | Misión: Y"
- El contexto de requirements.md aparece en las respuestas posteriores.
