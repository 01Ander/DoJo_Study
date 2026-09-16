# 09 - Protocolo de Generación de Contenido (Chronicles)

> **Propósito:** Este documento es la **única instrucción** que un LLM (dentro de Antigravity) debe leer para generar una Chronicle completa del DoJo Study. Define el pipeline de 7 pasos, los 5 gates de auditoría, y las reglas de ejecución resiliente.
>
> **Alcance:** Aplica a toda generación de Chronicles nuevas (no retroactivo).
>
> **Generador:** LLM dentro de Antigravity (Gemini Pro o Claude Opus), ejecutado en sesiones de Modo Arquitecto (Lunes tarde/noche).

---

## 1. Fuentes de Verdad (Qué Leer y en Qué Orden)

El generador opera sobre un subconjunto estricto del repositorio. **Está prohibido leer** archivos fuera de este subconjunto (en particular: `meta/`, `content/subjects/` de chronicles ya completadas, o cualquier archivo de sesión anterior).

| # | Documento | Propósito | Modo |
|---|---|---|---|
| 1 | **Este protocolo** (`system/docs/09-generation-protocol.md`) | Instrucciones del pipeline | Solo lectura |
| 2 | [`04-campaign-as-course.md`](04-campaign-as-course.md) | Reglas de estructura, nomenclatura, reglas de oro del lore | Solo lectura |
| 3 | [`05-syllabus-maestro.md`](05-syllabus-maestro.md) | Competencias requeridas por chronicle | Solo lectura |
| 4 | [`system/templates/chronicle-template.md`](../templates/chronicle-template.md) | Template de estructura de chronicle.md | Solo lectura |
| 5 | `content/_generation/<CODE>/roadmap.md` | Estado actual del pipeline para la chronicle en generación | Lectura + Escritura |
| 6 | `content/_generation/<CODE>/matriz-trazabilidad.md` | Inventario de términos/conceptos | Lectura + Escritura |
| 7 | `content/subjects/<area>/chronicles/<CODE>/` | Directorio de output de la chronicle | Solo escritura |

> [!CAUTION]
> **Prohibición explícita:** NO leer `meta/archive/`, `meta/_warmup/`, `meta/ideas/`, `meta/historial.md`, `meta/CHANGELOG.md`, ni el contenido de chronicles ya completadas (a menos que el paso actual indique explícitamente verificar prerequisites).

---

## 2. El Roadmap Persistente

Cada Chronicle en generación tiene su propio archivo de estado persistente:
```
content/_generation/<CHRONICLE-CODE>/roadmap.md
```

Este archivo es la **primera y única cosa** que el LLM lee al iniciar una sesión de trabajo. Contiene:
- En qué paso del pipeline se encuentra la generación.
- Qué archivos específicos debe leer para ese paso.
- El historial de resultados de gates anteriores (incluyendo fallos y acciones correctivas).

### Formato

El roadmap usa un bloque YAML (frontmatter) seguido de una sección de historial en Markdown. Ver el template completo en:
```
content/_generation/TEMPLATE-roadmap.md
```

### Reglas del Roadmap

1. **Punto de entrada único:** Un modelo que entra a trabajar en una Chronicle SIEMPRE empieza leyendo `roadmap.md` antes que cualquier otra cosa.
2. **Contexto declarativo:** El campo `contexto_minimo_requerido` lista exactamente qué archivos necesita el modelo para el paso actual. Nada más, nada menos.
3. **Actualización obligatoria:** Al terminar una unidad de trabajo, el modelo DEBE actualizar `roadmap.md` con el nuevo estado antes de cerrar la sesión.
4. **Retomabilidad:** Cualquier modelo, en cualquier hilo, puede retomar el trabajo desde donde quedó leyendo únicamente este archivo.

---

## 3. Pipeline de 7 Pasos

### PASO 0: Carga de Contexto

**Input:** Ninguno.
**Acción:** Leer — y solo leer — los documentos indicados en `contexto_minimo_requerido` del roadmap. Para el paso 0, estos son:
- `system/docs/09-generation-protocol.md` (este documento)
- `system/docs/04-campaign-as-course.md`
- `system/docs/05-syllabus-maestro.md`

**Output:** Contexto cargado. No se genera ningún archivo.
**Actualizar roadmap:** `paso_actual: 1`, `estado: en_progreso`.

---

### PASO 1: Identificación del Subject

**Input:** Syllabus Maestro + nombre de la chronicle target.
**Acción:**
1. Extraer del syllabus las **competencias específicas** de la chronicle.
2. Listar los **prerequisites** (qué chronicles anteriores debe haber completado el Operador).
3. Identificar si hay **prácticas transversales** (DQ, GIT-CI, ENG-INT) que se integran en esta chronicle.
4. Definir el **Domain Shifting** temático (dominio de los ejemplos de lore ≠ dominio del Rite).

**Output:** Nota interna en el roadmap (sección `notas_paso_1`).
**Actualizar roadmap:** `paso_actual: 2`.

---

### PASO 2: Scaffolding de Carpetas

**Input:** Chronicle code (ej. `CLOUD-AWS`), área (ej. `cloud`).
**Acción:** Crear la estructura física completa **en una sola generación**:

```
content/subjects/<area>/chronicles/<CHRONICLE-CODE>/
├── chronicle.md         ← Se genera en PASO 3
├── grimoire.md          ← Se genera en PASO 5
├── lore/                ← Vacío (se llena en PASO 4)
├── quests/              ← Vacío (se llena en PASO 6)
└── rite/                ← Se genera en PASO 7
    ├── requirements.md
    └── journal.md       ← Template vacío
```

Además, crear la carpeta de generación:
```
content/_generation/<CHRONICLE-CODE>/
├── roadmap.md                ← Inicializado desde el template
└── matriz-trazabilidad.md    ← Inicializado desde el template
```

**Output:** Estructura de carpetas creada. Archivos vacíos o con templates mínimos.
**Actualizar roadmap:** `paso_actual: 3`.

---

### PASO 3: Generación de `chronicle.md`

**Input:** Competencias del syllabus (PASO 1) + template de chronicle.
**Acción:**
1. Redactar `chronicle.md` con: Business Context, ROI, Technical Objective, Syllabus (lista de capítulos con títulos descriptivos), Definition of Done.
2. **Cada capítulo debe tener un título que refleje EXACTAMENTE los conceptos que se enseñarán.** No usar términos en títulos que no se definirán en el lore.
3. Definir el dominio de Domain Shifting (distinto al dominio del Rite).
4. Definir el Rite con sus fases desbloqueables (al menos el esqueleto de nombre y mapeo a capítulos).

**Output:** `chronicle.md` completo.
**Actualizar roadmap:** `paso_actual: gate_1`, `estado: listo_para_auditoria`, `requiere_aprobacion_humana: true`.

---

### PASO 4: Generación de Lore (Capítulo por Capítulo)

**Input:** `chronicle.md` aprobado (GATE 1 PASS) + reglas de oro (sección 9 de este documento) + `matriz-trazabilidad.md` (estado acumulado hasta el cap N-1).
**Acción:** Generar **un capítulo a la vez**, no todos juntos. Para cada capítulo:

1. **Definir:** Todo término técnico nuevo debe tener:
   - **QUÉ** es (definición).
   - **CÓMO** se usa (código funcional con Domain Shifting).
   - **POR QUÉ** importa (consecuencia de no hacerlo / valor de negocio).
2. **Domain Shifting:** Todos los ejemplos de código usan el dominio temático elegido en `chronicle.md` (nunca el del Rite).
3. **Zero Assumption:** Instrucciones de setup si hay herramienta nueva.
4. **Zero Surprise Syntax:** Todo operador/función/keyword nuevo se desglosa (qué, por qué, cómo). Aplica tanto para el tema central como para cualquier recurso auxiliar en un bloque de código.
5. **Objetivo de Negocio:** Todo ejemplo empieza con `🎯 Objetivo de Negocio:`.
6. **Densidad para Cap 03+:** Mínimo 2 analogías de la vida real + 2-3 ejemplos progresivos (mal camino → buen camino).
7. **Actualizar Matriz de Trazabilidad:** Al final de cada capítulo, agregar a `matriz-trazabilidad.md` todos los términos/conceptos introducidos, indicando el nivel de profundidad (Qué/Cómo/Por qué) y la competencia del syllabus que cubren.

**Output:** Archivo `lore/NN-titulo.md` por cada capítulo + `matriz-trazabilidad.md` actualizada.
**Actualizar roadmap:** Después de generar TODOS los capítulos: `paso_actual: gate_2`, `estado: listo_para_auditoria`.

> [!WARNING]
> **Regla Anti-Gap (Lección de DE-PIPELINES):**
> Si un concepto se menciona pero NO se explica con los 3 niveles (qué/cómo/por qué), es un gap. No basta con "mencionarlo de pasada". Todo concepto sin profundidad suficiente producirá un FAIL en el GATE 2.

---

### PASO 5: Generación de Grimoire

**Input:** Lore aprobado (GATE 2 PASS) + `matriz-trazabilidad.md`.
**Acción:**
1. Generar `grimoire.md` con 2 preguntas Feynman por capítulo.
2. **Regla Crítica:** Cada pregunta DEBE ser respondible **exclusivamente** con la información del capítulo correspondiente del lore. Si requiere conocimiento externo, la pregunta es inválida.
3. Las preguntas deben cubrir tanto el CÓMO como el POR QUÉ (no solo mecánica).
4. Incluir la plantilla de métricas vacías y Friction Log para que el Operador complete.
5. Incluir la sección de auditoría del DM al final (`**Auditoría del DM:** [Pendiente]`).

**Output:** `grimoire.md` completo con preguntas y campos vacíos.
**Actualizar roadmap:** `paso_actual: gate_3`, `estado: listo_para_auditoria`.

---

### PASO 6: Generación de Quests

**Input:** Lore aprobado + grimoire aprobado (GATE 3 PASS).
**Acción:**
1. Crear una carpeta por capítulo: `quests/NN-titulo/`.
2. Cada quest contiene como mínimo: `quest.md` (instrucciones), `solution.py` (o `.sql`, según el área), y `test_NN_titulo.py` (tests automatizados).
3. **Coherencia Secuencial:** Quest del Cap N solo usa conceptos de Cap 0..N.
4. **Cero Sintaxis Huérfana:** La solución no debe usar ningún keyword/función que no esté en el lore del capítulo correspondiente o anteriores.
5. Aplicar scaffolding progresivo de testing (5 niveles de andamiaje, del nivel más guiado al más autónomo conforme avancen los capítulos).
6. **Spaced Repetition:** Los capítulos avanzados (Cap 04+) pueden incluir ejercicios de revisión de capítulos pasados.

**Output:** Carpetas de quests completas con instrucciones, soluciones y tests.
**Actualizar roadmap:** `paso_actual: gate_4`, `estado: listo_para_auditoria`.

---

### PASO 7: Generación de Rite (Completo)

**Input:** Todo aprobado (GATE 4 PASS) + `matriz-trazabilidad.md`.
**Acción:**
1. Generar `rite/requirements.md` completo con:
   - Business Context y ROI del proyecto.
   - Fases desbloqueables (cada fase mapea a capítulos específicos del lore).
   - Criterios de aceptación por fase.
   - El Rite usa un dominio **DIFERENTE** al Domain Shifting del lore.
2. Generar `rite/journal.md` como template vacío (el Operador lo llena durante el desarrollo).
3. El Rite es un proyecto monolítico que integra TODAS las competencias de la chronicle.
4. **Restricción:** El Rite solo puede exigir conceptos que estén en la `matriz-trazabilidad.md`.

**Output:** `rite/requirements.md` + `rite/journal.md`.
**Actualizar roadmap:** `paso_actual: gate_5`, `estado: listo_para_auditoria`, `requiere_aprobacion_humana: true`.

---

## 4. Los 5 Gates de Auditoría

### Regla de Aislamiento Generación↔Auditoría

> [!CAUTION]
> **Regla dura:** La sesión/hilo que genera el contenido **NO puede ser** la misma sesión que lo audita.

Al pasar de un paso de generación a su gate, el roadmap se marca como `estado: listo_para_auditoria` y la sesión de generación **termina**. El gate lo ejecuta una sesión nueva que solo recibe:
1. El artefacto generado (el capítulo, el grimoire, la quest, el rite).
2. El checklist del gate correspondiente (documentado abajo).
3. El `contexto_minimo_requerido` del gate (declarado en el roadmap).

**Nunca** recibe el razonamiento o el hilo de pensamiento de por qué se escribió así. Esto es lo que hace que el gate audite de verdad en vez de autoconfirmar.

**Regla de Verificación Estricta:** Todo ítem de un checklist de auditoría debe resolverse citando la línea o sección exacta que lo sustenta, no solo marcarse como cumplido.

---

### GATE 1: Auditoría de Scope — 👤 HUMANO obligatorio

**Checklist:**
- [ ] ¿Cada capítulo del temario mapea a ≥1 competencia del syllabus maestro?
- [ ] ¿Hay competencias del syllabus que quedaron sin capítulo asignado?
- [ ] ¿El Domain Shifting es distinto al dominio del Rite?
- [ ] ¿Los títulos de capítulos NO contienen términos técnicos que no se planean definir en el cuerpo del lore?
- [ ] ¿Los prerequisites están correctamente identificados?
- [ ] ¿Las fases del Rite mapean coherentemente a los capítulos del lore?

**Si PASS:** Actualizar roadmap → `paso_actual: 4`, `estado: en_progreso`.
**Si FAIL:** Registrar hallazgo en roadmap, corregir `chronicle.md`, re-auditar.

---

### GATE 2: Auditoría de Lore — 🤖 IA en sesión nueva

**Contexto mínimo requerido:** `system/docs/09-generation-protocol.md` + todos los archivos de `lore/` + `matriz-trazabilidad.md`.

**Checklist por capítulo:**
- [ ] ¿Todo término técnico introducido tiene definición explícita (qué/cómo/por qué)?
- [ ] ¿Se cumple Domain Shifting? (ningún ejemplo usa el dominio del Rite)
- [ ] ¿Se cumple Zero Assumption? (herramientas nuevas tienen instrucciones de setup)
- [ ] ¿Se cumple Zero Surprise Syntax? (toda sintaxis nueva está desglosada con qué/por qué/cómo)
- [ ] ¿Todo ejemplo tiene `🎯 Objetivo de Negocio` explícito?
- [ ] ¿No hay redacción que induzca al error? (revisar "extra", "puedes", "a veces" cuando algo es obligatorio)
- [ ] ¿Capítulos 03+ tienen ≥2 analogías y ≥2 ejemplos progresivos (mal → buen camino)?

**Checklist global:**
- [ ] ¿La `matriz-trazabilidad.md` cubre TODAS las competencias del syllabus para esta chronicle?
- [ ] ¿No hay términos usados en títulos de capítulos que no se definen en el cuerpo del lore?

**Si PASS:** Actualizar roadmap → `paso_actual: 5`, `estado: en_progreso`.
**Si FAIL:** Registrar hallazgo con protocolo de fallo estructurado (sección 5), corregir el capítulo afectado, re-auditar.
**Escalada:** Si falla 2 veces seguidas el mismo gate → escala a revisión humana.

---

### GATE 3: Auditoría Lore↔Grimoire — 🤖 IA en sesión nueva

> [!CAUTION]
> **Este es el gate donde fallaron las generaciones anteriores.** Se debe ejecutar con rigor extremo.

**Contexto mínimo requerido:** `lore/` + `grimoire.md` + `matriz-trazabilidad.md`.

**Para CADA pregunta del grimoire:**
- [ ] ¿Se puede responder SOLO con la información del capítulo N del lore?
- [ ] ¿La pregunta no requiere conocimiento de capítulos superiores (N+1, N+2...)?
- [ ] ¿La pregunta no se sale del scope del syllabus maestro?
- [ ] ¿La pregunta cubre un concepto que SÍ está definido (qué/cómo/por qué) en el lore?

**Taxonomía de errores a detectar:**

| Tipo | Nombre | Test |
|---|---|---|
| Tipo 1 | "Enseña CÓMO, pregunta POR QUÉ" | ¿El lore explica el POR QUÉ o solo la mecánica? |
| Tipo 2 | "Término sin definir" | ¿Todo término en la pregunta está definido en el lore? |
| Tipo 3 | "Fuera de scope" | ¿La pregunta está dentro de las competencias del syllabus? |
| Tipo 4 | "Redacción inductora de error" | ¿La redacción del lore permite responder correctamente sin ambigüedad? |

**Si PASS:** Actualizar roadmap → `paso_actual: 6`, `estado: en_progreso`.
**Si FAIL:** Registrar hallazgo con protocolo de fallo estructurado, corregir, re-auditar.
**Escalada:** Si falla 2 veces seguidas → escala a revisión humana.

---

### GATE 4: Auditoría Quests↔Lore — 🤖 IA en sesión nueva

**Contexto mínimo requerido:** `lore/` + `quests/` + `matriz-trazabilidad.md`.

**Checklist por quest:**
- [ ] ¿La solución usa SOLO sintaxis enseñada en Cap 0..N del lore?
- [ ] ¿Las instrucciones (`quest.md`) son claras sin necesidad de consultar el lore para entender el enunciado?
- [ ] ¿Los tests validan el comportamiento esperado de la solución?
- [ ] ¿No hay keywords/funciones "huérfanas" en la solución que no aparezcan en el lore?

**Si PASS:** Actualizar roadmap → `paso_actual: 7`, `estado: en_progreso`.
**Si FAIL:** Registrar hallazgo, corregir, re-auditar.
**Escalada:** Si falla 2 veces seguidas → escala a revisión humana.

---

### GATE 5: Auditoría Final Integral — 👤 HUMANO obligatorio

**Contexto mínimo requerido:** `chronicle.md` + `lore/` + `grimoire.md` + `quests/` + `rite/` + `matriz-trazabilidad.md` + `system/docs/05-syllabus-maestro.md`.

**Tabla de coherencia cruzada:**

| Componente A | Componente B | Validación |
|---|---|---|
| Syllabus | Lore | Toda competencia tiene profundidad suficiente (verificar con matriz) |
| Lore | Grimoire | Toda pregunta es respondible con el lore |
| Lore | Quests | Toda solución usa solo sintaxis enseñada |
| Syllabus | Rite | Toda competencia se ejerce en alguna fase del Rite |
| Grimoire | Syllabus | Toda pregunta mapea a una competencia |
| Rite | Matriz | El Rite no exige conceptos fuera de la matriz |

**Checklist adicional:**
- [ ] ¿El `chronicle.md` refleja correctamente lo que contiene lore/quests/grimoire/rite?
- [ ] ¿El Rite usa un dominio DIFERENTE al Domain Shifting del lore?
- [ ] ¿El Rite tiene fases desbloqueables que cubren todas las competencias?

**Si PASS:** Actualizar roadmap → `estado: completado`. La chronicle está lista para estudio.
**Si FAIL:** Registrar hallazgo, corregir el componente afectado, re-auditar.

---

## 5. Protocolo de Fallo Estructurado

Un gate no puede resolverse en un simple "PASS/FAIL". Todo FAIL **debe** registrar en la sección `historial_gates` del `roadmap.md`:

```yaml
- gate: 2
  resultado: fail
  fecha: YYYY-MM-DD
  hallazgos:
    - capitulo: "02"
      termino: "particionado"
      tipo_error: "Tipo 2 — término sin definir"
      detalle: "Se usa en el ejemplo de negocio del Cap 02 (línea ~45) pero nunca se define qué es, cómo se implementa ni por qué importa."
      accion: "Agregar sección '## Particionado de Datos' en Cap 02 antes del ejemplo, con definición completa (qué/cómo/por qué) y una analogía."
```

### Reglas del fallo estructurado:
1. **Nunca "regenerar" a ciegas.** La acción correctiva debe ser quirúrgica: qué cambiar, dónde, y por qué.
2. **El reintento lee el detalle del fallo** y aplica la corrección. No regenera el capítulo completo.
3. **Si el mismo gate falla 2 veces seguidas**, escala a revisión humana (el roadmap queda en `estado: en_espera_operador`).

---

## 6. Matriz de Trazabilidad

Archivo persistente por Chronicle: `content/_generation/<CODE>/matriz-trazabilidad.md`

Este archivo mapea cada término/concepto introducido en el lore contra las competencias del syllabus, verificando la profundidad de cobertura.

### Formato

Ver template completo en:
```
content/_generation/TEMPLATE-matriz-trazabilidad.md
```

### Reglas de la Matriz:
1. Se actualiza **incrementalmente**, capítulo a capítulo (durante PASO 4).
2. Es input directo de GATE 2 (¿los conceptos tienen profundidad?), GATE 3 (¿las preguntas cubren conceptos definidos?), GATE 5 (¿el Rite usa solo conceptos de la matriz?) y PASO 7 (el Rite solo puede exigir conceptos presentes).
3. Permite auditar GATE 5 sin releer todo el lore de cero.

---

## 7. Asignación de Gates: Humanos vs. IA

| Gate | Auditor | Justificación | Condición de Escalada |
|---|---|---|---|
| **Gate 1 (Scope)** | 👤 Humano obligatorio | El más barato de corregir aquí, el más caro de arrastrar si está mal | — |
| **Gate 2 (Lore)** | 🤖 IA en sesión nueva (fría) | Auditoría mecánica contra checklist | Escala a humano si falla 2 veces seguidas |
| **Gate 3 (Lore↔Grimoire)** | 🤖 IA en sesión nueva (fría) | Cruce mecánico pregunta↔contenido | Escala a humano si falla 2 veces seguidas |
| **Gate 4 (Quests↔Lore)** | 🤖 IA en sesión nueva (fría) | Cruce mecánico sintaxis↔lore | Escala a humano si falla 2 veces seguidas |
| **Gate 5 (Final Integral)** | 👤 Humano obligatorio | Validación holística antes de cerrar la Chronicle | — |

El `roadmap.md` marca `requiere_aprobacion_humana: true/false` por paso. Si es `true`, el roadmap queda en `estado: en_espera_operador` hasta que el Operador (humano) lo revise y avance manualmente.

---

## 8. Flujo Resumido con Roadmap

```
1. Modelo entra → lee roadmap.md primero, nada más.
2. Roadmap le dice: paso actual, qué leer, si el paso anterior fue generación o auditoría.
3. Ejecuta solo esa unidad de trabajo (un capítulo, un gate, un componente).
4. Escribe el resultado en el artefacto correspondiente y actualiza roadmap.md.
5. Si el paso que sigue es un gate, la sesión TERMINA — el gate lo toma una sesión nueva.
6. Si el gate requiere aprobación humana, el roadmap queda en estado: en_espera_operador.
```

---

## 9. Reglas de Oro del Lore (Referencia Rápida)

Estas reglas están documentadas en detalle en [`04-campaign-as-course.md`](04-campaign-as-course.md). Aquí se listan como referencia rápida para el generador:

### 9.1 Domain Shifting
Todos los ejemplos de código del lore usan un dominio temático **diferente** al del Rite. Si el Rite trata sobre un sistema de biblioteca, los ejemplos del lore podrían tratar sobre una panadería, un zoológico, o un gremio de alquimistas. Esto fuerza al Operador a traducir la lógica, evitando el copy-paste.

### 9.2 Zero Assumption
Jamás se asume ninguna dependencia preinstalada, configuración de entorno (como `venv`), ni conocimiento de herramientas externas a menos que se hayan enseñado explícitamente en chronicles anteriores. Cada herramienta nueva incluye instrucciones de setup desde cero.

### 9.3 Zero Surprise Syntax
Todo comando, función, palabra clave, cláusula, argumento u operador de código que aparezca **por primera vez** en un capítulo DEBE ser explicado explícitamente:
1. Qué hace la instrucción.
2. Por qué se eligió en ese fragmento específico.
3. Cómo funciona su comportamiento interno.

Aplica tanto para el tema central del capítulo como para recursos auxiliares en bloques de código. Queda prohibido dar por sentada la comprensión intuitiva de sintaxis no enseñada.

### 9.4 Densidad y Abstracción (Cap 03+)
Para conceptos abstractos (típicamente del Cap 03 en adelante), el lore debe estar "descomprimido":
- **Mínimo 2 analogías claras** de la vida real.
- **2 a 3 ejemplos de código progresivos** (mostrando el "mal ejemplo" primero y luego la solución óptima).

### 9.5 Objetivo Explícito de Negocio
Todo ejemplo de código DEBE comenzar con:
```
🎯 Objetivo de Negocio: [descripción del problema que se resuelve]
```
El Operador jamás debe verse forzado a realizar ingeniería inversa del código para adivinar qué resultado se pretendía lograr.

### 9.6 Profundidad Mínima (Qué/Cómo/Por qué)
Todo concepto mencionado en el lore debe cubrir obligatoriamente tres niveles:
- **QUÉ es** (definición conceptual).
- **CÓMO se usa** (código funcional).
- **POR QUÉ importa** (consecuencia de no hacerlo / valor de negocio).

Si un concepto solo se menciona sin estos 3 niveles, es un gap y producirá un FAIL en la auditoría.

### 9.7 Redacción Anti-Error
Revisar que el lore no use palabras que impliquen opcionalidad ("extra", "puedes", "a veces", "opcionalmente") cuando el concepto es **obligatorio** o está **impuesto por defecto** en el contexto profesional. Redactar con precisión técnica.

### 9.8 Coherencia Secuencial (Quests)
Todo ejercicio del capítulo N solo puede utilizar conceptos y sintaxis de los capítulos 0..N que hayan sido formalmente explicados en el lore. Nunca debe requerir conocimiento de capítulos superiores ni incluir palabras clave sorpresa en la solución esperada.
