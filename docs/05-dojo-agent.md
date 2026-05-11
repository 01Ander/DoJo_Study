# 05 - The DoJo Agent v5.1 (Hermes Agent — Mundodisco Edition)

## ¿Qué es el DoJo Agent?

Es el componente "vivo" e interactivo del ecosistema DoJo. Originalmente un script Python monolítico con RAG local, ha evolucionado a un agente ligero sobre **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (NousResearch) con personalidades y skills inspiradas en el Mundodisco de Terry Pratchett.

El objetivo del Agente es reducir la carga cognitiva (*Protocol Yellow*), actuando como personalidades especializadas que guían sin resolver, y como gatekeeper (DM) que audita el progreso antes de autorizar el Rite final.

> GNU Terry Pratchett.

---

## Arquitectura (Hermes Agent Runtime)

El sistema opera sobre Hermes Agent con tres pilares:

1. **Constitución (`.hermes.md`):** Archivo en la raíz del repo que Hermes inyecta automáticamente al abrir en este directorio. Contiene las reglas globales del DoJo, el Definition of Done, restricciones y la estructura del sistema.

2. **Personalidades (`~/.hermes/personalities/`):** Archivos Markdown que definen el comportamiento de cada modo de trabajo. Se cambian con `/personality`.

3. **Skills (`dojo_agent/skills/dojo/`):** Paquetes de instrucciones que Hermes carga on-demand como slash commands. Versionados en el repo con git.

---

## Personalidades de Operación (`/personality`)

### 🧙 `/personality wizard` (El Mago — Adquisición Conceptual)

Inspirado en los magos de la Universidad Invisible. Domina el conocimiento arcano y enseña con **Domain Shifting** obligatorio — da ejemplos de código funcional pero en un dominio completamente distinto al del ejercicio, forzando al Operador a traducir la lógica. Define Criterios de Aceptación y casos borde a testear. Tiene permiso para dar código y guías paso a paso. Flexibilidad bilingüe.

### 🧹 `/personality witch` (La Bruja — Headología / Pair Programming)

Inspirada en las brujas del Mundodisco. Practica **headología** — el método socrático con otro nombre. Nunca da la respuesta directa. Revisa código bajo Clean Architecture con 4 niveles de escalación progresiva (pregunta abierta → pista → referencia teórica → override del operador). Criterio MVP para evitar parálisis por análisis.

---

## Skills Disponibles

| Comando | Nombre | Función |
|---|---|---|
| `/scry [chronicle]` | Scry (Adivinación del DM) | Audita el progreso: verifica grimoire y quests, autoriza el Rite. Modo `--deep` para evaluación cualitativa. |
| `/scroll [idea]` | Scroll (Pergamino Rápido) | Captura atómica de ideas sin romper el deep work. Fire-and-forget. |

---

## Flujo Operativo

### 1. Despliegue
Abre tu consola en la raíz de `DoJo_Study` y arranca:
```bash
cd ~/Documents/DoJo/DoJo_Study
hermes
```
> Hermes lee `.hermes.md` automáticamente. Las reglas del DoJo se inyectan sin que hagas nada.

### 2. Elegir Personalidad
```
/personality wizard     # Necesito aprender teoría o ver ejemplos
/personality witch      # Voy a codear y necesito pair programming socrático
```

### 3. Flujo Académico (Capítulos)
El avance por los capítulos es offline:
```
📖 Leer lore/Cap-N en Obsidian
✏️  Completar quests/Cap-N en VS Code
📓 Escribir grimoire.md en Obsidian
🔄 Repetir
```

### 4. Verificar Progreso (DM Gate)
Cuando creas que completaste todos los capítulos:
```
/scry PY-POO
```
> El DM verifica tu grimoire y tus quests. Si todo pasa: Rite desbloqueado.

### 5. Rite (Proyecto Final)
Con el Rite desbloqueado, activa `/personality witch` para pair programming socrático.

---

## Referencia Rápida

| v3 (Legacy) | v4 (Hermes) | v5.1 (Mundodisco) |
|---|---|---|
| `python dojo_agent/main.py` | `hermes` | `hermes` |
| `/mode main` | `/personality dojo-tutor` | `/personality wizard` |
| `/mode work` | `/personality dojo-reviewer` | `/personality witch` |
| `/mode think` | `/personality dojo-architect` | Antigravity (externo) |
| `/start py-basico B00` | `/dojo-start py-basico B00` | Eliminado (flujo offline) |
| `/log mensaje` | `/dojo-log mensaje` | Eliminado (grimoire es el registro) |
| — | `/dojo-idea mensaje` | `/scroll mensaje` |
| — | — | `/scry PY-POO` |

---

> *Nota: El código legacy del agente monolítico (v3) está archivado en `archive/legacy_main_v3.py`. Las skills v4 están archivadas en `archive/agent_v4_skills/`.*
