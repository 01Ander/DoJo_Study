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

## Misión a seguir
Dirígete a la carpeta `quests/00-arquitecturas-zonas` y completa los tests de andamiaje para construir tu primer paso entre zonas de datos.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar conceptos de arquitecturas ETL y ELT` o `feat(quests): implementar flujo base de zonas bronze a gold`.
