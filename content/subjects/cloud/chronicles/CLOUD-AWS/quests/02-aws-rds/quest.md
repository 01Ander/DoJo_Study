# Quest 02: Amazon RDS (Conexión Segura e Interfaz DBAPI)

Ahora que sabemos extraer datos y subirlos, debemos ser capaces de leer información crítica de negocio. La salud de los dragones reside en un clúster de Amazon RDS administrado por el Gremio Central.

## 🎯 Objetivo de Negocio
Crear una función robusta que consulte el `nivel_inestabilidad` de un dragón específico directamente en PostgreSQL, sin dejar las credenciales expuestas en tu script.

## 📝 Instrucciones

1. **Crear la función `consultar_estado(dragon_id: int)`:**
   - **Propósito:** Abrir una conexión de red hacia RDS usando `psycopg2`, consultar el nivel de inestabilidad y retornar el valor numérico. Asegurar que los recursos de red (cursores y conexiones) se limpien sin importar si hay error o no.
   - **Entrada:** `dragon_id` (el identificador único del dragón).
   - **Variables Requeridas:** Carga las variables locales (vía `dotenv`): `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. Asume el puerto por defecto `5432`.
   - **Consulta SQL:** La tabla se llama `dragones_salud`. Necesitas traer la columna `nivel_inestabilidad` donde la columna `dragon_id` coincida con el parámetro. *(Ojo: Usa parámetros parametrizados en `execute()` como `%s` para evitar inyección SQL)*.
   - **Salida (Retorno):** Debe retornar el número entero (ej. `89`) del nivel. Si la consulta no trae resultados, o si ocurre un error de red (excepción), debe retornar `None`.
   - **Obligatorio:** Utiliza un bloque `try/except/finally` para garantizar que la conexión (`conn.close()`) se ejecute SIEMPRE al terminar, previniendo conexiones zombie en el servidor.

> **Scaffolding Nivel 3:** En este nivel, el esqueleto básico ya no te lo damos. Debes armar la estructura lógica de conexión y de limpieza basándote en el Cap 02 y Cap 05. Los tests revisarán no solo tu respuesta, sino que `conn.close()` haya sido llamado estrictamente.
