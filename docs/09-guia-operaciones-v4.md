# 09 - Guía de Operaciones (Hermes Agent)

> Este documento es tu referencia rápida (Wiki Operativa). Si te pierdes en los comandos o flujos del DoJo, vuelve aquí.

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
/personality dojo-reviewer    # Voy a codear y necesito pair programming socrático
/personality dojo-architect   # Quiero analizar el ecosistema macro o debatir diseño
```

### Paso 3: Fijar tu misión activa
```
/dojo-start py-POO-FINANCE M00
```
> Esto carga el `requirements.md` y el `journal.md` de esa misión al contexto. El agente ahora sabe exactamente en qué estás trabajando.

### Paso 4: Trabajar normalmente
Haz preguntas, pide reviews, debate la arquitectura. El agente se comporta según la personalidad activa:
- **Tutor**: Te da código real pero con *Domain Shifting* (dominio diferente al tuyo, ej. zoologico vs finanzas).
- **Reviewer**: Te hace preguntas socráticas, **no** te da la respuesta ni código copiable.
- **Architect**: Te provee opiniones directas, análisis y refactorización a gran escala.

### Paso 5: Registrar avances
```
/dojo-log Completé el primer test del módulo. Descubrí que necesito manejar el edge case de lista vacía.
```
> Escribe en el `journal.md` de la misión con timestamp dinámico garantizando trazabilidad.

### Paso 6: Pausar o Terminar
Si vas a pausar tu bloque:
```
/stop-sesion
```
Si vas a cerrar tu proyecto/misión del todo:
```
/dojo-done
```
Para salir de Hermes, escribe `/exit`.

---

## ⚡ Comandos Rápidos (Cheat Sheet)

### 📋 Misiones y Skills
| Comando | Qué hace |
|---|---|
| `/dojo-start <campaña> <misión>` | Fija el contexto de la misión actual. |
| `/dojo-log <mensaje>` | Registra tu avance o fricciones en el `journal.md`. |
| `/stop-sesion` | Pausa el bloque de Deep Work guardando tu estado actual. |
| `/dojo-done` | Cierra formalmente la misión y te invita a pasar a la siguiente. |
| `/dojo-idea <mensaje>` | Captura ideas o bugs que te sacan del flujo para verlos luego. |

### 🛠 Protocolos Especiales
| Comando | Requisito | Función |
|---|---|---|
| `/domain-shifting` | `/personality dojo-tutor` | Pide explicaciones teóricas con analogías ajenas. |
| `/socratic-review` | `/personality dojo-reviewer` | Solicita una revisión profunda a tu código bajo TDD. |
| `/mini-rfc` | `/personality dojo-reviewer` | Carga un template estructurado para diseñar software. |

### 🧠 Cambio de Modelos
| Modelo | Costo | Escenario Ideal |
|---|---|---|
| **Qwen3.6 Plus** (default) | Muy Bajo | Tutor, Reviewer, operaciones del día a día. |
| **Gemini 3.1 Pro** | Premium | Arquitectura pura. Se activa al invocar `/architect`. |
| **Gemma 4 31B** | **FREE** | Auto-logging (Scribe sub-agente). Funciona en background. |

> **Tip:** Tras debatir con `dojo-architect` en Gemini, recuerda volver al modelo operativo con `/model openrouter/qwen/qwen3.6-plus`.

---

## 📁 Estructura del Ecosistema Operable

```text
~/Documents/DoJo/DoJo_Study/
├── .hermes.md                    ← Constitución Operativa (Hermes la lee automático)
├── README.md                     ← Índice del repo
├── CHANGELOG.md                  ← Historial de versiones del marco
│
├── subjects/python/campaigns/    ← Área principal de construcción y campañas
│   ├── PY-POO-FINANCE/missions/
│   │   ├── M00/code/             ← Entorno de ejecución puro
│   │   ├── M00/requirements.md   ← Lo que carga /dojo-start
│   │   └── M00/journal.md        ← Lo que actualiza /dojo-log
│   └── ...
│
├── dojo_agent/skills/dojo/       ← Habilidades de Hermes (versionados en git)
│   ├── session-start/            ← `/dojo-start`
│   ├── session-pause/            ← `/stop-sesion`
│   ├── mission-done/             ← `/dojo-done`
│   ├── journal-log/              ← `/dojo-log`
│   ├── idea-capture/             ← `/dojo-idea`
│   └── ...
│
└── docs/                         ← Manuales y documentación maestra

~/.hermes/ (Fuera del Repo)
├── config.yaml                   ← Config de tu instancia (external_dirs)
├── .env                          ← API keys (OpenRouter)
└── personalities/                ← Archivos prompt de Personalidades
```

---

## 🚑 Protocolo de Triaje en Vivo

> Cuando detectes un bug o carencia en la infraestructura del DoJo DURANTE una sesión de deep work técnica, usa este árbol de decisión. **NO abras "dos frentes" de trabajo.**

```text
¿El bug de infraestructura me BLOQUEA continuar mi código de la misión?
│
├── SÍ → ¿Lo puedo parchear en < 5 minutos?
│         │
│         ├── SÍ → ⚡ Parchea en vivo. Registra: `/dojo-log Hotfix en entorno: [tu_acción]`
│         │
│         └── NO → 🛑 STOP. Registra: `/dojo-idea BUG SISTEMA: [descripción]`
│                   Usa workaround temporal o mockup y sigue. Agenda arreglarlo para la próxima ventana de Modo Arquitecto.
│
└── NO → 💡 Registra la mejora: `/dojo-idea Mover configuración de X a Y` y SIGUE TU CÓDIGO.
          No abras archivos de configuración. No investigues. Vuelve al código.
```

### ❓ Troubleshooting de Hermes
- **Los skills no aparecen en `/skills`:** Verifica que `~/.hermes/config.yaml` tenga la variable `external_dirs` apuntando a `~/Documents/DoJo/DoJo_Study/dojo_agent/skills`.
- **Las personalidades fallan:** Revisa que los archivos de prompt se encuentren físicamente en `~/.hermes/personalities/`.
- **Fallo de LLM:** Revisa tu cuota o `OPENROUTER_API_KEY` en `~/.hermes/.env`.
