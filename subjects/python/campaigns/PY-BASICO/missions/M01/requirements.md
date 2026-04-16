# Mission: Ejecutar primer script (Configurar entorno)

**Friction Level:** [ ] / 10 *(If > 7, activate [Protocol Yellow](../../../../../docs/07-protocol-yellow.md))*


## Identification
Type: M  
Campaign Code: PY-BASICO  
Mission Code: M01  
Title: Ejecutar primer script (Configurar entorno)  
Status: 🟢 Ready

---

## Objective
Asegurar que el entorno de trabajo (VS Code + Python + terminal) funciona correctamente ejecutando el primer script básico.

---

## Description
Antes de avanzar a misiones con lógica o datos, necesitas verificar que tu entorno está completamente operativo.  
Esta misión confirma que:

- Python está instalado  
- VS Code reconoce el intérprete  
- La terminal integrada ejecuta scripts `.py` sin errores  

Es la base de todo el trabajo posterior.

---

## Required Knowledge
- Crear archivos en VS Code  
- Abrir la terminal integrada  
- Usar `print()`  

(No se requiere teoría adicional.)

---

## Steps
1. Crear la carpeta `missions/M01_primer_script/`.  
2. Crear el archivo `main.py`.  
3. Escribir un script que imprima exactamente:
       - "Hola, DoJo."
       - "Mi entorno de Python está configurado."
       - "Listo para la Misión 02."
4. Abrir la terminal integrada de VS Code.  
5. Ejecutar el script con:
       - `python main.py`  
         o  
       - `python3 main.py` (Linux/Mac)

---

## Completion Criteria
- [ ] El script se ejecuta sin errores.  
- [ ] Las tres frases aparecen en pantalla.  
- [ ] Puedes correr el archivo desde terminal sin usar el botón de “Run”.

---

## Notes
- Si aparece “python not found”, revisa la instalación o el PATH del sistema.  
- Si VS Code muestra múltiples intérpretes, selecciona el correcto desde:  
  `Ctrl + Shift + P → Python: Select Interpreter`.  