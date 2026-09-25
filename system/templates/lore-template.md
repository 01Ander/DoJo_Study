# Capítulo [NN]: [Título del Capítulo]

[Introducción breve del QUÉ es el concepto principal, utilizando estrictamente el Domain Shifting definido para esta chronicle. NO uses el dominio del Rite.]

> **[⚠️ INSTRUCCIÓN PARA EL GENERADOR]**
> *No comprimas toda la teoría en un solo bloque. Si el capítulo aborda múltiples sub-conceptos (ej. Roles vs Políticas), crea tantas secciones `## [Número]. [Sub-Tema]` como necesites para explicarlos con profundidad. Cada sección teórica debe cubrir el Qué y el Por qué.*

## 1. [Nombre del Primer Concepto o Sub-Tema] (Qué y Por qué)
[Explicación de alto nivel de por qué existe esta herramienta o técnica, y qué problema exacto de negocio resuelve. No asumas conocimiento previo.]

> **Densidad (Condicionado a la Complejidad del Tema):**
> Si este concepto es abstracto, arquitectónico o involucra lógica estructurada, añade aquí al menos 2 analogías de la vida real (usando el dominio temático del lore) para anclar la idea. Si es un paso atómico de configuración, puedes omitir esto.

## [X]. Setup Inicial (Zero Assumption)
[Si el capítulo introduce una nueva herramienta, CLI o librería externa, incluye aquí las instrucciones exactas de instalación o configuración asumiendo conocimiento nulo previo.]

## [X+1]. Implementación (Cómo)
[Desglose del código aplicando **Zero Surprise Syntax**: TODO operador, método, argumento o keyword nuevo (incluso los accesorios) debe explicarse explícitamente detallando qué hace, por qué se eligió y cómo funciona internamente.]

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** [Describe explícitamente qué cálculo o resultado queremos lograr antes del código]
[Muestra cómo se resolvería esto de forma ineficiente, acoplada o hardcodeada si no conociéramos el concepto de este capítulo.]
```python
# Código de ejemplo frágil
```

### El Camino Robusto (Ejemplo Óptimo)
**🎯 Objetivo de Negocio:** [Mismo objetivo]
[Muestra la solución arquitectónicamente correcta usando el concepto enseñado en este capítulo.]
```python
# Código de ejemplo robusto
```

## [X+2]. Conexión con Testing (Regla Crítica)
[TDD es el pilar. Explica aquí **cómo se prueba** el código de producción de la sección anterior. Si los ejercicios (quests) requerirán usar mocks (`unittest.mock`, `@patch`), fixtures de `pytest`, manejo temporal, o aserciones específicas, debes introducir y desglosar esa sintaxis de testing aquí mismo bajo la regla de Zero Surprise Syntax. Los tests no pueden ser una "caja negra" mágica en las quests.]

```python
# Ejemplo de cómo testear el código superior
# (Incluir explicaciones línea por línea de los mocks/fixtures si se usan)
```

## [X+3]. Mapa de Ejercicios

Dirígete a `quests/[NN-titulo]/` y completa la práctica deliberada:

```text
quests/[NN-titulo]/
├── quest.md          (Instrucciones)
├── my_solution.py    (Tu archivo de trabajo)
└── test_my_solution.py
```
*(El Operador no avanzará al siguiente capítulo de lore ni escribirá su grimoire hasta no pasar todos los tests de estas quests en color verde).*
