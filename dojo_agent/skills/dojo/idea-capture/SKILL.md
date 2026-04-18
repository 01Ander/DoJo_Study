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
