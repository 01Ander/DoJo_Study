# Personalidades portables — DoJo ⇄ Hermes ⇄ OpenCode

Una sola fuente de verdad para las personalidades del agente, que genera artefactos
nativos para **Hermes** y para **OpenCode**.

## Por qué existe este directorio

Hermes **no** lee `~/.hermes/personalities/*.md`: la resolución de personalidades vive en
`hermes_cli/personality.py` y solo consulta `config.yaml` (bloque raíz `personalities:` o
`agent.personalities`, este último gana) más un `SOUL.md` global. Por eso los ricos archivos
`wizard.md` / `witch.md` de `~/.hermes/personalities/` eran **código muerto**: lo que corría
eran los strings inline resumidos de `config.yaml`.

Además, OpenCode no tiene `/personality`: su equivalente son los **agentes**
(`.opencode/agents/<name>.md`, cuerpo = system prompt).

Este directorio invierte el flujo: aquí vive el prompt completo y **una** definición, y de
ella se generan los dos formatos de runtime.

## Capas de identidad (contexto)

| Capa | Hermes | OpenCode |
|---|---|---|
| Identidad global | `~/.hermes/SOUL.md` | `~/.config/opencode/AGENTS.md` |
| Constitución de proyecto | `.hermes.md` | `AGENTS.md` (raíz) |
| Personalidad / modo de trabajo | `agent.personalities.<name>` + `/personality <name>` | `.opencode/agents/<name>.md` |

> Pendiente complementario: generar el `AGENTS.md` de OpenCode desde `.hermes.md`.
> Fuera del alcance de este directorio (que cubre solo las personalidades).

## Fuente canónica

Un archivo por personalidad: `<name>.md`, con frontmatter neutro y **cuerpo = system prompt**.

```markdown
---
name: wizard                 # nombre canónico (== nombre de archivo == slug de comando)
description: ...             # frase corta; se usa en ambos runtimes
version: 5.1.0
opencode:                    # bloque solo-OpenCode (se ignora en Hermes)
  mode: primary              # primary | subagent | all
  color: "#8b5cf6"           # color de UI
  model: anthropic/claude-sonnet-4-5#high   # opcional
---

Eres **El Wizard** del DoJo Study — …
```

El cuerpo debe ser **tool-agnostic**: nada de sintaxis específica de un runtime. Las
referencias cruzadas entre personalidades se escriben como "cambia a la personalidad
`witch`" (no `:witch` ni `/personality witch`).

## Mapeo

| Concepto | Hermes (`config.yaml`) | OpenCode (`.opencode/agents/<name>.md`) |
|---|---|---|
| Prompt | `agent.personalities.<name>.system_prompt` (bloque literal `\|`) | cuerpo del `.md` |
| Descripción | `agent.personalities.<name>.description` (solo UI) | frontmatter `description` |
| Modo | — | frontmatter `mode` |
| Color | — | frontmatter `color` |
| Selección | `display.personality: <name>` + `/personality <name>` | agente seleccionado / `default_agent` |

Nota Hermes: en la forma dict, `system_prompt` es lo que llega al modelo; `description` solo
alimenta las vistas de lista. `tone` y `style` son opcionales.

## Uso

```bash
cd system/dojo_agent/personalities
python3 sync_personalities.py                      # genera dist/
python3 sync_personalities.py --install-opencode   # copia a <repo>/.opencode/agents/
```

Genera:

```
dist/hermes/personalities.yaml    # pegar bajo `agent:` en ~/.hermes/config.yaml
dist/opencode/agents/wizard.md
dist/opencode/agents/witch.md
```

`dist/` es salida generada: puede añadirse a `.gitignore` o commitearse como referencia.

### Instalar en Hermes

1. Copia el bloque de `dist/hermes/personalities.yaml` **bajo `agent:`** en
   `~/.hermes/config.yaml`, reemplazando las definiciones inline de `wizard` y `witch`.
2. Opcional — limpia el legado v4: las entradas `dojo-tutor`, `dojo-reviewer` y
   `dojo-architect` quedaron obsoletas (el arquitecto se externalizó a Antigravity). Si se
   teclean, devuelven comportamiento v4.0 contradictorio con la constitución v5.2.
3. `~/.hermes/personalities/*.md` ya no se usa; puede borrarse o conservarse como referencia.

El script **no** reescribe `config.yaml`: un round-trip con PyYAML destruiría comentarios y
orden. La fusión es manual (o vía `hermes config set`).

### Instalar en OpenCode

```bash
python3 sync_personalities.py --install-opencode                            # <repo>/.opencode/agents/
python3 sync_personalities.py --install-opencode ~/.config/opencode/agents  # global
```

El destino por defecto se ancla a la **raíz del repo** (donde vive `.git`), no al cwd.

Luego: selecciona el agente en la TUI, o fíjalo con `"default_agent": "witch"` en
`opencode.jsonc`.

## Hardening opcional (OpenCode)

La Constitución (regla 3) prohíbe que el agente escriba el código del Operador. En OpenCode
eso se puede **imponer** con `permissions` en el frontmatter:

```yaml
permissions:
  - action: edit
    resource: "content/**/*.py"
    effect: deny
  - action: edit
    resource: "content/**/*.sql"
    effect: deny
```

Se limita a código (`.py`/`.sql`) para no bloquear `grimoire.md`, `lore/` o docs, que el
agente **sí** debe poder editar (la sección `🔮 Auditoría del DM`).
