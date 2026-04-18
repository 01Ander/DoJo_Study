---
name: stop-sesion
description: Pausa el bloque de deep work actual, persiste el estado a disco y registra cierre parcial en journal
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, session, pause, deep-work]
    category: dojo
    requires_toolsets: [file]
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

2. **Validación de Cierre Preventivo (Anti-Premature Closure):** ANTES de pausar, verifica si en la conversación reciente hubo dudas operativas, revisión de código o cambios de personalidad. Si es así, **DEBES PREGUNTAR** obligatoriamente al Operador:
   `[Sistema] Antes de pausar: ¿La duda operativa fue resuelta? ¿Necesitas verificar algo antes de pausar?`
   *Nota: Solo procede al siguiente paso si el Operador confirma que puede pausar o si se invoca `/stop-sesion` con la instrucción clara de "forzar" o sin dudas pendientes.*

3. **Escribir archivo de estado** en `~/Documents/DoJo/DoJo_Study/.dojo-session.json`:
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
   - Usar `write_file` para crear/sobrescribir el archivo.

4. **[Solo si la misión activa es B01] Registrar marcador de pausa en `eval_log.md`:**
   **⚠️ PROHIBIDO usar `write_file` sobre eval_log.md — SOBRESCRIBE y destruye el historial.**
   Usar la herramienta `terminal` con el operador `>>` (append):
   ```bash
   cat >> ./subjects/python/campaigns/PY-BASICO/missions/B01/eval_log.md << 'EVAL_EOF'
   ---
   Timestamp: [YYYY-MM-DD HH:mm]
   Role: Sistema
   Personality: none
   Model: [Auto-identifícate: el modelo LLM que TÚ eres]
   Content: ⏸️ SESSION_PAUSE — Bloque {N} cerrado. El Operador ha pausado la sesión con /stop-sesion.
   ---
   EVAL_EOF
   ```
   Esto asegura que el Golden Dataset mantenga integridad cronológica entre bloques.

5. **Registrar pausa en `journal.md`** de la misión activa:
   ```
   - **[Sistema | YYYY-MM-DD HH:MM — Pausa de bloque {N}]:** {mensaje del operador si lo hay, o "Pausa de bloque de deep work."}
   ```

6. **Mostrar resumen al Operador:**
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
- **NO ejecutes scripts Python ni búsquedas globales.**
- El archivo `.dojo-session.json` va en la RAÍZ del proyecto (`~/Documents/DoJo/DoJo_Study/`), no dentro de la misión.
- Si el archivo ya existe, leer el `block_number` actual ANTES de sobrescribir para incrementarlo.

## Verification
- Existe `~/Documents/DoJo/DoJo_Study/.dojo-session.json` con contenido válido
- `journal.md` tiene la entrada de pausa con timestamp y número de bloque
- El agente muestra instrucciones claras de cómo retomar
