# Mission: Clasificador de números (Variables y tipos)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M02  
Title: Clasificador de números (Variables y tipos)  
Status: 🟢 Ready

---

## Objective
Recibir datos por consola, convertir tipos y aplicar lógica condicional básica.

---

## Description
Los scripts deben procesar información externa. En esta misión se capturará un dato del usuario, se convertirá al tipo correcto y se evaluará mediante condiciones lógicas.

Conceptos clave:
- Input siempre devuelve `str`.
- Conversión explícita (`int()`).
- Bloques `if / elif / else`.

---

## Required Knowledge
- `input()`
- `int()`
- Operadores de comparación (`>`, `<`, `==`)
- Operador módulo `%`

---

## Steps
1. Crear el archivo `clasificador.py`.
2. Solicitar al usuario un número entero mediante `input()`.
3. Convertir el valor ingresado a tipo `int`.
4. Implementar lógica para determinar e imprimir:
   - Si es positivo, negativo o cero.
   - Si es par o impar.
   - Si es mayor a 100.

---

## Completion Criteria
- [ ] El script solicita el dato correctamente.
- [ ] Clasifica correctamente números positivos, negativos y cero.
- [ ] Clasifica correctamente pares e impares.
- [ ] No utiliza bucles (`for`/`while`), solo condicionales.

---

## Notes
- Si se ingresa texto no numérico, el script fallará. Esto es esperado en esta etapa.
