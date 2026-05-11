---
name: scroll
description: Pergamino rápido — captura ideas sin romper la inmersión del deep work
version: 2.0.0
metadata:
  hermes:
    tags: [dojo, ideas, capture, fire-and-forget, discworld]
    category: dojo
    requires_toolsets: [file]
---

# Scroll (Pergamino Rápido)

## When to Use
Cuando el Operador tiene una idea, feature request, o reflexión sobre el sistema DoJo durante una sesión de deep work y quiere registrarla SIN romper su flujo de estudio.

## Usage
```
/scroll [descripción de la idea]
```
Ejemplo: `/scroll Crear un dashboard web que muestre el progreso por chronicle`

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Capturar la idea.** El texto después de `/scroll` es el contenido completo. No pidas aclaraciones ni hagas preguntas — este skill es atómico y no-interactivo.

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
   [Sistema] 📜 Scroll registrado en ideas-in-live.md
   ```
   **NO** hagas seguimiento, NO preguntes "¿quieres ampliar?", NO ofrezcas desarrollar la idea. El Operador debe volver inmediatamente a su deep work.

## Pitfalls
- **Este skill es ATÓMICO.** Un comando, una acción, un mensaje de confirmación. Nada más.
- Requiere que el Operador pase el texto de la idea como argumento. Si ejecuta `/scroll` sin texto, pedir: `[Sistema] Uso: /scroll [tu idea aquí]`
- **NO ejecutes scripts Python ni búsquedas globales.**
- La idea se inserta al final de la sección "Pendiente", ANTES de la sección "🔍 Evaluación Pendiente".
- Si `ideas-in-live.md` no existe, crearlo con la sección header.
