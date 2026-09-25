# 06 - Convenciones de Código y Arquitectura Transversales

> **Propósito:** Este documento actúa como la memoria a largo plazo del DoJo. Aquí se registran los estándares técnicos, patrones de arquitectura y convenciones de código que han sido establecidos en Chronicles anteriores. **Ninguna Chronicle nueva puede contradecir estas reglas** sin una justificación arquitectónica explícita.
> 
> **Regla de Actualización:** Al finalizar una Chronicle (GATE 5), si el Rito estableció un nuevo estándar de la industria que debe respetarse de aquí en adelante, se debe agregar a este documento.

---

## 1. Patrones de Testing (Establecido en `PY-POO`)
- **Ciclo AAA Estricto:** Todos los tests en el Lore y en Quests deben mostrar explícitamente las tres fases: **Arrange** (preparar mocks/datos), **Act** (ejecutar función real) y **Assert** (validar resultado). Queda prohibido mostrar tests incompletos.
- **Uso estricto de `assert`:** La palabra clave `assert` está reservada para los archivos de prueba (`test_*.py`). Queda prohibido usar `assert` en código de producción para validaciones de reglas de negocio.

## 2. Manejo de Errores y Validaciones (Establecido en `PY-POO`)
- **Excepciones de Dominio (Domain Exceptions):** Para validar reglas de negocio o flujos inválidos, se DEBEN lanzar Excepciones personalizadas heredadas de `Exception` (ej. `InvalidTransactionError`, `ExpiredCardError`). El orquestador es el encargado de atraparlas y decidir si continúa o aborta. 

## 3. Arquitectura de Datos y Data Lakes (Establecido en `DE-PIPELINES`)
- **Inmutabilidad de la Zona Raw/Bronze:** La capa Bronze (o Raw) es estrictamente inmutable. Nunca se modifican ni se limpian los datos en esta etapa; se guardan exactamente como llegaron (ej. JSON crudo) como evidencia histórica. Las transformaciones y estandarización (minúsculas, desduplicación, etc.) ocurren en capas posteriores.

## 4. Manipulación SQL (Establecido en `SQL-BASICO`)
- **Seguridad en Operaciones DML:** La "Regla de Oro en ingeniería de datos" dicta que antes de realizar cualquier actualización (`UPDATE`) o borrado (`DELETE`), primero se debe ejecutar un `SELECT` con la cláusula `WHERE` para verificar visualmente qué filas van a ser impactadas, procediendo luego a mutarlas exclusivamente usando su *Primary Key*.

## 5. Diseño Orientado a Eventos (Establecido en `CLOUD-AWS`)
- **Asincronía sin Respuestas HTTP:** En arquitecturas puramente Event-Driven asíncronas (ej. eventos de S3 detonando Lambdas), las funciones procesadoras **no deben retornar códigos HTTP** (como `statusCode: 200`). AWS ignora estas respuestas. Deben retornar `None` en éxito o lanzar una excepción (`raise e`) en caso de fallo para activar mecanismos de reintento o DLQ.
- **Inyección de Credenciales:** Prohibido el hardcodeo de llaves de AWS. En entornos Cloud, se leen dinámicamente usando variables de entorno o roles IAM subyacentes.
