# Mission: Menú interactivo (While loops y control de flujo)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M04  
Title: Menú interactivo (While loops y control de flujo)  
Status: 🟢 Ready

---

## Objective
Crear una interfaz de consola interactiva que permita al usuario controlar el flujo del programa mediante un menú.

---

## Description
Los programas útiles necesitan interactuar continuamente con el usuario hasta que este decida salir. Esta misión introduce el "Game Loop" o "Main Loop" usando `while True`.

Conceptos clave:
- Bucle infinito (`while True`).
- Control de flujo con `break`.
- Captura de opciones del usuario.
- Lógica condicional para menús (`if/elif/else`).

---

## Required Knowledge
- `while condition:`
- `input()`
- `if/elif/else`
- Operadores de comparación

---

## Steps
1. Crear el archivo `menu_inventario.py`.
2. Inicializar una lista vacía de productos (o copiar la estructura de M03).
3. Implementar un bucle `while True` que muestre las siguientes opciones:
   1. Agregar producto
   2. Ver inventario
   3. Salir
4. **Opción 1**: Solicitar nombre, precio y cantidad, crear el diccionario y agregarlo a la lista.
5. **Opción 2**: Recorrer la lista e imprimir los productos (reutilizando lógica de M03).
6. **Opción 3**: Imprimir "Saliendo..." y romper el bucle con `break`.
7. **Opción inválida**: Manejar el caso en que el usuario ingrese una opción no válida.

---

## Completion Criteria
- [ ] El menú se repite indefinidamente hasta elegir "Salir".
- [ ] Se pueden agregar productos dinámicamente.
- [ ] La opción de ver inventario muestra los datos actualizados.
- [ ] El programa no se cierra inesperadamente tras una acción (excepto al elegir Salir).

---

## Notes
- En la siguiente misión refactorizaremos este código usando funciones.
