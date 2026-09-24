# Grimoire — `CLOUD-AWS`

> **Instrucción para el Operador:** El aprendizaje pasivo no existe. Después de leer cada capítulo del `lore/` y completar su respectiva `quest/`, debes responder a las preguntas de ese capítulo usando **tus propias palabras** (Técnica Feynman). No copies y pegues del Lore.
> 
> Una vez completado, el Dungeon Master auditará este documento (`/scry`) para darte acceso al Rite final.

---

## Cap 00: AWS Identity & Access Management (IAM)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **¿Por qué es un riesgo de seguridad crítico darle a un script permisos de "Administrador Total" en AWS por conveniencia, y qué principio de IAM debemos aplicar en nuestras Políticas (Policies) para evitarlo?**
   > [Tu respuesta aquí]

2. **Describe exactamente cómo se debe autenticar un script de Python en AWS utilizando la librería `boto3` para evitar el peor pecado de seguridad en la nube (el hardcoding de credenciales directas en el código fuente).**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## Cap 01: Amazon S3 (Simple Storage Service)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **S3 permite almacenar tanto JSON como Parquet. ¿Por qué elegirías guardar un archivo en formato crudo JSON en la zona de ingesta, y por qué preferirías usar un formato columnar como Parquet para la zona de consumo analítico (Curated)?**
   > [Tu respuesta aquí]

2. **Explica cómo S3 organiza los objetos si no existe un sistema de carpetas real, y describe la convención arquitectónica de nomenclatura (*keys*) que se utiliza al ingerir datos para evitar escanear terabytes de histórico inútil al hacer consultas.**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## Cap 02: Amazon RDS (Relational Database Service)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **¿Por qué un ingeniero de datos preferiría usar Amazon RDS en lugar de instalar PostgreSQL manualmente en un servidor alquilado (auto-administrado), y qué herramienta nativa de AWS tipo firewall debe usar para evitar que bots en internet intenten hackear la base de datos?**
   > [Tu respuesta aquí]

2. **En el ecosistema de bases de datos con Python (DBAPI), ¿qué es exactamente un "cursor" y por qué es obligatorio crearlo cuando usamos librerías como `psycopg2` para enviar consultas a RDS?**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## Cap 03: AWS Lambda (Serverless Compute)
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **En una Arquitectura Orientada a Eventos en AWS, ¿por qué es financieramente y técnicamente superior usar una función Lambda disparada por un "Gatillo" (*Trigger*) en lugar de tener un script corriendo 24/7 en un bucle infinito preguntando si hay trabajo nuevo (*polling*)?**
   > [Tu respuesta aquí]

2. **Explica qué es el `Execution Role` de una función Lambda y por qué el código Python dentro de tu `lambda_handler` lanzaría un error instantáneo de `AccessDenied` al intentar leer un objeto de S3 si olvidas configurar este rol.**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## Cap 04: Amazon CloudWatch & Observabilidad
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **Si una función Lambda imprime logs con información de negocio normal, ¿por qué es financieramente peligroso dejar el comportamiento por defecto de CloudWatch, y qué configuración o política debemos aplicar para evitarlo?**
   > [Tu respuesta aquí]

2. **Explica la diferencia estructural entre un Log Group y un Log Stream dentro de Amazon CloudWatch para organizar los registros de tus aplicaciones.**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## Cap 05: Integración Cloud End-to-End
**Fecha de finalización:** [YYYY-MM-DD]
**Métricas:**
- Tiempo de lectura: [X]min
- Tiempo en ejercicios: [X]min
- Veces que recurrí al Tutor/DM: [X]
- Fricción (1-10): [X]

**Feynman Synthesis (Tus propias palabras):**
1. **Al intentar insertar datos leídos desde S3 hacia una base de datos RDS desde una Lambda, ¿por qué es imperativo utilizar transacciones ACID (`COMMIT` y `ROLLBACK`) en lugar de simplemente ejecutar un `INSERT` aislado en el código?**
   > [Tu respuesta aquí]

2. **Si tu función Lambda necesita conectarse a una base de datos RDS de producción, ¿cómo se le deben proporcionar las credenciales (como `DB_PASSWORD`) de forma segura, considerando que el uso de un archivo local `.env` no existe ni está permitido en la plataforma Serverless de AWS?**
   > [Tu respuesta aquí]

**Friction Log (Opcional):**
> [Obstáculos técnicos o conceptuales específicos de este capítulo]

---

## 🛑 Friction Log Global
Documenta aquí cualquier "rabbit hole", problema de configuración grave, o concepto que te haya tomado mucho tiempo entender a lo largo de toda la Chronicle. El Architect revisará esto para parchar el sistema.

- **Capítulo / Concepto:** 
- **Fricción:** [Qué pasó y cuánto tiempo perdiste]
- **Solución:** [Cómo lo resolviste]

---

## 📊 Métricas de Ejecución
Completa estas métricas antes de solicitar la auditoría del DM.
- **Fecha de inicio (Lectura primer Cap):** [YYYY-MM-DD]
- **Fecha de finalización (Rite completado):** [YYYY-MM-DD]
- **Horas netas estimadas de dedicación:** [X] horas

---

## 📊 Métricas de Retención
- **Concepto más claro:** [¿Qué dominas a la perfección?]
- **Concepto más débil:** [¿Qué requiere más práctica en el futuro?]

---

## 🔮 Auditoría del DM
> **Auditoría del DM:** [Pendiente]  
> *El agente completará esta sección con su evaluación tras ejecutar `/scry`.*
