# Mission: Manejo de errores (Input seguro)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/08-protocol-yellow.md))*


## Identification
Type: S  
Campaign Code: PY-BASICO  
Mission Code: S01  
Title: Manejo de errores (Input seguro)  
Status: 🟤 Optional

---

## Objective
Implementar control de excepciones para evitar la interrupción abrupta del programa ante datos inválidos.

---

## Description
Los errores de entrada de usuario son comunes. Esta misión consiste en proteger las conversiones de tipo (`int()`) utilizando bloques de manejo de excepciones.

Conceptos clave:
- Bloque `try / except`.
- Captura de `ValueError`.

---

## Required Knowledge
- Sintaxis `try: ... except Error: ...`
- `ValueError`

---

## Steps
1. Seleccionar uno de los scripts anteriores (M02 o M03) donde se solicite un número.
2. Envolver la conversión `int()` dentro de un bloque `try`.
3. En el bloque `except`, mostrar un mensaje de error informativo en lugar de dejar que el programa falle.
4. (Opcional) Usar un bucle para volver a pedir el dato hasta que sea válido.

---

## Completion Criteria
- [ ] El programa no se detiene si se ingresa texto en lugar de números.
- [ ] Se muestra un mensaje de error controlado.

---

## Notes
- El objetivo es la estabilidad, no la lógica compleja.
