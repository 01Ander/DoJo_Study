# Ejercicio 00-02: Query Reading & Output Prediction (Tipo B)

**Objetivo:** Desarrollar la capacidad de "ejecutar mentalmente" código SQL declarativo e interpretar las respuestas devueltas por la consola.

---

## Pregunta 1

Dado el siguiente script de creación e inserción:

```sql
CREATE TABLE servers (
    id INTEGER PRIMARY KEY,
    hostname TEXT NOT NULL,
    ram_gb INTEGER,
    ip_address TEXT
);

INSERT INTO servers (id, hostname, ram_gb, ip_address) VALUES (1, 'web-prod-01', 32, '192.168.1.10');
INSERT INTO servers (hostname, ram_gb) VALUES ('db-prod-01', 64);
INSERT INTO servers (hostname, ram_gb, ip_address) VALUES ('app-dev-01', 16, '192.168.1.15');
```

¿Qué valor tendrá la columna `id` del servidor `'app-dev-01'` y qué valor tendrá la columna `ip_address` del servidor `'db-prod-01'`?

Respuesta: 3, NULL

---

## Pregunta 2

Analiza la siguiente consulta y predice qué filas y columnas serán devueltas:

```sql
SELECT hostname FROM servers;
```

Respuesta: 
```sql
hostname
----------------
web-prod-01
db-prod-01
app-dev-01

```


---

<details>
<summary>👀 Ver Solución Esperada</summary>

### Respuesta 1:
- El `id` de `'app-dev-01'` será **3** (SQLite autoincrementa a partir del valor más alto asignado).
- La columna `ip_address` de `'db-prod-01'` será **NULL** (dado que se omitió en la sentencia `INSERT`).

### Respuesta 2:
La consulta retornará únicamente una columna (`hostname`) con 3 filas:

```text
hostname
-----------
web-prod-01
db-prod-01
app-dev-01
```
</details>
