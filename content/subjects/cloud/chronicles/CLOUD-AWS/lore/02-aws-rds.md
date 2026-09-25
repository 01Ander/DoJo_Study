# Capítulo 02: Amazon RDS (Relational Database Service)

S3 es perfecto para guardar millones de archivos crudos y masivos a muy bajo costo, pero no es una base de datos relacional; no puedes hacer consultas `JOIN` de manera nativa. Para esto, usamos **Amazon RDS**.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** Amazon RDS (*Relational Database Service*) es un servicio que aprovisiona, escala y opera bases de datos relacionales (PostgreSQL, MySQL) en la nube de forma **administrada**.
**POR QUÉ importa:** Nos libera de instalar Linux, configurar Postgres, parches o backups, permitiéndonos enfocarnos en modelar datos y construir ETLs. 

> **Densidad (Analogía del Gremio de Dragones):**
> Una base auto-administrada es como criar ovejas, esquilar e hilar la lana para tejer un traje ignífugo antes de poder acercarte a un dragón. RDS es ir al sastre y decir: "Dame un traje talla M"; AWS hace el trabajo sucio.
>
> **Security Groups (El Cortafuegos):** RDS usa Security Groups (firewalls). Si dejas abierta tu base de datos al mundo (`0.0.0.0/0`), bots atacarán el puerto 5432. Las DBs siempre deben restringirse a IPs privadas de confianza.

## 2. Setup Inicial (Zero Assumption)

Para conectarse a motores relacionales desde Python, usamos el estándar interno DBAPI. Para PostgreSQL instalamos `psycopg2-binary`.

```bash
pip install psycopg2-binary
```

Configura en tu `.env` las credenciales (siempre inyectadas, nunca hardcodeadas):
```env
DB_HOST=dragones-db.cxyz123.us-east-1.rds.amazonaws.com
DB_NAME=gremio_db
DB_USER=master_user
DB_PASSWORD=SuperSecretPassword!
```

## 3. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Consultar un nivel de salud específico del dragón filtrando por su ID.

Si concatenamos los valores usando F-strings directos:

```python
import psycopg2

dragon_id = 42 # Este valor podría venir de una API o del usuario
query = f"SELECT nivel FROM dragones_salud WHERE dragon_id = {dragon_id};"

# PELIGRO: Si dragon_id es "42; DROP TABLE dragones_salud;", 
# borrarían la base de datos completa (Ataque SQL Injection).
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Consultar un registro parametrizándolo de forma nativa para evitar SQL Injections, y garantizando el cierre de conexiones (Limpieza de recursos).

```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    # 1. Establecemos la conexión por red al clúster RDS (Puerto 5432)
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port="5432" 
    )
    
    # 2. Creamos un cursor temporal
    cur = conn.cursor()
    
    # 3. Ejecutamos la consulta usando PARÁMETROS SEGUROS (%s)
    dragon_id_buscado = 42
    query = "SELECT nivel_inestabilidad FROM dragones_salud WHERE dragon_id = %s;"
    
    # psycopg2 sanitiza automáticamente la tupla de parámetros
    cur.execute(query, (dragon_id_buscado,))
    
    # 4. Obtenemos el resultado
    registro = cur.fetchone()
    print(f"✅ Inestabilidad Nivel: {registro[0]}")

except Exception as e:
    print(f"❌ Error RDS: {e}")
finally:
    # 5. Siempre cerrar, sin importar si hubo error, para evitar conexiones zombie.
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
```

*Zero Surprise Syntax:*
- `psycopg2.connect(...)`: Abre un túnel de red TCP hacia RDS y retorna una conexión activa.
- `conn.cursor()`: Un "cursor" es una estructura de control; el cartero que lleva instrucciones SQL y vuelve con respuestas.
- `cur.execute(query, (param,))`: Ejecuta el string SQL delegando a `psycopg2` la sanitización para evitar *SQL Injections*.
- `cur.fetchone()`: Trae un único registro (la primera fila) resultado de la base de datos a Python, en forma de tupla.

## 4. Conexión con Testing (Test-Driven Lore)

Mockear una base de datos relacional es un poco más anidado porque los objetos interactúan en cadena: Te conectas (`psycopg2.connect`), lo que te devuelve la Conexión, la cual te devuelve un Cursor, el cual te devuelve tu Resultado.

Para probar un script sin usar una BD real, usamos `MagicMock` encadenados:

```python
from unittest.mock import patch, MagicMock

@patch('my_solution.psycopg2.connect')
def test_consulta(mock_connect):
    # Simulamos el objeto de conexión
    mock_conn = MagicMock()
    # Simulamos el objeto de cursor
    mock_cur = MagicMock()
    
    # Enlazamos: cuando llamen a connect(), que retorne mock_conn
    mock_connect.return_value = mock_conn
    # Cuando llamen a conn.cursor(), que retorne mock_cur
    mock_conn.cursor.return_value = mock_cur
    
    # Finalmente simulamos los datos reales que fetchone() debe retornar (una tupla)
    mock_cur.fetchone.return_value = (89,)
```

## 5. Mapa de Ejercicios

Ingresa a `quests/02-aws-rds/` y practica la creación de túneles DBAPI cerrando herméticamente tus recursos para evitar *leaks* de memoria.
