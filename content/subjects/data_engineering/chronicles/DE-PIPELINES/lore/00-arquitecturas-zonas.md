# Capítulo 00: Arquitecturas de Ingesta y Zonas de Datos

Bienvenido al Gremio de Alquimistas. Antes de que podamos automatizar la logística y distribución de pociones mágicas y artefactos arcanos en todo el continente, necesitamos entender **cómo** y **dónde** almacenamos nuestros ingredientes.

> 🎯 **Objetivo de Negocio:** Diseñar un flujo de trabajo que permita tomar ingredientes inestables recolectados por mercenarios (Raw Data), purificarlos de maldiciones (Clean Data), y finalmente combinarlos para reportar el stock de pociones listas para la venta (Curated Data).

## 1. ETL vs ELT: Dos caminos para la Alquimia

Existen dos arquitecturas principales para mover y procesar información (o ingredientes).

### ETL (Extract, Transform, Load)
Extraemos, Transformamos (en memoria o servidores de procesamiento intermedio) y finalmente Cargamos el resultado en la base de datos final.

**Analogía 1 (El Caldero Viajero):** 
Envías a un alquimista al bosque. Él extrae (Extract) las raíces, las hierve y limpia allí mismo en su campamento (Transform), y solo trae a la bóveda del gremio la poción terminada lista para usar (Load).
*Ventaja:* Ahorras espacio en la bóveda, solo guardas lo útil.
*Desventaja:* Si la receta cambia en el futuro, no tienes las raíces originales para volver a hacerla de otra forma.

### ELT (Extract, Load, Transform)
Extraemos, Cargamos todo el material crudo directamente al almacén final, y luego usamos el poder de ese mismo almacén para Transformar.

**Analogía 2 (La Bóveda Masiva):** 
Envías carros enteros al bosque. Extraen (Extract) raíces con tierra, ramas e insectos, y vuelcan todo directamente en un ala gigante de la bóveda del Gremio (Load). Luego, usando la maquinaria masiva de la bóveda, se limpia y prepara el inventario (Transform).
*Ventaja:* Tienes un historial completo; si te equivocaste en la poción, las raíces originales siguen guardadas. Es el estándar moderno gracias a los Data Warehouses baratos en la nube.
*Desventaja:* Requiere mucho más espacio de almacenamiento.

### Ejemplo Progresivo (Código Base)

Veamos cómo se vería esto en código Python puro, simulando un ETL simple.

**El Mal Camino (Todo acoplado):**
```python
# 🎯 Objetivo: Traer ingredientes, limpiar los venenosos y guardar.
def process_ingredients_bad_way(raw_ingredients):
    # Todo ocurre al mismo tiempo, difícil de testear y auditar
    vault = []
    for item in raw_ingredients:
        if "venenoso" not in item:
            clean_item = item.strip().lower()
            vault.append(clean_item)
    return vault
```

**El Buen Camino (Desacoplado):**
```python
def extract_ingredients():
    return [" Raíz Curativa ", "Hongo Venenoso", "  ESCAMA de DRAGÓN "]

def transform_ingredients(raw_data):
    # Solo transformamos
    clean_data = []
    for item in raw_data:
        if "venenoso" not in item.lower():
            clean_data.append(item.strip().lower())
    return clean_data

def load_to_vault(clean_data, vault):
    # Solo cargamos
    vault.extend(clean_data)
    return vault

# Flujo ETL Claro:
raw = extract_ingredients()
transformed = transform_ingredients(raw)
final_vault = load_to_vault(transformed, [])
```

> **Explicación de Sintaxis:**
> - `vault.extend(clean_data)`: A diferencia de `append` que agrega un solo elemento (y si le pasas una lista, agrega la lista como un único elemento), `extend` toma un iterable y añade cada uno de sus elementos al final de la lista objetivo. Lo usamos aquí porque `clean_data` ya es una lista de elementos.
> - `@pytest.fixture`: (Recordatorio de `PY-POO`) Un decorador que marca una función para que provea datos de prueba reutilizables a tus tests.

---

## 2. Las Zonas de Datos (Data Lakehouse)

Cuando usamos ELT (o arquitecturas modernas), necesitamos organizar el "caos" de volcar todo crudo. Para ello usamos Zonas (también llamadas arquitectura Medallion).

### Zona Bronze (Raw / Crudo)
Es el patio de carga. Aquí los ingredientes llegan tal cual fueron extraídos. Con barro, errores, y formatos extraños.
**Regla de Oro:** La zona Bronze es INMUTABLE. Nunca modificas ni limpias los datos aquí; solo los guardas tal como llegaron como evidencia histórica.

### Zona Silver (Cleaned / Limpio)
El laboratorio de purificación. Aquí los ingredientes ya no tienen barro. 
**Regla de Oro:** Se filtran valores nulos, se estandarizan nombres (ej. todo en minúsculas), se quitan duplicados. Sigue siendo un dato atómico, pero estandarizado.

### Zona Gold (Curated / Curado)
El catálogo de ventas. Aquí ya no hay raíces ni escamas individuales, hay agregaciones (sumas, promedios) listas para consumo de negocio.
**Regla de Oro:** Los datos aquí responden preguntas directas (ej. "Stock total de pociones de curación en Ankh-Morpork por mes").

---

## 3. Evolución Moderna del Stack de Datos (ELT, Columnar y Procesamiento Distribuido)

En los sistemas de producción actuales, las zonas Medallion (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) se apoyan en tres tecnologías clave que escucharás en toda entrevista técnica:

### 3.1 Transformación Declarativa en ELT con `dbt` (Data Build Tool)
Cuando adoptamos **ELT** y cargamos los datos crudos directamente en la base de datos o Data Warehouse, ya no necesitamos extraer millones de filas a la memoria de Python para transformarlas. En su lugar, ejecutamos las transformaciones **dentro del motor SQL** usando **`dbt`**:

* **Qué es `dbt`:** Un framework que convierte consultas `SELECT` modulares (archivos `.sql` dentro de una carpeta `models/`) en tablas o vistas materializadas automáticamente siguiendo el orden de dependencias.
* **Primitivas clave:**
  * `{{ source('raw_guild', 'potions_raw') }}`: Declara la tabla cruda de entrada (Zona Bronze).
  * `{{ ref('stg_potions_cleaned') }}`: Referencia otro modelo de `dbt`, construyendo el grafo de linaje automáticamente entre Zona Silver y Zona Gold.
  * **Tests Declarativos (`schema.yml`):** Permite declarar reglas de calidad como `not_null` y `unique` sobre las columnas sin escribir código imperativo.

```sql
-- Ejemplo conceptual de un modelo Gold en dbt: models/gold_alchemist_sales.sql
{{ config(materialized='table') }}

SELECT
    potion_category,
    COUNT(order_id) AS total_orders,
    SUM(gold_coins) AS total_revenue
FROM {{ ref('silver_potion_orders') }}
GROUP BY potion_category
```

### 3.2 Motores Orientados a Filas (OLTP) vs. Orientados a Columnas (OLAP)
¿Dónde guardamos la Zona Gold cuando el volumen crece de miles a cientos de millones de registros?

| Característica | Base Relacional por Filas (OLTP)<br>*(PostgreSQL, RDS)* | Almacenamiento Columnar (OLAP)<br>*(Parquet, DuckDB, Snowflake, BigQuery)* |
|---|---|---|
| **Cómo guarda en disco** | Guarda cada fila completa contigua: `[id1, nombre1, precio1], [id2, nombre2, precio2]` | Guarda cada columna completa contigua: `[id1, id2...], [nombre1, nombre2...], [precio1, precio2...]` |
| **Patrón ideal** | Buscar o insertar una transacción individual (`WHERE order_id = 99`). | Sumar o promediar una columna sobre millones de registros (`SELECT SUM(price) FROM sales`). |
| **Ventaja clave** | Integridad transaccional ACID rápida por registro. | **Column Pruning & Compresión:** Si tu consulta solo pide `SUM(price)`, el motor lee únicamente el bloque físico de la columna `price` e ignora las otras 50 columnas. |

### 3.3 Perspectiva de Arquitectura: ¿Cuándo Pandas/SQL y cuándo Apache Spark?
Un error frecuente es usar un cañón para matar una mosca:
* **Motores en un solo nodo (Pandas, Polars, DuckDB, PostgreSQL):** Resuelven el **90% de los pipelines empresariales** cuyos lotes caben en la RAM de un servidor moderno (desde megabytes hasta decenas de gigabytes). Son rápidos de desarrollar, fáciles de testear y no tienen sobrecosto de red (*network shuffle*).
* **Procesamiento Distribuido (Apache Spark / PySpark):** Entra en juego cuando un lote supera la memoria física de una sola máquina (cientos de gigabytes o terabytes) y debe particionarse a través de un clúster de múltiples nodos trabajadores (*workers*), tanto en **Batch** como en **Streaming**.

---

## Misión a seguir
Dirígete a la carpeta `quests/00-arquitecturas-zonas` y completa los tests de andamiaje para construir tu primer paso entre zonas de datos.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar conceptos de arquitecturas ETL y ELT` o `feat(quests): implementar flujo base de zonas bronze a gold`.
