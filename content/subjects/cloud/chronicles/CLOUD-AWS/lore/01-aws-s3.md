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
reporte = {"dragon_id": 42, "dieta": "carbón"}

# 1. Generamos la fecha actual para el particionamiento
hoy = datetime.now()
year = hoy.strftime('%Y')
month = hoy.strftime('%m')
day = hoy.strftime('%d')

# 2. Construimos la key particionada por fecha (convención Data Lake)
s3_key = f"raw/explosiones/{year}/{month}/{day}/dragon_{reporte['dragon_id']}.json"

# 3. Subimos el objeto crudo a S3
try:
    s3_client.put_object(
        Bucket="alimento-dragones-pantano-prod",
        Key=s3_key,
        Body=json.dumps(reporte)
    )
    print(f"✅ Reporte guardado en: s3://alimento-dragones-pantano-prod/{s3_key}")
except Exception as e:
    print(f"❌ Error S3: {e}")
```

*Zero Surprise Syntax:*
- `datetime.now()`: Obtiene el objeto con fecha y hora exactas.
- `hoy.strftime('%Y')`: Extrae año a 4 dígitos (`%Y`), mes (`%m`) o día (`%d`).
- `s3_client.put_object(...)`: Llama a la API de S3 para subir un objeto. `Bucket` es el destino, `Key` la ruta simulada y `Body` el string JSON crudo.

## 6. Conexión con Testing (Test-Driven Lore)

Cuando testeas código que interactúa con S3 y con fechas dinámicas, te encuentras con dos problemas: no quieres subir archivos reales, y el "día de hoy" cambia todos los días. 

- **Mockear boto3.client('s3'):** Como aprendimos, usamos `@patch('ruta.boto3.client')` para evitar la llamada de red real.
- **Mockear Fechas (Freezing Time):** Si tu código usa `datetime.now()`, el test podría fallar mañana porque el string de S3 (`2026/09/25/...`) cambiará. Parcheamos `datetime` devolviendo una fecha estática para que la aserción de la ruta siempre sea predecible.

```python
from unittest.mock import patch
import datetime

class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

# Congelamos el tiempo y simulamos AWS simultáneamente
@patch('my_solution.datetime', MockDatetime)
@patch('my_solution.boto3.client')
def test_guardar(mock_boto):
    # Ahora datetime.now() siempre será 24-09-2026 dentro de este test
    pass
```

## 7. Mapa de Ejercicios

Aplica este concepto en `quests/01-aws-s3/` implementando un *ingestor* crudo que divida correctamente las particiones.
