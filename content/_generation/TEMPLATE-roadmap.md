---
chronicle: <CHRONICLE-CODE>
area: <AREA>
paso_actual: 0
estado: pendiente
capitulo_actual: null
requiere_aprobacion_humana: false

contexto_minimo_requerido:
  - system/docs/09-generation-protocol.md
  - system/docs/07-campaign-as-course.md
  - system/docs/03-syllabus-maestro.md
---

# Roadmap de Generación — `<CHRONICLE-CODE>`

> **Instrucción para el modelo:** Este archivo es tu ÚNICA fuente de verdad sobre el estado de esta Chronicle. Léelo ANTES que cualquier otro archivo. El campo `contexto_minimo_requerido` te dice exactamente qué más leer para el paso actual.

## Estado Actual

| Campo | Valor |
|---|---|
| **Paso actual** | 0 — Carga de Contexto |
| **Estado** | `pendiente` |
| **Capítulo en progreso** | — |
| **Requiere aprobación humana** | No |

---

## Notas del Paso 1 (Identificación del Subject)

> _Se completa durante el PASO 1. El generador documenta aquí las competencias extraídas del syllabus, prerequisites, prácticas transversales y Domain Shifting elegido._

**Competencias del Syllabus:**
- [ ] _Pendiente_

**Prerequisites (Chronicles anteriores):**
- _Pendiente_

**Prácticas Transversales Integradas:**
- _Pendiente_

**Domain Shifting Elegido:**
- Dominio del lore: _Pendiente_
- Dominio del Rite: _Pendiente_

---

## Historial de Gates

> _Se actualiza automáticamente después de cada gate. Formato YAML._

```yaml
historial_gates: []
# Ejemplo de un gate completado:
# - gate: 1
#   resultado: pass
#   fecha: 2026-MM-DD
#
# Ejemplo de un gate fallido:
# - gate: 2
#   resultado: fail
#   fecha: 2026-MM-DD
#   hallazgos:
#     - capitulo: "02"
#       termino: "particionado"
#       tipo_error: "Tipo 2 — término sin definir"
#       detalle: "Se usa en el ejemplo de negocio pero nunca se define qué/cómo/por qué."
#       accion: "Agregar sección '## Particionado de Datos' en Cap 02 con definición completa."
```

---

## Contexto Mínimo Requerido por Paso

> _El generador actualiza esta sección conforme avanza. Solo se listan los archivos necesarios para el paso actual._

### Paso 0-3 (Setup y Scope)
```
- system/docs/09-generation-protocol.md
- system/docs/07-campaign-as-course.md
- system/docs/03-syllabus-maestro.md
- system/templates/chronicle-template.md
```

### Paso 4 (Lore) — Se actualiza capítulo a capítulo
```
- system/docs/09-generation-protocol.md (solo sección 9: Reglas de Oro)
- system/docs/07-campaign-as-course.md (solo sección 2.1: Capa lore/)
- content/subjects/<area>/chronicles/<CODE>/chronicle.md
- content/_generation/<CODE>/matriz-trazabilidad.md
# Si es Cap N > 0, agregar los capítulos anteriores para coherencia:
# - content/subjects/<area>/chronicles/<CODE>/lore/00-titulo.md
# - content/subjects/<area>/chronicles/<CODE>/lore/01-titulo.md
# ...
```

### Paso 5 (Grimoire)
```
- system/docs/09-generation-protocol.md (solo sección 3: PASO 5)
- content/subjects/<area>/chronicles/<CODE>/lore/ (todos los capítulos)
- content/_generation/<CODE>/matriz-trazabilidad.md
```

### Paso 6 (Quests)
```
- system/docs/09-generation-protocol.md (solo sección 3: PASO 6)
- system/docs/07-campaign-as-course.md (solo sección 2.2: Capa quests/)
- content/subjects/<area>/chronicles/<CODE>/lore/ (todos los capítulos)
- content/subjects/<area>/chronicles/<CODE>/grimoire.md
```

### Paso 7 (Rite)
```
- system/docs/09-generation-protocol.md (solo sección 3: PASO 7)
- content/subjects/<area>/chronicles/<CODE>/chronicle.md
- content/_generation/<CODE>/matriz-trazabilidad.md
```

### Gates (Auditoría)
```
# Cada gate declara su propio contexto mínimo en la sección 4 del protocolo.
# El auditor solo lee lo indicado ahí, nunca el razonamiento de generación.
```
