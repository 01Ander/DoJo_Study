---
name: dojo-done
description: Cierra formalmente una misión, actualiza su estado y registra la retrospectiva final
version: 2.0.0
metadata:
  hermes:
    tags: [dojo, mission, completion]
    category: dojo
    requires_toolsets: [file, terminal]
---

# DoJo Mission Done

## When to Use
Cuando el Operador ha completado los Criterios de Aceptación de una misión y quiere cerrarla formalmente de manera atómica ("Zero-Shot") sin consumir tokens adicionales en diálogos de confirmación.

## Usage
```
/dojo-done <mensaje_de_cierre_del_operador>
```
El Operador siempre proporcionará una nota o comentario de cierre. Usa ese texto íntegramente para la bitácora.

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio. NUNCA hagas búsquedas en `/home`, `/Users` ni en la raíz del sistema.**

1. **Verificar misión activa.** Utiliza la misión que está actualmente en el contexto de la sesión.

2. **EJECUCIÓN ATÓMICA (ZERO-SHOT):** Todo lo siguiente DEBE realizarse en **un solo turno** (paralelizando los tool calls si es posible), sin preguntar nada al usuario y sin hacer llamadas innecesarias para releer archivos que ya conoces. 
   
   a. **Actualizar `requirements.md`:**
      - Modificar la línea `Status:` a `✅ Completada` usando `replace_file_content` o equivalente.
      - Asume que los DoD están completos si el usuario ejecutó el comando. No le preguntes confirmación.
   
   b. **Registrar Retrospectiva y Cierre en `journal.md`:**
      - Agrega AL MISMO TIEMPO (en un solo append/escritura) el **Comentario del Operador**, la **Reflexión del Tutor** y el **Log del Sistema**.
      - **IMPORTANTE:** SIEMPRE incluye primero el comentario exacto proporcionado por el usuario en el comando `/dojo-done`. Luego, genera la reflexión del Tutor evaluando el desempeño del Operador basándote en el contexto de la sesión.
      - Formato a agregar al final del journal:
        ```markdown
        - **[User | YYYY-MM-DD HH:MM]:** {El argumento literal o nota de cierre proporcionada por el Operador al ejecutar el comando. NO LO RESUMAS, escríbelo en crudo}

        - **[Tutor | YYYY-MM-DD HH:MM]:** {Genera aquí tu reflexión profunda sobre la sesión, el desempeño del Operador, áreas de mejora y asimilación conceptual. Basealo en tu memoria de la conversación actual}
        
        ---
        
        - **[Sistema | YYYY-MM-DD HH:MM — MISIÓN {CÓDIGO} COMPLETADA]:**
          - **Tests finales:** Pasados (según contexto de la sesión)
          - **DoD:** Completo
          - **Nota de cierre:** Resumen técnico y métricas de costos de API / WakaTime / Tokens consumidos.
        ```
   
   c. **Limpiar archivo de sesión pausada:**
      - Usa un comando de terminal para eliminar `~/Documents/DoJo/DoJo_Study/.dojo-session.json`. (Ej: `rm -f ~/.dojo-session.json` o similar)

3. **Respuesta final al usuario:**
   - Reporta que todo fue ejecutado (Requirements actualizado, Journal escrito, Sesión limpiada).
   - Sugiere el siguiente paso listando las siguientes misiones de la campaña.

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- **NO ejecutes scripts Python ni búsquedas globales.** Las rutas son conocidas y fijas.
- Solo modifica la línea `Status:` en `requirements.md`. No toques el resto del archivo.
- **NUNCA preguntes por confirmación.** Ejecuta el comando inmediatamente asumiendo que el usuario sabe lo que hace.
- **NO** hagas `view_file` de `requirements.md` ni `journal.md` si ya tienes el contexto. Solo escribe en ellos directamente.
- Siempre eliminar `.dojo-session.json` al cerrar misión para evitar sesiones fantasma.
- **EVITA EL ERROR [Errno 63] File name too long:** El texto de este comando (`/dojo-done ...`) es un mensaje de chat, NO una ruta de archivo. Al invocar tus herramientas de escritura, el parámetro `TargetFile` DEBE ser estrictamente la ruta real a `requirements.md` o `journal.md`. **NUNCA** coloques el texto del operador ni el string `/dojo-done` en los parámetros de ruta. Extrae su nota e insértala únicamente como *contenido* a escribir.
## Verification
- `requirements.md` tiene `Status: ✅ Completada`
- `journal.md` tiene la reflexión del Tutor y la entrada de cierre del Sistema con timestamp
- `.dojo-session.json` fue eliminado (si existía)
- El agente sugiere la siguiente misión
