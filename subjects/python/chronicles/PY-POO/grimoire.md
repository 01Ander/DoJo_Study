# 📓 Grimoire — PY-POO

Este documento es tu registro académico. Después de leer cada capítulo en `lore/` y completar su laboratorio en `quests/`, debes documentar tu asimilación aquí utilizando la **Técnica Feynman**.

> **⚠️ Regla del DM:** El DoJo Agent (Dungeon Master) auditará este documento (`/scry`). Si detecta que estás copiando y pegando, o que no comprendes el concepto central, **denegará tu acceso al Rite**.

---

## Capítulo 00: From Functions to Classes
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: 3 min
- Tiempo en ejercicios: 22 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1
- ¿Completé el ejercicio de testing (Nivel 1) sin ver la solución?: [Sí]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Cuál es el problema fundamental que resuelven las clases que las funciones simples no pueden?
> La facilidad de crear planos que se puedan replicar miles de veces. Poder asegurar las caracteristicas propias de cada clase, otorgando una capa de seguridad de que fuera de la clase estas caracteristicas no podran ser modificadas tan facilmente.

2. ¿Qué es `self` en Python y por qué es obligatorio en los métodos de instancia?
> Self es el apuntador hacia el objeto creado. En quien indica a que objeto se le esta aplicando un metodo sin tener que equivocarse si existen mas objetos y pueda aplicar precisamente el metodo al objeto preciso. 

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 01: Abstract Classes and Interfaces
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __
- ¿Completé el ejercicio de testing (Nivel 1) sin ver la solución?: [Sí / No]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué es un "contrato" en programación y cómo lo hace cumplir el módulo `abc`?
> [Tu respuesta aquí...]

2. ¿Por qué una clase abstracta no puede ser instanciada (crear un objeto de ella)?
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 02: Domain Entities y Polimorfismo
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __
- ¿Completé el ejercicio de testing sin ver la solución?: [Sí / No]

**Feynman Synthesis:**
1. ¿Cuál es la diferencia entre usar un diccionario y una `@dataclass` para representar una entidad?
> [Tu respuesta aquí...]

2. Explica qué es el polimorfismo y por qué es útil.
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 03: Stateless Engines y Composición
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __
- ¿Completé el ejercicio de Spaced Repetition?: [Sí / No]

**Feynman Synthesis:**
1. ¿Por qué un "Stateless Engine" no debe guardar estado (variables en `self`)?
> [Tu respuesta aquí...]

2. ¿Cuál es la ventaja de la composición (pasar un objeto a otro) versus la herencia?
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 04: Orchestration & I/O
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __

**Feynman Synthesis:**
1. ¿Qué es un Orquestador y qué lógica de negocio debería tener? (Pista: ninguna).
> [Tu respuesta aquí...]

2. ¿Por qué aislar la lectura de archivos (I/O) en su propia clase facilita el testing con Mocks?
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 05: Testing with Pytest
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __
- ¿Completé el ejercicio de testing sin ver la solución?: [Sí / No]

**Feynman Synthesis:**
1. Explica la estructura GIVEN / WHEN / THEN (Arrange / Act / Assert).
> [Tu respuesta aquí...]

2. ¿Cuál es el propósito exacto de un `fixture` en pytest?
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 06: Logging y Error Handling
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __

**Feynman Synthesis:**
1. ¿Por qué es mejor usar Excepciones de Dominio personalizadas en lugar de un `ValueError` genérico?
> [Tu respuesta aquí...]

2. ¿En qué se diferencia usar `logger.error` de usar un simple `print`?
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 07: CLI and Production Assembly
**Fecha de finalización:** YYYY-MM-DD
**Métricas:**
- Tiempo de lectura: __ min
- Tiempo en ejercicios: __ min
- Veces que recurrí al Tutor/DM: __ (Objetivo: ≤ 2)
- Fricción (1-10): __

**Feynman Synthesis:**
1. ¿Para qué sirve el bloque `if __name__ == "__main__":` en Python?
> [Tu respuesta aquí...]

2. Describe cómo el `cli.py` se convierte en el lugar donde ensamblas ("inyectas") todas las dependencias.
> [Tu respuesta aquí...]

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]
