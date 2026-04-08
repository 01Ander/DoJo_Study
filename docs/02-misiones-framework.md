# 02 - Misiones Framework

## ¿Qué es el Framework de Misiones?

Es la capa táctica que convierte el marco de Ingeniería de Software en tareas accionables. Actualmente, una misión **no es un ejercicio rápido de sintaxis**; es un módulo funcional de un pipeline mayor.

El aprendizaje inicia definiendo **Arquitectura** (Mini-RFC), luego escribiendo las **Pruebas** (TDD) y finalmente **Implementando** la lógica en un entorno 100% en inglés.

---

## Niveles del Sistema de Ingeniería

### 1️ Campañas (Proyectos)
Grandes sistemas que simulan casos de uso reales de la industria.
*Ejemplos:*
- `DE-ETL-PIPELINE`
- `PY-POO-FINANCE`
- `QA-TEST-AUTOMATION`

### 2️ Main Missions (M - Core Architecture)
Desarrollo de los módulos críticos del sistema. Obligatorio el uso de Clean Architecture y TDD.
*Ejemplos:*
- `M01: Data Extractor Interface`
- `M02: Domain Entities Validation`

### 3️ Scaling Refactors (S - Quality & Scaling)
Misiones de evolución técnica, reemplazando las "Side Missions" opcionales de la versión anterior por requerimientos de Seniority.
*Ejemplos:*
- `S01: PyTest Coverage > 80%`
- `S02: Migrate from CSV to DuckDB`

### 4️ Boss Missions (B - Integración Continua)
Ensamblaje del pipeline completo. Sirve para lanzar el producto como un CLI, una API (FastAPI) o una función Serverless.
*Ejemplos:*
- `B01: Serverless Streamlit Dashboard`
- `B02: Typer CLI Execution`

---

## El Proceso de Desarrollo (The Operator Workflow)

1. **Abrir Bloque de "Deep Work" (90 mins).**  
2. **Definir el `Mini-RFC`:** Escribir en la plantilla de misión, en inglés, por qué se usará X patrón de diseño.
3. **Draft de Tests (TDD):** Crear el archivo en la carpeta `tests/` y fallar intencionalmente comprobando inputs/outputs esperados.
4. **Implementación:** Programar la lógica en VS Code (Nomenclatura y Docstrings en inglés puro).
5. **Cierre:** Si supera 4h, generar el *Friction Log* y salir del IDE.

***Nota:*** Las misiones de "Observación (O)" y "Optimización (OPT)" fueron dadas de baja. En el sistema actual, si sientes la necesidad de hacer misiones pequeñas por falta de energía, debes invocar el protocolo **Rest Day** de inmediato (Zero-Code policy).
