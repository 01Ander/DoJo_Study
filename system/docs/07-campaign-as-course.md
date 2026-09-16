# 07 - Campaign as Course (Mundodisco Edition)

> **RFC de referencia:** `ideas/proposal-study-guide-layer.md`
> GNU Terry Pratchett.

Este documento define la arquitectura "Campaign as Course", el modelo pedagógico estándar del DoJo con la nomenclatura Mundodisco.

## 0. El Glosario Mundodisco (Nomenclatura Oficial)

Para mantener la identidad del DoJo mientras adoptamos un modelo académico riguroso, esta es la traducción oficial de términos, inspirada en el Mundodisco de Terry Pratchett:

| Término Disco | Equivalente Académico | Descripción en v5.1 |
|---|---|---|
| **Chronicle** | Curso / Materia | Ruta completa de aprendizaje (ej. `PY-POO`). Antes: Campaign. |
| **Lore** | Lección Teórica | Archivos `.md` en `lore/` con conceptos. La Biblioteca de la UU. |
| **Quest** | Laboratorio / Ejercicio | Práctica guiada en `quests/` |
| **Grimoire** | Bitácora Feynman | Documento de síntesis del Operador (`grimoire.md`) |
| **Rite** | Proyecto Integrador | Rito de paso que demuestra dominio total, en `rite/`. Antes: Boss. |
| **Wizard** | Tutor / Instructor | Personalidad que enseña con Domain Shifting |
| **Witch** | Reviewer / Pair Programmer | Personalidad socrática (headología) |
| **Scry** | Auditoría del DM | Skill que valida progreso y autoriza el Rite |
| **Scroll** | Captura de idea | Skill atómica de registro rápido |
| **Dungeon Master (DM)** | Auditor / Gatekeeper | El agente que verifica el `grimoire.md` vía `/scry` |
| **Operator** | Estudiante | Quien ejecuta el aprendizaje |

---

## 1. Topología `CORE-SUBTEMA`

Las chronicles usan tipología estrictamente `CORE-SUBTEMA`.

**Ejemplos Válidos:**
- `PY-POO` (Python Object Oriented)
- `DE-ETL` (Data Engineering ETLs)
- `PY-API` (Python APIs)

**Ejemplos Inválidos:**
- `PY-POO-LEGACY`
- `DE-ETL-V2`

## 2. Anatomía de una Chronicle

La estructura adopta un enfoque de Curso + Laboratorio:

```
CHRONICLE/
├── chronicle.md         ← Descripción de alto nivel
├── grimoire.md          ← Bitácora académica (Técnica Feynman)
├── lore/                ← Libro de texto estático (.md)
├── quests/              ← Laboratorios atómicos y testing
└── rite/                ← Rite (proyecto final)
    ├── journal.md       ← Bitácora clásica técnica (solo para el Rite)
    └── requirements.md  ← Requisitos y fases del Rite
```

### 2.1 La Capa `lore/`
Actúa como un libro de texto. Son archivos Markdown con la teoría, código de ejemplo, e instrucciones de entorno.
- **Regla de Oro (Domain Shifting):** Siempre utiliza *Domain Shifting*. Si el proyecto de la chronicle trata sobre Finanzas, los ejemplos de la teoría deben tratar sobre Zoológicos, Reservas de Hotel, o cualquier otro dominio ajeno. Esto fuerza al Operador a traducir la lógica, evitando el "copy-paste".
- **Regla de Oro (Densidad y Abstracción):** Para conceptos abstractos (típicamente del Cap 03 en adelante), el lore debe estar "descomprimido". Debe incluir **mínimo 2 analogías claras** de la vida real y **2 a 3 ejemplos de código progresivos** (mostrando el "mal ejemplo" primero y luego la solución óptima).
- **Regla de Oro (Zero Assumption):** Jamás se asume ninguna dependencia preinstalada, configuración de entorno (como `venv`), ni conocimiento de herramientas externas a menos que se hayan enseñado explícitamente en chronicles anteriores. Cada pieza de Lore que introduzca una herramienta nueva (ej. `pytest`, `mypy`) debe incluir sus instrucciones explícitas de setup partiendo desde conocimiento cero.
- **Regla de Oro (Explicación de Primer Uso / Zero Surprise Syntax):** Todo comando, función, palabra clave, cláusula, argumento u operador de código que aparezca por primera vez en un capítulo **DEBE ser explicado explícitamente**, sin excepciones. Esto aplica tanto si es el tema central del capítulo como si es un recurso auxiliar o conciso empleado en un bloque de código (ej. usar `CROSS JOIN` para acoplar un promedio escalar, `DISTINCT` dentro de una subquery, o un marco `ROWS BETWEEN` en una ventana). Si una línea de código introduce sintaxis nueva no vista en capítulos anteriores (0..N-1), el texto debe desglosar inmediatamente:
  1. Qué hace la instrucción.
  2. Por qué se eligió en ese fragmento específico.
  3. Cómo funciona su comportamiento interno.  
  *Queda prohibido dar por sentada la comprensión intuitiva de sintaxis no enseñada.*
- **Regla de Oro (Objetivo Explícito de Negocio en Ejemplos):** Todo ejemplo de código —especialmente en los *Ejemplos Progresivos (Mal Camino vs. Buen Camino)*— **DEBE comenzar con un enunciado claro del objetivo o pregunta de negocio que se pretende resolver** antes de mostrar el bloque de código (ej: *"🎯 Objetivo de Negocio: Encontrar los proyectos cuyas horas reales superen el promedio global..."*). El Operador jamás debe verse forzado a realizar ingeniería inversa del código para adivinar qué resultado o cálculo se pretendía lograr.

### 2.2 La Capa `quests/`
Contiene la práctica deliberada, dividida por capítulos homólogos a la teoría.
- **Testing Progresivo (Scaffolding):** Para eliminar la fricción del TDD, se utiliza un modelo de andamiaje de 5 niveles que va desde "solo leer un test" hasta "escribir todo desde cero".
- **Spaced Repetition:** Los capítulos avanzados incluyen ejercicios de revisión de capítulos pasados.
- **Coherencia Secuencial y Cero Sintaxis Huérfana (Regla Crítica):** Todo ejercicio del capítulo N solo puede utilizar conceptos y sintaxis de los capítulos 0..N que hayan sido formalmente explicados en el `lore/`. Nunca debe requerir conocimiento de capítulos superiores ni incluir palabras clave sorpresa en la solución esperada que no hayan tenido su debida justificación en la teoría. Si se detecta una violación, el ejercicio o su solución deben corregirse de inmediato.

### 2.3 `grimoire.md` (El Requisito Socrático)
El aprendizaje pasivo no existe. Después de leer cada capítulo y hacer sus ejercicios, el Operador *debe* escribir en esta bitácora qué comprendió, usando sus propias palabras (Técnica Feynman).
- Solo cuando el DM certifica (vía `/scry`) que este documento refleja una verdadera asimilación, se autoriza el acceso al Rite.

### 2.4 La Capa `rite/` (Rite)
El proyecto final. Es un desarrollo monolítico (una CLI, una API, un pipeline) compuesto por fases internas desbloqueables.
- **Diagnóstico Quirúrgico:** Si el Operador falla gravemente en una fase del Rite (ej: Polimorfismo), no reinicia el Rite. La Witch diagnostica y le envía de regreso al Capítulo de Lore y Quests específicos.

## 3. El Flujo de Trabajo (Ciclo por Capítulo)

El Operador avanza offline o con el IDE:

```ascii
📖 Leer lore/Cap-N  (sin LLM)
     ↓
✏️  Completar quests/Cap-N  (con soluciones en archivo separado)
     ↓
📓 Escribir entrada en grimoire.md
     ↓
Repetir con el siguiente capítulo
     ↓
DM audita grimoire.md (/scry) → autoriza Rite
     ↓
🔨 Desarrollar Rite (apoyo de la Witch / headología)
```

## 4. El Dungeon Master (DM / Gatekeeper)

El rol del DoJo Agent como DM se ejerce mediante la skill `/scry`:

### `/scry [chronicle]` — Auditoría Estructural
Verifica automáticamente:
- Grimoire: campos llenos, métricas completas, respuestas Feynman escritas
- Quests: archivos `.py` existentes y con contenido
- Reporte: PASS/FAIL por capítulo

### `/scry [chronicle] --deep` — Auditoría Cualitativa
Evalúa la calidad de las síntesis Feynman:
- ¿Demuestra comprensión genuina?
- ¿Es copy-paste del lore?
- Se sugiere usar un modelo con mayores capacidades para esta evaluación.
