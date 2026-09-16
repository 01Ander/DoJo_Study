# Chronicle Template (v5.3)

## General Information
**Chronicle Name:**  
**Chronicle Code:**  
**Version:**  
**Chronicle Type:** CORE-SUBTEMA

---

## 🎯 Business Context & ROI
Describe el problema del mundo real que esta crónica pretende resolver y el retorno de inversión esperado (qué valor aporta a la empresa que un ingeniero sepa esto).

**Business Context:**
> [Problema de negocio o necesidad de la industria]

**ROI Estimado:**
> [Ej. "Permite desacoplar arquitecturas reduciendo tiempo de mantenimiento en un 30%"]

---

## 🎭 Domain Shifting Rule
Declara el dominio temático que se usará para los ejemplos del Lore (teoría) y el dominio que se usará para el Rite (proyecto final). **Deben ser diferentes.**

- **Dominio del Lore (Teoría):** [Ej. Zoológico, Panadería, Gremio de Magos]
- **Dominio del Rite (Proyecto Final):** [Ej. Sistema Bancario, E-commerce, Logística]

---

## 🛠️ Technical Objective
Describe the concrete technical result expected at the end of the chronicle.

**Example:**
> "Understand and apply Python OOP to build modular ETL pipelines."

---

## 📚 Syllabus (Course Structure)

### Lore (Capítulos Teóricos)
Lista 7–8 capítulos. El título debe reflejar **exactamente** los conceptos que se enseñarán.

- Cap 00: [Título] — [Conceptos clave]
- Cap 01: [Título] — [Conceptos clave]
- Cap 02: [Título] — [Conceptos clave]
- ...

---

### Quests (Laboratorios Prácticos)
Cada capítulo teórico (Lore) tiene una carpeta homóloga en `quests/` con ejercicios guiados y tests automatizados (TDD progresivo).

---

### Rite (Proyecto Final — Rito de Paso)
Describe el proyecto integrador. Este Rito debe construirse usando un dominio temático **diferente** al del Lore.
Solo es accesible después de la auditoría del DM (`/scry`).

**Descripción:**
> [Construir una aplicación CLI/Pipeline/API funcional...]

**Fases Desbloqueables:**
1. [Nombre Fase 1] (Mapea a Cap X-Y)
2. [Nombre Fase 2] (Mapea a Cap Z)

---

## 🎓 Domain Criteria (Definition of Done)
Define the indicators that confirm the chronicle is completed. Estos criterios deben cubrir TODAS las competencias extraídas del Syllabus Maestro.

- Can design abstract interfaces with `abc.ABC`.
- Can implement polymorphic behavior across domain entities.
- Can orchestrate an ETL pipeline with dependency injection.

> Nota: Los Domain Criteria se validan formalmente mediante el Rite y la auditoría final del DM.

---

## 🚀 Derived Future Chronicles
(Opcional) Siguientes pasos naturales tras completar esta crónica.
