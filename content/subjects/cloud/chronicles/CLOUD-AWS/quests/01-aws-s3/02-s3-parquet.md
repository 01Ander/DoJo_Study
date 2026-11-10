# Quest 01-02 (Misión M5): Creación de Buckets S3 con Validación DNS y Serialización Parquet (`AWS-005` + `AWS-006`)

**Objetivo:** Aprovisionar el Bucket del Data Lake de **FinCorp Global** validando las reglas globales DNS de Amazon S3 (`AWS-005`) y persistir el DataFrame de la Zona Gold en formato columnar **Parquet con compresión Snappy** en memoria usando `io.BytesIO` (`AWS-006`, Lore 01 §5.1 y §5.2).

---

## Archivo de Trabajo

Edita [`fincorp_s3_parquet.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/fincorp_s3_parquet.py) e implementa las dos funciones:

### 1. `provision_valid_bucket(s3_client: Any, bucket_name: str) -> str`
* Valida `bucket_name` contra la expresión regular `BUCKET_DNS_REGEX` (`re.fullmatch(BUCKET_DNS_REGEX, bucket_name)`).
* Si no cumple el formato DNS de S3, lanza `raise ValueError(...)`.
* Si es válido, invoca `s3_client.create_bucket(Bucket=bucket_name)` y retorna `bucket_name`.

---

### 2. `upload_gold_parquet(s3_client: Any, df: pd.DataFrame, bucket_name: str, s3_key: str) -> int`
* Crea un buffer binario en memoria RAM: `buffer = io.BytesIO()`.
* Serializa el DataFrame en formato Parquet:
  `df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)`
* Extrae los bytes (`parquet_bytes = buffer.getvalue()`), súbelos con `s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=parquet_bytes)` y retorna la cantidad de bytes subidos (`len(parquet_bytes)`).

---

## 🧪 Comando de Verificación Binaria (`M5`)
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/test_fincorp_s3_parquet.py -v
```
*(Criterio de éxito: `4 passed` con exit code 0).*

