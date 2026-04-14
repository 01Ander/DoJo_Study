---
name: dojo-log
description: Registra una entrada en la bitácora (journal.md) de la misión activa
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, journal, logging]
    category: dojo
    requires_toolsets: [terminal, file]
---

# DoJo Journal Log

## When to Use
Cuando el Operador quiere registrar un avance, reflexión, error o duda en la bitácora de la misión activa.

## Usage
```
/dojo-log [mensaje]
```
Ejemplo: `/dojo-log Completé el primer test unitario para la calculadora. Descubrí que decimal.Decimal es mejor que float para finanzas.`

## Procedure
1. Ejecuta el script `scripts/log_entry.py` con la campaña, misión y mensaje.
2. El script crea el journal.md si no existe.
3. Agrega una entrada con timestamp en formato: `- **[User | YYYY-MM-DD HH:MM:SS]:** mensaje`
4. Confirma al Operador que la entrada fue registrada.

## Pitfalls
- Requiere una misión activa (previamente fijada con `/dojo-start`).
- Si no hay misión activa, indica al usuario que use `/dojo-start` primero.

## Verification
- El archivo journal.md contiene la nueva entrada con timestamp correcto.
