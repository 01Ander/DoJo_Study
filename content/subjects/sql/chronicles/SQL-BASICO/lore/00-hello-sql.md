# Capítulo 00: Hello, SQL — Introduction to Databases & SQLite

Bienvenido al mundo de las **Bases de Datos Relacionales**. Hasta ahora en Python has trabajado con datos guardados en memoria (listas, diccionarios) o en archivos de texto (CSV, JSON). Aunque los archivos son útiles, tienen limitaciones graves: si dos procesos intentan escribir al mismo tiempo se corrompen, buscar un registro entre 1 millón de líneas requiere leer todo el archivo, y no hay garantía de que los datos respeten una estructura estricta.

Una **Base de Datos Relacional (RDBMS)** resuelve todos estos problemas. Organiza la información en **tablas** (filas y columnas) que garantizan integridad, velocidad de búsqueda e historial concurrente.

> 💡 **Nota sobre el entorno de estudio:** En esta chronicle utilizaremos **SQLite**, un motor de base de datos relacional serverless, ligero e integrado nativamente en la mayoría de sistemas operativos. Toda consulta de este capítulo y de los laboratorios se puede probar directamente desde tu terminal interactiva de macOS.

---

## 1. Conceptos Fundamentales: ¿Qué es SQL?

**SQL** significa *Structured Query Language* (Lenguaje de Consulta Estructurado). A diferencia de Python, que es un lenguaje **imperativo** (donde le indicas al computador el paso a paso detallado de *cómo* hacer algo), SQL es un lenguaje **declarativo**: le describes al motor de base de datos *qué* información deseas obtener o modificar, y el motor optimizador calcula internamente el mejor camino para ejecutarlo.

### Analogía 1: La Hoja de Cálculo con Superpoderes
Piensa en una base de datos como un archivo de Excel gigantesco donde cada pestaña es una **tabla**. Sin embargo, a diferencia de Excel donde puedes escribir texto en una celda destinada a números, la base de datos relacional actúa como un guardia de seguridad infalible: cada columna tiene un tipo de dato obligatorio (ej: entero, texto, decimal). Si intentas meter texto en una columna de fechas, la base de datos rechaza la operación inmediatamente.

### Analogía 2: El Mesero del Restaurante
Imagina que entras a un restaurante. Tú no vas a la cocina a cortar cebollas ni a encender la estufa (eso sería estilo imperativo/Python). Tú le pides al mesero: *"Tráeme la hamburguesa con papas sin cebolla"* (estilo declarativo/SQL). El mesero se encarga de transmitir la orden y la cocina ejecuta toda la preparación técnica para entregarte exactamente lo que pediste.

---

## 2. Setup en macOS (Zero Assumption Tooling)

En macOS, `sqlite3` viene instalado de forma nativa en el sistema operativo. No necesitas descargar instaladores externos ni configurar servidores en segundo plano.

### Paso 1: Verificación en Terminal
Abre tu terminal de macOS (`Terminal.app` o `iTerm2`) y ejecuta el siguiente comando:

```bash
sqlite3 --version
```

**Output esperado:** Un número de versión como `3.39.5 2022-10-14 ...` o superior.

### Paso 2: Crear tu primera Base de Datos en un archivo local
Para crear y abrir una base de datos llamada `zoo.db`, navega a tu directorio de trabajo y ejecuta:

```bash
sqlite3 zoo.db
```

Verás que el prompt de tu terminal cambia a `sqlite>`. Ahora estás dentro de la consola interactiva de SQLite.

### Paso 3: Configurar Comandos Dot (`.commands`)
La CLI de SQLite utiliza comandos especiales que empiezan con un punto (`.`) para configurar la visualización en pantalla:

```sql
.headers on          -- Muestra los nombres de las columnas en los resultados
.mode column         -- Alinea los resultados en columnas ordenadas estilo tabla
```

Para listar las tablas existentes usas `.tables`, para ver la estructura de una tabla usas `.schema nombre_tabla`, y para salir de la consola ejecutas `.quit` o presionas `Ctrl + D`.

---

## 3. Dominio de Ejemplo: Sistema de Zoológico (Domain Shifting)

Para comprender la estructura de una base de datos, modelaremos un **Sistema de Gestión de un Zoológico** (animales, recintos y cuidadores). 

### Creación de Tablas (`CREATE TABLE`)
Una tabla se define especificando el nombre de cada columna y su tipo de dato. SQLite soporta tipos nativos como `INTEGER` (enteros), `TEXT` (cadenas de texto), `REAL` (números decimales), `BLOB` (datos binarios) y `NULL`.

```sql
-- Creamos la tabla de animales del zoológico
CREATE TABLE animals (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    age INTEGER,
    weight_kg REAL
);
```

### Inserción de Datos (`INSERT INTO`)
Para agregar filas (registros) a la tabla, utilizamos la instrucción `INSERT INTO`:

```sql
INSERT INTO animals (id, name, species, age, weight_kg) 
VALUES (1, 'Simba', 'Leon', 5, 190.5);

INSERT INTO animals (name, species, age, weight_kg) 
VALUES ('Nala', 'Leon', 4, 175.0);

INSERT INTO animals (name, species, age, weight_kg) 
VALUES ('Kovu', 'Tigre', 3, 210.2);
```
> Notice: Como `id` es `INTEGER PRIMARY KEY`, si omitimos su valor al insertar, SQLite le asigna automáticamente un entero autoincremental (1, 2, 3...).

---

## 4. Consultas Progresivas (`SELECT`)

La instrucción `SELECT` nos permite recuperar información de una o varias tablas.

### Ejemplo 1: El Mal Camino (Seleccionar todo indiscriminadamente)
Un error común de los principiantes es usar siempre `SELECT * FROM`:

```sql
-- ❌ Mal camino: recuperar todas las columnas cuando solo necesitas el nombre
SELECT * FROM animals;
```
**Problema:** En tablas reales con 50 columnas y millones de filas, consultar `*` consume ancho de banda de red y memoria innecesarios.

### Ejemplo 2: El Buen Camino (Especificar columnas)
La buena práctica en ingeniería es solicitar explícitamente solo las columnas necesarias:

```sql
-- ✅ Buen camino: solicitar únicamente las columnas requeridas
SELECT name, species, weight_kg FROM animals;
```

**Output en la consola de SQLite:**
```text
name        species     weight_kg
----------  ----------  ----------
Simba       Leon        190.5
Nala        Leon        175.0
Kovu        Tigre       210.2
```

---

## 5. Conexión con Testing & Verificación

En SQL, "probar" tu código significa ejecutar scripts de creación e inserción y validar que el estado resultante de la base de datos coincida con lo esperado.

Puedes guardar tus comandos SQL en un archivo `.sql` (por ejemplo `setup_zoo.sql`) y ejecutarlo completo desde la terminal de macOS en un solo comando:

```bash
sqlite3 zoo.db < setup_zoo.sql
```

---

## 6. Mapa de Ejercicios

Dirígete a la carpeta `quests/00-hello-sql/` y completa los laboratorios:

- [[01-first-database.md]] (Tipo A: Crear tabla, insertar registros y realizar consultas básicas)
- [[02-query-reading.md]] (Tipo B: Leer comandos SQL y predecir el resultado devuelto por la consola)

```text
subjects/sql/chronicles/SQL-BASICO/quests/00-hello-sql/
├── 01-first-database.md   (Práctica de creación e inserción)
└── 02-query-reading.md     (Lectura e interpretación de consultas)
```
