---
name: dojo-log
description: Registra una entrada estructurada en la bitácora (journal.md) de la misión activa
version: 2.0.0
metadata:
  hermes:
    tags: [dojo, journal, logging]
    category: dojo
    requires_toolsets: [file, terminal]
---

# DoJo Journal Log

## When to Use
Cuando el Operador quiere registrar un avance, reflexión, error o duda en la bitácora de la misión activa. Este skill también se usa internamente por `/stop-sesion` y `/dojo-done` para entradas de sistema.

## Usage
```
/dojo-log [mensaje]
```
Ejemplo: `/dojo-log Completé el primer test unitario. Descubrí que decimal.Decimal es mejor que float para finanzas.`

### Modo resumen de bloque (al pausar o cerrar)
```
/dojo-log --summary
```
Genera una entrada de resumen del bloque con métricas de WakaTime (si disponibles).

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

1. **Identificar la misión activa.** Si el usuario ya usó `/dojo-start` en esta sesión, ya sabes la campaña y misión. Si no, pregúntale.

2. **Construir la ruta del journal:**
   `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CAMPAÑA}/missions/{MISIÓN}/journal.md`

3. **Determinar tipo de entrada:**

   **Si es una entrada normal** (sin `--summary`):
   
   Agregar al final de `journal.md` usando `write_file` (append). Formato:
   ```
   - **[User | YYYY-MM-DD HH:MM]:** {mensaje del usuario}
   ```

   **Si es un resumen de bloque** (con `--summary`):
   
   a. **Auto-identificar modelo LLM:** Reportar el nombre/ID del modelo que TÚ eres actualmente.
   
   b. **Intentar obtener métricas de WakaTime** (best-effort):
      - Leer la API key desde `~/.wakatime.cfg` (campo `api_key` bajo `[settings]`)
      - Si la key existe, ejecutar via `terminal`:
        ```bash
        curl -s -H "Authorization: Basic $(echo -n '{API_KEY}' | base64)" \
          "https://wakatime.com/api/v1/users/current/summaries?start=$(date +%Y-%m-%d)&end=$(date +%Y-%m-%d)" \
          | python3 -c "import sys,json; d=json.load(sys.stdin)['data'][0]; print(f\"Coding: {d['grand_total']['text']}\")"
        ```
      - Si falla (key no existe, API caída, error de red): usar `WakaTime: ⚠️ no disponible` y continuar sin bloquear.
   
   c. Agregar entrada de resumen al final de `journal.md`:
      ```
      ---
      
      ### 📊 Resumen de Bloque {N} — YYYY-MM-DD
      - **Modelo LLM:** {modelo auto-identificado}
      - **WakaTime:** {tiempo de coding | ⚠️ no disponible}
      - **Avance general:** {resumen breve del trabajo realizado durante este bloque — inferir del contexto de conversación}
      - **Siguiente paso:** {lo que indicó el Operador o inferir del estado actual}
      ```

4. **Confirmar** al Operador que la entrada fue registrada.

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- Si no hay misión activa, indica al usuario que use `/dojo-start` primero.
- **NO ejecutes scripts Python ni búsquedas globales.** Usa `write_file` directamente para el journal.
- La integración WakaTime es **best-effort**. Si falla, anota `⚠️ no disponible` y SIGUE. Nunca bloquees el log por WakaTime.
- El campo "Modelo LLM" es de **auto-identificación**: reporta tu propio modelo, no copies un ejemplo.
- Usa `terminal` solo para la llamada a WakaTime. El journal se escribe con `write_file`.

## Verification
- El archivo journal.md contiene la nueva entrada con timestamp correcto.
- Las entradas normales usan formato de una línea.
- Las entradas de resumen usan el template estructurado con separador `---`.
- Si WakaTime falló, la entrada dice `⚠️ no disponible` (no se bloqueó).
