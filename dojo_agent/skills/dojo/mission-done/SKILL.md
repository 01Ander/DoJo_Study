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
