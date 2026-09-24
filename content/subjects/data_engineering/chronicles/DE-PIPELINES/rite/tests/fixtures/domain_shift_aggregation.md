# Domain Shifting: agregar una lista de registros a un DataFrame agrupado

**Dominio prestado:** la armería de un herrero. Nada de ingredientes, nada de pociones.
**Qué se hace:** recibir una lista de dicts (un conteo de inventario) y devolver un DataFrame
con el total agrupado por arma.

Este archivo es de referencia temporal: capturá la **estructura**, no las palabras. Se borra
cuando termines.

---

## La entrada (lo que recibís)

```python
[
    {"weapon": "shortsword", "units": 40},
    {"weapon": "shortsword", "units": 15},
    {"weapon": "halberd", "units": 7},
    {"weapon": "buckler", "units": 22},
]
```

## La salida (lo que devolvés)

```
       weapon  total_units
0     buckler           22
1     halberd            7
2  shortsword           55
```

Y como dicts, que es lo que ven tus asserts:

```python
[{'weapon': 'buckler', 'total_units': 22},
 {'weapon': 'halberd', 'total_units': 7},
 {'weapon': 'shortsword', 'total_units': 55}]
```

## La estructura completa (verificada con Python 3.14 y pandas 3.0)

```python
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_armory_stock(counters: list[dict]) -> pd.DataFrame:
    """Group a list of records by weapon and sum the units."""
    logger.info("counters received: %d", len(counters))

    armory_df = pd.DataFrame(counters)
    totals_df = armory_df.groupby("weapon", as_index=False)["units"].sum()
    totals_df = totals_df.rename(columns={"units": "total_units"})

    logger.info("weapon groups produced: %d", len(totals_df))
    return totals_df
```

## Qué mirar (y qué no copiar)

1. **La lista de dicts entra directa al DataFrame.** Las llaves se vuelven columnas solas.
2. **`groupby("weapon", as_index=False)`**: el segundo argumento evita que la clave quede como
   índice, así sobrevive como columna. Sin él, tu `to_dict("records")` no vería la clave.
3. **`["units"].sum()`**: el corchete elige la columna, y `sum()` es lo que efectivamente agrega.
4. **`rename(columns={...})`**: le da al resultado un nombre distinto del original, para que
   nadie confunda la cantidad de una fila con el total agrupado.
5. **Los dos `logger.info`** con formato diferido (`%d`) y el conteo como argumento aparte.
6. **Se devuelve el DataFrame**, no una lista de dicts: eso lo decide el consumidor (`to_sql`).
7. **El orden de las filas sale alfabético por la clave** y no lo elegís vos: el `groupby`
   ordena. No armes un test que dependa de ese orden.

## Mapeo a tu dominio

| Armería | Tu Rite |
|---|---|
| `counters` | los registros de Silver (`list[dict]`) |
| `weapon` | `name` |
| `units` | `stock` |
| `total_units` | `total_stock` |
| `armory_df` | el DataFrame reconstruido desde Silver |
| `aggregate_armory_stock` | `aggregate_silver_market` |
