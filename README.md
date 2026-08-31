# ⛩️ DoJo Study — High Performance Engineering Framework (v5.2)

DoJo Study es un framework de aprendizaje inmersivo y de alto rendimiento diseñado para la formación rigurosa hacia el perfil **Data Automation Engineer / Python Automation Developer / ETL Integration Developer**. Basado en la metodología de **Campaign as Course**, con nomenclatura inspirada en el Mundodisco de Terry Pratchett, garantiza que el conocimiento teórico, la práctica guiada y los proyectos finales residan en entornos desacoplados para asegurar una asimilación real y autónoma.

> GNU Terry Pratchett.

## 🎯 El Objetivo
Acelerar la inserción profesional hacia un **primer empleo remoto internacional** en ingeniería de automatización e integración de datos antes de mediados de 2027. El sistema elimina la brecha entre la educación tradicional y el entorno productivo real, integrando **Data Quality**, **TDD**, **Arquitectura modular** y **justificación de negocio (ROI)** como estándares no negociables.

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
/personality wizard      # 🧙 El Mago — Instructor + Domain Shifting (Analogías)
/personality witch       # 🧹 La Bruja — Pair Programming Socrático (Headología) & Mock Interviews

# Skills (Hechizos)
/scry SQL-BASICO         # 🔮 DM audita tu grimoire y autoriza el Rite
/scry SQL-BASICO --deep  # 🔮 Auditoría cualitativa Feynman profunda
/scroll "Idea rápida"    # 📜 Captura una idea sin romper el Deep Work
```

---

## ⚙️ Metodología de Entrenamiento (Campaign as Course)
El framework se basa en una estructura de progresión jerárquica con nomenclatura del Mundodisco:

- **Chronicles (Crónicas):** Cursos completos modulares con tipología `CORE-SUBTEMA` (ej. `PY-POO`, `SQL-BASICO`, `DE-PIPELINES`).
- **Lore:** Capítulos teóricos con *Domain Shifting* obligatorio. El conocimiento arcano de la Biblioteca de la Universidad Invisible.
- **Quests:** Laboratorios prácticos con Testing Progresivo (andamiaje de 5 niveles).
- **Grimoire:** Bitácora personal del Operador donde sintetiza conceptos con sus propias palabras (Técnica Feynman).
- **Rite:** El proyecto final integrador — rito de paso que demuestra dominio total del lore antes de avanzar.

---

## 🤖 El DoJo Agent (Hermes — Mundodisco Edition)

El sistema integra un agente sobre **Hermes Agent** (NousResearch) con personalidades inspiradas en el Mundodisco:

- **`wizard` (El Mago):** Provee teoría y ejemplos funcionales mediante *Domain Shifting* (analogías en dominios externos ajenos al problema).
- **`witch` (La Bruja):** Practicante de headología (método socrático). No escribe código de producción; guía al estudiante a descubrir los errores y conduce simulacros de entrevistas técnicas en inglés (*Mock Interviews*).

### Auditoría del DM (`/scry`)
Antes de acceder al Rite, el Dungeon Master escudriña el `grimoire.md` y los `quests/`. Solo cuando el progreso conceptual es verificado, el Rite se desbloquea.

---

## 📅 Modelo de Rendimiento

| Día / Momento | Modo | Actividad |
|---|---|---|
| **Fase Cero (Diario)** | English Commando | Sintonización de 30–60 min en inglés (Busuu, Duolingo, lectura técnica). |
| **Martes a Viernes** | Operador | Inmersión Deep Work: `lore/` → `quests/` → `grimoire.md` → `rite/`. |
| **Post-Gate SQL-BASICO** | Búsqueda Activa | Bloques de postulación activa (5-10 semanales) y Mock Interviews en inglés. |
| **Lunes tarde/noche** | Arquitecto | Mantenimiento y refactorización del framework (con Antigravity). |
| **Sábado y Domingo** | Descanso | Desconexión obligatoria (*Zero-Code Policy*). |

---

## ✅ Definition of Done (DoD) Global
Para que un artefacto técnico sea considerado completado:

1. **Business Justification:** El código resuelve un problema real con un ROI cuantificable.
2. **Architecture First:** El diseño está documentado y validado antes de escribir la primera línea de código.
3. **TDD & Data Quality:** Implementación obligatoria de Test-Driven Development (`pytest`), tipado estricto (`mypy`), validaciones de esquema/nulos y logging estructurado.
4. **Professional English:** Documentación técnica, código, commits, PRs y READMEs en inglés profesional.

---

## 📁 Estructura del Repositorio
```text
DoJo_Study/
├── .hermes.md                          ← Constitución del DoJo Agent (v5.2)
├── README.md                           ← Visión general del ecosistema
├── CHANGELOG.md                        ← Registro histórico de versiones
├── subjects/                           ← Divisiones de aprendizaje
│   ├── python/chronicles/              ← PY-POO (Done), PY-BASICO (Legacy)
│   └── sql/chronicles/                 ← SQL-BASICO (En curso)
├── dojo_agent/skills/dojo/             ← Skills atómicas de Hermes
│   ├── scry/                           ← /scry — Auditoría del DM
│   └── scroll/                         ← /scroll — Captura de ideas
├── templates/                          ← Plantillas estandarizadas de misiones y RFCs
├── docs/                               ← Documentación canónica (00 a 08)
│   ├── 03-syllabus-maestro.md          ← Syllabus 2.0 (100% Pre-Empleo)
│   └── 08-syllabus-post-empleo-fase2.md← Syllabus Fase 2 (Post-Empleo)
└── archive/                            ← Memoria histórica (agent v3, skills v4, v2 canada)
```
