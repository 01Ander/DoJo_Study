# Subjects – The DoJo Engineering Divisions

Este directorio organiza todas las divisiones operativas técnicas del DoJo Study.  
La finalidad es mantener el ecosistema de aprendizaje estructurado en **Proyectos Reales (Campañas)**, alejándonos de los scrips básicos y acercándonos a verdaderos Pipelines de datos.

---

## 1. Objetivo Operativo de este Directorio

`subjects/` funciona como tu entorno corporativo simulado:
- Punto de acceso masivo a las ramas técnicas.
- Base central donde se documentan Mini-RFCs y pruebas bajo estándares de QA. 
- Aislante del ruido teórico: Aquí se programa bajo protocolos de **Deep Work** (cero distracciones).

---

## 2. Estructura General

Cada materia técnica de ingeniería (`python/`, `sql/`, `cloud/`, etc.) opera con sus propios requerimientos técnicos pero bajo el mismo andamiaje estructural.

```text
subjects/
├─ python/
│  ├─ campaigns/
│  │  ├─ PY-BASICO/            <- (Entry level assessment)
│  │  ├─ PY-POO/               <- (Data Engineering ETL)
│  │  └─ PY-CLOUD/
│  └─ README.md
├─ sql/
├─ cloud/
└─ data/
```

---

## 3. Topología Interna (Campañas)

El centro neural del avance son las Campañas. Cada directorio de una campaña mantiene un estándar de grado corporativo:

```text
PY-POO/
├─ campaign.md         <- Documento de la Campaign (Contexto & Requisitos)
├─ study-journal.md    <- Grimoire / Bitácora Feynman
├─ theory/             <- Lore (Lecciones teóricas)
├─ exercises/          <- Quests (Laboratorios guiados)
└─ project/            <- Final Boss (Proyecto integrador)
   ├─ requirements.md  <- Requisitos y Missions (Fases) del Boss
   ├─ journal.md       <- Bitácora de aprendizaje técnica
   ├─ src/             <- Código fuente (Python)
   ├─ tests/           <- Pruebas unitarias
   └─ data/            <- Archivos de datos o mocks
```

### Reglas para Campaigns y Missions:
- **Campaign (Materia):** Toda la ruta de aprendizaje modular.
- **Lore & Quests:** Adquisición teórica y asimilación (requiere técnica Feynman en el Study Journal).
- **Missions (Fases del Boss):** Unidades del Final Boss con TDD obligatorio.

---

## 4. The 3.2 Engineering Standards

Al operar en el entorno de `subjects/`, te sometes obligatoriamente a estas 3 directrices:

1. **English Friendly:** Las carpetas, nombres de archivo, variables de código, tests y Documentos Técnicos de las Misiones (`.md`) **SE FOMENTAN EN INGLÉS** (enfoque "English friendly en primeras instancias, hasta que el operador maneje un mejor nivel de inglés"). Se permite el español de forma transicional.
2. **Architecture First:** Jamás abres `src/` sin haber escrito antes el campo *Mini-RFC* de tu misión actual detallando el patrón de diseño a usar.
3. **Fail First (TDD):** El desarrollo funcional no existe si no escribiste primero la prueba y la hiciste fallar nativamente en la consola.

---

Este archivo rige toda tu interacción práctica de las materias Técnicas. Si estás aquí, has superado la fase de planeación y estás en fase de codificación (Operador).
