# Mission: Inventario simple (Colecciones y for loops)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M03  
Title: Inventario simple (Colecciones y for loops)  
Status: 🟢 Ready

---

## Objective
Gestionar conjuntos de datos utilizando listas, diccionarios y bucles `for`.

---

## Description
El manejo de datos requiere estructuras que permitan almacenar y recorrer múltiples elementos. Esta misión se enfoca en la creación de una lista de diccionarios y la iteración sobre ella para mostrar información.

Conceptos clave:
- Listas como contenedores ordenados.
- Diccionarios para datos estructurados (clave-valor).
- Bucle `for` para recorrido secuencial.
- `f-strings` para formateo de salida.

---

## Required Knowledge
- Listas `[]` y métodos `.append()`
- Diccionarios `{}`
- Bucle `for item in lista:`
- Acceso a valores de diccionario `diccionario["clave"]`

---

## Steps
1. Crear el archivo `inventario_simple.py`.
2. Crear una lista de diccionarios llamada `productos` con al menos 3 productos pre-cargados (ej: manzanas, pan, leche).
   - Cada producto debe tener: `nombre`, `precio`, `cantidad`.
3. Agregar un nuevo producto a la lista usando `.append()` (simulando una entrada manual o hardcodeada).
4. Recorrer la lista con un bucle `for`.
5. Para cada producto, imprimir una línea con el formato:
   `Producto: [Nombre] | Precio: $[Precio] | Stock: [Cantidad]`
6. Calcular e imprimir el valor total del inventario (suma de `precio * cantidad` de todos los productos).

---

## Completion Criteria
- [ ] El script define una lista de diccionarios.
- [ ] Se utiliza un bucle `for` para mostrar los datos.
- [ ] El formato de salida es legible y ordenado.
- [ ] Se calcula el valor total del inventario correctamente.
- [ ] No se utiliza `while` ni menús interactivos.

---

## Notes
- Esta misión sienta las bases para la gestión de datos que luego se hará interactiva.
