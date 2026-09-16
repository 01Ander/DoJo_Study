# 🗺️ Plan de Acción — DoJo v5.0 Beta (`PY-POO`)

> **Fecha:** 2026-04-29
> **Estado:** ACTIVO
> **Objetivo:** Cerrar PY-POO v4 limpiamente y lanzar `PY-POO` como beta del nuevo modelo "Campaign as Course"
> **RFC de referencia:** `ideas/proposal-study-guide-layer.md` (v3, APROBADO)
> **Tipología:** `CORE-SUBTEMA` → La nueva campaign se llamará `PY-POO` (no `PY-POO-FINANCE-V2`)

---

## Estándar de Calidad del Contenido Generado (CRÍTICO)

Antes del plan de fases, este estándar aplica a TODO archivo de `theory/` y `exercises/` que se genere. Si un archivo no lo cumple, se rechaza y se regenera.

Cada archivo debe ser tan completo que el Operador pueda ejecutarlo sin preguntar al LLM. El LLM durante la sesión de estudio solo recibe preguntas muy puntuales o auditorías del `study-journal.md`.

**Checklist de calidad por archivo:**
- [ ] ¿Incluye comandos de instalación exactos? (`pip install pytest==8.x`, no "instala pytest")
- [ ] ¿Incluye verificación post-instalación? (`python -m pytest --version`)
- [ ] ¿Especifica rutas exactas desde la raíz del proyecto?
- [ ] ¿Incluye el comando exacto para ejecutar? (`pytest exercises/01-abstractions/ -v`)
- [ ] ¿Muestra exactamente qué output esperar en la terminal si salió bien?
- [ ] ¿Documenta errores comunes con su traceback real y solución?
- [ ] ¿El árbol de carpetas está dibujado (no descrito en prosa)?
- [ ] ¿Los ejemplos de código están en dominio diferente al del proyecto?
- [ ] ¿Cada bloque de código es ejecutable sin modificaciones?

---

## Fase 1 — Cierre Formal de PY-POO-FINANCE v4

> **Quién:** Operador
> **Cuándo:** Antes de generar cualquier contenido v5

### 1.1 Actualizar status de B01

Editar `subjects/python/campaigns/PY-POO-FINANCE/missions/B01/requirements.md`:

```
Status: ❌ Descartada
```

Añadir en `## Architectural/Friction Notes`:
```
[2026-04-29] B01 descartada. Causa: inestabilidad del provider DeepSeek v4-flash
(generó código sin pedirlo — violación de Regla 3). Misión no completada por el
Operador. Se cierra PY-POO v4 y se relanza como beta del sistema v5.
```

### 1.2 Actualizar status de la campaign

Editar `subjects/python/campaigns/PY-POO-FINANCE/campaign.md`:
```
Status: 🔒 Archivada (v4) — Ver campaigns/PY-POO para el beta v5
```

### 1.3 Commit del RFC y cierre

```bash
cd ~/Documents/DoJo/DoJo_Study
git add ideas/proposal-study-guide-layer.md
git add ideas/action-plan-dojo-v5-beta.md
git add subjects/python/campaigns/PY-POO-FINANCE/
git commit -m "docs: close PY-POO v4 (B01 discarded) + RFC v3 Campaign as Course approved"
```

### 1.4 Actualizar CHANGELOG.md

Añadir entrada `[5.0.0-proposal]` documentando la decisión arquitectónica y el inicio del beta.

---

## Fase 2 — Generación (Docs → Scaffold → Contenido)

> **Quién:** LLM frontera externo (Antigravity/Gemini 2.5 Pro) en ventana de Arquitecto
> **Output:** Docs fundacionales actualizados + archivos `.md` estáticos listos para usar sin conexión

> ⚠️ **Skills v4.3 intactas:** Este plan NO modifica ninguna skill existente. La actualización de skills (`/dojo-ask`, rol del DM en `.hermes.md`) se ejecuta en la **Fase 4 post-beta**, una vez validado el modelo pedagógico. Modificar infraestructura antes de validar el contenido introduce ruido en los resultados del beta.

### 2.1 Documentos Fundacionales (PRIMERO)

Antes de generar el contenido de la campaign, actualizar la documentación del sistema para que las nuevas mecánicas queden formalizadas como fuente de verdad.

| Acción | Archivo | Qué cambia |
|--------|---------|------------|
| **Crear** | `docs/12-campaign-as-course.md` | Doc fundacional del nuevo modelo. Mecánicas de `theory/`, `exercises/`, `project/`, `study-journal.md`, ciclo por capítulo, rol del DM |
| **Deprecar** | `docs/02-misiones-framework.md` | Añadir banner `> ⚠️ DEPRECADO en v5.0. Ver docs/12-campaign-as-course.md` |
| **Deprecar** | `docs/04-estructura-campanas.md` | Mismo banner. Tipología de campaigns actualizada a `CORE-SUBTEMA` |
| **Deprecar** | `docs/06-manual-operativo-misiones.md` | Mismo banner |
| **Actualizar** | `docs/08-dojo-agent.md` | Rol del agente: de Tutor a DM/Auditor. Skill `/dojo-ask` documentada |
| **Renumerar** | `docs/` (todos) | Los 3 docs deprecados quedan marcados pero se renumeran los activos para mantener secuencia limpia. Nueva numeración de docs activos: `00-index`, `01-dojo-core`, `02-sistema-energia`, `03-syllabus-maestro`, `04-protocol-yellow`, `05-dojo-agent`, `06-guia-operaciones-v5`, `07-campaign-as-course` |
| **Actualizar** | `docs/00-index.md` | Reflejar nueva numeración, marcar deprecados con `~~tachado~~`, añadir entrada de `07-campaign-as-course.md` |
| **Actualizar** | `README.md` (raíz) | Sección `📁 Estructura del Repositorio` actualizada con nueva numeración de docs y referencia a la nueva tipología de campaigns `CORE-SUBTEMA` |

**Contenido mínimo de `docs/12-campaign-as-course.md`:**
- Descripción del modelo Campaign as Course
- Ciclo por capítulo (diagrama ASCII)
- Anatomía de `theory/`, `exercises/`, `study-journal.md`, `project/`
- Rol del DM: funciones, `/dojo-ask`, Estándar de Respuesta Académica
- Tipología de campaigns: `CORE-SUBTEMA` con ejemplos válidos/inválidos
- Referencia al RFC: `ideas/proposal-study-guide-layer.md`

### 2.2 Scaffold de la nueva campaign

```bash
cd ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns

mkdir -p PY-POO/theory
mkdir -p PY-POO/exercises/{00-classes,01-abstractions,02-entities,03-transformations,04-orchestration,05-testing,06-validation,07-cli}
mkdir -p PY-POO/project/{src,tests,data}
touch PY-POO/study-journal.md
touch PY-POO/project/journal.md
touch PY-POO/campaign.md
touch PY-POO/project/requirements.md
```

**Estructura resultante:**
```
PY-POO/
├── campaign.md
├── study-journal.md
├── theory/
├── exercises/
│   ├── 00-classes/
│   ├── 01-abstractions/
│   ├── 02-entities/
│   ├── 03-transformations/
│   ├── 04-orchestration/
│   ├── 05-testing/
│   ├── 06-validation/
│   └── 07-cli/
└── project/
    ├── requirements.md
    ├── journal.md
    ├── src/
    ├── tests/
    └── data/
```

### 2.3 Generar theory/ — El Libro (8 capítulos)

Orden de generación. Prioridad beta: **00 → 01 → 05** primero (mayor gap en v4).

| # | Archivo | Conceptos clave | Dominio del ejemplo |
|---|---------|-----------------|---------------------|
| 00 | `00-from-functions-to-classes.md` | `class`, `__init__`, `self`, métodos de instancia | Reservas de hotel |
| 01 | `01-abstract-classes-and-interfaces.md` | `abc`, `ABC`, `abstractmethod`, contratos | Notificaciones (email/SMS/push) |
| 02 | `02-domain-entities-and-polymorphism.md` | Herencia, `super()`, polimorfismo | Empleados (full-time/contractor) |
| 03 | `03-data-transformation-patterns.md` | Stateless, `collections.defaultdict` | Análisis de logs de servidor |
| 04 | `04-output-and-orchestration.md` | Orchestrator, dependency injection | Reportes (PDF/CSV/JSON) |
| 05 | `05-testing-with-pytest.md` | GIVEN/WHEN/THEN, fixtures, mocks, TDD | Carrito de compras |
| 06 | `06-validation-and-logging.md` | Pydantic, `logging`, error handling | Formularios de registro |
| 07 | `07-cli-applications.md` | Typer/Click, argumentos, `CliRunner` | To-do app CLI |

> ⚠️ **Nota al generador:** El dominio de la campaign es finanzas/ETL. Los ejemplos en `theory/` NUNCA usan finanzas. Usar los dominios de la tabla.

**Cada capítulo debe incluir obligatoriamente:**
- Árbol de archivos exacto para los ejercicios del capítulo
- Comando de setup del entorno si aplica al capítulo
- Sección "Conexión con Testing" con el test más básico del concepto
- "Mapa de Ejercicios" al final: lista exacta de los `.md` en `exercises/` para ese capítulo

### 2.4 Generar exercises/ — Los Ejercicios

Por capítulo: **3-5 ejercicios**, con ≥1 de tipo B (Testing — Desbloqueo Progresivo).

Templates en: `ideas/proposal-study-guide-layer.md` → Sección 4.2

**Gradiente de testing por capítulo:**
- Cap 00-01: Nivel 1-2 (leer y describir)
- Cap 02-04: Nivel 2-3 (describir y estructura)
- Cap 05-07: Nivel 4-5 (fill-blanks y desde cero)

**A partir de Cap 03:** Incluir 1 "Ejercicio de Revisión" (Spaced Repetition) de un capítulo anterior.

### 2.5 Generar project/ — El Boss Final

Equivalente funcional a M00-M04-B01 de v4, como proyecto monolítico con fases desbloqueables:

```
Fase 1: Extraction Layer  ← Cap 00 + 01
  - AbstractExtractor + CSVExtractor
  - 3 tests obligatorios

Fase 2: Domain Entities   ← Cap 02
  - Transaction, Income, Expense
  - Tests de polimorfismo

Fase 3: Transformation Engine ← Cap 03
  - AnalyticsEngine stateless
  - Tests de calculate_report + aggregate_by_category

Fase 4: Orchestration + CLI ← Cap 04 + 07
  - PipelineOrchestrator + Typer CLI
  - Tests con CliRunner
```

**Condición de acceso:** DM certifica `study-journal.md` completo antes de abrir el Boss.

---

## Fase 3 — Ejecución Beta

> **Quién:** Operador
> **Cuándo:** Cuando Fase 2 tenga al menos Cap 00, 01, 05 y sus ejercicios

### Flujo por capítulo
```
📖 Leer theory/Cap-N  (sin LLM)
     ↓
✏️  Completar exercises/Cap-N  (soluciones desbloqueables)
     ↓
📓 Escribir entrada en study-journal.md
     ↓
Repetir con el siguiente capítulo
     ↓
DM audita study-journal.md → autoriza Boss Final
     ↓
🔨 Boss Final con Reviewer como único apoyo
```

### Métricas a capturar en cada entrada del study-journal.md

```markdown
- Tiempo de lectura del capítulo: __min
- Tiempo en ejercicios: __min
- Veces que recurrí al LLM: __ (objetivo: ≤ 2)
- Fricción del capítulo: __/10
- ¿Pude hacer el ejercicio de testing sin ver la solución? Sí/No
```

Estas métricas son el dataset de validación del sistema v5.

---

## Fase 4 — Retrospectiva y Formalización

> **Cuándo:** Al completar el Boss Final
> **Output:** Decisión sobre adopción de v5 como estándar

### Preguntas de validación

- ¿El Operador llegó al Boss con menos fricción que en v4?
- ¿Los tests dejaron de ser un muro? (¿completó algún ejercicio Nivel 4-5 sin ayuda?)
- ¿Recurrió a Tutor ≤ 2 veces por capítulo durante la teoría?
- ¿El `study-journal.md` fue útil o una carga?

### Si el beta es exitoso → Formalización v5.0

- [ ] Crear templates maestros: `theory-chapter-template.md`, `exercise-template.md`, `study-journal-template.md`
- [ ] Actualizar `.hermes.md` con rol del DM (Gatekeeper) y skill `/dojo-ask`
- [ ] Implementar skill `/dojo-ask` en `dojo_agent/skills/`
- [ ] Registrar `CHANGELOG.md` como v5.0.0
- [ ] Actualizar `subjects/python/README.md` con la nueva tipología `CORE-SUBTEMA`

> Docs fundacionales (`12-campaign-as-course.md`, deprecaciones) ya fueron actualizados en Fase 2.1 — no repetir aquí.

---

## Próximo Paso Inmediato

**Ahora:** Fase 1 — Editar B01 + campaign.md + git commit.

**Próxima ventana de Arquitecto:** Generar `theory/00`, `theory/01`, `theory/05` y sus ejercicios. Son los tres capítulos que cubren el mayor gap de PY-POO v4.
