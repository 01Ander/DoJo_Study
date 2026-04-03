# Guía Práctica de Operación de Misiones

Este documento explica el funcionamiento práctico de las misiones dentro del DoJo Study:  
cómo se usan, dónde se realizan, qué rol tiene cada chat y cómo se avanza de una a otra sin perder claridad.

Su propósito es evitar confusión y mantener un método de estudio estable, modular y sostenible.

---

# 1. ¿Qué es una misión?

Una **misión** es una tarea práctica, concreta y ejecutable que desarrolla una habilidad técnica real.

- No es teoría.
- No es una clase.
- No es una explicación larga.
- No se desarrolla dentro del chat.

Una misión es **acción real**, realizada por ti en tu entorno técnico (VS Code, terminal, Python, etc.).

Cada misión del DoJo está diseñada para que aprendas *haciendo*, no leyendo.

---

# 2. ¿Dónde se hace una misión?

**Siempre en tu computador.**

- VS Code  
- Terminal  
- Archivos reales  
- Scripts reales  
- Directorios reales  

Nunca en el chat.

La misión es tu “práctica en el mundo real”.

---

# 3. ¿Cuándo se usa cada chat?

El DoJo utiliza tres chats por materia para que NO te confundas.

## 3.1 XX-EXERCISES → Generación de misiones
Este chat sirve para:

- crear nuevas misiones  
- generar variaciones  
- pedir más misiones de práctica  
- ajustar misiones existentes  

**Aquí nacen las misiones.  
No se resuelven aquí.**

## 3.2 XX-MAIN → Teoría mínima (solo cuando la misión lo requiere)
Este chat se usa SOLO si te atoras o desconoces un concepto.

Ejemplo:
- “Explícame diccionarios para completar M03.”  
- “¿Cómo funciona int()?”  
- “¿Qué es un loop while?”

La teoría dentro del DoJo:
- siempre es mínima  
- siempre es contextual  
- nunca es larga  
- aparece *después* del problema  
- solo responde lo necesario para avanzar la misión

## 3.3 XX-WORK → Debugging y acompañamiento técnico
Este chat es para:

- revisar tu código  
- corregir errores  
- validar tu lógica  
- refactorizar  
- entender por qué algo no funciona  

**Aquí sí compartes tu código.**

Este es el chat donde “trabajamos” mano a mano.

---

# 4. Flujo completo de estudio de una misión

El ciclo es siempre el mismo:

1. Abrir la misión (en el repo).
2. Intentarla por tu cuenta en VS Code.
3. Si falta teoría → ir a XX-MAIN.
4. Si hay errores → ir a XX-WORK.
5. Terminar la misión en tu entorno real.
6. Marcarla como completada en el repo.
7. Avanzar a la siguiente misión.

Este ciclo evita:
- saturación  
- teoría excesiva  
- dependencia de la IA  
- aprendizaje pasivo  

---

# 5. ¿Qué hacer si una misión introduce un concepto nuevo?

No te “preparas antes”.  
No estudias teoría sin contexto.

Simplemente:

1. **Intentas la misión.**  
2. Cuando aparece el bloqueo:  
   → “Voy a XX-MAIN y pido la teoría mínima para desbloquear esto.”

Esto te hace aprender 3× más rápido  
porque tu cerebro aprende mejor cuando resuelve un problema real.

---

# 6. ¿Cuándo avanzo a la siguiente misión?

Cuando se cumple lo siguiente:

- La misión está completa.  
- Funciona lo que pedía.  
- No estás confundido respecto a su objetivo.  
- Puedes explicar (breve) lo que aprendiste.

No necesitas perfección.  
No necesitas sentirte “maestro”.  
No necesitas memorizar teoría.

**El DoJo avanza por pequeñas victorias, no por perfección.**

---

# 7. ¿Cómo se conectan las misiones con las Boss Missions?

Las **Misiones Principales (M)** dan la base técnica.  
Las **Side Missions (S)** profundizan.  
Las **Boss Missions (B)** integran todo en un proyecto real.

Ejemplo en PY-BASICO:

- M02 → input  
- M03 → colecciones  
- M04 → funciones  
- M05 → archivos  

La Boss Mission (Procesador de Logs) usa TODAS esas habilidades para un proyecto real.

---

# 8. ¿Qué pasa con la teoría más avanzada?

La teoría avanzada NO aparece en PY-BASICO.  
Aparece en campaigns superiores:

- PY-POO  
- PY-AUTO  
- PY-DATA  
- PY-API  
- PY-TEST  
- PY-CLOUD  

El DoJo evita adelantarse.  
El ritmo es estrictamente progresivo.

---

# 9. ¿Dónde se integran las misiones en el repo?

Cada misión vive dentro de:

`subjects/<materia>/campaigns/<campaign>/missions/`

Ejemplo:

`subjects/python/campaigns/PY-BASICO/missions/M03/`

Cada misión tiene su propio archivo `.md` usando el template oficial.

---

# 10. Resumen final

- Las misiones se HACEN en VS Code, no en chat.  
- XX-EXERCISES → generar misiones.  
- XX-MAIN → teoría mínima.  
- XX-WORK → debugging y acompañamiento.  
- Teoría solo aparece cuando es necesaria.  
- Cada misión te prepara para la siguiente.  
- Las Boss Missions integran todo en un proyecto real.  
- El DoJo avanza por práctica, no por teoría.

---

Este documento define la forma oficial de operar misiones dentro del DoJo Study.
