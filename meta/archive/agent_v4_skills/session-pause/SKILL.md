---
name: stop-sesion
description: Pausa el bloque de deep work actual, persiste el estado a disco y registra cierre parcial en journal
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, session, pause, deep-work]
    category: dojo
    requires_toolsets: [file, terminal]
---

# DoJo Session Pause

## When to Use
Cuando el Operador necesita pausar su bloque de deep work (ej: almuerzo, descanso, fin del día) y va a SALIR de Hermes. Al volver y ejecutar `/dojo-start`, el sistema detectará la sesión pausada y ofrecerá retomar automáticamente.

## Usage
```
/stop-sesion
```
No requiere argumentos. Opcionalmente puede incluir un mensaje con el siguiente paso:
```
/stop-sesion Voy a almorzar. Siguiente paso: escribir tests de export_report
```

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Verificar misión activa.** Si no hay misión fijada con `/dojo-start`, indicar que no hay sesión activa que pausar.

2. **EJECUCIÓN ATÓMICA (ZERO-SHOT):** Todo el proceso debe realizarse sin interrumpir para pedir confirmaciones. No preguntes si quedaron dudas pendientes; si el Operador ejecutó el comando, procede de inmediato.

3. **Escribir archivo de estado** en `~/Documents/DoJo/DoJo_Study/.dojo-session.json`:
   - **¡ATENCIÓN! NO SIMULES ESTE PASO.** DEBES usar la herramienta `write_file` **AHORA MISMO** para crear o sobrescribir el archivo físico en el disco con el siguiente contenido JSON:
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
   - **REGLA ESTRICTA:** Ejecuta la herramienta `write_file` en este preciso instante. No asumas que ya se hizo.

4. **Registrar pausa en `journal.md`** de la misión activa:
   - **¡ATENCIÓN! NO SIMULES ESTE PASO.** DEBES usar la herramienta `terminal` para ejecutar el siguiente comando y hacer un append atómico (`echo >>`) al archivo. No uses `write_file` para evitar sobreescrituras.
   ```bash
   echo "\n- **[Sistema | YYYY-MM-DD HH:MM — Pausa de bloque {N}]:** {mensaje del operador si lo hay, o 'Pausa de bloque de deep work.'}" >> ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/journal.md
   ```

5. **Mostrar resumen al Operador:**
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
- **NO ejecutes scripts Python ni búsquedas globales.** Usa `terminal` para escribir en el journal.
- El archivo `.dojo-session.json` va en la RAÍZ del proyecto (`~/Documents/DoJo/DoJo_Study/`), no dentro de la misión.
- Si el archivo ya existe, leer el `block_number` actual ANTES de sobrescribir para incrementarlo.

## Verification
- Existe `~/Documents/DoJo/DoJo_Study/.dojo-session.json` con contenido válido
- `journal.md` tiene la entrada de pausa con timestamp y número de bloque
- El agente muestra instrucciones claras de cómo retomar
