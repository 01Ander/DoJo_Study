---
name: dojo-log
description: Registra una entrada en la bitácora (journal.md) de la misión activa
version: 1.1.0
metadata:
  hermes:
    tags: [dojo, journal, logging]
    category: dojo
    requires_toolsets: [file]
---

# DoJo Journal Log

## When to Use
Cuando el Operador quiere registrar un avance, reflexión, error o duda en la bitácora de la misión activa.

## Usage
```
/dojo-log [mensaje]
```
Ejemplo: `/dojo-log Completé el primer test unitario. Descubrí que decimal.Decimal es mejor que float para finanzas.`

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Identificar la misión activa.** Si el usuario ya usó `/dojo-start` en esta sesión, ya sabes la campaña y misión. Si no, pregúntale.

2. **Construir la ruta del journal:**
   `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/journal.md`

3. **Agregar la entrada** al final de `journal.md` usando `write_file` (append). Formato:
   ```
   - **[User | YYYY-MM-DD HH:MM]:** {mensaje del usuario}
   ```

4. **Confirmar** al Operador que la entrada fue registrada.

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- Si no hay misión activa, indica al usuario que use `/dojo-start` primero.
- **NO ejecutes scripts Python ni búsquedas globales.** Usa `write_file` directamente.

## Verification
- El archivo journal.md contiene la nueva entrada con timestamp correcto.
