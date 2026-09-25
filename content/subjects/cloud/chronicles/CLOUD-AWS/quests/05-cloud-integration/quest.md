# Quest 05: Integración Cloud End-to-End

¡Has llegado a la prueba final de la infraestructura del Gremio! Todo lo que has aprendido —Seguridad, Almacenamiento, Bases de Datos, Cómputo Serverless y Observabilidad— debe unirse en un solo artefacto cohesivo.

## 🎯 Objetivo de Negocio
Construir el Pipeline Definitivo: Una función Lambda que se dispare por un archivo nuevo en S3, lo descargue, extraiga su contenido, lo inserte en PostgreSQL garantizando transacciones seguras (ACID) y registre todo en CloudWatch.

## 📝 Instrucciones

1. **El Entorno Verdadero:** A diferencia del Quest 00, **está estrictamente prohibido usar `load_dotenv()`**. En la verdadera nube de AWS Lambda, ese archivo no existe; las credenciales ya vienen inyectadas en el sistema operativo. Debes extraerlas directamente con `os.environ[]`.
2. **Crear la función `lambda_handler(event, context)`:**
   - **Paso 1 (Extracción S3):** Usando `boto3`, obtén el nombre del bucket y la key del `event`. Descarga el archivo, lee su Body, decodifícalo en `utf-8` y conviértelo a un diccionario de Python.
   - **Paso 2 (Conexión RDS):** Conéctate a Postgres usando las variables de entorno: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. 
   - **Paso 3 (Inserción ACID):** Extrae del JSON el `dragon_id` y los `kilos_carne`. Insértalos en la tabla `consumos` (columnas: `dragon_id, kilos`) usando parámetros seguros `%s`. 
   - **Paso 4 (Consolidación):** Ejecuta un `commit()` para guardar permanentemente en el disco de AWS RDS.
   - **Paso 5 (Manejo de Errores):** Si **cualquier cosa** falla (ej. red caída, JSON malo), atrapa la excepción. Si la conexión a BD estaba abierta, haz un `rollback()`. Retorna statusCode 500 y loguea el error con `.error()`.
   - **Paso 6 (Limpieza Absoluta):** Sin importar el éxito o el fracaso, usa el bloque `finally` para asegurarte de que, si la conexión existe, se cierre con `conn.close()`.
3. **Salida:** Si todo es exitoso, retorna `{'statusCode': 200, 'body': 'ETL Cloud Completado'}`.

> **Scaffolding Nivel 5 (100% Autónomo):** Recibes `my_solution.py` y `test_my_solution.py` vacíos. Debes construir el pipeline completo y diseñar tus propios tests utilizando mocks para simular el ecosistema de AWS. Los archivos de referencia siguen ahí si te bloqueas irreversiblemente. ¡Buena suerte, Arquitecto!
