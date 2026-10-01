# Rite Requirements — `<CHRONICLE-CODE>`

> **Instrucción para el Operador:** Este es tu proyecto final (Rito de Paso). Integra todos los conceptos aprendidos en la Chronicle. Debes implementar cada fase de manera progresiva y registrar tus avances en `journal.md`.
>
> ⚠️ **Zero Surprise Syntax:** Solo puedes emplear herramientas y sintaxis que estén documentadas en la Matriz de Trazabilidad de esta Chronicle.

---

## 🎯 Business Context
**Problema de Negocio:**
> [El generador detalla un problema complejo del mundo real en el dominio temático exclusivo del Rite]

**ROI (Return of Investment):**
> [El impacto de negocio que tendrá construir este sistema]

---

## 🛠️ Arquitectura Esperada
- **Inputs:** [Qué recibe el sistema]
- **Procesamiento:** [Qué hace con los datos]
- **Outputs:** [Qué genera o dónde guarda los resultados]
- **Domain Shifting:** Este proyecto ocurre en el dominio de **[Dominio del Rite]**, lo que significa que deberás traducir lógicamente los conceptos aprendidos en los ejemplos del Lore a este nuevo entorno.

---

## 📄 Data Contract *(incluir si el proyecto procesa datos externos)*

> **Nota para el Generador:** Esta sección aplica cuando el Rite involucra procesamiento de datos provenientes de un sistema upstream (archivos, eventos, APIs, streams). Es el contrato que el Data Engineer recibe — no diseña. Omitir si el proyecto no tiene fuente de datos externa definida.

### Payload Raw
Ejemplo representativo del dato tal como llega desde el sistema upstream:

```json
{
  "[campo_1]": "[valor_ejemplo]",
  "[campo_2]": "[valor_ejemplo]"
}
```

> Indicar qué campos son relevantes para el pipeline y cuáles son metadata que se descarta.

### Evento / Trigger del Sistema *(si aplica)*
Si el entry point recibe un evento estructurado (S3 Event, SQS Message, API Gateway payload), mostrar su estructura:

```json
{
  "[estructura_del_evento]": "..."
}
```

### Schema Destino *(si aplica)*
Estructura del destino donde el pipeline carga los datos (tabla SQL, coleccion NoSQL, archivo de salida):

```sql
-- O el formato que corresponda al destino del proyecto
CREATE TABLE [nombre_tabla] (
    [columna] [TIPO] [restricciones]
);
```

---

## 🚀 Fases Desbloqueables

> **Nota Arquitectónica para el Generador:** Las fases deben seguir el flujo de construcción real del proyecto, no la secuencia numérica de los capítulos del Lore. Las referencias a capítulos son de soporte conceptual (`Referencia: Cap X`), no de orden de ejecución. Si el proyecto tiene un punto de entrada orquestador definido (handler, router, CLI, pipeline), la Fase 1 define ese contrato. El número de fases responde a los hitos funcionales del proyecto: varios capítulos pueden consolidarse en una sola fase cuando su integración conjunta es el hito real de entrega de valor.

### Fase 1: [Nombre de la Fase] (Referencia: Cap [X])
[Descripción del objetivo de esta fase como hito de construcción del proyecto.]

**Criterios de Aceptación (DoD):**
- [ ] Criterio 1 (Ej: "El punto de entrada `handler` está definido con su contrato documentado")
- [ ] Criterio 2
- [ ] Realiza un Semantic Commit al completar esta fase.

### Fase 2: [Nombre de la Fase] (Referencia: Cap [Y])
[Descripción del objetivo de esta fase como hito de construcción del proyecto.]

**Criterios de Aceptación (DoD):**
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Realiza un Semantic Commit al completar esta fase.

*(El generador definirá las fases necesarias según los hitos funcionales del proyecto. No se fuerza una fase por capítulo.)*

---

## ✅ Criterios de Aprobación Final (Gate 5)
Para que el DM certifique que has superado esta Chronicle:
1. El proyecto completo debe ejecutarse sin errores de principio a fin.
2. La suite de pruebas (TDD) debe tener cobertura completa sobre la lógica de negocio.
3. **Sin hardcoding ni artefactos descartables:** El artefacto final no puede depender de herramientas de desarrollo local que el entorno de producción no usa (ej. `dotenv` donde el runtime inyecta variables nativas). Toda configuración externalizada debe seguir el patrón de producción real del sistema.
4. El `journal.md` debe estar completamente documentado.
