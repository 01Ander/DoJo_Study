# 📓 Grimoire — DE-PIPELINES

Este documento es tu registro académico. Después de leer cada capítulo en `lore/` y completar su laboratorio en `quests/`, debes documentar tu asimilación aquí utilizando la **Técnica Feynman**.

> **⚠️ Regla del DM:** El DoJo Agent (Dungeon Master) auditará este documento (`/scry`). Si detecta que estás copiando y pegando, o que no comprendes el concepto central, **denegará tu acceso al Rite**.

---

## 📝 Capítulo 00: Arquitecturas de Ingesta y Zonas de Datos
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. ¿Cuál es la diferencia fundamental entre el enfoque ETL y ELT, y en qué escenarios modernos se recomienda usar cada uno?
> [Escribe aquí tu explicación]

2. Explica el propósito de dividir un Data Lake o Data Warehouse en zonas Bronze, Silver y Gold. ¿Qué nivel de limpieza tiene cada una?
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## 📝 Capítulo 01: Extracción Automatizada (APIs)
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué es crítico implementar el manejo de la paginación al realizar extracciones masivas de una API REST?
> [Escribe aquí tu explicación]

2. Explica cómo funciona la autenticación por Tokens (ej. Bearer) y por qué es más segura que usar credenciales directas en cada petición HTTP con `requests`.
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## 📝 Capítulo 02: Manipulación con Pandas
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué es importante imponer un tipado estricto (strict casting) en tu DataFrame de Pandas en lugar de dejar tipos dinámicos o genéricos?
> [Escribe aquí tu explicación]

2. Menciona un proceso común de limpieza de datos en Pandas (ej. manejo de nulos) y describe qué problema de negocio resuelve.
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## 📝 Capítulo 03: Data Quality & Observability
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué es la validación de esquemas y qué riesgos de consistencia previene si se aplica tempranamente en un pipeline?
> [Escribe aquí tu explicación]

2. ¿Qué es la "reconciliación de datos" y por qué se considera una práctica clave en Observability?
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## 📝 Capítulo 04: Carga de Datos a PostgreSQL
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué ventajas aporta usar una capa como SQLAlchemy para gestionar conexiones frente a inyectar consultas SQL directas como strings?
> [Escribe aquí tu explicación]

2. Explica conceptualmente la diferencia entre un `INSERT` convencional y una estrategia `UPSERT` (Insert or Update). ¿Cuándo es vital usar el UPSERT?
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## 📝 Capítulo 05: Orquestación con Prefect (Local)
**Fecha de finalización:** 
**Métricas:**
- Tiempo de lectura: 
- Tiempo en ejercicios: 
- Veces que recurrí al Tutor/DM: 
- Fricción (1-10): 

**Feynman Synthesis (Tus propias palabras):**
1. En el contexto de Prefect, explica la diferencia jerárquica y de responsabilidad entre lo que hace un `Flow` y lo que hace una `Task`.
> [Escribe aquí tu explicación]

2. ¿Cómo el uso de "reintentos automáticos" (retries) y dependencias mejora la resiliencia de tu pipeline de datos ante fallos esporádicos?
> [Escribe aquí tu explicación]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---
**Auditoría del DM:** [Pendiente]
