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

## 5. Diseño Orientado a Eventos y Ciclo de Vida de Recursos AWS (Establecido en `CLOUD-AWS`)
- **Asincronía sin Respuestas HTTP:** En arquitecturas puramente Event-Driven asíncronas (ej. eventos de S3 detonando Lambdas), las funciones procesadoras **no deben retornar códigos HTTP** (como `statusCode: 200`). AWS ignora estas respuestas. Deben retornar `None` en éxito o lanzar una excepción (`raise e`) en caso de fallo para activar mecanismos de reintento o DLQ.
- **Inyección de Credenciales:** Prohibido el hardcodeo de llaves de AWS. En entornos Cloud, se leen dinámicamente usando variables de entorno o roles IAM subyacentes.
- **Clientes SDK sin Estado a Nivel de Módulo:** Los clientes de servicios AWS sin estado (`boto3.client('s3')`, `boto3.client('sns')`, `boto3.resource('dynamodb')`, etc.) **deben instanciarse a nivel de módulo**, fuera del handler, para aprovechar el Execution Environment Reuse de Lambda (reutilización de conexiones TCP en Warm Invocations y reducción de costos por milisegundo de cómputo). Queda prohibido instanciarlos dentro del cuerpo del handler en código de producción o referencia.
- **Conexiones Relacionales por Invocación:** Las conexiones directas a bases de datos (`psycopg2.connect`, `pymysql.connect`) son recursos con estado y **deben abrirse y cerrarse dentro de la misma invocación** usando un bloque `finally: conn.close()`. No se instancian a nivel de módulo (riesgo de agotamiento del pool de conexiones de RDS), salvo que se enseñe explícitamente RDS Proxy como solución al problema.
- **Alineación de Mocks con el Código de Producción:** Los andamiajes y tests unitarios deben parchear el recurso tal como está instanciado en el código real. Si el cliente vive a nivel de módulo (`s3_client = boto3.client('s3')`), el patch apunta a la variable instanciada (`@patch('modulo.s3_client')`), no a la fábrica (`@patch('modulo.boto3.client')`). La divergencia entre el patrón de mock enseñado y el código de producción genera fricción en el Rite y es pregunta frecuente en entrevistas técnicas de Data Engineering.

## 6. Idioma del Código y Nomenclatura (English First)
- **Código y Tests en Inglés:** Todo bloque de código ejecutable, nombres de variables, funciones, clases, archivos de prueba (`test_*.py`), docstrings, logs y comentarios dentro de bloques de código deben escribirse estrictamente en **inglés profesional**.
- **Explicaciones en Español:** La prosa explicativa, títulos de sección, analogías y guías fuera de los bloques de código se redactan en **español** para facilitar la comprensión conceptual rápida.
