# Capítulo 05: Orquestación Local de Flujos (Prefect)

> 🎯 **Objetivo de Negocio:** Ya tenemos el código para extraer (Cap 01), limpiar (Cap 02), auditar (Cap 03) y guardar (Cap 04). Pero si un alquimista novato tiene que ejecutar el script manualmente todos los días a las 3:00 AM, eventualmente se quedará dormido. Necesitamos al Gran Maestro Alquimista (Orquestador) que dirija el proceso a nivel macro y nos avise si algo falla.

En el mercado laboral, a esto se le llama **Orquestación de Pipelines**. Usaremos **Prefect**, una herramienta moderna construida nativamente en Python.

## 1. El Gran Maestro y sus Ayudantes

*Zero Assumption Setup:* Necesitamos instalar prefect en nuestro entorno.
```bash
pip install prefect
```

**Analogía (El Laboratorio Central):**
Imagina que las funciones de Python que hiciste antes son pequeños ayudantes mágicos (homúnculos). Por sí solos no hacen mucho. Prefect es el Gran Maestro Alquimista. Toma a los ayudantes y les asigna tareas específicas (Tasks). Luego, coordina a todos los ayudantes en un mecanismo principal llamado Flujo (Flow). Si un ayudante tropieza y derrama un vial, el Gran Maestro lo sabe y puede ordenarle intentarlo de nuevo (Retries).

## 2. Decoradores: La Magia de Prefect

En Python, un decorador (el símbolo `@` arriba de una función) es una forma de inyectarle superpoderes a tu función sin cambiar su código interno (conceptos vistos en `PY-POO`).

Prefect usa dos decoradores principales:
- `@task`: Convierte una función normal en un "Ayudante Mágico" observable. Prefect registrará cuánto tarda en ejecutarse y si falló.
- `@flow`: Convierte una función en el "Flujo". Un Flow es el Gran Maestro que manda a llamar a las Tasks.

### Ejemplo Progresivo: El Orquestador Mágico

**El Mal Camino (Script secuencial ciego):**
```python
import time

def get_dust():
    # Si esto falla por un error de red temporal, todo el programa explota 
    # y hay que despertarse a correrlo de nuevo a mano.
    time.sleep(1)
    return "Polvo recolectado"

def potion_master():
    print("Iniciando trabajo...")
    p = get_dust()
    print(f"Terminado: {p}")

# Ejecución ciega
potion_master()
```

**El Buen Camino (Prefect Flow con Retries):**
```python
import time
from prefect import task, flow

# Le damos el superpoder de reintentar hasta 3 veces si hay un error
@task(retries=3, retry_delay_seconds=2)
def get_dust():
    print("Intentando conseguir polvo...")
    # Simulamos un error de red aleatorio
    if int(time.time()) % 2 == 0:
        raise ConnectionError("El mensajero tropezó. Reintentando...")
    return "Polvo recolectado"

# Este es el mecanismo principal
@flow(name="Daily_Potion_Logistics")
def potion_master():
    print("El Gran Maestro Alquimista inicia su turno.")
    p = get_dust() # Llama a la tarea
    print(f"Reporte Final: {p}")

# Ejecución observada
if __name__ == "__main__":
    potion_master()
```

> **Explicación de Sintaxis:**
> - `from prefect import task, flow`: Importamos los decoradores mágicos de Prefect.
> - `@task(retries=3, retry_delay_seconds=2)`: Le decimos a Prefect: "Si esta función lanza un error, no mates el programa. Espera 2 segundos y vuelve a ejecutarla. Ríndete solo si falla 3 veces seguidas".
> - `@flow(name="...")`: Define el punto de entrada principal. Cuando ejecutes este script en tu terminal, verás unos hermosos logs de colores indicando el estado de cada tarea.

## 3. Dependencias y Grafos (DAGs)

Un pipeline rara vez es una sola tarea. Normalmente tienes múltiples pasos: extraer, limpiar, cargar. Estas tareas tienen **dependencias**: no puedes limpiar si la extracción falló.

En orquestación, a esto se le llama un **DAG** (Directed Acyclic Graph - Grafo Acíclico Dirigido). Es una secuencia de tareas donde el flujo viaja en una sola dirección.

En Prefect, las dependencias se crean de forma natural (implícita) simplemente pasando el resultado de una `@task` como parámetro a la siguiente `@task` dentro del `@flow`.

**Ejemplo de DAG (Tareas Dependientes):**
```python
@task(retries=3)
def get_dust():
    return ["polvo", "tierra"]

@task
def clean_dust(raw_data):
    # Esta tarea depende de que get_dust() termine exitosamente y le pase raw_data
    return [item for item in raw_data if item != "tierra"]

@flow(name="Refinery_Pipeline")
def potion_master():
    # El Grafo se construye automáticamente por el paso de datos:
    raw = get_dust()        # Tarea A
    clean = clean_dust(raw) # Tarea B (depende de A)
    print(f"Resultado final: {clean}")
```

**¿Por qué esto mejora la resiliencia?**
Si `get_dust()` falla (y agota sus 3 reintentos), el orquestador marcará la tarea como fallida, y **automáticamente cancelará** `clean_dust()` porque depende de ella. Así evitas que la segunda tarea intente procesar datos que no existen (evitando errores crípticos más adelante).

**Analogía:** El Gran Maestro no envía al Herbolario a limpiar raíces hasta que el Mensajero haya regresado del bosque con ellas. Si el Mensajero se pierde, la orden del Herbolario se cancela automáticamente.

---

## Misión a seguir
Es hora de ensamblar todas las piezas de la Chronicle. Ve a `quests/05-orquestacion-prefect/` y agrégale superpoderes a tus funciones usando los decoradores de Prefect.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar orquestacion con prefect` o `feat(quests): orquestar pipeline final con flows y tasks`.
