# Grimoire — `CLOUD-AWS`

> **Instrucción para el Operador:** El aprendizaje pasivo no existe. Después de leer cada capítulo del `lore/` y completar su respectiva `quest/`, debes responder a las preguntas de ese capítulo usando **tus propias palabras** (Técnica Feynman). No copies y pegues del Lore.
> 
> Una vez completado, el Dungeon Master auditará este documento (`/scry`) para darte acceso al Rite final.

---

## Cap 00: AWS Identity & Access Management (IAM)
**Fecha de finalización:** 2026-09-28
**Métricas:**
- Tiempo de lectura: 8min
- Tiempo en ejercicios: 10min
- Veces que recurrí al Tutor/DM: 0
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **¿Por qué es un riesgo de seguridad crítico darle a un script permisos de "Administrador Total" en AWS por conveniencia, y qué principio de IAM debemos aplicar en nuestras Políticas (Policies) para evitarlo?**
   > Se debe aplicar la politica IAM, dandole permiso extricto y acceso minimo neceario para la tarea que vaya a cumplir, ya que sin esta, el script puede generar un peligro de seguridad, puesto que dentro de un hackeo se pueden obtener las licencias y accesos de dicho script y dar entrada al sistema a cualquiera con intenciones maliciosas.

2. **Describe exactamente cómo se debe autenticar un script de Python en AWS utilizando la librería `boto3` para evitar el peor pecado de seguridad en la nube (el hardcoding de credenciales directas en el código fuente).**
   > Las credenciales deben vivir en un archivo .env, el cual debe estar dentro del .gitignore. En el codigo de produccion se debe importar librerias de os, boto3 y dotenv, posteriormente, se cargan las variables de entorno del archivo .env con la funcion load_dotenv() y ya se puede intentar hacer una validacion de ususario, a partir de boto3.client('iam') creando la conexion y iam_client.get_user() para hacer la peticion de API a AWS.

**Friction Log (Opcional):**
> Se habia confundido en test que para captar el error de autenticacion se debia hacer con with pytest.raises, pero la funcion original retornaba el mensaje de error, solo eso, por lo que no era necesario, solo igualar al mensaje como un assert normal.

---

## Cap 01: Amazon S3 (Simple Storage Service)
**Fecha de finalización:** 2026-09-28
**Métricas:**
- Tiempo de lectura: 10min
- Tiempo en ejercicios: 10min
- Veces que recurrí al Tutor/DM: 0
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **S3 permite almacenar tanto JSON como Parquet. ¿Por qué elegirías guardar un archivo en formato crudo JSON en la zona de ingesta, y por qué preferirías usar un formato columnar como Parquet para la zona de consumo analítico (Curated)?**
   > JSON en la zona de ingesta tiene como facilidad la lectura humana, por lo que se vuelve en la fuente de verdad en el momento de una verificacion de dicha entrada. Parquet tiene la caracteristica de ser columnar dando una compresion significativa de la informacion ya limpia, esto facilita el procesamiento, analisis, busqueda, todo el manejo que se pueda hacer con informacion muy cercana a una db, de manera eficaz y eficiente. 

2. **Explica cómo S3 organiza los objetos si no existe un sistema de carpetas real, y describe la convención arquitectónica de nomenclatura (*keys*) que se utiliza al ingerir datos para evitar escanear terabytes de histórico inútil al hacer consultas.**
   > Al tratarse de un sistema plano que puede escalar sumamente facil, se adopta un convencion de date partitioning, el cual agrega una key con fecha que permita presisamente particionar la informacion que entro al sistema, evitando un consumo absurdo de recursos al momento de hacer una busqueda de informacion cuando el sistema cuente con millones de registros ya cargados, a partir del 'filtro' de la fecha.

**Friction Log (Opcional):**
> Externo al contenido, gaps detectados en el sistema frente a la solucion propuesta y lo que requeria la quest.

---

## Cap 02: Amazon RDS (Relational Database Service)
**Fecha de finalización:** 2026-09-28
**Métricas:**
- Tiempo de lectura: 11min
- Tiempo en ejercicios: 19min
- Veces que recurrí al Tutor/DM: 1
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **¿Por qué un ingeniero de datos preferiría usar Amazon RDS en lugar de instalar PostgreSQL manualmente en un servidor alquilado (auto-administrado), y qué herramienta nativa de AWS tipo firewall debe usar para evitar que bots en internet intenten hackear la base de datos?**
   > Se usa Amazon RDS por la facilidad a la hora de mantener la propia base de datos. Este servicio se encarga de mantener actualizado dependencias, seguridad, tramites operativos netamente del servidor, mientras que el programador solo se encarga de las consultas como tal y uso neto de la base de datos. Para manejar una seguridad dentro de este sistema se usa Security Group, el cual actua como firewall para evitar la entrada a extranos y la salida de informacion hacia los mismos. Esto se logra permitiendo la entrada de puertos exclusivamente a un grupo selecto de IPs privadas con las cuales se este trabajando.
   > 	

2. **En el ecosistema de bases de datos con Python (DBAPI), ¿qué es exactamente un "cursor" y por qué es obligatorio crearlo cuando usamos librerías como `psycopg2` para enviar consultas a RDS?**
   > cursor es el encargado de enviar las peticiones sql y regresar las respuestas de la misma. Esto se hace para evitar que se presenten inyecciones de codigo sql en campos donde se permita la entrada de strings de manera oculta, dando paso por ejemplo, que se elimine la db. Aclaracion. quien hace el trabajo de de prevenir la inyeccion de codigo son los parametros que maneja cursor; este es simplemente un vehiculo que solicita y transporta la informacion. 

**Friction Log (Opcional):**
> Error al realizar el return de la funcion principal, no se habia leido bien el codigo del lore y se estaba retornando completamente la tupla, no solo el valor solicitado. 

---

## Cap 03: AWS Lambda (Serverless Compute)
**Fecha de finalización:** 2026-09-29
**Métricas:**
- Tiempo de lectura: 7min
- Tiempo en ejercicios: 12min
- Veces que recurrí al Tutor/DM: 1
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **En una Arquitectura Orientada a Eventos en AWS, ¿por qué es financieramente y técnicamente superior usar una función Lambda disparada por un "Gatillo" (*Trigger*) en lugar de tener un script corriendo 24/7 en un bucle infinito preguntando si hay trabajo nuevo (*polling*)?**
   > Al menejar una arquitectura que responda unicamente a eventos, se logra una reduccion de costos sumamente considerable a comparacion de mantener un servidor activo 24/7 con un costo fijo alto. Mientras que Lamda de aws efectua costos unicamente en la fraccion de segundo donde se ejecute el codigo exacto para la carga de archivos como tal, bajo la llamada de un trigger programado.

2. **Explica qué es el `Execution Role` de una función Lambda y por qué el código Python dentro de tu `lambda_handler` lanzaría un error instantáneo de `AccessDenied` al intentar leer un objeto de S3 si olvidas configurar este rol.**
   > Execution Role tiene la misma filosofia de IAM, si no hay un rol claro y establecido para la funcion o automatizacion para cargar o descargar informacion, la seguridad de lambda lo tomara como un fallo grave, esto para aclarar que realiza dicha funcion o codigo, y acotar sus permisos y accesos, cumpliendo unicamente su tarea a realizar. Siendo asi, como se maneja IAM, si la funcion o automatizacion no presenta un rol claramente especifico, la llamada nunca sera ejecutada, AWS rechazara la peticion inmediatamente.

**Friction Log (Opcional):**
> La referencia de solucion presentaba los assert para obtener la key y el body de las peticiones a partir de un .get, en vez de la consulta normal de un dict[key]. Se entiende que .get() permite hacer una diferenciacion entre un assertionerror o un keyerror, el primero indica claramente porque falla el test cuando la key no existe, y el segundo solo dice que algo fallo con la key (un typo? no existe? existen dos?)

---

## Cap 04: Amazon CloudWatch & Observabilidad
**Fecha de finalización:** 2026-09-29
**Métricas:**
- Tiempo de lectura: 8min
- Tiempo en ejercicios: 15min
- Veces que recurrí al Tutor/DM: 0
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **Si una función Lambda imprime logs con información de negocio normal, ¿por qué es financieramente peligroso dejar el comportamiento por defecto de CloudWatch, y qué configuración o política debemos aplicar para evitarlo?**
   > Si el codigo se ejecuta correctamente cientos de miles de veces en un dia, se tendran cientos de miles logs con un 'Correct load' a lo largo de toda la vida util de codigo, esto genera una carga importante de almacenamiento que aws cobra por ello. La mejor manera de tratarlo pasar de Never Expire que esta como default en la configuracion de CloudWatch, a una politica de retencion explicita, esto permitiendo mantener los logs bajo un rango temporal relativamente corto, por ejemplo de 15 a 30 dias, o segun los requerimientos del sistema o del negocio que los trate. 

2. **Explica la diferencia estructural entre un Log Group y un Log Stream dentro de Amazon CloudWatch para organizar los registros de tus aplicaciones.**
   > Un Log Group es el conglomerado completo de todos los logs generados por el propio codigo, es un container con el historial completo. Log Stream es la suma de logs precisos que comparten un evento en especifico o un momento de ejecucion preciso, en si, es una fraccion de un Log Group, o una seleccion precisa de logs.

**Friction Log (Opcional):**
> CloudWatch no presenta diferencia alguna a como se manejan loggers en codigo python normal, es como traer esa misma logica que ya existe en python y aplicarla a aws, siendo una herramienta util y sin necesidad de crear otra herramienta que haga el mismo trabajo que ya hace logging.

---

## Cap 05: Integración Cloud End-to-End
**Fecha de finalización:** 2026-09-29
**Métricas:**
- Tiempo de lectura: 10min
- Tiempo en ejercicios: 25min
- Veces que recurrí al Tutor/DM: 1
- Fricción (1-10): 1

**Feynman Synthesis (Tus propias palabras):**
1. **Al intentar insertar datos leídos desde S3 hacia una base de datos RDS desde una Lambda, ¿por qué es imperativo utilizar transacciones ACID (`COMMIT` y `ROLLBACK`) en lugar de simplemente ejecutar un `INSERT` aislado en el código?**
   > Se debe manejar transacciones ACID para evitar que un error dentro del propio sistema contamine la carga o descarga de datos con informacion erronea, de esta manera se detiene la ejecucion de manera inmediata si algo falla dentro del proceso y no se llega hasta el final con datos corruptos o faltantes. Si todo sale bien el pipeline se ejecuta completamente, si existe un error en alguna etapa, el sistema hace un rollback automatico al momento antes de la ejecucion del pipeline a ese punto exacto.

2. **Si tu función Lambda necesita conectarse a una base de datos RDS de producción, ¿cómo se le deben proporcionar las credenciales (como `DB_PASSWORD`) de forma segura, considerando que el uso de un archivo local `.env` no existe ni está permitido en la plataforma Serverless de AWS?**
   > La manera mas segura de inyectar estas variables de entorno es mediante la propia configuracion por consola web de AWS. No existe un .env, no se carga con load_dotenv(), directamente no existen en el sistema o computador que este desarrollando el pipeline, todo se maneja con la seguridad interna de AWS.

**Friction Log (Opcional):**
> Ligero error de tipado en el codigo de produccion. 

---

## 🛑 Friction Log Global
Documenta aquí cualquier "rabbit hole", problema de configuración grave, o concepto que te haya tomado mucho tiempo entender a lo largo de toda la Chronicle. El Architect revisará esto para parchar el sistema.

- **Capítulo / Concepto:** 
- **Fricción:** [Qué pasó y cuánto tiempo perdiste]
- **Solución:** [Cómo lo resolviste]

---

## 📊 Métricas de Ejecución
Completa estas métricas antes de solicitar la auditoría del DM.
- **Fecha de inicio (Lectura primer Cap):** 2026-09-26
- **Fecha de finalización (Rite completado):** [YYYY-MM-DD]
- **Horas netas estimadas de dedicación:** [X] horas

---

## 📊 Métricas de Retención
- **Concepto más claro:** [¿Qué dominas a la perfección?]
- **Concepto más débil:** [¿Qué requiere más práctica en el futuro?]

---

## 🔮 Auditoría del DM
> **Auditoría del DM:** ✅ **PASS - ALL CAPS (00-05)**  
> *Evaluación del DM (Cap 00):* El Operador ha comprendido correctamente la importancia de aplicar políticas restrictivas (Mínimo Privilegio) y la arquitectura de autenticación segura sin hardcoding usando `boto3`.
> *Evaluación del DM (Cap 01):* Respuestas impecables sobre el uso estratégico de formatos crudos (JSON) vs analíticos (Parquet) y la implementación obligatoria de Date Partitioning para la eficiencia de lectura en repositorios planos tipo S3.  
> *Evaluación del DM (Cap 02):* Excelente comprensión del valor de RDS como servicio administrado y del uso de Security Groups. Aclaración técnica: el cursor en sí no previene la inyección SQL; es la *parametrización* al usar `cur.execute(query, (params,))` la que sanitiza los inputs, pero el concepto de seguridad está asimilado.
> *Evaluación del DM (Cap 03):* Entendimiento claro del modelo Serverless: cobro fraccionado por milisegundo vs costos fijos 24/7, y la importancia del Execution Role para dotar de identidad y permisos a una función Lambda en la nube.
> *Evaluación del DM (Cap 04):* Dominio total del riesgo financiero de las políticas "Never Expire". Excelente deducción en el Friction Log: la magia de CloudWatch radica en no reinventar la rueda, interceptando el módulo `logging` nativo de Python limpiamente. Diferenciación macro/micro entre Log Group y Log Stream bien asimilada.
> *Evaluación del DM (Cap 05):* Entendimiento perfecto de la inyección nativa de variables en Serverless y la importancia crítica de las transacciones ACID (Commit/Rollback) para mantener consistencia en arquitecturas distribuidas E2E.
> *Siguiente Acción:* Autorizado para iniciar la ejecución del **RITE (Prueba Final)**.
