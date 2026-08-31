# Capítulo 01: DDL & Relational Modeling

El modelado relacional es el proceso de estructurar la información en tablas conectadas lógicamente entre sí. Crear tablas sin un diseño previo lleva a duplicación de datos, inconsistencias graves y consultas imposibles de mantener.

En este capítulo aprenderás **DDL (Data Definition Language)**, que es el conjunto de comandos SQL utilizados para definir, modificar y destruir estructuras de tablas, así como los principios de **Normalización** y restricciones de integridad (**Constraints**).

---

## 1. Conceptos Clave de Modelado Relacional

En el diseño relacional existen tres tipos principales de relaciones entre entidades:
1. **Relación 1:N (Uno a Varios):** Un registro de la Tabla A se conecta con múltiples registros de la Tabla B, pero cada registro de B pertenece a uno solo de A. (Ej: Un aeropuerto maneja muchos vuelos, pero un vuelo despega de un solo aeropuerto).
2. **Relación N:M (Varios a Varios):** Múltiples registros de A se conectan con múltiples registros de B. (Ej: Un pasajero puede tomar muchos vuelos, y un vuelo lleva a muchos pasajeros).
3. **Relación 1:1 (Uno a Uno):** Cada registro de A se relaciona con máximo uno de B.

### Analogía 1: La Foreign Key como Número de Pieza Único
Imagina el ensamble de un avión comercial. Cada componente tiene un código de parte registrado en un catálogo maestro de piezas. Si los mecánicos instalan un perno con un código que no existe en el catálogo, la inspección rechaza el ensamble. Una **Foreign Key (FK)** es exactamente esa regla: prohíbe asociar un registro hijo a un registro padre que no existe previamente en la tabla principal.

### Analogía 2: Las Relaciones N:M y la Tabla de Créditos
Piensa en una película y sus actores. Si intentaras guardar la lista de actores en una sola celda de la tabla de películas separada por comas, tendrías un desastre imposible de consultar. Tampoco puedes poner los títulos de las películas dentro de la tabla de actores. La solución es crear una tercera tabla: la "Tabla de Créditos" (o tabla intermedia/junction table), donde cada fila conecta el `ID_Actores` con el `ID_Pelicula`.

---

## 2. Dominio de Ejemplo: Sistema de Aerolínea (Domain Shifting)

Modelaremos un **Sistema de Gestión de Vuelos y Pasajeros** en una aerolínea comercial.

### Esquema Relacional (Diagrama ER en ASCII)

```text
  ┌──────────────┐          ┌────────────────┐          ┌──────────────┐
  │   airports   │          │    flights     │          │  passengers  │
  ├──────────────┤ 1      N ├────────────────┤ N      1 ├──────────────┤
  │ code (PK)    │──────────│ flight_number  │          │ id (PK)      │
  │ name         │          │ origin_code(FK)│          │ full_name    │
  │ city         │          │ dest_code (FK) │          │ passport_no  │
  └──────────────┘          └────────────────┘          └──────────────┘
                                    │ 1                        │ 1
                                    │                          │
                                    │ N                        │ N
                               ┌────┴──────────────────────────┴────┐
                               │            bookings                │
                               ├────────────────────────────────────┤
                               │ id (PK)                            │
                               │ flight_id (FK)                     │
                               │ passenger_id (FK)                  │
                               │ seat_number                        │
                               └────────────────────────────────────┘
```

---

## 3. DDL y Constraints de Integridad

SQLite requiere activar explícitamente el soporte para llaves foráneas en cada sesión con el comando `PRAGMA foreign_keys = ON;`.

### Creación de Tablas con Constraints (`CREATE TABLE`)

```sql
PRAGMA foreign_keys = ON;

-- 1. Tabla de Aeropuertos
CREATE TABLE airports (
    code TEXT PRIMARY KEY,                   -- Identificador IATA (ej: 'BOG', 'JFK')
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    capacity INTEGER CHECK(capacity > 0)     -- Constraint CHECK para números válidos
);

-- 2. Tabla de Vuelos (Relación 1:N con aeropuertos)
CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL UNIQUE,       -- Constraint UNIQUE: no pueden existir 2 vuelos iguales
    origin_code TEXT NOT NULL,
    destination_code TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    status TEXT DEFAULT 'Scheduled',          -- Valor por defecto si no se proporciona
    FOREIGN KEY (origin_code) REFERENCES airports(code),
    FOREIGN KEY (destination_code) REFERENCES airports(code)
);

-- 3. Tabla de Pasajeros
CREATE TABLE passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    passport_number TEXT NOT NULL UNIQUE
);

-- 4. Tabla Intermedia: Reservas (Junction Table N:M entre Flights y Passengers)
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    passenger_id INTEGER NOT NULL,
    seat_number TEXT NOT NULL,
    price_paid REAL NOT NULL CHECK(price_paid >= 0),
    FOREIGN KEY (flight_id) REFERENCES flights(id) ON DELETE CASCADE,
    FOREIGN KEY (passenger_id) REFERENCES passengers(id),
    UNIQUE(flight_id, seat_number)            -- No se puede reservar el mismo asiento 2 veces en el mismo vuelo
);
```

---

## 4. Normalización Relacional (1NF a 3NF)

La **Normalización** es la técnica para organizar las columnas y tablas para minimizar la redundancia de datos.

### Ejemplo Progresivo de Normalización

#### ❌ El Mal Camino: Tabla Monolítica Desnormalizada (Violación de 1NF, 2NF y 3NF)
Imagina guardar las reservas de la aerolínea en una sola tabla sin normalizar:

```sql
-- ❌ MAL: Todos los datos mezclados en una sola tabla
CREATE TABLE unnormalized_flights (
    flight_number TEXT,
    origin_airport TEXT,
    origin_city TEXT,          -- Redundante: Si cambia la ciudad del aeropuerto BOG, hay que modificar 10,000 filas
    passengers_list TEXT,      -- Violación 1NF: Almacena múltiples nombres separados por comas 'Juan, Maria, Pedro'
    seat_numbers TEXT          -- Violación 1NF: '12A, 12B, 14C'
);
```

**Consecuencias desastrosas:**
- Imposible consultar cuántos vuelos ha tomado un pasajero específico.
- **Anomalía de Actualización:** Cambiar el nombre del aeropuerto requiere actualizar miles de filas.
- **Anomalía de Inserción:** No puedes registrar un nuevo aeropuerto sin haber creado un vuelo primero.

#### ✅ El Buen Camino: Aplicación de las 3 Formas Normales (3NF)

1. **Primera Forma Normal (1NF):** Todo valor debe ser atómico (indivisible). Se eliminan listas separadas por comas. Cada celda contiene un solo dato.
2. **Segunda Forma Normal (2NF):** Debe estar en 1NF y cada columna que no sea clave debe depender de la totalidad de la Primary Key (se separan tablas de Vuelos y Pasajeros).
3. **Tercera Forma Normal (3NF):** Debe estar en 2NF y ninguna columna no clave debe depender de otra columna no clave (la ciudad del aeropuerto depende únicamente del código del aeropuerto, por lo que `city` vive en `airports`, no en `flights`).

---

## 5. Modificación y Borrado de Estructuras (`ALTER` & `DROP`)

Si necesitas modificar la estructura de una tabla existente o eliminarla:

```sql
-- Agregar una nueva columna a una tabla existente
ALTER TABLE passengers ADD COLUMN email TEXT;

-- Renombrar una columna
ALTER TABLE passengers RENAME COLUMN full_name TO legal_name;

-- Eliminar una tabla si existe (¡Cuidado: Borra los datos permanentemente!)
DROP TABLE IF EXISTS unnormalized_flights;
```

---

## 6. Setup y Verificación en Terminal

Para verificar tus llaves foráneas y constraints en SQLite via terminal de macOS:

```bash
sqlite3 airline.db
```

```sql
PRAGMA foreign_keys = ON;

-- Intento de insertar un vuelo con un aeropuerto inexistente (Debe fallar con error de Foreign Key)
INSERT INTO flights (flight_number, origin_code, destination_code, departure_time)
VALUES ('AV9301', 'XYZ', 'BOG', '2026-10-15 08:00');
-- Error esperado: FOREIGN KEY constraint failed
```

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/01-ddl/`:

- [[01-schema-design.md]] (Tipo A: Diseñar y crear el esquema de tablas en 3NF con constraints)
- [[02-er-interpretation.md]] (Tipo B: Leer un diagrama ER y escribir las sentencias DDL correspondientes)

```text
subjects/sql/chronicles/SQL-BASICO/quests/01-ddl/
├── 01-schema-design.md
└── 02-er-interpretation.md
```
