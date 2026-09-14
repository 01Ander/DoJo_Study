# Capítulo 03: Data Quality y Observabilidad

> 🎯 **Objetivo de Negocio:** Antes de que las pociones lleguen a las estanterías de las tiendas, el Gremio exige certificaciones de calidad. Si una poción de invisibilidad dice "100 ml" y trae "None", el cliente podría quedar semi-visible, lo cual atrae demandas. Debemos aplicar Data Quality (DQ).

## 1. La Balanza del Alquimista (Reconciliación)

En el mundo de los datos, la materia no se crea ni se destruuye, solo se transforma. Si el mensajero trajo 100 frascos de la Zona Bronze, y en la Zona Silver limpiamos 5 venenosos, deben quedar 95. Si hay 94, perdimos un frasco por un bug.

Esto se llama **Row Count Check** o reconciliación pre/post carga.

**Analogía (El guardia de la bóveda):**
El guardia cuenta los cofres que entran. Si el número no cuadra con el manifiesto de envío, detiene la caravana entera. En código, hacemos que el programa se detenga si la validación falla usando `assert` o lanzando una excepción.

### Ejemplo Progresivo: Quality Gates

**El Mal Camino (Esperar a que alguien se queje):**
```python
def move_to_gold_bad(silver_data):
    # Aquí podríamos perder datos silenciosamente por un bug en el código
    gold = silver_data[silver_data['amount'] > 0] 
    return gold
```

**El Buen Camino (Quality Gates Explícitos):**
```python
def move_to_gold(silver_data):
    initial_count = len(silver_data)
    
    # Bug simulado: la lógica pierde datos
    gold = silver_data[silver_data['amount'] > 0] 
    final_count = len(gold)
    
    # 1. Gate de Reconciliación: Esperamos no perder más del 10% de registros
    # por limpieza. Si se pierde más, algo catastrófico ocurrió.
    loss_rate = (initial_count - final_count) / initial_count
    assert loss_rate < 0.1, f"🚨 Data Quality Fallida: Se perdió el {loss_rate*100}% de los datos."
    
    # 2. Gate de Esquema (Null Checks)
    assert gold['amount'].notnull().all(), "🚨 Data Quality Fallida: Hay nulos en la cantidad"
    
    return gold
```

> **Explicación de Sintaxis:**
> - `assert condicion, "Mensaje"`: Evalúa la `condición`. Si es Verdadera, no pasa nada y el programa continúa. Si es Falsa, lanza un `AssertionError` con el "Mensaje" e interrumpe el pipeline inmediatamente. ¡Mejor fallar rápido que guardar datos corruptos!
> - `gold['amount'].notnull()`: Pandas revisa cada fila y devuelve True si no es nula.
> - `.all()`: Revisa si TODOS los valores resultantes de la comprobación anterior son True. Si uno solo es False, devuelve False.

## 2. Prevención de Duplicados

A veces el mensajero del Mercado Negro pasa dos veces el mismo recibo. Para evitar pagar doble, eliminamos los duplicados basándonos en una llave única.

```python
# Elimina filas repetidas basándose solo en el nombre del ingrediente.
# keep='first' significa que se queda con el primero que vio y borra los demás.
df = df.drop_duplicates(subset=['name'], keep='first')
```

Y si solo quisieras saber cuántos ingredientes distintos existen, podrías usar `unique()`, el cual te devuelve una lista de los valores únicos en esa columna, descartando repetidos visualmente:
```python
unique_names = df['name'].unique()
```

---

## Misión a seguir
El Gran Maestro sospecha que hay pociones duplicadas y mermas irregulares. Ve a `quests/03-data-quality/` y construye los portones de calidad para auditar el inventario.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar reconciliacion y dq` o `feat(quests): aplicar gates de calidad en zona silver`.
