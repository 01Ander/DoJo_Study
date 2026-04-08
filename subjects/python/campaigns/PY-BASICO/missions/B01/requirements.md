# Mission: Procesador de Logs (Integración)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/08-protocol-yellow.md))*


## Identification
Type: B  
Campaign Code: PY-BASICO  
Mission Code: B01  
Title: Procesador de Logs (Integración)  
Status: 🟢 Ready

---

## Objective
Integrar lectura de archivos, manipulación de strings, estructuras de datos y funciones en un script completo capaz de analizar un archivo de logs y generar un reporte resumen.

---

## Description
Esta Boss Mission cierra la campaña PY-BASICO.  
El objetivo es procesar un archivo de texto con líneas de logs y extraer información útil.

El script final debe:
- leer un archivo línea por línea,
- filtrar entradas que contengan errores,
- contar ocurrencias,
- y generar un reporte en un archivo nuevo.

Conceptos clave:
- file I/O (`with open`)
- filtrado mediante condiciones
- conteos y agregación
- organización mediante funciones

No se usa regex ni manejo avanzado de errores en esta etapa.

---

## Required Knowledge
- Todos los conceptos vistos en M01–M06.
- Funciones simples con parámetros.
- Lectura/escritura de archivos.
- Filtrado de listas.

---

## Steps
1. Crear un archivo `server.log` con líneas simuladas, por ejemplo:

[INFO] Server started at 10:00
[WARNING] Disk space low
[ERROR] Connection timeout
[ERROR] Invalid user input
[INFO] Connection closed


2. Crear el script `analizador_logs.py`.

3. Definir una función `leer_archivo(ruta)` que:
- abra el archivo con `with open`
- devuelva todas las líneas como una lista

4. Definir una función `filtrar_errores(lineas)` que:
- recorra la lista
- retorne solo las que contengan `"[ERROR]"`

5. Calcular:
- total de líneas procesadas  
- total de errores encontrados  
- porcentaje de líneas con error (opcional)

6. Crear la función `generar_reporte(ruta_salida, datos)` que:
- escriba un archivo `reporte.txt`
- incluya:
  - total de líneas
  - total de errores
  - listado de errores (opcional)

7. Ejecutar el programa completo desde `main` (bloque principal).

---

## Completion Criteria
- [ ] El script corre de principio a fin sin errores.
- [ ] Se genera `reporte.txt` correctamente.
- [ ] Los conteos coinciden con el archivo fuente.
- [ ] El código está organizado en funciones (`leer_archivo`, `filtrar_errores`, `generar_reporte`).
- [ ] No se usa regex ni manejo de errores avanzado.

---

## Notes
- No introduzcas nuevas estructuras complejas; la prioridad es integrar lo aprendido.
- Procesa el archivo secuencialmente, sin librerías externas.
- Esta Boss Mission completa la campaña PY-BASICO y abre el camino hacia **PY-POO** y **PY-DATA**.