# 📓 Grimoire — DE-PIPELINES

Este documento es tu registro académico. Después de leer cada capítulo en `lore/` y completar su laboratorio en `quests/`, debes documentar tu asimilación aquí utilizando la **Técnica Feynman**.

> **⚠️ Regla del DM:** El DoJo Agent (Dungeon Master) auditará este documento (`/scry`). Si detecta que estás copiando y pegando, o que no comprendes el concepto central, **denegará tu acceso al Rite**.

---

## 📝 Capítulo 00: Arquitecturas de Ingesta y Zonas de Datos
**Fecha de finalización:** 2026-09-15
**Métricas:**
- Tiempo de lectura: 5min
- Tiempo en ejercicios: 1h30m
- Veces que recurrí al Tutor/DM: 8
- Fricción (1-10): 4

**Feynman Synthesis (Tus propias palabras):**
1. ¿Cuál es la diferencia fundamental entre el enfoque ETL y ELT, y en qué escenarios modernos se recomienda usar cada uno?
> ETL transforma los datos originales, dandose por perdidos, mientras ELT mantiene los datos originales, los guarda y con una copia se transforman luego para su carga. Esto ultimo es el escenario mas moderno para poder tener una trazabilidad y a la vez poder recuperar datos en caso de errores o si se requieren en algun cambio.

2. Explica el propósito de dividir un Data Lake o Data Warehouse en zonas Bronze, Silver y Gold. ¿Qué nivel de limpieza tiene cada una?
> En el primer nivel se cargan los datos tal cual vienen, sin modiicar ni hacer nada con ellos, solo mantenerlos en memoria. En el segundo nivel se hace su limpieza y transformacion requerida. En el tercer nivel se hace aggregation o analisis que se necesiten con dichos datos. 

**Friction Log (Opcional):**
> Costo bastante recordar codigo 'basico' de python para crear un nuevo dict en el paso 2 y poblar la lista de dicts con los valores nuevos, al igual que para el paso 3. No se recordaban las estructuras de python para poder hacer la tarea.

---

## 📝 Capítulo 01: Extracción Automatizada (APIs)
**Fecha de finalización:** 2026-09-16
**Métricas:**
- Tiempo de lectura: 5min
- Tiempo en ejercicios: 33min
- Veces que recurrí al Tutor/DM: 4
- Fricción (1-10): 3

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué es crítico implementar el manejo de la paginación al realizar extracciones masivas de una API REST?
> Esto permite ver la informacion que se obtenga de la api de manera mas sencilla, acotada, y no una lista interminable respuestas.
> **Nota:** El lore describe la paginación como un "parámetro extra", lo cual implica que es opcional. En realidad, la mayoría de APIs de producción imponen paginación por defecto (page_size de 20-100). Si no se implementa el loop de paginación, solo se obtiene la primera página y se pierden datos silenciosamente. Este concepto no viene en el lore.

2. Explica cómo funciona la autenticación por Tokens (ej. Bearer) y por qué es más segura que usar credenciales directas en cada petición HTTP con `requests`.
> Se hace uso de headers para indicar la autorizacion obligatoria para poder consumir la API, donde posterior se hace la peticion con .get(), se usa una capa de seguridad en caso que el servidor entregue algun error y no romper todo el proceso, y posterior se almacena la informacion como se requiera. De esta manera se valida que quien hace la peticion sea 'confiable' y se entrege de manera mas segura. 

**Friction Log (Opcional):**
> Nuevamente, falencias en conceptos de python, no captar la diferencia entre una lista '[]' a '()'

---

## 📝 Capítulo 02: Manipulación con Pandas
**Fecha de finalización:** 2026-09-17
**Métricas:**
- Tiempo de lectura: 5min
- Tiempo en ejercicios: 15min
- Veces que recurrí al Tutor/DM: 0
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. ¿Por qué es importante imponer un tipado estricto (strict casting) en tu DataFrame de Pandas en lugar de dejar tipos dinámicos o genéricos?
> Porque puede llegar el caso que pasen typos se sean 'validos' dentro de la lista al no ser nulls pero que no son los requeridos dentro de la propia lista, lo cual puede a la larga generar errores silenciosos y al momento de usar los datos erroneos, crashee el programa como tal. Esto no solo como medida de seguridad, tambien ayuda a estandarizar un solo typo establecido para toda la tabla o columna, y de igual manera es un uso mas optimizado de recursos para las operaciones dentro de pandas.

2. Menciona un proceso común de limpieza de datos en Pandas (ej. manejo de nulos) y describe qué problema de negocio resuelve.
> Se establece el DataFrame para tomar los datos y pasarlos a pandas en forma de tabla estructurada bidimensional. Se elimina las fillas con espacios null con dropna.
> Esta operacion permite limpiar registros que venga con informacion faltante dentro de una gran cantidad de datos sucios.

**Friction Log (Opcional):**
> No recordar correctamente el comando 'isinstance', se recordaba que se hacia una igualacion por comando, pero no se recordaba que se podia hacer por instance, se pensaba como typeof, o algo asi. Ademas que se transforma la informacion a una tabla mucho mas eficiente para el trabajo posterior o incluso su propia limpieza. 

---

## 📝 Capítulo 03: Data Quality & Observability
**Fecha de finalización:** 2026-09-17
**Métricas:**
- Tiempo de lectura: 5min
- Tiempo en ejercicios: 15min
- Veces que recurrí al Tutor/DM: 0
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué es la validación de esquemas y qué riesgos de consistencia previene si se aplica tempranamente en un pipeline?
> Quien ha creado la api puede hacer las modificaciones que quiera y eso puede traer errores o inconsistencias frente a un desarrollo hecho con unos parametros establecidos de antes. Para evitar esto, se hace un chequeo previsorio antes de que la informacion entre a la aplicacion, para validar que la informacion que viene de la api sea la que se espera, es decir, los titulos de las columnas sean los que se esparan y sean la cantidad de columnas que se requieren, en caso de que hayan cambio de nombres o se agregen o eliminen columnas y a la vez, se valida que los tipos de datos dentro de estas columnas sean los tipos que se esperan de ellas y no existan tipos erroneos o basura.

2. ¿Qué es la "reconciliación de datos" y por qué se considera una práctica clave en Observability?
> la reconciliacion permite verificar que si llegan 20 datos de una fuente, se obtengan 20 datos limpios igualmente, y no se pierdan datos durante la limpieza de estos mas de los deseados. Dentro de observability es clave por que es la primera gate de verificacion por si pasan fallos dentro de la aplicacion para evitar guardado de datos corruptos.

**Friction Log (Opcional):**
> Recordar el uso correcto de pytest.raises

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

2. Explica qué hace el parámetro `if_exists` de `to_sql()` y describe un escenario donde usar `'append'` vs `'replace'` haría la diferencia entre un pipeline correcto y uno que destruye datos históricos.
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
