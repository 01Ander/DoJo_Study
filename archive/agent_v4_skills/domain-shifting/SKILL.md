---
name: domain-shifting
description: Protocolo de analogías de dominio para enseñanza técnica sin spoilers
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, teaching, tutor]
    category: dojo
---

# Domain Shifting Protocol

## When to Use
Cuando el Tutor necesita explicar un concepto técnico con ejemplos de código, pero debe evitar resolver directamente la misión del Operador.

## Qué es Domain Shifting
Es la técnica de enseñar un concepto usando una **analogía de dominio completamente diferente** al de la misión activa. El objetivo es que el Operador:
1. Entienda la mecánica del concepto (sintaxis, patrón, estructura).
2. **Traduzca** la lógica por sí mismo al dominio de su misión.
3. Desarrolle la habilidad de abstracción que distingue a un Senior de un Junior.

## Reglas

### 1. Nunca usar el mismo dominio
- Si la misión es sobre **datos financieros**, los ejemplos deben ser sobre videojuegos, naves espaciales, zoológicos, cocina, deportes, etc.
- Si la misión es sobre **gestión de inventario**, los ejemplos deben ser sobre astronomía, música, construcción, etc.

### 2. El código debe ser REAL y FUNCIONAL
- No pseudocódigo.
- El Operador debe poder copiar y ejecutar el ejemplo.
- Incluir type hints y docstrings (modelar buenas prácticas).

### 3. Tabla de Dominios Análogos

| Dominio de la Misión | Dominios Análogos Válidos |
|---|---|
| Finanzas / Banca | Videojuegos, Zoológico, Cocina |
| E-Commerce / Inventario | Astronomía, Música, Ejército |
| Healthcare / Medicina | Deportes, Arquitectura, Agricultura |
| Logística / Transporte | Química, Arte, Educación |
| IoT / Sensores | Cocina, Ecosistemas, Teatro |

### 4. Estructura del Ejemplo
```
1. Declarar el dominio análogo explícitamente
2. Mostrar el código funcional completo
3. Explicar qué patrón o concepto ilustra
4. Dejar al Operador la tarea de "traducir" al dominio real
```

## Pitfalls
- No mezclar múltiples dominios análogos en un solo ejemplo (confunde).
- No usar analogías demasiado abstractas (el código debe ser concreto).
- Si el Operador no logra hacer la traducción tras 2 intentos, dar una pista más directa pero sin resolver.
