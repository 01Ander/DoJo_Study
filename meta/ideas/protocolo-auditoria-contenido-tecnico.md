# Protocolo de Auditoría: Profundidad Técnica y Suficiencia de Contenido (2026)

> **Propósito:** Definir el marco metodológico para auditar de forma independiente y triangulada (mediante 3 modelos de lenguaje distintos) todo el contenido técnico generado en el sistema (`PY-BASICO`, `PY-POO`, `SQL-BASICO`, `DE-PIPELINES`, `CLOUD-AWS`).
> 
> **Objetivo Exclusivo:** Determinar si el temario, la profundidad teórica, los ejemplos de código, las quests y los rites son técnicamente suficientes para superar pruebas técnicas rigurosas de la industria (live coding, take-home projects y preguntas de arquitectura).
> 
> **Regla de Alcance y Contención:** Esta auditoría busca diagnosticar la salud del sistema sin provocar una proliferación infinita de cursos (evitando la trampa histórica de rediseños perpetuos). Los hallazgos que impliquen "Creación de Nuevo Subject" se registran en un backlog priorizado, pero su ejecución queda supeditada a completar primero el subject de conceptos faltantes (Track 1) y el Rite del syllabus — ningún subject nuevo se genera automáticamente solo por alcanzar consenso de los modelos.

---

## 1. El Pilar de Vigencia Externa (Evidencia Técnica de Mercado 2026)

Este pilar consolida la evidencia técnica de la industria recopilada para el año 2026. Se entrega como insumo fijo a los modelos auditores para evaluar la vigencia del contenido sin depender de búsquedas en vivo ni sesgos subjetivos.

### 1.1 Núcleo Técnico No Negociable
* **SQL Avanzado:** El filtrado básico (`SELECT * WHERE`) no es suficiente. Pruebas técnicas y evaluaciones en vivo exigen dominio fluido de: JOINs complejos, agregaciones condicionales, expresiones de tabla común (CTEs), funciones de ventana (`ROW_NUMBER`, `DENSE_RANK`, `LAG`, `LEAD`, sumas acumuladas) y modelado de datos.
* **Python de Ingeniería:** Enfoque en robustez de ingeniería: consumo resiliente de APIs, paginación exhaustiva, serialización de formatos de datos (JSON, Parquet, CSV), limpieza vectorial, tipado estricto, logging estructurado y modularización orientada a objetos.
* **Control de Versiones (Git):** Convenciones semánticas de commits, branching y pipelines de CI básicos con ejecución automatizada de tests.
* **Pipeline Integrador End-to-End:** Capacidad de conectar la cadena completa: extracción de API externa → validación de calidad → almacenamiento raw/cloud → transformación → carga en base de datos/warehouse → orquestación periódica automatizada.

### 1.2 Bases de Datos y Almacenamiento: El Desacople RDBMS vs. Data Warehouse
* **RDBMS Transaccionales de Producción:** La industria exige experiencia práctica con motores de producción reales (**PostgreSQL**, MySQL). Los entornos aislados o simplificados en memoria/archivo único (como SQLite) sirven para prototipos rápidos, pero dejan lagunas críticas en: gestión de conexiones concurrentes, tipos de datos específicos de motor, índices avanzados y administración de transacciones reales bajo carga.
* **Cloud Data Warehouses (OLAP):** Separación explícita entre almacenamiento transaccional (OLTP) y analítico masivo. La industria exige comprender y manipular almacenes analíticos en la nube (**Snowflake, BigQuery o Redshift**) o motores de consulta serverless sobre objetos (**Athena / AWS Glue Catalog**).
* **Modelado Dimensional y SCD Tipo 2:** Comprensión rigurosa de esquemas en estrella (*Star Schema*), tablas de hechos y dimensiones, y manejo de dimensiones lentamente cambiantes (**Slowly Changing Dimensions - SCD Tipo 2**) para seguimiento de historial, un tópico cardinal en pruebas de diseño analítico.

### 1.3 Orquestación y Transformación Moderna
* **Apache Airflow como Estándar Dominante:** Airflow representa la herramienta con mayor presencia en evaluaciones técnicas y sistemas en producción (concepto de DAGs, operadores, tareas dependientes, scheduler, sensors y reintentos). Herramientas más ligeras (como Prefect) son válidas pedagógicamente, pero conocer la arquitectura y terminología de Airflow es indispensable para las evaluaciones técnicas de la industria.
* **Transformación Declarativa:** dbt (*data build tool*) como patrón de facto para modelado y transformación dentro del warehouse.

### 1.4 Arquitectura Cloud y Manejo Seguro de Infraestructura
* **Servicios de Datos en la Nube (AWS):** Almacenamiento distribuido (S3 con particionamiento eficiente `year/month/day`), cómputo serverless (Lambda para tareas ligeras e ingesta), bases de datos gestionadas (RDS PostgreSQL), catálogo de metadatos (Glue) y consultas directas sobre almacenamiento de objetos (Athena).
* **Seguridad y Secretos:** Cero tolerancia al hardcoding o variables inseguras de consola. Manejo mediante gestores de secretos dedicados (AWS Secrets Manager / KMS) o autenticación IAM a bases de datos.

### 1.5 Contenerización
* **Docker Básico:** Empaquetado de scripts, orquestadores y bases de datos locales mediante `Dockerfile` y `docker-compose.yml` para garantizar reproducibilidad exacta y desacoplamiento de dependencias del sistema operativo host.

---

## 2. Insumos Fijos del Proceso de Auditoría

Cada modelo auditor recibirá como contexto inmutable:

1. **El Pilar de Vigencia Externa:** Sección 1 de este documento.
2. **Estándares de Código del Sistema:** [`system/docs/06-convenciones-codigo.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/system/docs/06-convenciones-codigo.md) (PEP 8, tipado estricto, logging forense, TDD con `pytest`).
3. **Syllabus Maestro Actual:** [`system/docs/05-syllabus-maestro.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/system/docs/05-syllabus-maestro.md).
4. **Materia Prima del Subject a Auditar:**
   * Archivo de estructura: `chronicle.md`
   * Todos los capítulos teóricos: `lore/`
   * Todos los laboratorios y código de soporte: `quests/`
   * Proyecto integrador y criterios: `rite/requirements.md` y `solution.py` (si existe).

> [!CAUTION]
> **Confinamiento de Filesystem (Aislamiento Antisesgos):**
> Al operar con agentes que disponen de herramientas nativas de lectura de archivos, el modelo tiene terminantemente prohibido inspeccionar cualquier ruta fuera del perímetro del subject en turno (prohibido leer otras Chronicles, archivos de `meta/` o historial de commits de Git). La triangulación exige que cada subject sea evaluado como una unidad atómica y aislada.

---

## 3. Los Cinco Filtros de Evaluación (Criterios de Corte)

Cada modelo auditor evaluará el contenido sometiéndolo a cinco preguntas deterministas:

### Filtro 0: Fidelidad y Trazabilidad Interna (Lore ↔ Quests ↔ Rite ↔ solution.py)
* ¿Existe una correspondencia exacta entre lo enseñado en `lore/`, lo ejercitado en `quests/`, y lo exigido en `rite/requirements.md`?
* ¿El `rite/requirements.md` exige conceptos, herramientas o restricciones que nunca fueron introducidos ni practicados en `lore/` o `quests/` (falsos positivos pedagógicos)?
* ¿El archivo `solution.py` (o soluciones de laboratorio, si existen) se mantiene estrictamente dentro del scope declarado de la quest/rite, sin excederse con herramientas no vistas ni quedarse corto?
* *Criterio de fallo:* Cualquier desincronía entre las tres piezas (Lore enseña A, Quest ejercita B, Rite pide C, o Solution resuelve usando Z no enseñado). Este filtro es prioritario para subjects tempranos (`PY-BASICO`, `PY-POO`) construidos antes del estándar de matriz de trazabilidad.

### Filtro 1: Profundidad Conceptual vs. Explicación Superficial (Lore)
* ¿El contenido explica únicamente la sintaxis básica ("cómo se llama la función"), o profundiza en los mecanismos internos, casos de borde (*edge cases*) y compensaciones (*trade-offs*) arquitectónicos?
* ¿Prepara al estudiante para responder con solidez preguntas teóricas y conceptuales en una evaluación técnica en vivo?
* *Criterio de fallo:* Capítulos que presentan conceptos complejos de forma trivial o que omiten las implicaciones de rendimiento y escalabilidad.

### Filtro 2: Código de Producción vs. Código de Juguete (Quests y Rites)
* ¿Los ejercicios y proyectos enseñan patrones de código reales de la industria?
  * Manejo granular de excepciones de dominio (no `except Exception: pass`).
  * Validación estricta de contratos y esquemas de datos.
  * Estrategias de reintento con backoff exponencial ante fallos transitorios de red/APIs.
  * Paginación obligatoria y control de límites de tasa (*rate limits*) en ingesta.
  * Idempotencia en cargas de datos (garantía de no duplicación ante ejecuciones repetidas).
  * Logging forense estructurado.
* *Criterio de fallo:* Scripts lineales, uso de `assert` genéricos en lugar de validaciones de producción, falta de tipado estricto o suposición de datos limpios ideales.

### Filtro 3: Cobertura de Herramientas y Patrones Estructurales
* ¿Qué herramientas, patrones o estándares indispensables para interactuar en un equipo de datos moderno fueron omitidos en este subject?
* *Criterio de fallo:* Ejemplos: haber practicado SQL únicamente en SQLite sin ver un motor cliente-servidor real; enseñar orquestación sin mencionar el estándar dominante de DAGs; omitir contenedores para aislar dependencias; tratar la paginación como algo opcional.

### Filtro 4: Suficiencia para Pruebas Técnicas (Live Coding & Take-Home)
* Si a un estudiante se le presenta una prueba técnica de codificación en vivo o un ejercicio para llevar a casa (*take-home challenge*) basado en los temas de este subject:
  * ¿Cuenta con el andamiaje necesario para superarla con soltura?
  * ¿En qué puntos específicos se quedaría bloqueado por falta de entrenamiento en el sistema?

---

## 4. Plantilla de Salida Estandarizada para los Auditores

Para permitir la triangulación objetiva entre los 3 modelos, cada auditor debe responder estrictamente con esta matriz por cada subject:

```markdown
# Auditoría de Subject: [CÓDIGO-DEL-SUBJECT]
**Modelo Auditor:** [Nombre del Modelo y Versión]
**Ruta de Destino:** `meta/audits/2026-q3-contenido/[CARPETA-DEL-SUBJECT]/[nombre-modelo].md`
**Veredicto General:** [APTO / PARCIAL / INSUFICIENTE]

> REGLA DE ETIQUETADO OBLIGATORIO: TODO bullet point de las secciones 0, 1, 2 y 3 DEBE iniciar obligatoriamente con una etiqueta entre corchetes:
> `[🔴 Bloqueante Técnico]` : Descalificación en entrevista, falso positivo evaluativo o bug grave.
> `[🟡 Deficiencia / Antipatrón]` : Explicación superficial, código frágil o deuda técnica.
> `[🟢 Conforme / Cosmético]` : Conforme al estándar de industria, o detalle menor de redacción.

## 0. Fidelidad y Trazabilidad Interna (Lore ↔ Quests ↔ Rite ↔ solution.py)
* [Etiqueta] **Exigencias del Rite vs. Lore:** [¿El Rite exige conceptos no explicados en el Lore? Sí/No. Si es Sí, cita archivo, línea y concepto no enseñado. Si es No, marca 🟢 Conforme]
* [Etiqueta] **Scope de Soluciones vs. Quests:** [¿El solution.py o quests desbordan o recortan el scope declarado? Sí/No/No aplica. Cita archivo y técnica. Si no desborda, marca 🟢 Conforme]
* [Etiqueta] **Coherencia y Trazabilidad General:** [Desincronías detectadas entre las 3 piezas, o "🟢 Conforme: alineación completa"]

## 1. Evaluación de Profundidad Conceptual (Lore)
* [Etiqueta] **Rigor y Mecanismos Internos:** [Análisis en máx 4 líneas sobre si el Lore explica mecanismos internos, trade-offs y edge cases, o solo sintaxis básica]
* [Etiqueta] **Defensa en Evaluaciones Teóricas:** [Listado de 2-3 preguntas técnicas de arquitectura que el estudiante no podría responder con este Lore, o "🟢 Conforme: preparación teórica sólida"]

## 2. Evaluación de Rigor de Código (Quests & Rites)
* [Etiqueta] **Realismo y Calidad de Código:** [Análisis en máx 4 líneas de antipatrones detectados vs código de producción con archivo y línea si aplica, o "🟢 Conforme: código realista"]
* [Etiqueta] **Resiliencia, TDD y Calidad:** [Evaluación de excepciones de dominio, tipado, logging, TDD e idempotencia, o "🟢 Conforme: estándares de producción cumplidos"]

## 3. Brechas de Cobertura y Herramientas (Faltantes Críticos)
* [Etiqueta] **Herramientas de Industria Ausentes:** [Herramientas del Pilar de Mercado omitidas en este subject que generan brecha crítica, o "🟢 Conforme: cobertura adecuada"]
* [Etiqueta] **Patrones Arquitectónicos Omitidos:** [Patrones que debieron introducirse y faltan, o "🟢 Conforme: patrones cubiertos"]

## 4. Recomendación de Reestructuración
* [ ] **Ajuste de Fidelidad Interna (Fix Quirúrgico):** Sincronizar Lore, Quests y Rite para eliminar desbordes o conceptos no enseñados.
* [ ] **Ajuste Menor de Profundidad:** Expandir capítulos existentes de Lore o corregir tests en Quests.
* [ ] **Refactor Mayor del Subject:** Rehacer Quests/Rites para elevar el estándar a código de producción.
* [ ] **Propuesta de Nuevo Subject (Al Backlog Priorizado):** Requiere un Subject independiente; se registra en backlog sin ejecución inmediata.
  * *Propuesta de nuevo módulo o subject:* [Nombre, alcance y justificación técnica en máx 4 líneas]
```

---

## 5. Metodología de Ejecución, Triangulación y Consolidación

### 5.1 Entorno Git y Ubicación de Archivos
* **Rama Git:** Exclusiva de **`chronicles`**. El material evaluado (`content/subjects/`) solo existe en esta rama. Mantener los artefactos de auditoría en `chronicles` preserva la rama `main` como blueprint limpio.
* **Propagación hacia `main`:** Si la auditoría deriva en ajustes a la gobernanza o syllabus maestro ([`system/docs/05-syllabus-maestro.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/system/docs/05-syllabus-maestro.md)), ese commit puntual se traslada a `main` quirúrgicamente vía `git cherry-pick`, jamás mediante merge completo.
* **Estructura de Directorios:** Los artefactos de auditoría se centralizan en:
  ```text
  meta/audits/2026-q3-contenido/
  ├── 00-protocolo.md               ← Copia/referencia a este protocolo
  ├── 01-py-basico/
  │   ├── gemini.md
  │   ├── opus.md
  │   ├── sonnet.md
  │   └── consolidado-py-basico.md  ← Matriz de consenso del subject
  ├── 02-py-poo/
  │   ├── gemini.md
  │   ├── opus.md
  │   ├── sonnet.md
  │   └── consolidado-py-poo.md
  ├── 03-sql-basico/
  │   └── ...
  ├── 04-de-pipelines/
  │   └── ...
  ├── 05-cloud-aws/
  │   └── ...
  └── REPORTE-CONSOLIDADO-FINAL.md  ← El wrap ejecutivo global de los 5 subjects
  ```

### 5.2 Estrategia de Consolidación Atómica (Por Subject)
Para evitar la saturación de contexto (gestionar 15 documentos a la vez) y no postergar la deuda técnica, **no se realiza una consolidación masiva al final**. Se opera de forma modular por subject:

1. **Ejecución Asíncrona Externa:** El Operador corre el prompt del protocolo en los 3 modelos para el subject en turno y guarda las 3 respuestas en su carpeta (`gemini.md`, `opus.md`, `sonnet.md`).
2. **Triangulación Inmediata (Antigravity en Modo Arquitecto):** Antigravity lee los 3 reportes y genera el archivo `consolidado-[subject].md` cruzando consensos y divergencias.
3. **Registro y Aislamiento de Hallazgos (Cero Hotfixes en Caliente):** Los hallazgos de **Filtro 0** (fidelidad interna Lore ↔ Quests ↔ Rite ↔ solution.py) y antipatrones de código se registran y tipifican en `consolidado-[subject].md`, pero **no se corrigen durante la ejecución de la auditoría**. La tarea en esta fase es única y exclusivamente auditar. Las correcciones se postergan hasta completar la auditoría de los 5 subjects, permitiendo consolidar múltiples gaps menores y resolverlos en una fase separada agrupados por tipo (trazabilidad, antipatrones de código, gaps de cobertura) en vez de intervenir subject por subject de forma aislada y sin visión de conjunto.

### 5.3 Reglas de la Matriz de Consenso
* **Consenso en Fidelidad Interna o Antipatrones (2/3 o 3/3):** Se clasifican como *Correcciones Obligatorias* en el consolidado del subject, para ser agrupadas y ejecutadas en el lote de remediación post-auditoría.
* **Consenso en Propuesta de Nuevo Subject (2/3 o 3/3):** **No se ejecuta de inmediato.** Se archiva en el *Backlog Priorizado de Subjects*. Su construcción queda formalmente supeditada a terminar primero el subject de conceptos faltantes (Track 1) y el Rite del syllabus.
* **Divergencia (1/3):** Se descarta como sobreingeniería o preferencia estilística del modelo, a menos que señale un bug de sintaxis objetivo.

### 5.4 El "Wrap" y Cierre Global (`REPORTE-CONSOLIDADO-FINAL.md`)
Una vez completados y consolidados los 5 subjects:
1. Antigravity compila y analiza los 5 archivos `consolidado-*.md`.
2. Genera `REPORTE-CONSOLIDADO-FINAL.md` con tres entregables:
   * **Plan Agrupado de Remediación:** Inventario consolidado de todos los fixes de fidelidad interna y antipatrones detectados, organizados por categoría técnica (ej. desincronías Lore-Rite, refactorización de tests/quests, sanitización de antipatrones) para ejecutarse como un bloque de trabajo coordinado.
   * **Backlog Priorizado de Subjects/Módulos:** Inventario consolidado de temas estructurales acordados para fases posteriores.
   * **Propuesta de Commit para `05-syllabus-maestro.md`:** Actualización canónica del blueprint para ser llevada a `main` vía cherry-pick.

### 5.5 Flujo de Ejecución Paso a Paso para el Operador
1. **Crear el directorio de trabajo:**  
   Las subcarpetas ya se encuentran creadas en `meta/audits/2026-q3-contenido/` (`01-py-basico/` a `05-cloud-aws/`).
2. **Lanzar la auditoría con el prompt inicial:**  
   Copiar la plantilla de lanzamiento de la Sección 5.6 con los parámetros del subject y modelo en turno, ejecutándola directamente en Antigravity.
3. **Ejecutar en paralelo en los 3 modelos:**  
   Entregar el prompt de lanzamiento idéntico a Gemini Pro, Claude Opus y Sonnet.
4. **Verificar respuestas en crudo:**  
   Confirmar que cada modelo haya escrito su archivo respectivo (`gemini.md`, `opus.md`, `sonnet.md`) en la carpeta del subject.
5. **Detonar la consolidación:**  
   En sesión de Arquitecto, solicitar a Antigravity: *"Triangula los 3 reportes en `meta/audits/2026-q3-contenido/XX-subject/` y genera `consolidado-[subject].md`"*.
6. **Avanzar secuencialmente:**  
   Repetir los pasos 2 a 5 para los 5 subjects en orden (`PY-BASICO` ➔ `PY-POO` ➔ `SQL-BASICO` ➔ `DE-PIPELINES` ➔ `CLOUD-AWS`).
7. **Detonar el Wrap Final:**  
   Al completar los 5 subjects, solicitar a Antigravity la generación de `REPORTE-CONSOLIDADO-FINAL.md` y proceder a la fase agrupada de remediación.

### 5.6 Invocación de la Auditoría (Llamado a Función en Modo Agente)

El archivo [`meta/ideas/prompt-auditoria-modelos.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/ideas/prompt-auditoria-modelos.md) opera como una especificación funcional autónoma: contiene las reglas, calibración, insumos de lectura y la tabla de resolución automática de rutas del repositorio.

Para detonar la auditoría de cualquier subject en Antigravity, el Operador solo envía este llamado directo de dos parámetros:

```text
Ejecuta la auditoría técnica definida en meta/ideas/prompt-auditoria-modelos.md con:
- SUBJECT: [PY-BASICO | PY-POO | SQL-BASICO | DE-PIPELINES | CLOUD-AWS]
- MODELO: [gemini | opus | sonnet]
```

> **Aclaración de Nomenclatura del Repositorio:**  
> En la estructura física actual de `content/subjects/`, la división `python` es la única que contiene múltiples Chronicles (`PY-BASICO` y `PY-POO`). Las divisiones `sql`, `data_engineering` y `cloud` albergan una sola Chronicle cada una (`SQL-BASICO`, `DE-PIPELINES`, `CLOUD-AWS`). La tabla interna de `prompt-auditoria-modelos.md` resuelve automáticamente la ubicación exacta de cada una.
