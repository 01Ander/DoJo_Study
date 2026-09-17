# Capítulo 04: Carga de Datos a Bases Relacionales (SQLAlchemy)

> 🎯 **Objetivo de Negocio:** El inventario de pociones en la Zona Gold está listo. Ahora necesitamos guardarlo de forma permanente y segura en el Gran Archivo del Gremio (nuestra base de datos PostgreSQL) para que los maestros puedan consultarlo con SQL.

Para hablar con bases de datos relacionales desde Python, usamos una librería llamada **SQLAlchemy**. Esta actúa como un puente mágico (ORM y DBAPI) entre el código Python y el motor de la base de datos.

## 1. Instalación y Connection Strings

*Zero Assumption Setup:* Necesitas instalar sqlalchemy. Si estuviéramos conectándonos a Postgres de verdad, necesitarías `psycopg2-binary`. Para este laboratorio usaremos SQLite (incluido en Python), así que solo necesitas SQLAlchemy.
```bash
pip install sqlalchemy
```

**Analogía (El Portal de Teletransporte):**
Para mandar objetos de tu laboratorio al Gran Archivo, primero debes "dibujar" las runas de conexión del portal. A esto se le llama **Connection String**. Tiene el formato: `motor://usuario:contraseña@servidor/base_de_datos`.

## 2. El Engine y la Carga de Datos

Pandas tiene un método mágico llamado `to_sql()` que toma un DataFrame entero y lo inserta en la base de datos de un solo golpe.

### Ejemplo Progresivo: Carga a Base de Datos

**El Mal Camino (SQL concatenado - Vulnerable y Lento):**
```python
# 🎯 Objective: Save potions to the database
def load_potions_bad(gold_data, db_conn):
    # Doing inserts one by one writing SQL by hand is prone 
    # to SQL injection and takes too long.
    for potion, amount in gold_data.items():
        sql = f"INSERT INTO inventory VALUES ('{potion}', {amount})"
        db_conn.execute(sql)
```

**El Buen Camino (Pandas + SQLAlchemy):**
```python
import pandas as pd
from sqlalchemy import create_engine

def load_potions_good(df_gold: pd.DataFrame):
    # 1. Dibujamos el portal (Engine). 
    # Aquí usamos sqlite en memoria por simplicidad, pero para 
    # Postgres sería algo como: 'postgresql://user:pass@localhost:5432/mydb'
    db_engine = create_engine('sqlite:///:memory:')
    
    # 2. Pasamos el cargamento a través del portal
    # df_gold viaja completo hacia la tabla 'potion_inventory'
    df_gold.to_sql(
        name='potion_inventory',
        con=db_engine,
        if_exists='append',
        index=False
    )
```

> **Explicación de Sintaxis:**
> - `create_engine(url)`: Esta función no se conecta inmediatamente, solo prepara la maquinaria y las reglas para conectarse cuando sea necesario (crea el pool de conexiones).
> - `df.to_sql(...)`: 
>   - `name`: El nombre de la tabla en la base de datos.
>   - `con`: El motor (engine) que acabamos de crear.
>   - `if_exists='append'`: ¿Qué hacemos si la tabla ya existe? `append` agrega las filas nuevas al final de la tabla. Otras opciones son `fail` (explotar) o `replace` (borrar tabla y crearla de nuevo).
>   - `index=False`: Le dice a Pandas que no guarde el número de fila (el índice 0, 1, 2...) como una columna extra en la base de datos, solo nos interesan los datos reales.

## 3. Consultas Crudas (Testing con SQLAlchemy Core)

En nuestros tests, a veces necesitamos verificar si Pandas de verdad insertó los datos. Para hacer consultas SQL crudas directamente al motor, SQLAlchemy provee métodos de bajo nivel:
- `text("SELECT * FROM tabla")`: Envuelve tu string SQL plano en una estructura segura de SQLAlchemy.
- `with engine.connect() as conn:`: Abre una conexión viva con la base de datos y la cierra automáticamente al terminar el bloque `with`.
- `conn.execute(sql)`: Envía el comando SQL al servidor.
- `.fetchall()`: Toma el resultado de `execute` y te devuelve todas las filas encontradas como una lista de tuplas.

**Ejemplo: Verificar datos insertados**
```python
from sqlalchemy import text

# Después de haber cargado datos con to_sql()...
with db_engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM potion_inventory")).fetchall()
    print(result)  # [(Invisibility, 10), (Healing, 25)]
```

---

## Misión a seguir
El inventario está auditado y listo. Ve a `quests/04-carga-postgresql/` y diseña la función para teletransportar el DataFrame a la base de datos.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar carga masiva con to_sql` o `feat(quests): cargar datos gold a postgresql`.
