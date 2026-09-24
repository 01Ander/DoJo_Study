---
chronicle: CLOUD-AWS
area: cloud
paso_actual: completado
estado: finalizado
capitulo_actual: null
requiere_aprobacion_humana: false

contexto_minimo_requerido:
  - system/docs/09-generation-protocol.md
  - system/docs/04-campaign-as-course.md
  - system/docs/05-syllabus-maestro.md
  - system/templates/chronicle-template.md
---

# Roadmap de Generación — `CLOUD-AWS`

> **Instrucción para el modelo:** Este archivo es tu ÚNICA fuente de verdad sobre el estado de esta Chronicle. Léelo ANTES que cualquier otro archivo. El campo `contexto_minimo_requerido` te dice exactamente qué más leer para el paso actual.

## Estado Actual

| Campo | Valor |
|---|---|
| **Paso actual** | Completado |
| **Estado** | `finalizado` |
| **Capítulo en progreso** | — |
| **Requiere aprobación humana** | No |

---

## Notas del Paso 1 (Identificación del Subject)

> _Se completa durante el PASO 1. El generador documenta aquí las competencias extraídas del syllabus, prerequisites, prácticas transversales y Domain Shifting elegido._

**Competencias del Syllabus:**
- [x] Fundamentos de arquitectura cloud para ingeniería de datos.
- [x] AWS IAM: Creación de usuarios de servicio, roles, políticas de mínimo privilegio y manejo de credenciales mediante variables de entorno (sin hardcoding de llaves).
- [x] Amazon S3: Creación de buckets, particionamiento de carpetas por fecha (`year/month/day`), almacenamiento de payloads raw JSON y Parquet.
- [x] Amazon RDS: Aprovisionamiento y conexión segura a instancias administradas de PostgreSQL.
- [x] AWS Lambda: Funciones serverless para tareas ligeras de extracción y disparo de eventos.
- [x] Amazon CloudWatch: Monitoreo de logs de ejecución y configuración de alertas de fallo.

**Prerequisites (Chronicles anteriores):**
- `DE-PIPELINES`, `SQL-BASICO`, `PY-POO`, `PY-BASICO`

**Prácticas Transversales Integradas:**
- `GIT-CI` (Control de versiones & CI Automático)
- `ENG-INT` (Inglés Técnico Aplicado)
- `DQ` (Data Quality) heredado de DE-PIPELINES.

**Domain Shifting Elegido:**
- Dominio del lore: Logística y Monitoreo de Dragones de Pantano (Swamp Dragons).
- Dominio del Rite: E-commerce Startup B2B (Almacenamiento y procesamiento logístico de inventarios).

---

## Historial de Gates

> _Se actualiza automáticamente después de cada gate. Formato YAML._

```yaml
historial_gates:
  - gate: 5
    resultado: pass
    fecha: 2026-09-24
  - gate: 5
    resultado: fail
    fecha: 2026-09-24
    hallazgos:
      - capitulo: "Rite/requirements.md (Fases 3 y 5)"
        termino: "Incongruencia de Nomenclatura (quantity vs quantity_added)"
        tipo_error: "Incongruencia entre fases"
        detalle: "La Fase 3 pide insertar los datos en la columna 'quantity', pero la Fase 5 exige validar que el payload JSON contenga la llave 'quantity_added'. El esquema esperado choca entre fases, impidiendo que el pipeline fluya limpiamente."
        accion: "Unificar la nomenclatura a 'quantity' (o 'quantity_added') en ambas fases de rite/requirements.md."
      - capitulo: "Rite/requirements.md (Fases 4 y 5)"
        termino: "Incongruencia Arquitectónica (S3 Trigger vs HTTP Status Codes)"
        tipo_error: "Incongruencia conceptual"
        detalle: "La Fase 4 establece que el evento proviene de S3 (trigger asíncrono). Sin embargo, la Fase 5 exige retornar HTTP 'statusCode: 400/200/500'. Los eventos S3 no evalúan respuestas HTTP de Lambda (eso es propio de API Gateway). Mezclar esto es un error conceptual."
        accion: "Eliminar la exigencia de retornar statusCodes en la Fase 5. Reemplazarlo por 'lanzar excepciones formales (raise Exception)' para marcar el fallo real en CloudWatch."
  - gate: 5
    resultado: fail
    fecha: 2026-09-24
    hallazgos:
      - capitulo: "07-Rite"
        termino: "Scaffolding prohibido"
        tipo_error: "Formato incorrecto"
        detalle: "Se generaron archivos solution y tests en lugar de requirements.md en fases."
        accion: "Eliminar solución, reestructurar requirements.md en 5 fases desbloqueables, journal."
  - gate: 4
    resultado: pass
    fecha: 2026-09-24
  - gate: 3
    resultado: pass
    fecha: 2026-09-24
  - gate: 2
    resultado: pass
    fecha: 2026-09-24
  - gate: 2
    resultado: fail
    fecha: 2026-09-24
    hallazgos:
      - capitulo: "05"
        termino: "Analogía faltante"
        tipo_error: "Falta de densidad"
        detalle: "El Cap 05 es capítulo 03+ y solo tiene 1 analogía. La regla 9.4 del protocolo exige mínimo 2."
        accion: "Agregar 1 analogía adicional sobre ACID transactions usando el dominio Dragones de Pantano."
  - gate: 1
    resultado: pass
    fecha: 2026-09-24
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
- system/docs/04-campaign-as-course.md
- system/docs/05-syllabus-maestro.md
- system/templates/chronicle-template.md
```

### Paso 4 (Lore) — Se actualiza capítulo a capítulo
```
- system/docs/09-generation-protocol.md (solo sección 9: Reglas de Oro)
- system/docs/04-campaign-as-course.md (solo sección 2.1: Capa lore/)
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
- system/docs/04-campaign-as-course.md (solo sección 2.2: Capa quests/)
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
