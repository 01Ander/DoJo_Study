# Capítulo 01: Amazon S3 (Simple Storage Service)

Una vez que tenemos nuestras llaves de acceso (vistas en el Capítulo 00), podemos empezar a interactuar con los recursos en la nube. El servicio más fundamental es el almacenamiento. En AWS, el rey indiscutible del almacenamiento es **Amazon S3**.

## 1. ¿Qué es Amazon S3?

**QUÉ es:** S3 (*Simple Storage Service*) es un servicio de almacenamiento de objetos, diseñado para guardar y recuperar cualquier cantidad de datos desde cualquier parte de internet. Piensa en él como un disco duro infinito en la nube administrado por AWS.
**CÓMO se usa:** Puedes subir y bajar archivos a través de la consola web, usando la CLI de AWS, o programáticamente desde Python usando `boto3`.
**POR QUÉ importa:** Es extremadamente barato, altamente duradero (AWS promete 99.999999999% de durabilidad) y se integra nativamente con casi cualquier otra herramienta de datos y analítica en la nube. Es la base fundacional de cualquier Data Lake moderno.

*Analogía del Gremio:* S3 es como los interminables sótanos de almacenamiento de la Universidad Invisible, pero sin el riesgo de que la magia altere los pergaminos. Puedes meter millones de reportes sobre la dieta de los dragones de pantano y saber que seguirán ahí, idénticos, dentro de 100 años.

## 2. Buckets y Objetos

**QUÉ es:** S3 no usa "carpetas" y "archivos" en el sentido tradicional del disco duro de tu computadora. Usa **Buckets** (contenedores de nivel superior) y **Objects** (los archivos en sí, junto con su metadata). Una regla crítica: el nombre de un Bucket debe ser *globalmente único* en todo AWS (no puede haber dos buckets llamados "mi-bucket-de-pruebas" en todo el mundo, aunque sean de cuentas distintas).
**CÓMO se usa:** Creas un bucket una sola vez, y luego subes objetos especificando su *key* (la ruta completa simulando carpetas, ej. `dieta/2026/09/dragon.json`).
**POR QUÉ importa:** Al no ser un sistema de archivos jerárquico real (aunque lo simulemos visualmente con barras `/`), S3 puede escalar masivamente y entregar archivos en paralelo sin los cuellos de botella de un disco local tradicional.

🎯 **Objetivo de Negocio:** Crear un espacio seguro en la nube para guardar los reportes diarios de alimentación de los dragones, accesible desde cualquier sede del Gremio en Ankh-Morpork.

```python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

try:
    # Creamos un cliente para S3
    s3_client = boto3.client('s3')
    
    # Nombre del bucket (recuerda: debe ser único a nivel global)
    bucket_name = 'alimento-dragones-pantano-prod'
    
    # Intentamos crear el bucket
    # Nota: Si el nombre ya existe y le pertenece a otra persona, lanzará un error.
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"✅ Bucket '{bucket_name}' creado exitosamente.")
    
except Exception as e:
    print(f"❌ Error al crear el bucket: {e}")
```

*Zero Surprise Syntax:*
- `s3_client.create_bucket(Bucket='nombre')`: Llama a la API de S3 para aprovisionar un nuevo bucket de almacenamiento. El argumento `Bucket` especifica el nombre deseado.

## 3. Particionamiento por Fecha (Date Partitioning)

**QUÉ es:** Es una convención arquitectónica de nomenclatura donde las *keys* (las rutas de los objetos) se organizan jerárquicamente usando componentes de tiempo: típicamente `año/mes/día/archivo.json`.
**CÓMO se usa:** En vez de guardar un archivo como `reporte-2026-09-24.json` amontonado en la raíz del bucket, se guarda de manera anidada como `2026/09/24/reporte.json`.
**POR QUÉ importa:** S3 permite listar y filtrar archivos rápidamente a través de un *prefijo* (ej. "dame todo lo que empiece con `2026/09/`"). Particionar por fecha permite a los motores de procesamiento analítico escanear solo una pequeña porción relevante de los datos (lo de ese mes o día), reduciendo drásticamente el costo y tiempo de procesamiento en vez de escanear terabytes de histórico.

## 4. Almacenamiento de Ingesta: JSON vs Parquet

Cuando hacemos Ingesta de Datos, recibimos datos "crudos" (Raw) y eventualmente los transformamos para análisis. S3 es el lugar ideal para alojar ambas capas.

### Payload Crudo (JSON)

**QUÉ es:** JSON es el formato universal de intercambio de datos en internet. Es texto plano, legible por humanos, estructurado como diccionarios.
**CÓMO se usa:** Se recibe una respuesta de una API, se convierte a un string JSON y se guarda directamente en S3 sin alteraciones.
**POR QUÉ importa:** Guarda los datos *exactamente* como llegaron, sirviendo como la "fuente de la verdad" inmutable. Si un proceso posterior (como la limpieza) tiene un bug, siempre podemos volver al JSON crudo y reprocesar.

### Formato Columnar (Parquet)

**QUÉ es:** Parquet es un formato de almacenamiento *columnar*. A diferencia de un CSV o JSON donde los datos se leen secuencialmente fila por fila, Parquet guarda los datos columna por columna y los comprime enormemente mediante diccionarios internos.
**CÓMO se usa:** Se utiliza Pandas o PyArrow para convertir datos tabulares ya limpios a formato `.parquet` y se suben a S3 en la zona de consumo (Curated).
**POR QUÉ importa:** Es muchísimo más rápido de leer por motores analíticos (como Amazon Athena) y pesa una fracción de lo que pesaría un CSV o JSON equivalente, ahorrando mucho dinero en costos de S3.

🎯 **Objetivo de Negocio:** Subir el reporte diario crudo de las explosiones de los dragones, particionado por fecha, garantizando que quede un registro inmutable del evento antes de cualquier procesamiento posterior.

```python
import boto3
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 1. Simulemos el dato crudo que nos llegó de un sensor de calor
reporte = {
    "dragon_id": 42,
    "tipo": "Errol",
    "nivel_inestabilidad": 89.5,
    "dieta_ingerida": ["carbón", "botas viejas"]
}

# 2. Convertimos el diccionario nativo a un string JSON
payload_json = json.dumps(reporte)

# 3. Generamos la fecha actual para el particionamiento
hoy = datetime.now()
year = hoy.strftime('%Y')
month = hoy.strftime('%m')
day = hoy.strftime('%d')

# 4. Construimos la key particionada por fecha (convención Data Lake)
# Quedará algo como: raw/explosiones/2026/09/24/dragon_42.json
s3_key = f"raw/explosiones/{year}/{month}/{day}/dragon_{reporte['dragon_id']}.json"

bucket_name = 'alimento-dragones-pantano-prod'

# 5. Subimos el objeto crudo a S3
s3_client = boto3.client('s3')

try:
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=payload_json
    )
    print(f"✅ Reporte guardado exitosamente en: s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"❌ Error al subir el objeto: {e}")
```

*Zero Surprise Syntax:*
- `json.dumps(reporte)`: Función de la librería estándar de Python que "vuelca" (dumps) un diccionario nativo en un string de texto con sintaxis JSON válida.
- `datetime.now()`: Obtiene el objeto con la fecha y hora exactas del momento de la ejecución.
- `hoy.strftime('%Y')`: Formatea (*string format time*) la fecha, extrayendo el año a cuatro dígitos (`%Y`), el mes a dos dígitos (`%m`) o el día a dos dígitos (`%d`).
- `s3_client.put_object(...)`: Llama a la API de S3 para "poner" (subir o sobreescribir) un objeto. `Bucket` es el destino, `Key` es la ruta del archivo simulada y `Body` es el contenido crudo en sí.
