# Mission: Limpiador de archivos (Lectura y escritura de archivos)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M06  
Title: Limpiador de archivos (Lectura y escritura de archivos)  
Status: 🟢 Ready

---

## Objective
Leer datos desde un archivo de texto, procesarlos y escribir el resultado en un nuevo archivo.

---

## Description
La persistencia de datos y el procesamiento por lotes son fundamentales. Esta misión se centra en abrir archivos, leer su contenido línea por línea, aplicar transformaciones de strings y guardar el output.

Conceptos clave:
- Context manager (`with open`).
- Modos de apertura (`r`, `w`).
- Métodos de limpieza de strings (`strip`, `lower`).

---

## Required Knowledge
- `with open(ruta, modo) as alias:`
- Métodos `.read()`, `.readlines()` o iteración directa sobre el archivo.
- `.write()`

---

## Steps
1. Crear manualmente un archivo `emails_sucios.txt` con correos que tengan espacios irregulares y mezclas de mayúsculas/minúsculas.
2. Crear el script `limpiador.py`.
3. Leer el archivo de origen línea por línea.
4. Para cada línea:
   - Eliminar espacios en blanco al inicio y final.
   - Convertir todo a minúsculas.
5. Escribir los correos procesados en un nuevo archivo `emails_limpios.txt`.

---

## Completion Criteria
- [ ] Se genera el archivo de salida.
- [ ] El contenido del archivo de salida está normalizado (sin espacios extra, todo minúsculas).
- [ ] Se utiliza `with open` para el manejo de archivos.

---

## Notes
- Asegurar que el archivo de origen exista antes de ejecutar el script.
