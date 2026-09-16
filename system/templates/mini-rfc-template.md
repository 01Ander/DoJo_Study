# Mini-RFC: [Título del Módulo / Feature]

> **Instrucción:** Completa cada sección respondiendo las preguntas guía. No elimines las preguntas — respóndelas debajo. El Reviewer validará este documento antes de dar luz verde para codear.

---

## 1. Business Context (¿Por qué existe esto?)

**¿Qué problema del mundo real resuelve este código?**
> [Tu respuesta aquí]

**¿Quién se beneficia y cómo lo usaría?**
> [Tu respuesta aquí]

**ROI estimado** (ej: "Elimina X horas semanales de trabajo manual", "Reduce errores de Y tipo en Z%"):
> [Tu respuesta aquí]

---

## 2. Technical Scope (¿Qué hace exactamente?)

**Input:** ¿Qué recibe? (formato de archivo, tipo de datos, fuente)
> [Tu respuesta aquí]

**Output:** ¿Qué produce? (formato, destino, estructura)
> [Tu respuesta aquí]

**Funciones principales** (máximo 8 — si necesitas más, el scope es demasiado grande):

| # | Función | Responsabilidad (1 oración) | Input → Output |
|---|---------|----------------------------|----------------|
| 1 | `nombre_funcion()` | | → |
| 2 | | | → |
| 3 | | | → |

---

## 3. Architecture Decision (¿Cómo y por qué así?)

**Patrón elegido** (ej: Pipeline secuencial, Event-driven, Repository, etc.):
> [Tu respuesta aquí]

**¿Por qué este patrón y NO otro?** (Trade-offs explícitos):
> [Tu respuesta aquí]

**Diagrama de flujo de datos** (ASCII o descripción textual):
```
[Input] → [Paso 1] → [Paso 2] → [Output]
                ↓ (error)
          [Error Handler]
```

**Dependencias** (solo stdlib permitida en PY-BASICO):
> [Listar módulos: csv, json, datetime, collections, etc.]

---

## 4. Edge Cases & Error Strategy

**¿Qué puede salir mal?** Lista al menos 3 escenarios:

| # | Escenario | Estrategia |
|---|-----------|------------|
| 1 | | |
| 2 | | |
| 3 | | |

**Política de errores:** ¿Fallar rápido (raise) o fallar suave (log + continuar)?
> [Tu respuesta aquí]

---

## 5. Testing Strategy (TDD-First)

**¿Qué test escribo PRIMERO?** (el más simple que demuestre que la función core funciona):
> [Tu respuesta aquí]

**Tests mínimos requeridos** (al menos 3):

| # | Test | Qué valida | Tipo |
|---|------|-----------|------|
| 1 | `test_nombre()` | | Happy path |
| 2 | `test_nombre()` | | Edge case |
| 3 | `test_nombre()` | | Error handling |

---

## 6. Checklist de Aprobación (para el Reviewer)

- [ ] Business Context está definido y es concreto (no genérico)
- [ ] Funciones ≤ 8 y cada una tiene una sola responsabilidad
- [ ] Trade-offs están explicitados (no solo "es mejor así")
- [ ] Al menos 3 edge cases identificados con estrategia
- [ ] Test #1 definido (se puede escribir AHORA sin más diseño)
- [ ] Zero third-party libs (si aplica por campaña)

> **Reviewer:** Si todas las cajas están marcadas → 🟢 Luz verde para TDD.
> Si falta alguna → 🔴 Devolver al Operador con preguntas específicas.
