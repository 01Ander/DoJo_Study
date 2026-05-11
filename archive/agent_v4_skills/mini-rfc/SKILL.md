---
name: mini-rfc
description: Template y proceso para documentos de diseño previo (Mini-RFC) antes de codificar
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, design, architecture]
    category: dojo
    requires_toolsets: [file]
---

# Mini-RFC Protocol

## When to Use
Antes de escribir cualquier línea de código en una misión. En el DoJo, **está prohibido codificar sin un diseño justificado**.

## Usage
```
/mini-rfc
```
Carga el template y las reglas. El agente puede ayudar a completar el RFC.

## Procedure
1. El Operador crea un archivo `mini-rfc.md` en el directorio de la misión.
2. Completa las secciones del template usando el archivo `templates/mini-rfc-template.md`.
3. El Reviewer (en modo `/personality dojo-reviewer`) valida el RFC.
4. Solo cuando el Reviewer da "luz verde" se puede pasar a TDD.

## Template
Ver `templates/mini-rfc-template.md` para el template completo.

## Criterios de Aprobación
Un Mini-RFC es **suficiente** cuando:
- [ ] El Business Context está definido (¿qué problema resuelve?)
- [ ] El ROI está cuantificado (¿cuánto vale resolverlo?)
- [ ] La arquitectura alto nivel está diagramada o descrita
- [ ] Los componentes principales están identificados
- [ ] Los edge cases críticos están listados
- [ ] La estrategia de testing está definida (qué se testea primero)

## Pitfalls
- No sobre-diseñar. Un Mini-RFC no es un documento de 20 páginas.
- El objetivo es **lo mínimo necesario** para empezar el primer test.
- Si el Reviewer te da luz verde, no sigas diseñando — codea.
