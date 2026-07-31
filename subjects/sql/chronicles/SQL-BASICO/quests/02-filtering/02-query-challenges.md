# Ejercicio 02-02: Advanced Query Challenges (Tipo B)

**Objetivo:** Resolver retos de filtrado complejo utilizando los operadores `IN`, `BETWEEN`, `LIKE`, y `IS NULL`.

---

## Setup de Datos

```sql
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_email TEXT NOT NULL,
    priority TEXT NOT NULL, -- 'Low', 'Medium', 'High', 'Urgent'
    status TEXT NOT NULL,   -- 'Open', 'Pending', 'Closed'
    assigned_agent TEXT
);

INSERT INTO tickets (customer_email, priority, status, assigned_agent) VALUES
('alice@test.com', 'High', 'Open', 'Agent_Smith'),
('bob@domain.org', 'Low', 'Closed', 'Agent_Jones'),
('charlie@company.com', 'Urgent', 'Open', NULL),
('david@test.com', 'Medium', 'Pending', 'Agent_Smith'),
('eve@company.com', 'High', 'Open', NULL);
```

---

## Retos

1. Escribe una consulta `SELECT` que encuentre todos los tickets con prioridad `'High'` o `'Urgent'` que **no hayan sido asignados a ningún agente** (`assigned_agent IS NULL`).
2. Escribe una consulta `SELECT` para obtener todos los tickets de clientes cuyos correos pertenezcan al dominio `@company.com` (Pista: usa `LIKE '%@company.com'`).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- Reto 1: Tickets de alta prioridad sin agente asignado
SELECT customer_email, priority, status 
FROM tickets 
WHERE priority IN ('High', 'Urgent') AND assigned_agent IS NULL;

-- Reto 2: Filtrar por patron de correo
SELECT customer_email, priority 
FROM tickets 
WHERE customer_email LIKE '%@company.com';
```
</details>
