 # ⛩️ DoJo Study v4.0 — Guía de Operaciones

> Este documento es tu referencia rápida. Si te pierdes, vuelve aquí.

---

## 🗺️ Qué cambió (en 30 segundos)

Antes tenías `python dojo_agent/main.py` — un script Python custom que hacía todo.

Ahora usas **Hermes Agent** — una plataforma completa que hace lo mismo pero mejor. Tu `main.py` descansa en `archive/`.

| Antes (v3) | Ahora (v4) |
|---|---|
| `python dojo_agent/main.py` | `hermes` |
| `/mode work` | `/personality dojo-reviewer` |
| `/mode main` | `/personality dojo-tutor` |
| `/mode think` o `/mode global` | `/personality dojo-architect` |
| `/start py-basico B00` | `/dojo-start py-basico B00` |
| `/log "algo"` | `/dojo-log "algo"` |
| `/audit` | Ya no existe (usa architect + model switch) |

---

## 🚀 Cómo iniciar una sesión de estudio

### Paso 1: Abrir Hermes en el directorio DoJo
```bash
cd ~/Documents/DoJo/DoJo_Study
hermes
```
> Hermes lee automáticamente el archivo `.hermes.md` de este directorio. Eso le inyecta todas las reglas del DoJo (la "Constitución"). No tienes que hacer nada más.

### Paso 2: Elegir tu modo de trabajo
```
/personality dojo-tutor       # Necesito aprender teoría o ver ejemplos
/personality dojo-reviewer    # Voy a codear y necesito pair programming
/personality dojo-architect   # Quiero analizar el sistema o debatir diseño
```

### Paso 3: Fijar tu misión activa
```
/dojo-start py-basico B00
```
> Esto carga el `requirements.md` y el `journal.md` de esa misión al contexto. El agente ahora sabe en qué estás trabajando.

### Paso 4: Trabajar normalmente
Hazle preguntas, pide reviews, debate. El agente se comporta según la personalidad activa:
- **Tutor**: Te da código real pero con Domain Shifting (dominio diferente al tuyo)
- **Reviewer**: Te hace preguntas socráticas, no te da la respuesta
- **Architect**: Te da opiniones directas y análisis macro

### Paso 5: Registrar avances
```
/dojo-log Completé el primer test. Descubrí que necesito manejar el edge case de lista vacía.
```
> Escribe en el `journal.md` de la misión con timestamp automático.

### Paso 6: Terminar la sesión
Simplemente cierra el terminal o escribe `/exit`.
Tu historial de conversación se guarda automáticamente en Hermes (SQLite). La próxima vez que abras `hermes`, puedes continuar donde dejaste.

---

## ⚡ Comandos rápidos (cheat sheet)

### 📋 Cambiar personalidad

#### Quiero aprender teoría o ver ejemplos:
```
/personality dojo-tutor
```
> Modelo: Qwen3.6 Plus (ya es el default, no necesitas cambiarlo)

#### Quiero codear con pair programming socrático:
```
/personality dojo-reviewer
```
> Modelo: Qwen3.6 Plus (ya es el default, no necesitas cambiarlo)

#### Quiero análisis macro o debatir arquitectura:
```
/personality dojo-architect
/model google/gemini-3.1-pro-preview
```
> ⚠️ Dos comandos. El modelo cambia a Gemini (premium).

#### Cuando termino con Architect, volver al modo barato:
```
/model qwen/qwen3.6-plus
```

---

### Skills del DoJo — qué va con qué

#### Fijar misión (funciona con CUALQUIER personalidad):
```
/dojo-start py-basico B00
```

#### Registrar en bitácora (funciona con CUALQUIER personalidad):
```
/dojo-log Completé el primer test de la calculadora
```

#### Pausar bloque de deep work (funciona con CUALQUIER personalidad):
```
/stop-sesion
```

#### Cerrar misión formalmente (funciona con CUALQUIER personalidad):
```
/dojo-done
```

#### Cargar protocolo de Domain Shifting (usar con Tutor):
```
/personality dojo-tutor
/domain-shifting
```

#### Cargar protocolo Socrático (usar con Reviewer):
```
/personality dojo-reviewer
/socratic-review
```

#### Cargar template Mini-RFC (usar con Reviewer):
```
/personality dojo-reviewer
/mini-rfc
```

#### Capturar idea rápida (funciona con CUALQUIER personalidad):
```
/dojo-idea Automatizar la carga de datos crudos con un script CLI
```

### Modelos (referencia rápida)

| Modelo | Costo | Cuándo |
|---|---|---|
| **Qwen3.6 Plus** (default) | $0.325 / $1.95 per M | Se carga solo. Tutor, Reviewer, día a día. |
| **Gemini 3.1 Pro** | Premium | Solo Architect. Se activa con `/architect`. |
| **Gemma 4 31B** | **FREE** | Auto-logging (Scribe sub-agente). Automático. |

### Otros comandos útiles de Hermes
| Comando | Qué hace |
|---|---|
| `/skills` | Lista todos los skills disponibles |
| `/personality` | Lista o cambia personalidad |
| `/model` | Cambia modelo de LLM |
| `/session` | Muestra info de la sesión actual |
| `/memory` | Muestra memorias persistentes guardadas |
| `/history` | Busca en sesiones anteriores |

---

## 📁 Dónde vive todo

```
~/Documents/DoJo/DoJo_Study/
├── .hermes.md                    ← Constitución (Hermes la lee automática)
├── README.md                     ← Este repo, actualizado a v4.0
├── CHANGELOG.md                  ← Historial de versiones
├── dojo_core.md                  ← Filosofía del DoJo (referencia)
│
├── subjects/python/campaigns/    ← Tus campañas y misiones
│   ├── py-basico/missions/B00/
│   │   ├── requirements.md       ← Lo que carga /dojo-start
│   │   └── journal.md            ← Lo que actualiza /dojo-log
│   └── ...
│
├── dojo_agent/skills/dojo/       ← Skills del DoJo (versionados en git)
│   ├── session-start/            ← /dojo-start
│   ├── session-pause/            ← /stop-sesion
│   ├── mission-done/             ← /dojo-done
│   ├── journal-log/              ← /dojo-log
│   ├── domain-shifting/          ← /domain-shifting
│   ├── socratic-review/          ← /socratic-review
│   ├── idea-capture/             ← /dojo-idea
│   └── mini-rfc/                 ← /mini-rfc
│
├── archive/                      ← Código legacy (main.py v3)
│   ├── legacy_main_v3.py
│   └── legacy_requirements_v3.txt
│
└── docs/                         ← Manuales y documentación

~/.hermes/
├── config.yaml                   ← Config de Hermes (ya tiene external_dirs)
├── .env                          ← API keys (OpenRouter)
├── SOUL.md                       ← Personalidad base de Hermes (no del DoJo)
├── personalities/                ← Personalidades del DoJo
│   ├── dojo-tutor.md
│   ├── dojo-reviewer.md
│   └── dojo-architect.md
└── skills/                       ← Skills globales de Hermes (no del DoJo)
```

---

## 🔄 Flujo típico de un día de estudio

```
1. Abrir terminal

2. cd ~/Documents/DoJo/DoJo_Study && hermes

3. /personality dojo-reviewer        ← Voy a codear hoy

4. /dojo-start py-basico B00         ← Fijo mi misión

5. "Tengo este código, revísame..."  ← Trabajo normal

5.5. Si necesito pausar (almuerzo, descanso):
   /stop-sesion                      ← Guarda estado a disco, registra en journal
   (puedes cerrar Hermes y suspender el Mac)
   Cuando vuelvas: hermes → /dojo-start (sin args) → retoma automáticamente

6. /dojo-log "Terminé tests de..."   ← Registro mi avance

7. Si me atasco en teoría:
   /personality dojo-tutor           ← Cambio a modo aprendizaje

8. Si quiero visión macro:
   /personality dojo-architect
   /model google/gemini-3.1-pro-preview  ← Modelo potente

9. Cuando termino con Architect:
   /model qwen/qwen3.6-plus          ← Vuelvo al barato

10. Al terminar la misión:
    /dojo-done                       ← Cierre formal
```

---

## 🚑 Protocolo de Triaje en Vivo

> Cuando detectas un bug o carencia del sistema DoJo DURANTE una sesión de deep work, usa este árbol de decisión. **NO abras "dos frentes" de trabajo.**

```
¿El bug me BLOQUEA continuar mi misión actual?
│
├── SÍ → ¿Lo puedo parchear en < 5 minutos?
│         │
│         ├── SÍ → ⚡ Parchea en vivo. Registra con /dojo-log "Hotfix: [qué hice]"
│         │
│         └── NO → 🛑 STOP. Registra con /dojo-idea "BUG BLOQUEANTE: [descripción]"
│                   Usa workaround temporal y sigue. Agenda para próxima ventana Architect.
│
└── NO → 💡 Registra con /dojo-idea "[descripción]" y SIGUE TRABAJANDO.
          No abras el archivo. No investigues. Vuelve a tu misión.
```

### Reglas del Triaje
1. **Si no bloquea, no lo toques.** `/dojo-idea` y sigue.
2. **Si bloquea pero es complejo, busca workaround.** El workaround te desbloquea; la solución real va a la ventana Architect.
3. **Nunca dediques más de 5 minutos a un parche en vivo.** Si pasan 5 minutos y no está resuelto, aplica regla 2.
4. **Los bugs del sistema NO son tu misión.** Tu misión es aprender a codear. El sistema es infraestructura.

---

## ❓ Troubleshooting rápido

| Problema | Solución |
|---|---|
| Los skills del DoJo no aparecen en `/skills` | Verifica que `~/.hermes/config.yaml` tiene `external_dirs` apuntando a `~/Documents/DoJo/DoJo_Study/dojo_agent/skills` |
| Las personalidades no aparecen | Verifica que los archivos `.md` existen en `~/.hermes/personalities/` |
| OpenRouter da error | Verifica `OPENROUTER_API_KEY` en `~/.hermes/.env` |
| Quiero volver al main.py viejo | `python archive/legacy_main_v3.py` (pero necesitarás las deps antiguas) |
| Hermes no arranca | `~/.hermes/bin/tirith` es el binario. Verifica que está en tu PATH. |
