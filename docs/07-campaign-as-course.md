# 07 - Campaign as Course (Modelo v5.0)

> **Implementado en:** v5.0
> **RFC de referencia:** `ideas/proposal-study-guide-layer.md`

Este documento define la arquitectura "Campaign as Course", el modelo pedagógico estándar del DoJo a partir de la v5.0.

## 0. El Glosario RPG (Nomenclatura Oficial)

Para mantener la identidad del DoJo mientras adoptamos un modelo académico riguroso, esta es la traducción oficial de términos:

| RPG Term | Equivalente Académico | Descripción en v5 |
|---|---|---|
| **Campaign** | Curso / Materia | Ruta completa de aprendizaje (ej. `PY-POO`) |
| **Lore** | Lección Teórica | Archivos `.md` en `lore/` con conceptos |
| **Quest** | Laboratorio / Ejercicio | Práctica guiada en `quests/` |
| **Grimoire** | Bitácora Feynman | Documento de síntesis del Operador (`grimoire.md`) |
| **Boss** | Proyecto Integrador | Artefacto monolítico que demuestra dominio total en `boss/` |
| **Dungeon Master (DM)** | Auditor / Gatekeeper | El agente que verifica el `grimoire.md` |
| **Operator** | Estudiante | Quien ejecuta el aprendizaje |
| **Architect** | Diseñador del Sistema | Rol de mantenimiento del DoJo |

---

## 1. Topología `CORE-SUBTEMA`

Las campañas dejan de tener sufijos históricos (`-FINANCE`, `-V2`). Su tipología es estrictamente `CORE-SUBTEMA`.

**Ejemplos Válidos:**
- `PY-POO` (Python Object Oriented)
- `DE-ETL` (Data Engineering ETLs)
- `PY-API` (Python APIs)

**Ejemplos Inválidos:**
- `PY-POO-LEGACY`
- `DE-ETL-V2`

## 2. Anatomía de una Campaña v5.0

La estructura abandona el esquema de misiones progresivas "ciegas" en favor de un enfoque estructurado de Curso + Laboratorio:

```
CAMPAÑA/
├── campaign.md          ← Descripción de alto nivel
├── grimoire.md     ← Bitácora académica (Técnica Feynman)
├── lore/              ← Libro de texto estático (.md)
├── quests/           ← Laboratorios atómicos y testing
└── boss/             ← Boss (monolito)
    ├── journal.md       ← Bitácora clásica técnica (solo para el Boss)
    └── requirements.md  ← Requisitos y fases del Boss
```

### 2.1 La Capa `lore/`
Actúa como un libro de texto. Son archivos Markdown con la teoría, código de ejemplo, e instrucciones de entorno.
- **Regla de Oro:** Siempre utiliza *Domain Shifting*. Si el proyecto de la campaña trata sobre Finanzas, los ejemplos de la teoría deben tratar sobre Zoológicos, Reservas de Hotel, o cualquier otro dominio ajeno. Esto fuerza al Operador a traducir la lógica, evitando el "copy-paste".

### 2.2 La Capa `quests/`
Contiene la práctica deliberada, dividida por capítulos homólogos a la teoría.
- **Testing Progresivo (Scaffolding):** Para eliminar la fricción del TDD, se utiliza un modelo de andamiaje de 5 niveles que va desde "solo leer un test" hasta "escribir todo desde cero".
- **Spaced Repetition:** Los capítulos avanzados incluyen ejercicios de revisión de capítulos pasados.

### 2.3 `grimoire.md` (El Requisito Socrático)
El aprendizaje pasivo no existe. Después de leer cada capítulo y hacer sus ejercicios, el Operador *debe* escribir en esta bitácora qué comprendió, usando sus propias palabras (Técnica Feynman).
- Solo cuando el DM certifica que este documento refleja una verdadera asimilación, se autoriza el acceso al Boss.

### 2.4 La Capa `boss/` (Boss)
El proyecto final reemplaza las "Misiones" v4. Es un desarrollo monolítico (una CLI, una API, un pipeline) compuesto por fases internas desbloqueables.
- **Diagnóstico Quirúrgico:** Si el Operador falla gravemente en la Fase 2 del Boss (ej: Polimorfismo), no reinicia el Boss. El Reviewer diagnostica y le envía de regreso al Capítulo 02 de Teoría y Ejercicios específicos.

## 3. El Flujo de Trabajo (Ciclo por Capítulo)

El Operador no pide código al LLM. Avanza offline o con el IDE:

```ascii
📖 Leer lore/Cap-N  (sin LLM)
     ↓
✏️  Completar quests/Cap-N  (con soluciones en archivo separado)
     ↓
📓 Escribir entrada en grimoire.md
     ↓
Repetir con el siguiente capítulo
     ↓
DM audita grimoire.md → autoriza Boss
     ↓
🔨 Desarrollar Boss (apoyo del Reviewer Socrático)
```

## 4. El Dungeon Master (DM / Gatekeeper)

El rol del DoJo Agent muta de "explicador interactivo" a Auditor y Gatekeeper.

### Estándar de Respuesta Académica
Cuando el Operador utiliza la skill `/dojo-ask` para resolver dudas de la capa de teoría, el DM responde bajo este estándar restrictivo para proteger la concentración (flow) del Operador:
- **Límite Estructural:** Máximo 3 párrafos por explicación.
- **Tono:** Claro y directo. Sin verbosidad ni preámbulos tipo "Claro, aquí tienes la explicación".
- **Fragmentación:** Si la duda requiere una respuesta inmensa, el DM la divide: *"Esta pregunta tiene dos partes, ¿comenzamos por X o por Y?"*
- **Precisión Contextual:** La respuesta debe basarse estrictamente en la teoría leída, sin alucinar con bibliotecas externas.
