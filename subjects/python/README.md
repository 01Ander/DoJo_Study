# Python – Engineering Base del DoJo Study

Python es la espina dorsal funcional para alcanzar el portafolio de **Data & Automation Engineer**. Esta materia está diseñada para operar como una StartUp de software técnico: no hacemos pequeños scripts procedimentales, creamos **Módulos, Pipelines de Datos y Herramientas Serverless** testeables y desacopladas.

---

## 1. Reglas Sagradas del Código (The Python Zone)

Al entrar a esta carpeta o a cualquier de sus campañas, activas obligatoriamente la Inmersión:

- **English Friendly Coverage:** Toda clase, variable, docstring y log se apunta a mantener en un formato "English friendly en primeras instancias, hasta que el operador maneje un mejor nivel de inglés".
- **Design Patterns First:** Los "pequeños ejercicios" no existen. Abordamos POO (Clases Abstractas, Factory, Inversión de Dependencias) como el suelo mínimo de desarrollo.
- **Tests Are Not Optional:** Cada misión debe tener correspondencia directa en una carpeta de `tests/` con asserts ejecutados en `pytest`.

---

## 2. Estructura de Campañas (Python Engineering Track)

Las campañas se alinean rigurosamente con los módulos avanzados del Syllabus Maestro. Priorizan el conocimiento aplicable requerido para puestos remotos de Middle/Senior Data Engineer.

| Código        | Enfoque del Proyecto                       | Estado       |
|---------------|-------------------------------------------|--------------|
| **PY-BASICO**      | Python Core Fundamentals & Data Assessment | 🟢 Ready     |
| **PY-POO-FINANCE** | ETL Modular, Abstracción, Patrones, Pytest | 🟢 Ready     |
| **PY-API-AUTO**    | FastApi, Automation Scripts, OAuth         | 🟡 Pending   |
| **DE-ETL-BATCH**   | Pandas pesado, DuckDB, Pipelines Batch     | 🟡 Pending   |
| **PY-CLOUD**       | AWS Boto3, Lambda Deployments, SQS         | 🟡 Pending   |

---

## 3. Workflow Diario 

1. Levantas tu entorno `venv`.
2. Escribes el **Mini-RFC** de tu misión con un enfoque "English friendly" documentando la estructura.
3. Te atoras en **Red-Green-Refactor**.
4. Validas convenciones (`mypy`, `flake8`).
5. Haces Push con un mensaje semántico: `feat(etl): abstract extractor implementations`.
