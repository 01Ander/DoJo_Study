# ⛩️ DoJo Study: High Performance Engineering Framework v4.3.0

DoJo Study es un framework de aprendizaje inmersivo y de alto rendimiento diseñado para la formación rigursa de perfiles en **Data & Automation Engineering**. Basado en la metodología de **Aislamiento Estructural de Misiones**, garantiza que el código, los datos y la teoría residan en entornos desacoplados para simular sprints reales de ingeniería.

## 🎯 El Objetivo
El sistema busca eliminar la brecha entre la educación académica y el entorno profesional, integrando la **justificación económica y el valor de negocio (ROI)** como requisitos técnicos tan estrictos como la funcionalidad del código.

---

## 🚀 Quick Start

### 1. Requisitos Previos
- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** instalado y corriendo.
- Cuenta en **[OpenRouter](https://openrouter.ai)** con API key configurada.
- (Opcional) **[Ollama](https://ollama.com/)** como fallback local con `gemma4:e4b`.

### 2. Instalación de Hermes Agent
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup  # Configura OpenRouter API key y modelo default
```

### 3. Configurar DoJo Skills
Agrega el directorio de skills del DoJo a tu configuración de Hermes:
```yaml
# En ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/Documents/DoJo/DoJo_Study/dojo_agent/skills
```

### 4. Modelos Configurados

| Rol | Modelo | Costo |
|---|---|---|
| **Tutor / Reviewer** | Qwen3.6 Plus (OpenRouter) | $0.325 / $1.95 per M tokens |
| **Scribe** (auto-logging) | Gemma 4 31B (OpenRouter) | **FREE** |
| **Architect** | Gemini 3.1 Pro / Opus 4.6 | Premium |
| **Fallback** | Gemma 4 e4b (Ollama local) | $0 |

### 5. Ejecución
```bash
cd ~/Documents/DoJo/DoJo_Study
hermes  # Inicia el agente con contexto del DoJo
```

### 6. Comandos Básicos
```bash
# Personalidades (antes: /mode)
/personality dojo-tutor      # Instructor + Domain Shifting
/personality dojo-reviewer   # Pair Programmer Socrático
/personality dojo-architect  # Visión macro + debate

# Skills del DoJo
/dojo-start py-basico B00   # Fijar campaña y misión activa
/dojo-log "Completé X..."   # Registrar en bitácora
/domain-shifting             # Cargar protocolo de analogías
/socratic-review             # Cargar protocolo socrático
/mini-rfc                    # Cargar template de diseño

# Cambio de modelo
/model openrouter/qwen/qwen3.6-plus    # Para coding
/model gemini-3.1-pro                   # Para arquitectura
```

---

## ⚙️ Metodología de Entrenamiento
El framework se basa en una estructura de progresión jerárquica y el estándar de **Topología Aislada**:

- **Campaigns (Campañas):** Rutas de aprendizaje temáticas (ej. `PY-POO-FINANCE`).
- **Missions (Misiones):** Unidades de trabajo desacopladas. Cada misión encapsula su propia lógica de ejecución en un subdirectorio `code/` independiente (src, tests, data).
- **Journals (Bitácoras):** Registros cronológicos de progreso, errores y reflexiones del estudiante.
- **Mini-RFCs:** Documentos de diseño previo obligatorios para la fase de arquitectura.

---

## 🤖 El DoJo Agent v4.0 (Multi-Agent sobre Hermes)

El sistema integra un ecosistema multi-agente sobre **Hermes Agent** (NousResearch) con personalidades especializadas y modelos cost-optimizados:

- **`dojo-tutor` (Instructor):** Provee teoría y ejemplos mediante "Domain Shifting" (analogías externas). Genera código funcional real para obligar al estudiante a "traducir" la lógica.
- **`dojo-reviewer` (Senior Reviewer):** Pair Programmer socrático. Bloquea el avance si no existe un contexto de negocio definido. Guía el código mediante preguntas, nunca con respuestas directas.
- **`dojo-architect` (Analista):** Visión sistémica del DoJo completo. Audita coherencia, propone refactorizaciones y debate sobre arquitectura y patrones de diseño.

### Auto-Logging (Scribe)
Después de cada interacción significativa, el agente delega automáticamente a un sub-agente (Gemma 4 31B, FREE) que registra un resumen en la bitácora de la misión activa.

---

## ✅ Definition of Done (DoD) Global
Para que un artefacto técnico sea considerado "completado":

1. **Business Justification:** El código debe resolver un problema real con un ROI definido.
2. **Architecture First:** El diseño debe estar documentado y validado antes de la primera línea de código.
3. **TDD & Type Safety:** Implementación obligatoria de Test-Driven Development y tipado fuerte con Mypy.
4. **English Friendly:** Toda la documentación técnica y el código se fomentan en formato "English friendly en primeras instancias, hasta que el operador maneje un mejor nivel de inglés".

---

## 📁 Estructura del Repositorio
- `/subjects` — Tracks de aprendizaje, campañas activas y misiones.
- `/dojo_agent/skills` — Skills de Hermes Agent para el DoJo (session-start, journal-log, etc.).
- `/templates` — Plantillas estandarizadas para misiones, campañas y registros diarios.
- `/docs` — Documentación operativa y manuales.
- `/archive` — Código legacy del agente monolítico v3.x.
- `.hermes.md` — Constitución del DoJo Agent (inyectada automáticamente por Hermes).
