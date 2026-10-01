# Journal del Rito: B2B Warehouse Inventory Pipeline

> **Instrucción para el Operador:** Utiliza este documento como tu bitácora diaria de desarrollo. Anota aquí todos los bloqueos técnicos, errores de pruebas, descubrimientos de documentación, o decisiones de diseño arquitectónico que tomes mientras desarrollas las 5 Fases del Rite. Es tu prueba ante el Architect de cómo resolviste los problemas reales.

## Registro de Desarrollo

### 2026-10-01 - Ejecución Integral del Rite (Fases 1 a 4)

#### 1. Arquitectura Top-Down y Separación de Responsabilidades
Se implementó un pipeline *Event-Driven* desacoplado bajo el principio de responsabilidad única (un archivo = un propósito):
- **`pipeline.py` (Orquestador Serverless):** Entry point `lambda_handler(event, context)`. Desempaqueta dinámicamente `bucket` y `key` del evento de S3, ejecuta las compuertas de validación de negocio y delega la I/O a los helpers.
- **`extract_s3.py` (Capa de Extracción):** Función pura de lectura `extraction_from_s3(bucket, key)`. Consume el stream de bytes de `boto3`, decodifica UTF-8 y deserializa el JSON crudo.
- **`rds.py` (Capa de Persistencia Relacional):** Función `load_to_rds(data)` responsable del ciclo de vida completo de la conexión PostgreSQL vía `psycopg2`.

#### 2. Decisiones Técnicas y Gaps Resueltos (Fricción vs Lore)

- **Gap de Inicialización de Boto3 (Fábrica vs Objeto Global):**
  - *Problema:* El Lore enseñó a instanciar clientes adentro de las funciones. En el Rite se instanció `s3_client = boto3.client('s3')` a nivel de módulo (estándar oficial de AWS para reutilizar conexiones y mitigar *Cold Starts*).
  - *Impacto en Testing:* Intentar usar el patrón de la Quest (`@patch('extract_s3.boto3.client')`) provocaba llamadas al AWS real con error `Unable to locate credentials` porque el módulo ya había ejecutado la inicialización antes del test.
  - *Solución:* Parcheo directo sobre la variable instanciada (`@patch('extract_s3.s3_client')`), eliminando intermediarios y recibiendo directamente el mock del cliente en la firma del test.

- **Validación Semántica vs Existencia Estructural:**
  - *Problema:* La especificación pedía validar que los campos "existan". Comprobar únicamente la presencia física de la clave (`key in data`) permitía el paso de valores `None` o strings vacíos, rompiendo los constraints `NOT NULL` de la tabla en Postgres.
  - *Solución:* Validación booleana estricta con `.get()` evaluando contenido real y comprobando `quantity > 0` con tipos seguros para evitar colisiones con `NoneType`. Ante fallos, se ejecuta registro con `logger.error` y `raise ValueError("VALIDATION_FAILED: ...")` para alertar a CloudWatch.

- **Encapsulación de Transacciones ACID y Recursos:**
  - *Decisión:* La transacción (`conn.commit()`, `conn.rollback()`) y la garantía de cierre (`finally: conn.close()`) se aislaron al 100% dentro de `rds.py`. `pipeline.py` no debe gestionar conexiones ni filtrar cursores.
  - *Inyección SQL y Tipado:* Se utilizaron parámetros seguros (`%s`) y se especificaron las columnas de destino explícitamente en el `INSERT INTO inventory_logs (warehouse_id, item_id, quantity)` para evitar que Postgres colisionara el string con la columna autoincremental `id SERIAL`.

- **Política Fail-Fast en Serverless:**
  - *Decisión:* Tanto los helpers como el orquestador relanzan excepciones (`raise e`) tras registrar el fallo. Silenciar errores con `pass` provocaría que AWS Lambda marque invocaciones como exitosas en CloudWatch mientras los datos se pierden silenciosamente.

#### 3. Estado de la Suite de Pruebas
- `tests/test_extraction_s3.py`: Test unitario hermético de extracción y parseo S3 con doble de bytes en `Body.read`.
- `tests/test_rds.py`: Test unitario hermético de persistencia, verificación de query parametrizada y ciclo ACID/cierre.
- `tests/test_pipeline.py`: Test de integración E2E del contrato completo ante un evento simulado de S3.
- **Resultado:** 3 tests en verde (100% PASSED).

---

#### 4. Notas del Operador & Friction Log (Subjetivo)
- **Nivel de Fricción:** 4 / 5.
- **Causa de la fricción:**  Sensaciones diversas frente al rite y el propio subject. Al tratarse de una tool como tal, y no de logica, se presenta un gran rechazo a estudiarla. Bajando un poco dicha friccion, se rehace el rite y reglas de generacion de contenido a la par. Sigue siendo un subject de mas memorizacion o de entender que codigo debe funcionar para que caso. 
- **Aprendizaje clave:**  Relativamente correcto, pero si o si merece un repaso de una manera distinta, con una explicacion mas precisa sobre que hace el codigo en si, ya que son netamente comandos para validaciones de seguridad y de autenticidad. Se puede decir que se asimila un 60% del subject como tal.

