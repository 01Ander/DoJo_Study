# Capítulo 02: Amazon RDS (Relational Database Service)

S3 es perfecto para guardar millones de archivos crudos y masivos a muy bajo costo, pero no es una base de datos relacional; no puedes hacer consultas `JOIN` de manera nativa. Para esto, usamos **Amazon RDS**.

## 1. Bases de Datos Administradas

**QUÉ es:** Amazon RDS (*Relational Database Service*) es un servicio que aprovisiona, escala y opera bases de datos relacionales (PostgreSQL, MySQL) en la nube de forma **administrada**.
**POR QUÉ importa:** Instalar PostgreSQL manualmente en un servidor alquilado implica que tú debes encargarte de instalar Linux, programar los backups diarios y aplicar parches de seguridad de madrugada. RDS asume toda esa "carga operativa pesada". Te permite pedir simplemente: "Dame un Postgres versión 15", liberándote para enfocarte en modelar datos y crear pipelines de valor para el negocio.

*Analogía del Gremio:* Una base auto-administrada es como criar ovejas, esquilar e hilar la lana para tejer un traje ignífugo antes de poder acercarte a un dragón. RDS es ir al sastre del gremio y decir: "Dame un traje talla M"; AWS hace todo el trabajo sucio.

## 2. Seguridad de Red (Security Groups)

**QUÉ es:** Un *Security Group* es un firewall (cortafuegos) virtual que controla qué tráfico entra (Inbound) y sale (Outbound) de tu base de datos en AWS.
**POR QUÉ importa:** Si dejas la red de tu base de datos abierta al mundo entero (lo que se conoce técnicamente como permitir la ruta `0.0.0.0/0`), bots rusos y chinos atacarán el puerto 5432 intentando adivinar tu contraseña 24 horas al día. Las bases de datos *siempre* deben estar bloqueadas por defecto, abriendo el puerto únicamente para las IPs privadas de tus Lambdas o la IP de tu oficina.

## 3. DBAPI y Prevención de Inyecciones

**QUÉ es:** Para conectarnos a bases de datos relacionales desde Python, usamos librerías que implementan el estándar DBAPI, como `psycopg2`. La forma en que inyectamos valores (como un ID) dentro del código SQL marca la diferencia entre un código seguro y un desastre de seguridad.
**POR QUÉ importa:** Nunca debes concatenar strings (como *F-strings*) para construir SQL. Si lo haces, estás expuesto a un ataque de **SQL Injection**, donde un usuario malicioso manda código SQL oculto dentro de un campo de texto para borrar tus tablas. DBAPI soluciona esto obligándote a parametrizar tus consultas (usando `%s`), delegando al driver la limpieza (*sanitización*) del texto antes de que toque la base.

## 4. Setup Inicial (Zero Assumption)

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

## 5. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Consultar un nivel de salud específico del dragón filtrando por su ID.

Si concatenamos los valores usando F-strings directos:

```python
import psycopg2

dragon_id = 42 # Este valor podría venir de una API o del usuario
query = f"SELECT nivel FROM dragones_salud WHERE dragon_id = {dragon_id};"

# DANGER: If dragon_id is "42; DROP TABLE dragons_health;", 
# it would delete the entire database (SQL Injection attack).
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Consultar un registro parametrizándolo de forma nativa para evitar SQL Injections, y garantizando el cierre de conexiones (Limpieza de recursos).

```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    # 1. Establish network connection to RDS cluster (Port 5432)
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port="5432" 
    )
    
    # 2. Create temporary cursor
    cur = conn.cursor()
    
    # 3. Execute query using SAFE PARAMETERS (%s)
    target_dragon_id = 42
    query = "SELECT instability_level FROM dragons_health WHERE dragon_id = %s;"
    
    # psycopg2 automatically sanitizes parameter tuple
    cur.execute(query, (target_dragon_id,))
    
    # 4. Fetch result
    record = cur.fetchone()
    print(f"✅ Instability level: {record[0]}")

except Exception as e:
    print(f"❌ RDS Error: {e}")
finally:
    # 5. Always close connection to avoid zombie connections
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

---

## 5.1 Gestión de Credenciales con AWS Secrets Manager y KMS (`MKT-AWS-002`)

En producción dentro de AWS, ni siquiera escribimos contraseñas de base de datos en variables de entorno planas: las almacenamos cifradas con llaves **AWS KMS (*Key Management Service*)** dentro de **AWS Secrets Manager**.

Cuando tu pipeline arranca, solicita el secreto por su identificador (`SecretId`), AWS KMS lo descifra al vuelo en memoria y `get_secret_value()` te devuelve el JSON de credenciales en el campo `"SecretString"`. Con ese diccionario podemos instanciar directamente nuestra clase `DatabaseConfig` (el mismo patrón que construiste en `M1`):

```python
import json
from dataclasses import dataclass
from typing import Any

# 🎯 Objetivo de Negocio: Recuperar credenciales de RDS desde Secrets Manager sin hardcoding.

@dataclass
class RDSConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    driver: str = "postgresql+psycopg2"

    def get_uri(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

def load_rds_config_from_secrets(secrets_client: Any, secret_id: str) -> RDSConfig:
    # 1. Consultar el secreto cifrado en AWS Secrets Manager
    response = secrets_client.get_secret_value(SecretId=secret_id)
    
    # 2. Parsear el JSON contenido en 'SecretString'
    secret_payload = json.loads(response["SecretString"])
    
    return RDSConfig(
        host=secret_payload["host"],
        port=int(secret_payload.get("port", 5432)),
        database=secret_payload["dbname"],
        username=secret_payload["username"],
        password=secret_payload["password"],
    )
```

---

## 5.2 Reglas de Red Administradas en Security Groups (`AWS-007`)

Para que el worker pueda conectarse al puerto `5432` de RDS sin abrir la base de datos a todo internet (`0.0.0.0/0`), configuramos una regla de entrada (*Ingress Rule*) en el **Security Group** usando `ec2_client.authorize_security_group_ingress(...)`, exigiendo siempre un bloque CIDR privado (por ejemplo, `10.0.0.0/16`):

```python
from typing import Any

# 🎯 Objetivo de Negocio: Autorizar tráfico TCP al puerto 5432 de RDS bloqueando 0.0.0.0/0.

def authorize_rds_ingress(ec2_client: Any, group_id: str, cidr_ip: str) -> dict[str, Any]:
    if cidr_ip == "0.0.0.0/0":
        raise ValueError("Violación de seguridad: Prohibido abrir el puerto 5432 de RDS a 0.0.0.0/0")
    
    return ec2_client.authorize_security_group_ingress(
        GroupId=group_id,
        IpProtocol="tcp",
        FromPort=5432,
        ToPort=5432,
        CidrIp=cidr_ip,
    )
```

> **Zero Surprise Syntax:**
> * **`secrets_client.get_secret_value(SecretId=...)`:** Retorna un diccionario cuya llave `"SecretString"` contiene el JSON de credenciales en formato texto (`str`).
> * **`ec2_client.authorize_security_group_ingress(...)`:** En AWS, los Security Groups pertenecen a la capa de red VPC/EC2, por lo que se administran con `boto3.client('ec2')` especificando protocolo (`"tcp"`), rango de puertos (`5432` a `5432`) y rango IP autorizado (`CidrIp`).

## 6. Conexión con Testing (Test-Driven Lore)

- **`MagicMock` encadenados:** Conectas (`psycopg2.connect`), lo que devuelve la Conexión (`mock_conn`), la cual devuelve un Cursor (`mock_cur`), el cual retorna tu Resultado (`mock_cur.fetchone.return_value`).
- **Verificar limpieza con `mock_conn.close.assert_called_once()`:** En bases de datos es vital probar que `conn.close()` se ejecuta **siempre**, incluso si `cur.execute()` explota con una excepción (bloque `finally`). Forzamos ese error asignando una excepción a `mock_cur.execute.side_effect`.

```python
from unittest.mock import patch, MagicMock

# 1. Success Case Test
@patch('my_solution.psycopg2.connect')
def test_query_success(mock_connect):
    # Mock chained connection and cursor objects
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Mock data returned by fetchone() (tuple)
    mock_cur.fetchone.return_value = (89,)
    
    # Act: Execute real function
    from my_solution import check_status
    level = check_status(42)
    
    # Assert: Verify value and resource cleanup
    assert level == 89
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

# 2. Error and Connection Cleanup Test
@patch('my_solution.psycopg2.connect')
def test_query_error_cleanup(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Force a database exception during execute using side_effect
    mock_cur.execute.side_effect = Exception("Relation dragons_health does not exist")
    
    from my_solution import check_status
    level = check_status(99)
    
    # Assert: Must return None on error, but MUST have closed connection
    assert level is None
    mock_conn.close.assert_called_once()
```

## 7. Mapa de Ejercicios

Ingresa a `quests/02-aws-rds/` y practica la creación de túneles DBAPI cerrando herméticamente tus recursos para evitar *leaks* de memoria.
