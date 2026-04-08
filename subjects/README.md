# Subjects – The DoJo Engineering Divisions

Este directorio organiza todas las divisiones operativas técnicas del DoJo Study v3.3.  
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
│  │  ├─ PY-POO-FINANCE/       <- (Data Engineering ETL)
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
PY-POO-FINANCE/
├─ campaign.md         <- Documento de proyecto (Contexto & Requisitos)
├─ src/                <- Código fuente 100% en inglés
├─ tests/              <- Unit Tests (TDD / Pytest)
└─ missions/           <- Tickets de Jira simulados. 
   ├─ M01.md
   ├─ S01.md
   └─ B01.md
```

### Reglas para Misiones:
- **Main Missions (M):** Construcción Core y TDD obligatorios.
- **Scaling Refactors (S):** Escalabilidad, Logging, Integración Continua (CI).
- **Boss Missions (B):** La entrega a Producción (CLI, API Web).

---

## 4. The 3.2 Engineering Standards

Al operar en el entorno de `subjects/`, te sometes obligatoriamente a estas 3 directrices:

1. **English-Only Zone:** Las carpetas, nombres de archivo, variables de código, tests y Documentos Técnicos de las Misiones (`.md`) **SE ESCRIBEN EN INGLÉS**. No negociable. Esto es mitigación pura de la barrera lingüística.
2. **Architecture First:** Jamás abres `src/` sin haber escrito antes el campo *Mini-RFC* de tu misión actual detallando el patrón de diseño a usar.
3. **Fail First (TDD):** El desarrollo funcional no existe si no escribiste primero la prueba y la hiciste fallar nativamente en la consola.

---

Este archivo rige toda tu interacción práctica de las materias Técnicas. Si estás aquí, has superado la fase de planeación y estás en fase de codificación (Operador).
