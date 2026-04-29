# 📐 RFC v3: Campaign as Course — "El Libro + El Laboratorio"

> **Estado:** APROBADO — Pendiente de Implementación
> **Fecha:** 2026-04-29
> **Versión objetivo:** DoJo v5.0
> **Autor:** Operador + Architect (Antigravity + Gemini)
> **Historial:** v1 (Study Guide Layer) → v2 (Campaign as Course) → v3 (Final)
> **Conecta con:** Protocolo de Fases (ideas-in-live.md L23-67), Skills Tracker

---

## 1. Contexto: El Problema Raíz

El sistema DoJo v4 tiene un gap estructural: cada misión enseña Y pide construir al mismo tiempo. El Operador llega sin conocimiento previo, usa a Tutor como primera exposición al tema (costoso, frágil, dependiente de API), y nunca hay una verificación granular de asimilación — solo el Exit Gate al final de toda la campaign.

**Evidencia de los journals de PY-POO-FINANCE:**
- **M01:** *"aún no se observa esa habilidad para poder escribir los tests antes del código"*
- **M03:** *"fricción subió a 7 tratando de entender un test, ni siquiera entenderlo"*

El problema no es que las misiones sean malas. Es que te lanzaron a hacer TDD de ABC sin haber visto TDD antes. Es como pedir un examen de cálculo cuando apenas viste álgebra.

---

## 2. El Modelo: Campaign as Course

### 2.1 Analogía

```
┌─────────────────────────────────────────────────────────┐
│                    CAMPAIGN = CURSO                     │
│                                                         │
│  📖 Capítulos (theory/)     = Libro de texto            │
│  ✏️  Ejercicios (exercises/) = Problemas del capítulo   │
│  📓 Study Journal           = Apuntes del estudiante    │
│  🔨 Boss Final (project/)   = Proyecto de semestre      │
│                                                         │
│  El libro enseña. Los ejercicios practican.             │
│  El journal consolida. El Boss Final demuestra.         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 El Ciclo Fundamental (CRÍTICO)

El ciclo es **por capítulo**, no por libro completo. Leer todo el libro antes de hacer ejercicios recrea la educación formal pasiva que se quiere evitar.

```
┌──────────────────────────────────────────────────────────────────┐
│  CICLO POR CAPÍTULO (se repite N veces)                          │
│                                                                  │
│  📖 Leer Cap. N  →  ✏️ Ejercicios Cap. N  →  📓 Study Journal   │
│                                                                  │
│  Solo cuando TODOS los capítulos y ejercicios están completos:   │
│                                                                  │
│  🔨 Boss Final (con Reviewer como único apoyo)                   │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Diferencia clave vs. Educación Formal

| Educación Formal | DoJo v5 |
|------------------|---------|
| Lees → Haces ejercicios → Examen teórico | Lees → Haces ejercicios → **Construyes algo real** |
| El examen evalúa memorización | El Boss evalúa **si puedes crear sin ayuda** |
| Nota de 1 a 10 | **O lo construiste o no** (binario, como producción) |
| El profesor da las respuestas | El libro da **herramientas**, el Boss exige **transferencia** |

---

## 3. Nueva Estructura de Campaign

```
PY-POO-FINANCE/
├── campaign.md                        # Syllabus del curso
│
├── theory/                            # 📖 EL LIBRO
│   ├── 00-from-functions-to-classes.md
│   ├── 01-abstract-classes-and-interfaces.md
│   ├── 02-domain-entities-and-polymorphism.md
│   ├── 03-data-transformation-patterns.md
│   ├── 04-output-and-orchestration.md
│   ├── 05-testing-with-pytest.md      # ← CAPÍTULO DEDICADO A TESTING
│   ├── 06-validation-and-logging.md
│   └── 07-cli-applications.md
│
├── exercises/                         # ✏️ LOS EJERCICIOS (paralelos a theory/)
│   ├── 00-classes/
│   │   ├── ex01-basic-class.md
│   │   ├── ex02-init-and-self.md
│   │   └── ex03-refactor-function-to-class.md
│   ├── 01-abstractions/
│   │   ├── ex01-define-abc.md
│   │   ├── ex02-concrete-implementation.md
│   │   └── ex03-write-test-for-abc.md
│   ├── 02-entities/
│   ├── 03-transformations/
│   ├── 04-orchestration/
│   ├── 05-testing/                    # ← BLOQUE COMPLETO DE TESTING
│   │   ├── ex01-anatomy-of-a-test.md
│   │   ├── ex02-describe-then-code.md
│   │   ├── ex03-fixtures-and-mocks.md
│   │   └── ex04-tdd-red-green-refactor.md
│   ├── 06-validation/
│   └── 07-cli/
│
├── study-journal.md                   # 📓 APUNTES DEL OPERADOR (fase de estudio)
│
└── project/                           # 🔨 EL BOSS FINAL
    ├── requirements.md
    ├── journal.md                     # Journal clásico (solo fase de ejecución)
    ├── src/
    ├── tests/
    └── data/
```

---

## 4. Anatomía de Cada Capa

### 4.1 Theory/ — El Libro

Cada capítulo sigue esta estructura fija:

```markdown
# Capítulo N: [Título]

## Pre-requisitos
Capítulo(s) anterior(es) que debes haber completado (theory + exercises).

## ¿Qué es [concepto] y por qué importa en la industria?
Explicación clara. Contexto de negocio real.
Por qué un ingeniero Middle/Senior necesita dominar esto.

## Domain Shifting (Analogía)
Analogía del mundo real para anclar el concepto antes del código.

## El Concepto en Código
Código completo, comentado línea por línea.
**SIEMPRE en un dominio diferente al del proyecto de la campaign.**
(Si el proyecto es finanzas → ejemplos con videojuegos, recetas, logística, etc.)

## Errores Comunes
- Qué suele salir mal y por qué
- Cómo identificar el error
- Cómo corregirlo

## Conexión con Testing
¿Cómo se testearía este concepto? Vista previa del ejercicio de testing correspondiente.

## Mapa de Ejercicios
Listado explícito de los ejercicios que se encuentran en la carpeta `exercises/` para este capítulo. Esta es la conexión directa entre la teoría y la práctica.
*(Obligatorio completarlos antes de pasar al Study Journal).*
- Ejercicio 1: [Nombre y concepto a practicar]
- Ejercicio 2: [Nombre y concepto a practicar]
- Ejercicio de Testing Nivel [X]: [Nombre y objetivo]

## Auto-evaluación
Preguntas que deberías poder responder en tus propias palabras:
- [ ] ¿Puedo explicar [X] sin mirar el código?
- [ ] ¿Qué pasaría si [edge case]?
- [ ] ¿En qué se diferencia de [concepto similar]?
```

**Principio clave — Domain Shifting obligatorio:**
Los ejemplos NUNCA usan el dominio del proyecto. Esto garantiza que en el Boss Final el Operador haga la transferencia cognitiva, no copie el ejemplo del libro.

### 4.2 Exercises/ — Los Ejercicios

Cada ejercicio es atómico. Hay dos tipos:

#### Tipo A: Ejercicio de Concepto
```markdown
# Ejercicio: [Título]
**Capítulo:** N | **Concepto:** [nombre]

## Objetivo
Practicar [concepto específico] en un dominio diferente al del proyecto.

## Contexto
[Escenario breve — dominio diferente al proyecto]

## Instrucciones
1. Paso concreto
2. Paso concreto

## Solución
> ⚠️ INTENTA PRIMERO. Solo desbloquea si llevas más de 20 minutos trabado.
<details>
<summary>Ver solución</summary>
[Código de referencia completo]
</details>
```

#### Tipo B: Ejercicio de Testing — El "Desbloqueo Progresivo"

Este tipo aborda directamente el muro del testing. Flujo de 4 pasos:

```markdown
# Ejercicio de Testing: [Título]
**Capítulo:** N | **Nivel:** [1-5]

## Paso 1: Describe el test en español
"Quiero verificar que si creo un Extractor sin implementar extract_data,
Python me lance un TypeError"

## Paso 2: Traduce a GIVEN / WHEN / THEN
# GIVEN: una clase IncompleteExtractor que hereda de AbstractExtractor
#        pero NO implementa extract_data
# WHEN:  intento crear una instancia de IncompleteExtractor
# THEN:  Python lanza TypeError

## Paso 3: Escribe la estructura del test (intento propio)
def test_incomplete_extractor_raises():
    # ¿Qué va aquí?
    pass

## Paso 4: Desbloqueo — Ver el test completo
> Solo después de intentar el Paso 3
<details>
<summary>Ver test completo</summary>

def test_incomplete_extractor_raises():
    with pytest.raises(TypeError):
        IncompleteExtractor()

</details>

## Reflexión (para el Study Journal)
- ¿Qué parte no pudiste escribir solo?
- ¿Fue la sintaxis de pytest o la lógica del test?
```

**Gradiente de niveles de testing:**
```
Nivel 1: Leer un test existente y explicar qué valida
Nivel 2: Describir en español qué quieres testear
Nivel 3: Escribir el GIVEN/WHEN/THEN en comentarios
Nivel 4: Completar un test parcialmente escrito (fill the blanks)
Nivel 5: Escribir un test completo desde cero
```

El objetivo es que al llegar al Boss Final el Operador opere en Nivel 4-5, no en Nivel 1 como ocurrió en PY-POO.

### 4.3 Study Journal — Los Apuntes del Operador

Un único archivo `study-journal.md` en la raíz de la campaign. Su propósito es que el Operador **consolide en sus propias palabras** lo que está aprendiendo, detecte sus propias brechas, y construya el registro que el DM usará para autorizar el acceso al Boss Final.

**Estructura de entrada por capítulo:**
```markdown
## Cap. N: [Título] — [Fecha]

### Lo que vi
[Qué conceptos presentó el capítulo — en tus propias palabras, no copiado]

### Lo que entendí
[Qué quedó claro. Incluye tu propia analogía si la construiste]

### Lo que no entendí / me costó
[Qué quedó confuso o requirió varias lecturas]

### Dónde pedí ayuda a Tutor
[Si consultaste algo puntual, qué fue y qué te respondió]

### Auto-evaluación
- [ ] Puedo explicar [concepto principal] sin mirar el capítulo
- [ ] Completé todos los ejercicios del capítulo
- [ ] Entiendo cómo se conecta con el capítulo anterior

### Reflexión de ejercicios
[Qué ejercicios te costaron más y por qué]
```

**El Study Journal NO es el Journal del proyecto.** Es el cuaderno de apuntes del estudiante. El `journal.md` clásico (dentro de `project/`) es exclusivo de la fase de ejecución del Boss Final.

### 4.4 Project/ — El Boss Final

El Boss Final es el equivalente al proyecto de semestre. Se enfrenta **únicamente** después de que el DM certifica que todos los capítulos y ejercicios están completos en el Study Journal.

**Condiciones de acceso:**
- Todos los capítulos leídos (registrados en `study-journal.md`)
- Todos los ejercicios completados
- Auto-evaluación marcada en cada capítulo
- DM aprueba el acceso revisando el `study-journal.md`

**Estructura interna del Boss (fases desbloqueables):**
El Boss es conceptualmente monolítico pero tiene fases internas que el DM desbloquea progresivamente. Cada fase mapea a un capítulo. Si una fase falla, no se reinicia todo — se diagnóstica.

```
Fase 1: Extractores       ← Cap 00 + 01
Fase 2: Entidades         ← Cap 02
Fase 3: Transformaciones  ← Cap 03
Fase 4: Orquestación CLI  ← Cap 04 + 07
```

**Rol de Tutor y Reviewer en el Boss:**
| Rol | Cuándo | Para qué |
|-----|--------|----------|
| **Tutor** | Bloqueos críticos no resueltos por el libro | Emergencia real. El libro debería haber cubierto lo necesario |
| **Reviewer** | Siempre disponible | TDD, code review socrático, gatekeeper de calidad |

---

## 5. El DM (Dungeon Master) — Rol del DoJo Agent

Con este modelo el DoJo Agent **asciende** de profesor particular a Director del Juego y Auditor de Progreso.

### 5.1 Funciones del DM

| Función | Descripción |
|---------|-------------|
| **Tracker de progreso** | Registra qué capítulos y ejercicios están completos vía `study-journal.md` |
| **Gatekeeper del Boss** | Audita el `study-journal.md` y **autoriza** el acceso al Proyecto Final |
| **Consultor puntual** | Responde dudas conceptuales específicas durante la fase de teoría |
| **Diagnóstico de fallos** | Si el Boss falla en una fase, mapea el error al capítulo y lo devuelve |

### 5.2 Diagnóstico de Fallos en el Boss

Si el Reviewer detecta que el Operador falla conceptos en el Boss Final, NO se reinicia la campaign. El proceso es quirúrgico:

```
Reviewer detecta fallo en Fase N
          │
          ▼
Reviewer identifica: "Parece que [concepto X] no está consolidado"
          │
          ▼
Reviewer indica: "Revisa el Capítulo [N] de theory/,
                  especialmente la sección [Y].
                  Haz los ejercicios de nivel 4-5 del bloque [Z]."
          │
          ▼
Operador regresa a exercises/ → completa ejercicios específicos
          │
          ▼
Operador retoma el Boss en la fase donde falló
```

Diagnóstico quirúrgico. No reinicio total.

### 5.3 Nueva Skill: /dojo-ask (Consultas Contextuales Estrictas)

Para evitar preguntas genéricas que consumen tokens innecesarios o confunden al LLM por falta de contexto, se implementará una skill dedicada para consultar al DM durante la fase de estudio:

**Uso:**
```
/dojo-ask --cap="03" --ex="ex02" --pregunta="[tu duda]"
```

**Comportamiento de la skill:**
1. Lee los parámetros proporcionados.
2. Carga en memoria **exclusivamente** el archivo de teoría o ejercicio indicado.
3. Lee la pregunta del Operador.
4. Responde siguiendo el **Estándar de Respuesta Académica del DM** (ver abajo).

> *Esto asegura que el LLM sepa exactamente sobre qué responder, limitando alucinaciones y respuestas generalistas de libros de texto externos.*

### 5.4 Estándar de Respuesta Académica del DM

Todas las respuestas del DM — incluyendo `/dojo-ask` — siguen este estándar. El objetivo es usar un LLM más caro pero más rápido, economizando contexto y tokens al ser quirúrgicamente preciso.

- **Tono:** Ni técnico-árido ni informal. Claro, directo, con peso académico justo.
- **Límite estructural:** Máximo 3 párrafos por respuesta explicativa.
- **Ejemplo:** 1 ejemplo concreto si aplica, siempre en dominio diferente al proyecto (Domain Shifting obligatorio).
- **Sin desperdicio de tokens:** Prohibido preámbulos (`"Claro, con gusto..."`), cierres redundantes (`"Espero que haya quedado claro..."`), y reformulaciones de la pregunta del Operador.
- **Fragmentación inteligente:** Si la respuesta requiere más de 3 párrafos, el DM fracciona la pregunta:
  > *"Esta pregunta tiene dos partes. ¿Empezamos por [X] o por [Y]?"*

> **Principio:** Una respuesta larga rompe el estado de flow del Operador igual que una desconexión de API. El DM protege la concentración del Operador siendo preciso, no exhaustivo.

### 5.4 Impacto en Tokens (Estimado)

| Modelo anterior | Modelo v5 |
|----------------|-----------|
| Tutor explica todo desde cero (~70% del costo) | Tutor solo en emergencias (~10% del costo) |
| Sin verificación granular de asimilación | Study Journal + diagnóstico quirúrgico |
| API en tiempo real para estudiar | `theory/` y `exercises/` son offline (NotebookLM-ready) |
| Estimado: $0.80-1.20/misión | Estimado: $0.20-0.40/capítulo+ejercicios |

---

## 6. Abordaje Específico del Testing

### 6.1 Diagnóstico (basado en journals PY-POO)

El Operador puede:
- ✅ Entender conceptos OOP (construyó analogías propias en M01)
- ✅ Escribir código de producción con guía
- ❌ Escribir tests de forma independiente
- ❌ Leer un test existente y entender qué valida

### 6.2 Solución de Tres Capas

**Capa 1 — Capítulo dedicado** (`theory/05-testing-with-pytest.md`):
- Anatomía de un test (GIVEN/WHEN/THEN = arrange/act/assert)
- Qué es un fixture y por qué existe
- Qué es un mock y cuándo usarlo
- Ciclo Red-Green-Refactor paso a paso
- Cómo **leer** un test antes de aprender a **escribirlo**

**Capa 2 — Testing integrado en cada capítulo:**
- Cada capítulo de `theory/` incluye sección "¿Cómo se testea este concepto?"
- Cada bloque de `exercises/` incluye al menos 1 ejercicio de testing tipo B

**Capa 3 — Gradiente de ejercicios de testing:**
- Nivel 1-2 en capítulos iniciales
- Nivel 3-4 en capítulos intermedios
- Nivel 5 (desde cero) en capítulos finales y en el Boss Final

---

## 7. Compatibilidad con NotebookLM

Toda la carpeta `theory/` es compatible con Google NotebookLM:
- Se sube como fuente
- NotebookLM genera un tutor conversacional sobre el contenido
- El Operador puede hacer preguntas sobre los capítulos sin gastar tokens
- Es interactivo sin depender de APIs externas

Esto convierte NotebookLM en un **Tutor offline gratuito** durante la fase de teoría.

---

## 8. Generación del Contenido

### 8.1 ¿Quién genera theory/ y exercises/?
**Fuera del sistema DoJo**, con un LLM frontera (Antigravity/Gemini/Opus) al diseñar la campaign. Son archivos estáticos que no cambian.

**Input para la generación:**
1. Perfil profesional objetivo (Data & Automation Engineer)
2. Lista de conceptos a cubrir (extraída de `campaign.md`)
3. Dominio del proyecto → para saber qué dominio EVITAR en los ejemplos

**Output:**
- N archivos `.md` en `theory/` (uno por capítulo)
- M archivos `.md` en `exercises/` (3-5 ejercicios por capítulo, con ≥1 de testing)
- Español para explicaciones, inglés para código/naming

### 8.2 ¿Quién genera el Boss Final?
Se genera junto con la campaign (como hoy los `requirements.md`), pero con fases internas explícitas mapeadas a capítulos.

---

## 9. ¿Viola la Filosofía DoJo?

### Lo que NO cambia:
- El Operador escribe todo su código en el Boss Final
- TDD sigue siendo obligatorio
- El proyecto es real, con valor de negocio simulado
- Reviewer sigue siendo el gatekeeper socrático
- La empleabilidad es el objetivo, no la nota

### Lo que SÍ cambia:
- **Antes:** "Aprende lanzándote al vacío con Tutor como paracaídas"
- **Ahora:** "Estudia, practica, y luego lánzate — con Reviewer como red de seguridad"

> **El producto final sigue siendo código funcionando, no un examen aprobado.**

---

## 10. Implementación

### Fase A — Prueba de Concepto (próxima campaign)
- [ ] PY-POO-FINANCE se cierra con el flujo actual (B01 + EG01)
- [ ] Definir la próxima campaign (nueva o repetición de POO según resultado del EG01)
- [ ] Generar `theory/` (capítulos 00-02) y `exercises/` correspondientes como piloto
- [ ] Probar el ciclo: Leer Cap → Ejercicios → Study Journal → Leer Cap siguiente
- [ ] El DM audita el `study-journal.md` antes de abrir el Boss

### Fase B — Campaign Completa (v5.0-alpha)
- [ ] Generar el libro completo y todos los ejercicios
- [ ] Ejecutar la campaign completa bajo el nuevo flujo
- [ ] Medir: ¿el Operador llega al Boss con menor fricción que en PY-POO?

### Fase C — Documentos Fundacionales y Templates (v5.0)
*(Estos documentos serán la única "fuente de verdad" del sistema. De ellos nacerán todas las futuras campaigns para garantizar el estándar).*
- [ ] **Auditoría y Deprecación de Docs v4:**
  - Archivar o reescribir `02-misiones-framework.md`, `04-estructura-campanas.md` y `06-manual-operativo-misiones.md` (ya que el modelo de "misión entrelazada" desaparece).
  - Actualizar `08-dojo-agent.md` para reflejar la evolución a Dungeon Master/Auditor.
  - Marcar `09-guia-operaciones-v4.md` como deprecado frente a la inminente v5.0.
- [ ] Crear el doc fundacional de arquitectura: `docs/12-campaign-as-course.md` (detallando la conexión inquebrantable Teoría ↔ Ejercicios).
- [ ] Crear templates maestros (fuentes de verdad para generación): `theory-chapter-template.md`, `exercise-template.md`, `study-journal-template.md`.
- [ ] Actualizar `.hermes.md` con las reglas estrictas del nuevo rol del DM (Gatekeeper).
- [ ] **Auditoría de Skills del Agent:**
  - > ⚠️ **NOTA OPERATIVA:** Debido a restricciones recientes en `.hermes.md` (prevención de auto-ejecución y conflictos de rutas), los journals (`study-journal.md` y `journal.md`) se escribirán **manualmente por el Operador fuera del Agent**.
  - Revisar y limpiar skills actuales (como `dojo-done`) que intentan auto-escribir logs y fallan.
  - El DM pasará a ser un **lector/auditor** de los journals, no el escritor.
- [ ] Actualizar `mission-template.md` a `campaign-boss-template.md`.
- [ ] Construir la nueva skill atómica `/dojo-ask` para centralizar consultas contextuales.

---

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| El Operador lee capítulos sin hacer ejercicios | Alta | El DM verifica los ejercicios en el `study-journal.md` antes de autorizar el Boss. Sin ejercicios completos → sin acceso |
| El Boss falla por gap no detectado en ejercicios | Media | Reviewer hace diagnóstico quirúrgico → mapea el fallo al capítulo específico, no reinicio total |
| El `study-journal.md` se vuelve una carga | Baja | Estructura fija por capítulo (6 campos). Es responsabilidad exclusiva del Operador — escribir el journal es una habilidad en sí misma. |
| El libro genera falsa confianza (conocimiento pasivo) | Media | Mitigado por el ciclo por capítulo: ejercicios inmediatamente después de cada capítulo, no al final del libro |
| Fricción de velocidad bajo presión no entrenada | Baja (diferida) | WakaTime ya registra tiempos. Se evalúa como métrica en v5.1 si el Operador la considera útil sin que genere fricción adicional |

---

## 12. Decisiones Resueltas

1. **PY-POO-FINANCE:** No se aplica retroactivamente. Se cierra con B01 + EG01. El resultado del EG01 determina si la próxima campaign es nueva o una repetición de POO con el nuevo modelo.
2. **Ciclo de estudio:** Por capítulo (Cap → Ejercicios → Journal → Cap siguiente). NO por libro completo.
3. **Volumen de ejercicios:** 3-5 por capítulo, con ≥1 de testing. Si el concepto se domina con 3, no se fuerza más.
4. **Boss Final:** Monolítico en concepto, con fases internas desbloqueables revisadas por el DM.
5. **Boss fallido:** Reviewer diagnostica el concepto fallido y señala el capítulo específico. Diagnóstico quirúrgico.
6. **Dos journals:** `study-journal.md` (apuntes del Operador durante teoría) + `journal.md` clásico (solo durante el Boss Final).
7. **Nomenclatura y Tipología:**
   - Se mantiene "Campaign". El espíritu RPG se preserva.
   - Tipología de campaigns: `CORE-SUBTEMA`. Sin adiciones ni adornos.
   - Ejemplos válidos: `PY-POO`, `PY-PAND`, `PY-API`, `DE-ETL`, `PY-CLOUD`.
   - Ejemplos inválidos: `PY-POO-FINANCE`, `PY-POO-FINANCE-V2`, `PY-API-AUTO`.
   - La campaign beta usará: **`PY-POO`** (sin el `-FINANCE-V2` histórico).
8. **Idioma:** Español para teoría/explicaciones, inglés para código/testing/arquitectura/naming.
9. **Velocidad bajo presión:** Diferida. WakaTime como métrica de referencia futura, no como herramienta de presión activa.
10. **NotebookLM:** `theory/` es compatible y se puede subir para interactividad offline gratuita.

---

## 13. Core Pedagógico (Metodologías Formales)

Para garantizar la asimilación profunda sin violar el principio de "aprender creando", este RFC se apoya estructuralmente en cinco metodologías con respaldo científico sólido:

1. **La Técnica Feynman (Fase de Consolidación):**
   - **Evidencia:** Fuerza recuperación activa y detección de gaps reales. Si no puedes explicarlo simple, no lo entendiste.
   - **Aplicación:** En el `study-journal.md`. El DM audita que el Operador explique los conceptos en sus propias palabras con analogías cotidianas (Domain Shifting) y sin jerga técnica. Si la explicación parece copiada del libro, el DM la rechaza.

2. **Práctica Intercalada / Interleaving (Fase de Ejercicios):**
   - **Evidencia:** Uno de los hallazgos más robustos de la ciencia cognitiva. Mezclar problemas de distintos temas fuerza al cerebro a identificar qué estrategia aplicar, no solo a ejecutarla mecánicamente.
   - **Aplicación:** A partir del Capítulo 3, los ejercicios en `exercises/` combinan conceptos del capítulo actual con los de capítulos anteriores (ej. construir una abstracción del Cap 2 y aplicarle un validador del Cap 4). Prepara el cerebro para la integración del Boss Final.

3. **Andamiaje Cognitivo / Scaffolding (Para el "Muro de los Tests"):**
   - **Evidencia:** La Zona de Desarrollo Próximo de Vygotsky — el apoyo temporal que se retira gradualmente conforme el aprendiz gana autonomía.
   - **Aplicación:** Los 5 niveles del gradiente de testing actúan como andamios temporales. Capítulos 1-2: andamio completo (solo leer el test). Capítulos 3-4: andamio parcial (pseudo-código y estructura). Boss Final: andamio retirado por completo para forzar la autonomía.

4. **Retrieval Practice / Efecto de Testing (Auto-evaluación activa):**
   - **Evidencia:** El hallazgo más robusto de la psicología cognitiva moderna. Recuperar información activamente (sin mirar el libro) consolida la memoria significativamente más que releer el material. No es el examen lo que mide el aprendizaje — es el examen lo que *produce* el aprendizaje.
   - **Aplicación:** Los checkboxes de auto-evaluación al final de cada capítulo (`¿Puedo explicar X sin mirar el código?`) son actos de retrieval, no de repaso. El Operador debe responderlos sin abrir el capítulo. Los ejercicios Tipo B (intentar escribir el test antes de ver la solución) también son retrieval puro.

5. **Spaced Repetition / Práctica Espaciada (Retención a Largo Plazo):**
   - **Evidencia:** Descrita por Ebbinghaus en 1885 y replicada cientos de veces. Revisar material en intervalos crecientes justo antes de olvidarlo produce retención duradera. Es la base científica de sistemas como Anki.
   - **Aplicación:** A partir del Capítulo 3, cada bloque de `exercises/` incluye un **"Ejercicio de Revisión"** — un ejercicio corto de un capítulo anterior seleccionado por el DM. No es contenido nuevo, es reactivación de lo ya visto en el momento óptimo. Complementa al Interleaving: donde Interleaving mezcla para forzar transferencia, Spaced Repetition reactiva para combatir el olvido.
