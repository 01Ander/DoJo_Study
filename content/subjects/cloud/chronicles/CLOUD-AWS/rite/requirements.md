# Rito de Paso: B2B Warehouse Inventory Pipeline

## Contexto del Proyecto (Domain Shifting: E-commerce Startup B2B)
Felicidades, has sido contratado como Data Engineer Mid-Level en *SupplyChain B2B*, una startup de logística de rápido crecimiento. Manejamos el inventario en tiempo real de decenas de almacenes físicos. Actualmente, los escáneres de montacargas envían archivos JSON a la nube (AWS), pero no tenemos un sistema automático para integrarlos a nuestra base de datos relacional central. Tu misión es construir ese pipeline de orquestación desde cero.

Este Rito se divide en Fases Desbloqueables. No puedes avanzar a la siguiente sin dominar la anterior.

---

## Fases del Proyecto

### Fase 1: Seguridad e Identidad (Capítulo 00 — IAM)
Antes de construir nada, tu script necesita permisos para operar en AWS de forma segura.
- **Requisito 1:** Configurar tus variables de entorno locales (con `dotenv`) para que tu script pueda autenticarse temporalmente hacia S3 sin hardcodear credenciales en el código fuente.
- **Requisito 2:** Al finalizar esta fase, realiza un Semantic Commit evidenciando tu progreso inicial.

### Fase 2: Data Lake Raw (Capítulo 01 — S3)
El origen de los datos es el bucket de ingesta donde caen los reportes de inventario.
- **Requisito 1:** Escribir código usando `boto3` que pueda descargar un archivo JSON crudo desde Amazon S3 (asumiendo que el bucket y el key serán dinámicos).
- **Requisito 2:** Parsear el Body (flujo de bytes) del archivo descargado hacia un diccionario estándar de Python usando `json.loads`.
- **Requisito 3:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 3: Warehouse Relacional (Capítulo 02 — RDS)
El destino final de los datos es la base de datos PostgreSQL corporativa.
- **Requisito 1:** Crear una función de conexión a RDS utilizando la librería `psycopg2`, inyectándole los parámetros puramente a través de variables de entorno (DBAPI).
- **Requisito 2:** Escribir el código que inserte los datos parseados de la Fase 2 en la tabla `inventory_logs` (columnas: `warehouse_id, item_id, quantity`), utilizando paso seguro de parámetros (`%s`) para evitar Inyección SQL.
- **Requisito 3:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 4: Worker Serverless (Capítulo 03 — Lambda)
El pipeline debe correr automáticamente impulsado por Arquitectura Event-Driven, sin servidores encendidos 24/7.
- **Requisito 1:** Consolidar el código de extracción (Fase 2) y de carga (Fase 3) dentro del punto de entrada estándar `lambda_handler(event, context)`.
- **Requisito 2:** Hacer que el código extraiga dinámicamente el `bucket` y el `key` analizando la estructura del objeto de entrada `event` (asumiendo que el evento proviene de S3).
- **Requisito 3:** Remover todo uso de `load_dotenv` para leer las variables de base de datos, utilizando en su lugar `os.environ` directamente, simulando el comportamiento real de AWS Lambda.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 5: Observabilidad e Integración E2E (Capítulos 04 y 05)
Un ingeniero profesional sabe que los sistemas fallan. Debes garantizar resiliencia total y rastreabilidad en CloudWatch.
- **Requisito 1:** Validar el diccionario JSON antes de procesarlo (debe existir `warehouse_id`, `item_id`, y un `quantity` > 0). Si falla la validación, abortar todo e imprimir un `ERROR` estricto usando el módulo `logging`: `"VALIDATION_FAILED: Payload corrupto o invalido"` y luego lanzar una excepción explícita (`raise ValueError(...)`) para que CloudWatch marque la invocación como fallida.
- **Requisito 2:** Proteger la inserción con transacciones ACID. Ejecuta el `COMMIT` únicamente si la base de datos acepta el dato. Si lanza una excepción, ejecuta un `ROLLBACK` manual.
- **Requisito 3:** Garantizar mediante un bloque `finally` que la conexión a la base de datos se cierre siempre con `conn.close()`, sin importar si el código fue exitoso o catastrófico. No debes retornar códigos HTTP, ya que los eventos de S3 son asíncronos y no los procesan.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

---

## Criterios de Éxito y Evaluación
- **Independencia Funcional:** Todo tu código debe residir y ser ejecutable en un pipeline lógico.
- **Testing y Validaciones:** Aunque el scaffolding no existe, debes asegurar con pruebas (`pytest`) y mocks que tu código no explotará en producción.
- **Logging Forense:** El módulo `logging` es obligatorio. No utilices instrucciones simples de `print()`.
- **Transparencia:** Durante el desarrollo del Rito, todo bloqueo mental, bug encontrado y decisión técnica DEBE estar detalladamente documentado en tu archivo `journal.md`.

¡Buena suerte, Operador!
