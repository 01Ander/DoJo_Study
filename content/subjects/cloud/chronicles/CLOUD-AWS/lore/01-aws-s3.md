# Capítulo 01: Amazon S3 (Simple Storage Service)

Una vez que tenemos nuestras llaves de acceso, podemos empezar a interactuar con los recursos en la nube. En AWS, la base del almacenamiento y de los Data Lakes modernos es **Amazon S3**.

## 1. Buckets y Objetos

**QUÉ es:** S3 (*Simple Storage Service*) es un servicio de almacenamiento de objetos diseñado para guardar y recuperar datos virtualmente infinitos. A diferencia de tu computadora (que usa un sistema jerárquico de carpetas en un disco duro local), S3 tiene una arquitectura plana. Usa contenedores globales llamados **Buckets** y archivos individuales llamados **Objects**.
**POR QUÉ importa:** Al ser plano, puede escalar masivamente. Los nombres de los buckets son únicos globalmente en todo el mundo. Si alguien ya registró el bucket `dragones-db`, ese nombre estará bloqueado para ti.

*Analogía del Gremio:* S3 es como los interminables sótanos de la Universidad Invisible, pero sin el riesgo de que la magia altere los pergaminos. Creas un "Bucket" que funge como tu gran bóveda inmutable.

## 2. Arquitectura de Data Lake (Date Partitioning)

**QUÉ es:** Aunque S3 es plano, podemos simular "carpetas" en la ruta del objeto (su *key*). El **Date Partitioning** (Particionamiento por Fecha) es la convención obligatoria en ingeniería de datos de organizar estas llaves usando tiempo, típicamente `año/mes/día/archivo.json`.
**POR QUÉ importa:** Si lanzas millones de archivos a la raíz de un bucket, los motores analíticos tendrán que leer (y cobrarte) por todo el bucket cada vez que busques algo de "hoy". Al particionar, el motor filtra instantáneamente la "carpeta" de hoy (`2026/09/25/`), reduciendo los costos analíticos en un 99% y acelerando las consultas.

## 3. Formatos de Almacenamiento (JSON vs Parquet)

En un Data Lake, los datos pasan por varias fases de limpieza, y el formato de almacenamiento cambia según la necesidad:
- **Ingesta Raw (JSON):** Cuando un sistema nos envía datos, llegan comúnmente en JSON. Guardamos el JSON crudo en S3 sin alterarlo. Es nuestra "fuente inmutable de la verdad" por si algo falla después. Es fácil de leer para los humanos pero ineficiente para búsquedas matemáticas.
- **Lectura Analítica (Parquet):** Una vez limpios, los datos se convierten a formato `.parquet`. A diferencia del JSON (basado en filas), Parquet es un formato **columnar**. Comprime enormemente la información, agrupa valores similares y permite a los motores analíticos saltarse columnas enteras que no necesitan, procesando gigabytes en milisegundos.

## 4. Setup Inicial (Zero Assumption)

Asumiendo que ya posees `boto3` instalado y tu `.env` configurado, puedes interactuar nativamente con S3.

## 5. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Guardar el reporte diario de la dieta de un dragón crudo en S3 para llevar un registro histórico inmutable.

Si guardamos los archivos en la raíz del bucket:

```python
import boto3
import json

s3_client = boto3.client('s3')
reporte = {"dragon_id": 42, "dieta": "carbón"}

# PELIGRO Analítico: Guardar archivos acumulados en la raíz sin jerarquía.
# En un año habrá millones de archivos aquí y será carísimo buscarlos.
s3_client.put_object(
    Bucket="alimento-dragones-pantano-prod",
    Key=f"dragon_{reporte['dragon_id']}.json", 
    Body=json.dumps(reporte)
)
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Guardar el reporte diario en S3 aplicando **Particionamiento por Fecha** (*Date Partitioning*) para acelerar consultas futuras y reducir costos.

El particionamiento por fecha organiza las *keys* (las rutas) jerárquicamente: `año/mes/día/archivo.json`.

```python
import boto3
import json
from datetime import datetime

s3_client = boto3.client('s3')
report = {"dragon_id": 42, "diet": "coal"}

# 1. Generate current date for partitioning
today = datetime.now()
year = today.strftime('%Y')
month = today.strftime('%m')
day = today.strftime('%d')

# 2. Build date-partitioned key (Data Lake convention)
s3_key = f"raw/explosions/{year}/{month}/{day}/dragon_{report['dragon_id']}.json"

# 3. Upload raw object to S3
try:
    s3_client.put_object(
        Bucket="dragon-food-swamp-prod",
        Key=s3_key,
        Body=json.dumps(report)
    )
    print(f"✅ Report saved to: s3://dragon-food-swamp-prod/{s3_key}")
except Exception as e:
    print(f"❌ S3 Error: {e}")
```

*Zero Surprise Syntax:*
- `datetime.now()`: Obtiene el objeto con fecha y hora exactas.
- `today.strftime('%Y')`: Extrae año a 4 dígitos (`%Y`), mes (`%m`) o día (`%d`).
- `s3_client.put_object(...)`: Llama a la API de S3 para subir un objeto. `Bucket` es el destino, `Key` la ruta simulada y `Body` el string JSON crudo.

### El Camino Robusto (Lectura y Decodificación)
**🎯 Objetivo de Negocio:** Descargar un reporte previamente guardado y convertirlo de un flujo de bytes a un diccionario de Python.

```python
import boto3
import json

s3_client = boto3.client('s3')

try:
    # 1. Download file from S3
    response = s3_client.get_object(
        Bucket="dragon-food-swamp-prod",
        Key="raw/explosions/2026/09/24/dragon_42.json"
    )
    
    # 2. Decode binary stream to Python dictionary
    payload = json.loads(response['Body'].read().decode('utf-8'))
    print(f"✅ Diet loaded successfully: {payload['diet']}")
    
except Exception as e:
    print(f"❌ Error reading from S3: {e}")
```

*Zero Surprise Syntax:*
- `response['Body'].read().decode('utf-8')`: Cuando AWS responde a `get_object`, no entrega texto directamente, sino un flujo de bytes en el campo `Body`. El método `.read()` extrae esos bytes, y `.decode('utf-8')` los convierte a un string legible que `json.loads` puede transformar en un diccionario.

---

## 5.1 Aprovisionamiento de Buckets con Validación DNS (`AWS-005`)

Antes de subir objetos, la infraestructura debe aprovisionar el Bucket mediante `s3_client.create_bucket(Bucket=bucket_name)`. Debido a que cada bucket de S3 tiene una dirección DNS global (`https://<bucket>.s3.amazonaws.com`), AWS impone **reglas estrictas de nomenclatura DNS**:
1. Longitud entre **3 y 63 caracteres**.
2. Solo puede contener **letras minúsculas (`a-z`), números (`0-9`) y guiones medios (`-`)**. (Quedan prohibidos los espacios, las mayúsculas y los guiones bajos `_`).
3. Debe comenzar y terminar con una letra minúscula o un número (nunca con un guion `-`).

Podemos validar esto en una sola línea con una expresión regular (`re.fullmatch`):

```python
import re
from typing import Any

# 🎯 Objetivo de Negocio: Validar reglas DNS de S3 antes de aprovisionar el bucket en AWS.

BUCKET_DNS_REGEX = r"^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$"

def provision_valid_bucket(s3_client: Any, bucket_name: str) -> str:
    if not re.fullmatch(BUCKET_DNS_REGEX, bucket_name):
        raise ValueError(f"Nombre de bucket inválido según DNS de S3: '{bucket_name}'")
    
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name
```

---

## 5.2 Serialización Columnar a Parquet (Snappy) en Memoria hacia S3 (`AWS-006`)

En la Zona Gold de un Data Lake, nunca guardamos DataFrames como CSV o JSON sueltos; los serializamos a **Apache Parquet** con compresión **Snappy**. Para no escribir archivos temporales en el disco de la Lambda o del contenedor, usamos un buffer de bytes en memoria RAM con **`io.BytesIO`**:

```python
import io
from typing import Any
import pandas as pd

# 🎯 Objetivo de Negocio: Serializar un DataFrame a formato columnar Parquet (Snappy) y subirlo a S3.

def upload_gold_parquet(
    s3_client: Any,
    df: pd.DataFrame,
    bucket_name: str,
    s3_key: str,
) -> int:
    # 1. Creamos un archivo binario virtual en la memoria RAM
    buffer = io.BytesIO()

    # 2. Volcamos el DataFrame en formato Parquet comprimido con Snappy (sin el índice de Pandas)
    df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)

    # 3. Extraemos los bytes puros con buffer.getvalue() y los enviamos a S3
    parquet_bytes = buffer.getvalue()
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=parquet_bytes,
    )
    return len(parquet_bytes)
```

> **Zero Surprise Syntax:**
> * **`io.BytesIO()`:** Crea un flujo binario en RAM que se comporta igual que un archivo abierto con `open("archivo.parquet", "wb")`, pero sin tocar el disco duro.
> * **`df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)`:** Convierte el DataFrame al formato columnar Parquet usando el motor C++ `pyarrow` y el algoritmo `snappy` (el estándar de AWS por su equilibrio entre alta velocidad y buena compresión).
> * **`buffer.getvalue()`:** Devuelve el contenido completo del buffer en RAM como un objeto `bytes` listo para pasarse al parámetro `Body=` de `put_object`.

---

## 5.3 Consultas Analíticas Serverless sobre S3: AWS Glue Data Catalog & Amazon Athena

Una vez que nuestros archivos `.parquet` están particionados en S3 (`s3://fincorp-gold/transactions/year=2026/month=11/data.parquet`), ¿cómo los consultan los analistas con SQL sin tener que copiarlos a una base de datos RDS?

En AWS se utiliza la dupla serverless **AWS Glue + Amazon Athena**:
1. **AWS Glue Data Catalog (El Índice / Metadatos):** Un *Glue Crawler* inspecciona las carpetas de S3, detecta las columnas del archivo Parquet y registra la definición de la tabla (`gold_transactions`) en el catálogo central. No mueve ni duplica los datos.
2. **Amazon Athena (El Motor SQL Serverless):** Permite ejecutar consultas SQL estándar (`SELECT status, SUM(amount) FROM gold_transactions WHERE year='2026' GROUP BY status`) leyendo **directamente los archivos Parquet desde S3**. Gracias al formato columnar Parquet y al particionamiento por fecha, Athena lee solo los megabytes de las columnas solicitadas y cobra únicamente por terabyte escaneado.

## 6. Conexión con Testing (Test-Driven Lore)

Cuando testeas código que interactúa con S3 y con fechas dinámicas, te encuentras con dos problemas: no quieres subir archivos reales, y el "día de hoy" cambia todos los días. 

- **Mockear `boto3.client('s3')`:** Como aprendimos, usamos `@patch('ruta.boto3.client')` para evitar la llamada de red real.
- **Mockear Fechas (Freezing Time):** Si tu código usa `datetime.now()`, el test podría fallar mañana porque el string de S3 (`2026/09/25/...`) cambiará. Parcheamos `datetime` devolviendo una fecha estática para que la aserción de la ruta siempre sea predecible.
- **Simular errores con `side_effect`:** Si queremos comprobar que nuestro bloque `try/except` atrapa errores de S3 (por ejemplo, si no hay permisos de acceso `Access Denied` o se cae la red) y retorna `None` en lugar de que el programa explote ruidosamente, le asignamos una excepción a `side_effect` en el método `put_object`.

```python
import datetime
from unittest.mock import patch, MagicMock

class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

# 1. Success Test: Freeze time and mock S3 simultaneously
@patch('my_solution.datetime', MockDatetime)
@patch('my_solution.boto3.client')
def test_save_diet_success(mock_boto):
    from my_solution import save_diet
    
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3
    
    # Act: Call our function (which will use frozen datetime.now())
    result = save_diet(42, ["sulfur", "rocks"])
    
    # Assert: Validate returned key and exact arguments sent to S3
    expected_key = "raw/explosions/2026/09/24/dragon_42.json"
    assert result == expected_key
    mock_s3.put_object.assert_called_once()
    assert mock_s3.put_object.call_args[1]['Key'] == expected_key

# 2. Error Test: Force S3 failure with side_effect
@patch('my_solution.boto3.client')
def test_save_diet_error(mock_boto):
    from my_solution import save_diet
    
    mock_s3 = MagicMock()
    # Instruct mock to raise an exception when uploading
    mock_s3.put_object.side_effect = Exception("Access Denied")
    mock_boto.return_value = mock_s3
    
    result = save_diet(99, ["salad"])
    
    # Assert: Verify error was handled and returned None
    assert result is None
```

## 7. Mapa de Ejercicios

Aplica este concepto en `quests/01-aws-s3/` implementando un *ingestor* crudo que divida correctamente las particiones.
