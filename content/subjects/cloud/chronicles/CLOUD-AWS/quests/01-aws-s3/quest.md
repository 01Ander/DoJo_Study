# Quest 01: Amazon S3 (Particionamiento y Almacenamiento)

Ahora que tenemos nuestro Gafete Mágico (IAM), necesitamos ponerlo a trabajar. El Archivo de la Biblioteca del Gremio nos ha pedido un script automatizado para ingestar los reportes diarios de dieta de los dragones hacia la nube.

## 🎯 Objetivo de Negocio
Construir una función que empaquete el reporte de alimentación de un dragón y lo envíe a nuestro Data Lake crudo en S3, utilizando la convención arquitectónica estricta de particionamiento por fecha (`year/month/day`) vista en el Lore.

## 📝 Instrucciones

1. **Crear la función `guardar_dieta(dragon_id: int, dieta_lista: list)`:**
   - **Propósito:** Construir un documento JSON a partir de los datos, generar dinámicamente la ruta particionada por fecha, y subir el archivo al bucket `alimento-dragones-pantano-prod`.
   - **Entrada:** Recibe el ID numérico del dragón (`dragon_id`) y una lista de strings con lo que comió (`dieta_lista`).
   - **Formato del Diccionario:** El diccionario interno antes de convertirse a JSON debe lucir exactamente así:
     ```python
     {
         "dragon_id": 42,
         "dieta": ["carbón", "botas viejas"]
     }
     ```
   - **Reglas de Ruta (Key):** La ruta debe ser calculada dinámicamente según la fecha en que se ejecute el script usando `datetime.now()`, con el formato: `raw/dietas/YYYY/MM/DD/dragon_{ID}.json`. *(Ejemplo: Si hoy es 24 de Septiembre de 2026 y el ID es 42, la ruta debe ser `raw/dietas/2026/09/24/dragon_42.json`)*.
   - **Salida (Retorno):** Si la subida a S3 es exitosa, la función debe retornar el string exacto de la ruta (`key`) generada.
   - **Manejo de Errores:** Si `boto3` lanza una excepción (ej. no tienes conexión o no existe el bucket), debes atraparla y retornar `None`.

> **Scaffolding Nivel 2:** Implementa tu código en `my_solution.py` siguiendo las guías. En `test_my_solution.py`, el andamiaje del "mock" ya está configurado para simular a AWS S3 y congelar el tiempo. Solo debes completar el llamado a la función y su aserción.
