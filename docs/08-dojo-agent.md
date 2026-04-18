# 08 - The DoJo Agent v4.0 (Hermes Agent)

## ¿Qué es el DoJo Agent?

Es el componente "vivo" e interactivo del ecosistema DoJo. Originalmente un script Python monolítico con RAG local, ha evolucionado a un ecosistema multi-agente sobre **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (NousResearch) — una plataforma profesional de agentes IA con herramientas, memoria persistente y delegación de sub-agentes.

El objetivo del Agente es reducir la carga cognitiva (*Protocol Yellow*), actuando como múltiples *Personalidades* especializadas dependiendo de tus necesidades de estudio y blindando el flujo técnico.

---

## Arquitectura (Hermes Agent Runtime)

El sistema opera sobre Hermes Agent con tres pilares:

1. **Constitución (`.hermes.md`):** Archivo en la raíz del repo que Hermes inyecta automáticamente al abrir en este directorio. Contiene las reglas globales del DoJo, el Definition of Done, restricciones anti-leakage y la estructura del sistema.

2. **Personalidades (`~/.hermes/personalities/`):** Archivos Markdown que definen el comportamiento de cada modo de trabajo. Se cambian con `/personality`.

3. **Skills (`dojo_agent/skills/dojo/`):** Paquetes de instrucciones y scripts que Hermes carga on-demand como slash commands (`/dojo-start`, `/dojo-log`, etc.). Versionados en el repo con git.

---

## Modelos LLM (Cost-Optimized via OpenRouter)

| Rol | Modelo | Costo | Cuándo |
|---|---|---|---|
| **Tutor / Reviewer** | Qwen3.6 Plus | $0.325 / $1.95 per M | Default, uso diario |
| **Scribe** (auto-logging) | Gemma 4 31B | **FREE** | Automático (sub-agente) |
| **Architect** | Gemini 3.1 Pro | Premium | Solo con `/model` explícito |
| **Fallback** | Gemma 4 e4b (Ollama) | $0 | Si OpenRouter cae |

---

## Personalidades de Operación (`/personality`)

Con el comando `/personality [NOMBRE]`, instruyes a Hermes para asumir un rol especializado:

* **`/personality dojo-tutor` (El Instructor / Adquisición Conceptual):** Explica teoría arquitectónica y conceptos. Utiliza **Domain Shifting** obligatorio — da ejemplos de código funcional pero en un dominio completamente distinto (videojuegos, zoológicos, cocina) para forzar la traducción de lógica. Define Criterios de Aceptación (DoD) y casos borde a testear. Tiene permiso para dar código y guías paso a paso. Flexibilidad bilingüe. *(Modelo: Qwen3.6 Plus)*

* **`/personality dojo-reviewer` (El Revisor Socrático / Pair Programming):** Revisa tu código bajo Clean Architecture (lee tu Mini-RFC) y actúa estrictamente bajo el **MÉTODO SOCRÁTICO**. Tiene prohibido darte soluciones literales. Valida el Contexto de Negocio (ROI) antes de aprobar áreas técnicas y evalúa TDD. 
  - *Criterio MVP:* Te da "luz verde" para codear cuando el diseño es suficiente.
  - *Override del Operador:* Si declaras explícitamente que ya tomaste la decisión, acepta tu autoridad y te deja avanzar. *(Modelo: Qwen3.6 Plus)*

* **`/personality dojo-architect` (El Arquitecto / Visión Macro):** Audita la coherencia de todo el sistema DoJo y tu progresión en campañas. Debate filosofía de ingeniería, rediseño de syllabus o propone refactorizaciones. Libertad total para dar opiniones directas. *(Modelo recomendado: Gemini 3.1 Pro via `/model`)*

---

## Flujo Operativo

### 1. Despliegue
Abre tu consola en la raíz de `DoJo_Study` y arranca:
```bash
cd ~/Documents/DoJo/DoJo_Study
hermes
```
> Hermes lee `.hermes.md` automáticamente. Las reglas del DoJo se inyectan sin que hagas nada.

### 2. Anclaje de Contexto
Fija tu misión activa para que el agente sepa en qué trabajas:
```
/dojo-start py-basico B00
```
> Esto carga `requirements.md` y las últimas entradas de `journal.md` al contexto activo.

### 3. Ejecución y Bitácoras
Registra tus avances manualmente:
```
/dojo-log No logro entender cómo funciona la herencia aquí. Voy a reiniciar mañana.
```
> Además, después de cada interacción significativa, el agente puede delegar automáticamente a un sub-agente Scribe (Gemma 4, FREE) que registra un resumen en tu journal.

### 4. Pausas y Cierres (Gestión de Misión)
Si precisas interrumpir tu sesión de *Deep Work*, usa:
```
/stop-sesion
```
> Persiste el contexto localmente en `.dojo-session.json` de manera que al usar `/dojo-start` después del receso, te proponga reanudar exactamente en el bloque que dejaste.

Cuando cumples todos los criterios *Definition of Done* de una misión, ciérrala con:
```
/dojo-done
```

### 5. Skills On-Demand
```
/domain-shifting     → Carga reglas de analogía de dominio
/socratic-review     → Carga protocolo socrático del Reviewer
/mini-rfc            → Carga template de diseño previo
```

---

## Referencia Rápida

| v3 (Legacy) | v4 (Hermes) |
|---|---|
| `python dojo_agent/main.py` | `hermes` |
| `/mode main` | `/personality dojo-tutor` |
| `/mode exercises` | `/personality dojo-tutor` (unificado) |
| `/mode work` | `/personality dojo-reviewer` |
| `/mode think` / `/mode global` | `/personality dojo-architect` |
| `/start py-basico B00` | `/dojo-start py-basico B00` |
| `/log mensaje` | `/dojo-log mensaje` |
| `/audit pregunta` | `/personality dojo-architect` + preguntar |

---

> *Nota: El código legacy del agente monolítico (v3) está archivado en `archive/legacy_main_v3.py` como referencia histórica.*
