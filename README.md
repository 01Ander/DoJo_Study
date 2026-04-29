# ⛩️ DoJo Study: High Performance Engineering Framework v5.0.0 (Beta)

DoJo Study es un framework de aprendizaje inmersivo y de alto rendimiento diseñado para la formación rigurosa de perfiles en **Data & Automation Engineering**. Basado en la metodología de **Campaign as Course** (v5.0), garantiza que el conocimiento teórico, la práctica guiada y los proyectos finales residan en entornos desacoplados para asegurar una asimilación real.

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

## ⚙️ Metodología de Entrenamiento (v5.0: Campaign as Course)
El framework se basa en una estructura de progresión jerárquica y el estándar de **Topología Aislada**:

- **Campaigns (Campañas):** Rutas de aprendizaje modulares con tipología `CORE-SUBTEMA` (ej. `PY-POO`, `DE-ETL`).
- **Theory & Exercises:** Adquisición de conocimiento pre-generado y práctica guiada de Testing Progresivo (niveles 1-5).
- **Study Journals:** Bitácoras donde el estudiante escribe con sus propias palabras (Técnica Feynman) para consolidar conceptos.
- **Boss Project:** El proyecto final donde se integra todo lo aprendido en un artefacto monolítico con despliegue progresivo.

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
- `/subjects` — Tracks de aprendizaje y campañas activas.
- `/dojo_agent/skills` — Skills de Hermes Agent para el DoJo.
- `/templates` — Plantillas estandarizadas para el contenido de aprendizaje.
- `/docs` — Documentación oficial numerada del 00 al 07 (index, manifiesto, syllabus, campaign-as-course, etc.).
- `/archive` — Código legacy.
- `.hermes.md` — Constitución del DoJo Agent.
