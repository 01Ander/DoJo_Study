# ⛩️ DoJo Study — High Performance Engineering Framework

DoJo Study es un framework de aprendizaje inmersivo y de alto rendimiento diseñado para la formación rigurosa de perfiles en **Data & Automation Engineering**. Basado en la metodología de **Campaign as Course**, con nomenclatura inspirada en el Mundodisco de Terry Pratchett, garantiza que el conocimiento teórico, la práctica guiada y los proyectos finales residan en entornos desacoplados para asegurar una asimilación real.

> GNU Terry Pratchett.

## 🎯 El Objetivo
El sistema busca eliminar la brecha entre la educación académica y el entorno profesional, integrando la **justificación económica y el valor de negocio (ROI)** como requisitos técnicos tan estrictos como la funcionalidad del código.

---

## 🚀 Quick Start

### 1. Requisitos Previos
- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** instalado y corriendo.
- Cuenta en **[OpenRouter](https://openrouter.ai)** con API key configurada.

### 2. Configurar DoJo Skills
Agrega el directorio de skills del DoJo a tu configuración de Hermes:
```yaml
# En ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/Documents/DoJo/DoJo_Study/dojo_agent/skills
```

### 3. Ejecución
```bash
cd ~/Documents/DoJo/DoJo_Study
hermes  # Inicia el agente con contexto del DoJo
```

### 4. Comandos Básicos
```bash
# Personalidades (Arquetipos Mundodisco)
/personality wizard      # 🧙 El Mago — Instructor + Domain Shifting
/personality witch       # 🧹 La Bruja — Pair Programming Socrático (Headología)

# Skills (Hechizos)
/scry PY-POO             # 🔮 DM audita tu grimoire y autoriza el Rite
/scry PY-POO --deep      # 🔮 Auditoría cualitativa (síntesis Feynman)
/scroll "Idea rápida"    # 📜 Captura una idea sin romper el deep work
```

---

## ⚙️ Metodología de Entrenamiento (Campaign as Course)
El framework se basa en una estructura de progresión jerárquica con nomenclatura del Mundodisco:

- **Chronicles (Crónicas):** Rutas de aprendizaje modulares con tipología `CORE-SUBTEMA` (ej. `PY-POO`, `DE-ETL`).
- **Lore:** Capítulos teóricos pre-generados. El conocimiento arcano de la Biblioteca de la Universidad Invisible.
- **Quests:** Laboratorios prácticos con Testing Progresivo (niveles 1-5).
- **Grimoire:** Bitácora personal del Operador donde escribe con sus propias palabras (Técnica Feynman).
- **Rite:** El proyecto final — rito de paso que demuestra dominio total del lore.

---

## 🤖 El DoJo Agent (Hermes — Mundodisco Edition)

El sistema integra un agente sobre **Hermes Agent** (NousResearch) con personalidades inspiradas en el Mundodisco:

- **`wizard` (El Mago):** Provee teoría y ejemplos mediante "Domain Shifting" (analogías externas). Genera código funcional real para obligar al estudiante a "traducir" la lógica.
- **`witch` (La Bruja):** Practicante de headología (método socrático). Nunca da la respuesta directa — te hace descubrirla con preguntas. Pair programming para code review.

### Auditoría del DM (`/scry`)
Antes de acceder al Rite, el Dungeon Master escudriña tu grimoire y tus quests. Solo cuando el progreso es verificado, el Rite se desbloquea.

---

## 📅 Modelo de Rendimiento

| Día | Modo | Actividad |
|---|---|---|
| **Martes a Viernes** | Operador | Estudiar: lore → quests → grimoire. No se modifica el sistema. |
| **Lunes tarde/noche** | Arquitecto | Refactorización del framework (con Antigravity). |
| **Sábado y Domingo** | Descanso | Desconexión obligatoria. |

---

## ✅ Definition of Done (DoD) Global
Para que un artefacto técnico sea considerado "completado":

1. **Business Justification:** El código debe resolver un problema real con un ROI definido.
2. **Architecture First:** El diseño debe estar documentado y validado antes de la primera línea de código.
3. **TDD & Type Safety:** Implementación obligatoria de Test-Driven Development y tipado fuerte.
4. **English Friendly:** Documentación técnica y código en inglés profesional.

---

## 📁 Estructura del Repositorio
```text
DoJo_Study/
├── .hermes.md                          ← Constitución del DoJo Agent
├── README.md
├── CHANGELOG.md
├── subjects/python/chronicles/         ← Chronicles activas
│   ├── PY-POO/                         ← Chronicle actual
│   └── PY-BASICO/                      ← Chronicle completada (legacy)
├── dojo_agent/skills/dojo/             ← Skills de Hermes
│   ├── scry/                           ← /scry — Auditoría del DM
│   └── scroll/                         ← /scroll — Pergamino rápido
├── templates/                          ← Plantillas estandarizadas
├── docs/                               ← Documentación (00-07)
└── archive/                            ← Legacy (agent v3, skills v4)
```
