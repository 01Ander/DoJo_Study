# Mission: Refactor funcional (Funciones y modularidad)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M05  
Title: Refactor funcional (Funciones y modularidad)  
Status: 🟢 Ready

---

## Objective
Encapsular la lógica principal del inventario en funciones reutilizables para mejorar la organización y legibilidad del código.

---

## Description
El código monolítico de la misión M04 funciona, pero es difícil de mantener y extender.  
En esta misión vas a refactorizar ese código, separando:

- la lógica de agregar productos
- la lógica de mostrar el inventario

del bucle principal.

El objetivo es que el “main loop” solo coordine el flujo, mientras que el trabajo real se hace en funciones.

Conceptos clave:
- Definición de funciones (`def`)
- Parámetros y argumentos
- Separación de responsabilidades

No se introduce nada avanzado (no POO, no decoradores, no `*args`), solo funciones simples.

---

## Required Knowledge
- Sintaxis básica de funciones: `def nombre_funcion(...):`
- Paso de parámetros
- Alcance de variables (scope) a nivel básico

---

## Steps
1. Crear el archivo `inventario_func.py` copiando el código final de la M04.
2. Definir una función `agregar_producto(lista)` que:
   - pida nombre, precio y cantidad
   - cree el diccionario del producto
   - lo agregue a la lista
3. Definir una función `mostrar_inventario(lista)` que:
   - recorra la lista con un `for`
   - imprima cada producto de forma legible
4. Modificar el bucle `while True` para:
   - llamar a `agregar_producto(lista)` en la opción 1
   - llamar a `mostrar_inventario(lista)` en la opción 2
   - mantener la lógica de salida en la opción 3 (`break`)
5. Verificar que el programa se comporta igual que en la M04.

---

## Completion Criteria
- [ ] El bucle principal solo contiene:
      - lectura de opción
      - llamadas a funciones
      - control de flujo (`if/elif/else`, `break`)
- [ ] El comportamiento es equivalente al de la M04.
- [ ] Las funciones reciben la lista de productos como parámetro (no usan variables globales nuevas).
- [ ] No se añadieron nuevas funciones innecesarias ni opciones al menú.

---

## Notes
- Cada función debe encargarse de una sola tarea clara.
- No agregues manejo de errores (`try/except`) todavía.
- No introduzcas nuevas opciones en el menú; esta misión se centra solo en la modularidad.