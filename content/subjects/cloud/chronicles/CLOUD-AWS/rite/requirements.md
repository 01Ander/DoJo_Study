# Rito de Paso: B2B Warehouse Inventory Pipeline

## Contexto del Proyecto (Domain Shifting: E-commerce Startup B2B)
Felicidades, has sido contratado como Data Engineer Mid-Level en *SupplyChain B2B*, una startup de logística de rápido crecimiento. Manejamos el inventario en tiempo real de decenas de almacenes físicos. Actualmente, los escáneres de montacargas envían archivos JSON a la nube (AWS), pero no tenemos un sistema automático para integrarlos a nuestra base de datos relacional central. Tu misión es construir ese pipeline de orquestación desde cero.

Este Rito se divide en Fases Desbloqueables. No puedes avanzar a la siguiente sin dominar la anterior.

> **Nota arquitectónica:** La progresión de este Rito es **top-down**. Se conocen todos los requerimientos desde el inicio, por lo tanto el diseño parte del contrato final (Lambda) hacia abajo. Las referencias a capítulos del lore son de soporte conceptual, no imponen el orden de construcción.

---

## 📄 Data Contract

Este contrato lo define el equipo de hardware (escáneres de montacargas). Tú, como Data Engineer, lo recibes — no lo diseñas.

### Payload Raw (archivo JSON en S3)
Cada escáner deposita un archivo `.json` por operación de inventario. Así se ve un registro real:

```json
{
  "warehouse_id": "WH-BCN-01",
  "item_id": "SKU-78912",
  "quantity": 34,
  "scan_timestamp": "2026-10-01T13:45:00Z",
  "operator_id": "OP-003"
}
```

> Los campos `scan_timestamp` y `operator_id` son metadata del escáner. El pipeline **solo extrae** `warehouse_id`, `item_id` y `quantity` para la carga relacional.

### Evento S3 que recibe `lambda_handler`
Cuando el archivo cae en el bucket, S3 dispara Lambda con este evento. Es la estructura que debes parsear en la Fase 2:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "supplychainb2b-raw-inventory" },
        "object": { "key": "scans/WH-BCN-01/2026-10-01/scan_78912.json" }
      }
    }
  ]
}
```

### Schema Destino — Tabla `inventory_logs` (PostgreSQL)

```sql
CREATE TABLE inventory_logs (
    id            SERIAL PRIMARY KEY,
    warehouse_id  VARCHAR(20)  NOT NULL,
    item_id       VARCHAR(30)  NOT NULL,
    quantity      INTEGER      NOT NULL CHECK (quantity > 0),
    ingested_at   TIMESTAMP    DEFAULT NOW()
);
```

---

## Fases del Proyecto

### Fase 1: El Contrato — Skeleton del Pipeline (Referencia: Cap 03 — Lambda)
Antes de escribir una sola línea de lógica, defines el contrato del sistema: el punto de entrada que orquestará todo.
- **Requisito 1:** Crear el archivo principal del pipeline con el punto de entrada estándar `lambda_handler(event, context)` como función orquestadora vacía. Este será el único entry point del sistema.
- **Requisito 2:** Configurar el módulo `logging` a nivel de módulo (fuera de la función) con nivel `INFO`. No se usará `print()` en ningún punto del proyecto.
- **Requisito 3:** Documentar en el cuerpo de `lambda_handler` (como comentarios o docstring) los tres pasos que ejecutará: extracción desde S3, carga a RDS, y retorno implícito. Esto define el contrato de ejecución.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 2: Capa de Extracción — S3 Helper (Referencia: Cap 01 — S3)
Con el contrato definido, construyes la primera pieza: la función que extrae datos del Data Lake.
- **Requisito 1:** Escribir la función `extract_from_s3(bucket: str, key: str) -> dict` usando `boto3`. Las credenciales AWS serán resueltas automáticamente por el IAM Role de ejecución vía credential chain — sin `dotenv`, sin código explícito de autenticación.
- **Requisito 2:** Parsear el Body (flujo de bytes) del objeto S3 hacia un diccionario Python usando `json.loads`. La función debe retornar ese diccionario.
- **Requisito 3:** Conectar esta función al esqueleto de `lambda_handler`, extrayendo dinámicamente `bucket` y `key` desde la estructura del objeto `event` de S3.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 3: Capa de Carga — RDS Helper (Referencia: Cap 02 — RDS)
Construyes la segunda pieza: la función que persiste los datos en el warehouse relacional.
- **Requisito 1:** Escribir la función `load_to_rds(data: dict) -> None` que establezca una conexión a PostgreSQL usando `psycopg2`. Los parámetros de conexión (host, port, dbname, user, password) deben ser inyectados exclusivamente desde `os.environ` — nunca hardcodeados.
- **Requisito 2:** Implementar la inserción de los datos en la tabla `inventory_logs` (columnas: `warehouse_id, item_id, quantity`) usando paso seguro de parámetros (`%s`) para prevenir SQL Injection.
- **Requisito 3:** Conectar esta función al esqueleto de `lambda_handler`, pasándole el diccionario retornado por `extract_from_s3`.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 4: Resiliencia E2E — Observabilidad y ACID (Referencia: Cap 04 y 05)
El pipeline funciona en el happy path. Ahora lo blindas para producción.
- **Requisito 1:** Añadir validación del diccionario extraído antes de llamar a `load_to_rds`. Debe verificar que existan `warehouse_id`, `item_id`, y que `quantity > 0`. Si falla, loggear con nivel `ERROR` el mensaje `"VALIDATION_FAILED: Payload corrupto o invalido"` y lanzar `raise ValueError(...)` para que CloudWatch marque la invocación como fallida.
- **Requisito 2:** Proteger la inserción con transacciones ACID dentro de `load_to_rds`: ejecutar `COMMIT` solo si la BD acepta el dato; ejecutar `ROLLBACK` manual ante cualquier excepción.
- **Requisito 3:** Garantizar mediante un bloque `finally` dentro de `load_to_rds` que la conexión se cierre siempre con `conn.close()`, independientemente del resultado. No retornar códigos HTTP — los eventos S3 son asíncronos.
- **Requisito 4:** Al finalizar esta fase, realiza un Semantic Commit.

---

## Criterios de Éxito y Evaluación
- **Diseño top-down:** El pipeline fue diseñado con el contrato final en mente desde la Fase 1. No existe código "temporal" que luego se refactorizó.
- **Sin dotenv en el artefacto:** Las credenciales AWS las maneja el IAM Role; las de RDS las maneja `os.environ`. El artefacto final no depende de ningún archivo `.env`.
- **Testing y Validaciones:** Asegura con pruebas (`pytest`) y mocks que tu código no explotará en producción.
- **Logging Forense:** El módulo `logging` es obligatorio en todo el pipeline.
- **Transparencia:** Durante el desarrollo del Rito, todo bloqueo mental, bug encontrado y decisión técnica DEBE estar detalladamente documentado en tu archivo `journal.md`.

¡Buena suerte, Operador!

