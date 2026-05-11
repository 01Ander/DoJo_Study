# 06 - Guía de Operaciones (Hermes Agent — Mundodisco Edition)

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
/personality wizard       # Necesito aprender teoría o ver ejemplos (Domain Shifting)
/personality witch        # Voy a codear y necesito pair programming (Headología)
```

### Paso 3: Trabajar normalmente
Haz preguntas, pide reviews, debate la arquitectura. El agente se comporta según la personalidad activa:
- **Wizard**: Te da código real pero con *Domain Shifting* (dominio diferente al tuyo).
- **Witch**: Te hace preguntas socráticas (headología), **no** te da la respuesta ni código copiable.

### Paso 4: Verificar progreso antes del Rite
```
/scry PY-POO
```
> El DM audita tu grimoire y tus quests. Si todo pasa: Rite desbloqueado.

Para salir de Hermes, escribe `/exit`.

---

## ⚡ Comandos Rápidos (Cheat Sheet)

### 📋 Skills
| Comando | Qué hace |
|---|---|
| `/scry [chronicle]` | Auditoría del DM: valida grimoire y quests, autoriza el Rite. |
| `/scry [chronicle] --deep` | Auditoría cualitativa: evalúa la calidad de las síntesis Feynman. |
| `/scroll [idea]` | Captura una idea o bug rápidamente sin romper tu flujo de deep work. |

### 🎭 Personalidades
| Comando | Cuándo usarlo |
|---|---|
| `/personality wizard` | Necesito que me expliquen un concepto con ejemplos. |
| `/personality witch` | Necesito code review o pair programming socrático. |

---

## 📁 Estructura del Ecosistema

```text
~/Documents/DoJo/DoJo_Study/
├── .hermes.md                    ← Constitución Operativa (Hermes la lee automático)
├── README.md                     ← Índice del repo
├── CHANGELOG.md                  ← Historial de versiones del marco
│
├── subjects/python/campaigns/    ← Área principal de chronicles
│   └── PY-POO/
│       ├── chronicle.md          ← Descripción de alto nivel
│       ├── grimoire.md           ← Bitácora Feynman del Operador
│       ├── lore/                 ← Capítulos teóricos (la Biblioteca)
│       ├── quests/               ← Laboratorios prácticos
│       └── rite/                 ← Proyecto final (rito de paso)
│           ├── requirements.md
│           ├── journal.md
│           ├── src/
│           ├── tests/
│           └── data/
│
├── dojo_agent/skills/dojo/       ← Skills de Hermes (versionados en git)
│   ├── scry/                     ← `/scry` — Auditoría del DM
│   └── scroll/                   ← `/scroll` — Pergamino rápido de ideas
│
└── docs/                         ← Manuales y documentación maestra

~/.hermes/ (Fuera del Repo)
├── config.yaml                   ← Config de tu instancia (external_dirs)
├── .env                          ← API keys (OpenRouter)
└── personalities/                ← Archivos prompt de Personalidades
    ├── wizard.md                 ← El Mago (Tutor)
    └── witch.md                  ← La Bruja (Reviewer)
```

---

## 🚑 Protocolo de Triaje en Vivo

> Cuando detectes un bug o carencia en la infraestructura del DoJo DURANTE una sesión de deep work técnica, usa este árbol de decisión. **NO abras "dos frentes" de trabajo.**

```text
¿El bug de infraestructura me BLOQUEA continuar mi código?
│
├── SÍ → ¿Lo puedo parchear en < 5 minutos?
│         │
│         ├── SÍ → ⚡ Parchea en vivo.
│         │
│         └── NO → 🛑 STOP. Registra: `/scroll BUG SISTEMA: [descripción]`
│                   Usa workaround temporal y sigue. Arreglarlo el próximo lunes.
│
└── NO → 💡 Registra la mejora: `/scroll Mover configuración de X a Y` y SIGUE.
          No abras archivos de configuración. No investigues. Vuelve al código.
```

### ❓ Troubleshooting de Hermes
- **Los skills no aparecen en `/skills`:** Verifica que `~/.hermes/config.yaml` tenga la variable `external_dirs` apuntando a `~/Documents/DoJo/DoJo_Study/dojo_agent/skills`.
- **Las personalidades fallan:** Revisa que los archivos se encuentren en `~/.hermes/personalities/` (`wizard.md`, `witch.md`).
- **Fallo de LLM:** Revisa tu cuota o `OPENROUTER_API_KEY` en `~/.hermes/.env`.
