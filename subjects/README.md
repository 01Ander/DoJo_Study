# Subjects – The DoJo Engineering Divisions

Este directorio organiza todas las divisiones operativas técnicas del DoJo Study.  
La finalidad es mantener el ecosistema de aprendizaje estructurado en **Chronicles (Crónicas)**, alejándonos de los scripts básicos y acercándonos a verdaderos Pipelines de datos.

---

## 1. Objetivo Operativo de este Directorio

`subjects/` funciona como tu entorno corporativo simulado:
- Punto de acceso masivo a las ramas técnicas.
- Base central donde se documentan diseños y pruebas bajo estándares de QA. 
- Aislante del ruido teórico: Aquí se programa bajo protocolos de **Deep Work** (cero distracciones).

---

## 2. Estructura General

Cada materia técnica de ingeniería (`python/`, `sql/`, `cloud/`, etc.) opera con sus propios requerimientos técnicos pero bajo el mismo andamiaje estructural.

```text
subjects/
├─ python/
│  ├─ chronicles/
│  │  ├─ PY-BASICO/            <- (Entry level assessment)
│  │  ├─ PY-POO/               <- (Data Engineering ETL)
│  │  └─ PY-CLOUD/
│  └─ README.md
├─ sql/
├─ cloud/
└─ data/
```

---

## 3. Topología Interna (Chronicles)

El centro neural del avance son las Chronicles. Cada directorio de una chronicle mantiene un estándar de grado corporativo:

```text
PY-POO/
├─ chronicle.md        <- Documento de la Chronicle (Contexto & Requisitos)
├─ grimoire.md         <- Grimoire / Bitácora Feynman
├─ lore/               <- Lore (Lecciones teóricas)
├─ quests/             <- Quests (Laboratorios guiados)
└─ rite/               <- Rite (Proyecto integrador — Rito de paso)
   ├─ requirements.md  <- Requisitos y fases del Rite
   ├─ journal.md       <- Bitácora de aprendizaje técnica
   ├─ src/             <- Código fuente (Python)
   ├─ tests/           <- Pruebas unitarias
   └─ data/            <- Archivos de datos o mocks
```

### Reglas para Chronicles:
- **Chronicle (Crónica):** Toda la ruta de aprendizaje modular.
- **Lore & Quests:** Adquisición teórica y asimilación (requiere Técnica Feynman en el Grimoire).
- **Rite:** Proyecto final con TDD obligatorio. Solo accesible tras auditoría del DM (`/scry`).

---

## 4. The 3.2 Engineering Standards

Al operar en el entorno de `subjects/`, te sometes obligatoriamente a estas 3 directrices:

1. **English Friendly:** Las carpetas, nombres de archivo, variables de código, tests y Documentos Técnicos **SE FOMENTAN EN INGLÉS**. Se permite el español de forma transicional.
2. **Architecture First:** Jamás abres `src/` sin haber documentado el diseño y los trade-offs.
3. **Fail First (TDD):** El desarrollo funcional no existe si no escribiste primero la prueba y la hiciste fallar nativamente en la consola.

---

Este archivo rige toda tu interacción práctica de las materias Técnicas. Si estás aquí, has superado la fase de planeación y estás en fase de codificación (Operador).
