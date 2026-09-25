# Capítulo 01: Amazon S3 (Simple Storage Service)

Una vez que tenemos nuestras llaves de acceso, podemos empezar a interactuar con los recursos en la nube. En AWS, la base del almacenamiento y de los Data Lakes modernos es **Amazon S3**.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** S3 (*Simple Storage Service*) es un servicio de almacenamiento de objetos diseñado para guardar y recuperar datos infinitos. No usa "carpetas" reales, sino contenedores globales llamados **Buckets** y archivos llamados **Objects**.
**POR QUÉ importa:** Es extremadamente barato, altamente duradero (99.999999999% de durabilidad) y se integra nativamente con herramientas analíticas. Guarda los datos como llegaron (Ingesta de Payload crudo JSON) o procesados (Formato columnar Parquet).

> **Densidad (Analogía del Gremio de Dragones):**
> S3 es como los interminables sótanos de la Universidad Invisible, pero sin el riesgo de que la magia altere los pergaminos. Creas un "Bucket" que funge como la gran bóveda inmutable. Los nombres de los buckets son únicos globalmente. Si alguien en el mundo ya nombró su bóveda `dragones-db`, tú no podrás usar ese nombre.

## 2. Setup Inicial (Zero Assumption)

Asumiendo que ya posees `boto3` instalado y tu `.env` configurado, puedes interactuar nativamente con S3.

## 3. Implementación (Cómo)

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

## 4. Conexión con Testing (Test-Driven Lore)

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

## 5. Mapa de Ejercicios

Aplica este concepto en `quests/01-aws-s3/` implementando un *ingestor* crudo que divida correctamente las particiones.
