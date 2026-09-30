# Plan Post-Syllabus: Dos Tracks Independientes

> **Contexto:** Al cerrar `CLOUD-AWS`, surgieron dos necesidades distintas que se venían tratando como una sola "auditoría". Este documento las separa para no perder la distinción.

---

## Track 1 — Gaps Confirmados (Aditivo, listo para construir)

No requiere más validación. Ya está triangulado por dos fuentes de mercado independientes (búsqueda propia + búsqueda externa vía otro modelo) y por hallazgos directos del propio Grimoire de `CLOUD-AWS`. Va directo a diseño del **subject de conceptos faltantes** — no necesita auditoría, necesita generación de contenido nuevo.

### Gaps de herramienta (concepto ya dominado, falta superficie de la herramienta)
- **AWS Glue y Athena** — extensión natural sobre S3/zonas Bronze-Silver-Gold ya cubiertas.
- **Un cloud data warehouse** (Snowflake, BigQuery o Redshift — elegir uno) — separar explícitamente "base transaccional" (RDS) de "warehouse analítico".
- **Introducción conceptual a Apache Airflow** — no reemplaza Prefect; se agrega porque domina las ofertas reales de mercado.
- **Docker básico** — no cubierto en ningún subject hasta ahora.

### Gap conceptual real (requiere explicación nueva, no solo práctica de sintaxis)
- **SCD Type 2 (Slowly Changing Dimensions)** — profundización sobre el star schema/fact-dimension ya visto en `SQL-BASICO`.

### Gaps ya identificados antes de esta ronda de mercado (siguen vigentes)
- `DE-PIPELINES`: paginación de API tratada como opcional (riesgo de pérdida silenciosa de datos), orquestación que enseña reintentos pero nunca scheduling/deployment real, Quality Gates con `assert` genérico en vez de Domain Exceptions.
- `CLOUD-AWS` Cap 05: credenciales vía variables de entorno de consola, sin mencionar AWS Secrets Manager ni IAM Database Authentication.

### Explícitamente fuera de este track
- El hallazgo de que solo ~3-5% de las vacantes de Data Engineer son genuinamente entry-level (Apiva/InterviewStack) es una decisión de **estrategia de búsqueda de empleo**, no de contenido de syllabus. Se retoma en la fase de empleabilidad, junto con la estrategia de posicionarse con títulos adyacentes (Data Engineer Associate, ETL/Automation Engineer, Analytics Engineer).

---

## Track 2 — Auditoría de Contenido Ya Generado (Validar lo existente)

Cubre `PY-BASICO`, `PY-POO`, `SQL-BASICO`, `DE-PIPELINES`, `CLOUD-AWS`. A diferencia del Track 1, aquí sí puede aparecer algo que nadie ha visto todavía — requiere ejecución activa, no solo una lista.

### Dos pilares de verificación (no confundir)
1. **Fidelidad interna:** ¿el Lore enseñó lo que el Rite exige? ¿el código de la quest/solución respeta el scope de ambos, sin quedarse corto ni excederse? (mismo tipo de hallazgo que el bug de `SQL-BASICO` — Rite pidiendo algo no enseñado — y el de `solution.py` en `CLOUD-AWS` — solución excediendo el scope de la quest).
2. **Vigencia externa:** ¿lo enseñado sigue siendo correcto y suficiente frente al estándar de mercado 2026? Pilar fijo: `mercado-laboral-data-engineer-2026.md` (documento ya generado con dos búsquedas independientes).

### Método
- Recorrer subject por subject, no todos a la vez.
- Ningún subject se descarta por "parecer" ya sólido — el caso de SQL-BASICO/SQLite mostró que un gap de scope no se detecta con una revisión superficial.
- Triangular con 2-3 modelos distintos corriendo la **misma auditoría completa** (no dividir por especialidad) para poder comparar consenso y divergencia, igual que se hizo con la validación original del scope del syllabus (4 IAs) y con esta ronda de mercado (2 búsquedas independientes).
- Cada hallazgo se etiqueta como "gap de fidelidad" o "gap de cobertura" para saber en qué categoría hay consenso.
- Insumos fijos a entregar a cada modelo auditor: el `chronicle.md`/`requirements.md` del subject en cuestión, `06-convenciones-codigo.md`, y `mercado-laboral-data-engineer-2026.md`.

### Estado
Pendiente de ejecutar. El prompt de auditoría aún no se ha redactado.

---

## Orden Sugerido
1. Rite de `CLOUD-AWS` (mañana).
2. Diseñar y ejecutar el subject de conceptos faltantes (Track 1 — ya tiene su lista cerrada).
3. Rite del syllabus (proyecto de unificación, no subject nuevo).
4. Track 2 en paralelo o después, sin que compita por tiempo con los dos meses reservados para inglés y portafolio.
