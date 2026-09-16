# Adenda: Roadmap de Ejecución Resiliente

> **Propósito:** Complementar `09-generation-protocol.md`. El protocolo original define QUÉ hacer en cada paso y gate. Esta adenda define CÓMO ejecutarlo sin que la generación y la auditoría queden contaminadas por el mismo hilo de razonamiento, y sin perder progreso al cambiar de modelo o de sesión.

---

## Problema que resuelve

El protocolo original asume implícitamente una sesión continua: el mismo agente genera y audita. Esto reproduce el sesgo que causó los gaps detectados (un modelo que acaba de escribir algo tiende a confirmar su propio trabajo, no a impugnarlo). Además, si se corta la sesión o se cambia de modelo a mitad de una Chronicle, hoy no hay forma de retomar sin reconstruir contexto desde cero.

La solución: sacar el **estado del pipeline** de la conversación y ponerlo en un artefacto persistente por Chronicle. Cualquier modelo, en cualquier hilo, puede leer ese artefacto, entender exactamente qué le toca hacer, ejecutarlo, y dejar el resultado escrito para quien siga.

---

## Componente 1: Roadmap por Chronicle

Un archivo de estado, uno por Chronicle en generación (ej. `_generation/<CHRONICLE-CODE>/roadmap.md`), con esta estructura mínima:

```yaml
chronicle: CHRONICLE-CODE
paso_actual: 4              # 0-7, según el protocolo
estado: en_progreso         # pendiente | en_progreso | pass | fail
capitulo_actual: 3          # solo relevante en pasos 4-6
requiere_aprobacion_humana: false

contexto_minimo_requerido:
  # Lista exacta de qué debe leer el modelo entrante para ESTE paso,
  # nunca "toda la raíz del repo"
  - docs/09-generation-protocol.md
  - docs/07-campaign-as-course.md
  - subjects/<area>/chronicles/<CODE>/lore/00-intro.md
  - subjects/<area>/chronicles/<CODE>/lore/01-cap.md
  - subjects/<area>/chronicles/<CODE>/lore/02-cap.md

historial_gates:
  - gate: 1
    resultado: pass
    fecha: 2026-09-10
  - gate: 2
    resultado: fail
    fecha: 2026-09-11
    hallazgo:
      capitulo: 2
      termino: "particionado"
      tipo_error: "Tipo 2 - término sin definir"
      detalle: "Se usa en el ejemplo de negocio pero nunca se define qué/cómo/por qué"
      accion: "Regenerar Cap 02 incluyendo definición completa antes de reintentar GATE 2"
  - gate: 2
    resultado: pass
    fecha: 2026-09-11
```

**Reglas del archivo:**
- Es la única fuente de verdad sobre en qué punto está la Chronicle. Ningún modelo debe asumir progreso que no esté escrito aquí.
- `contexto_minimo_requerido` reemplaza al "lee todo el repo": cada paso declara exactamente qué necesita, aplicando el mismo principio de PASO 0 del protocolo original pero por paso, no solo al inicio.
- Un modelo que entra a trabajar en la Chronicle SIEMPRE empieza leyendo este archivo antes que cualquier otra cosa.

---

## Componente 2: Regla de aislamiento generación↔auditoría

**El modelo/sesión que ejecuta un gate no puede ser la misma sesión que generó el contenido que está auditando.** No es una sugerencia de buena práctica: es una regla de ejecución del roadmap.

En la práctica esto significa que al pasar de un paso de generación a su gate correspondiente, el roadmap se marca como "listo para auditoría" y la siguiente sesión que lo tome —sea el mismo modelo en un hilo nuevo, u otro modelo— entra **solo con**:
1. El artefacto generado (el capítulo, el grimoire, la quest — lo que toque).
2. El checklist del gate correspondiente.
3. El `contexto_minimo_requerido` de ese gate.

Nunca con el razonamiento previo de por qué se escribió así. Esto es lo que hace que el gate audite de verdad en vez de autoconfirmar.

---

## Componente 3: Protocolo de fallo estructurado

Un gate no puede resolverse en un simple "PASS/FAIL". Todo FAIL debe registrar en el roadmap:

| Campo | Ejemplo |
|---|---|
| Capítulo/artefacto afectado | Cap 02 |
| Elemento específico | término "particionado" |
| Tipo de error | Tipo 2 — término sin definir (taxonomía ya definida en el protocolo) |
| Detalle | dónde aparece y por qué no cumple |
| Acción concreta | qué debe cambiar, no solo "regenerar" |

Esto evita dos problemas: que el reintento sea a ciegas (repitiendo el mismo error), y que tú, como auditor humano, tengas que reconstruir por qué algo se regeneró dos veces.

---

## Componente 4: Matriz de trazabilidad como artefacto real

El "inventario de términos" del protocolo original queda hoy como lista interna dentro de PASO 4, usada solo por GATE 2. Debe elevarse a archivo real y persistente:

`subjects/<area>/chronicles/<CODE>/lore/matriz-trazabilidad.md`

Con una fila por término/concepto introducido, el capítulo donde se define, y qué competencia del syllabus cubre. Este archivo:
- Se actualiza incrementalmente, capítulo a capítulo (nunca de golpe al final).
- Es el input directo del PASO 7 (Rite): el Rite solo puede exigir conceptos que estén en esta matriz.
- Es lo que permite auditar GATE 5 (auditoría final integral) sin releer todo el Lore de cero.

---

## Componente 5: Gates humanos vs. gates de IA

No todos los gates necesitan tu revisión personal — eso anularía la ganancia de automatizar. Propuesta de reparto:

- **Gate 1 (Scope)** → revisión humana obligatoria. Es el más barato de corregir aquí y el más caro de arrastrar si está mal.
- **Gate 2, 3, 4** → auditoría IA en frío (Componente 2), sin tu intervención salvo que fallen dos veces seguidas el mismo gate.
- **Gate 5 (Final integral)** → revisión humana obligatoria antes de dar la Chronicle por cerrada.

El roadmap marca `requiere_aprobacion_humana: true/false` por gate, así el modelo que lo procesa sabe si debe detenerse a esperar tu firma o puede seguir solo.

---

## Resumen del flujo con roadmap

1. Modelo entra a la Chronicle → lee `roadmap.md` primero, nada más.
2. Roadmap le dice: paso actual, qué leer, si el paso anterior fue generación o auditoría.
3. Ejecuta solo esa unidad de trabajo (un capítulo, un gate).
4. Escribe el resultado en el artefacto correspondiente y actualiza `roadmap.md`.
5. Si el paso que sigue es un gate, la sesión termina ahí — el gate lo toma una sesión nueva, sin el razonamiento de este hilo.
6. Si el gate requiere aprobación humana, el roadmap queda en `estado: en_espera_operador` hasta que tú lo revises.
