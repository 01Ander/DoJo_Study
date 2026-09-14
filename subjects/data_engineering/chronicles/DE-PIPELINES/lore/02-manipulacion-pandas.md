# Capítulo 02: Manipulación y Limpieza con Pandas

> 🎯 **Objetivo de Negocio:** El mensajero nos trajo el catálogo del Mercado Negro en crudo (Zona Bronze). Está lleno de suciedad, valores nulos porque los duendes que registran el inventario son perezosos, y nombres mal escritos. Necesitamos transformar esto en un inventario limpio (Zona Silver) listo para análisis.

Podríamos usar diccionarios y bucles `for` nativos en Python. Pero cuando el Gremio maneja millones de viales de pociones, un bucle `for` tardará semanas en terminar. Aquí entra **Pandas**.

## 1. ¿Qué es Pandas?

**Analogía (El Gran Libro de Contabilidad):**
Imagina un libro contable mágico gigante. En lugar de leer línea por línea para tachar los errores (como harías con un bucle `for`), lanzas un hechizo sobre toda la columna "Nombres" a la vez, y en un parpadeo, todos los nombres se corrigen.

Ese libro contable mágico es el **DataFrame**, y los hechizos masivos son las operaciones vectorizadas de Pandas.

*Zero Assumption Setup:* Instala Pandas en tu entorno:
```bash
pip install pandas
```

## 2. El Hechizo Vectorizado (Ejemplo Progresivo)

Tenemos una lista de ingredientes crudos. Note que hay nulos (`None`) y textos en mayúsculas desordenadas.

**El Mal Camino (Bucles nativos - Lento y verboso):**
```python
bronze_ingredients = [
    {"id": 1, "name": "  Ojo de TRITÓN", "price": 150},
    {"id": 2, "name": None, "price": 300},
    {"id": 3, "name": "Roca de TROLL  ", "price": None}
]

# 🎯 Objetivo: Quitar nulos y poner nombres en minúscula sin espacios.
def clean_native(data):
    silver = []
    for row in data:
        if row["name"] is not None and row["price"] is not None:
            clean_row = {
                "id": row["id"],
                "name": row["name"].strip().lower(),
                "price": row["price"]
            }
            silver.append(clean_row)
    return silver
```

**El Buen Camino (Pandas - Vectorizado y limpio):**
```python
import pandas as pd

def clean_with_pandas(data: list) -> pd.DataFrame:
    # 1. Invocamos el Libro Contable (DataFrame)
    df = pd.DataFrame(data)
    
    # 2. Hechizo de Purificación: Eliminar cualquier fila con vacíos
    df = df.dropna()
    
    # 3. Hechizo de Transmutación: Todo a minúscula y sin espacios en los bordes
    df['name'] = df['name'].str.strip().str.lower()
    
    return df
```

> **Explicación de Sintaxis:**
> - `pd.DataFrame(data)`: Toma una lista de diccionarios y la convierte en una tabla estructurada bidimensional (filas y columnas).
> - `df.dropna()`: Un método ultra-rápido que escanea toda la tabla y elimina completamente cualquier fila que contenga al menos un valor nulo (`NaN` o `None`). Devuelve una tabla nueva limpia.
> - `df['name'].str.strip()`: `.str` es el "accesorio mágico" que le dice a Pandas: *"Trata toda esta columna como si fueran strings y aplícales la función de Python `strip()` a todos al mismo tiempo"*.

## 3. Tipado Estricto (Casteo)

En el Mercado Negro, a veces te entregan el precio como texto `"150"` en lugar de número `150`. Si intentas sumar eso luego en la Zona Gold, Python fallará.

Para forzar el tipo correcto en todo el libro de contabilidad usamos `astype()`:

```python
# Forzar a que la columna price sea un número entero
df['price'] = df['price'].astype(int)
```

## 4. Del Libro Contable a la Lista (Retorno de Datos)

Si necesitas exportar de nuevo el DataFrame a una lista estándar de diccionarios de Python (ej. para otra función que no sabe usar Pandas), usas:
```python
clean_data = df.to_dict(orient='records')
```
El parámetro `orient='records'` asegura que el resultado sea una lista donde cada elemento es un diccionario representando una fila, idéntico al formato original.

---

## Misión a seguir
El mensajero dejó la carga en la bóveda cruda. Abre `quests/02-manipulacion-pandas/` y usa tus primeros hechizos de Pandas para mover el inventario a la Zona Silver.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar manipulacion vectorizada con pandas` o `feat(quests): limpiar inventario bronze`.
