# 📓 Grimoire — PY-POO

Este documento es tu registro académico. Después de leer cada capítulo en `lore/` y completar su laboratorio en `quests/`, debes documentar tu asimilación aquí utilizando la **Técnica Feynman**.

> **⚠️ Regla del DM:** El DoJo Agent (Dungeon Master) auditará este documento (`/scry`). Si detecta que estás copiando y pegando, o que no comprendes el concepto central, **denegará tu acceso al Rite**.

---

## Capítulo 00: From Functions to Classes
**Fecha de finalización:** 2026-05-11
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
**Fecha de finalización:** 2026-06-02
**Métricas:**
- Tiempo de lectura: 5 min
- Tiempo en ejercicios: 20 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1
- ¿Completé el ejercicio de testing (Nivel 1) sin ver la solución?: [Sí]

**Feynman Synthesis (Tus propias palabras):**
1. ¿Qué es un "contrato" en programación y cómo lo hace cumplir el módulo `abc`?
> Un contrato es una "imposición" frente a una clase que se hereda, esto permite que las clases hijas sigan requerimientos, principalmente los metodos y los paramentros de entrada de los mismos, sigan unas reglas especificas que permiten tener una base primaria que se puede repetir o usar en distintos otros contextos que comparten cierta logica, una logica base, pero que los subsiguientes requieren una capa superior, sin tanta necesidad de repetir codigo inecesario y a su vez blindar la logica, para que no se llegue a romper o se intancien clases sin logica prescrita con las reglas puestas.

2. ¿Por qué una clase abstracta no puede ser instanciada (crear un objeto de ella)?
> Porque esta no contiene logica, instrucciones o procesos como tal. Hasta el momento, las clases abstractas solo presentan los requerimientos de metodos y sus paramentros que se ingresan a la base de la clase abstracta. Esta es unicamente el molde que sigen las clases hijas.

**Friction Log (Opcional):**
> []

---

## Capítulo 02: Domain Entities y Polimorfismo
**Fecha de finalización:** 2026-06-03
**Métricas:**
- Tiempo de lectura: 5 min
- Tiempo en ejercicios: 25 min
- Veces que recurrí al Tutor/DM: 1 (Objetivo: ≤ 2)
- Fricción (1-10): 1
- ¿Completé el ejercicio de testing sin ver la solución?: Si

**Feynman Synthesis:**
1. ¿Cuál es la diferencia entre usar un diccionario y una `@dataclass` para representar una entidad?
> dataclass permite de cierta manera 'blindar' los paramentros que se establecieron en la creacion de la clase evitando asi posibles errores al modificar en typo por ejemplo, cuando se vayan a modificar los datos puros.

2. Explica qué es el polimorfismo y por qué es útil.
> El poliformismo permite recrear un metodo, una accion en distintas entidades, con una respuesta distinta, es decir, hay una base, que es el metodo que se comparte en todas las clases que lo lleven, sin embargo la respuesta de estos metodos internos puede variar dependiendo de la logica del metodo en cuestion. De todas maneras se comparte la base, que seria el nombre y/o llamado de dicho metodo, lo que lo diferencia es la logica interna que puede variar, pero se tiene siempre las mismas entradas.

**Friction Log (Opcional):**
> Ligera confusion con el dataclass, porque no se habia leido bien que es para evitar posibles errores de typo. Esa fue la unica intervension de DM.

---

## Capítulo 03: Stateless Engines y Composición
**Fecha de finalización:** 2026-07-08
**Métricas:**
- Tiempo de lectura: 2 min
- Tiempo en ejercicios: 3 min
- Veces que recurrí al Tutor/DM: 2 (Objetivo: ≤ 2)
- Fricción (1-10): 3
- ¿Completé el ejercicio de Spaced Repetition?: Si

**Feynman Synthesis:**
1. ¿Por qué un "Stateless Engine" no debe guardar estado (variables en `self`)?
> No se guada estados en "stateless engine" ya que se busca que la clase no se contamine de informacion que se haya utilizado anteriormente. Esto permite que un estado y/o variable habite unicamente en el lugar donde va a ser utilizada dentro de la propia clase y en su propio metodo, dando asi paso a eliminacion de errores desde la raiz de la propia clase.

2. ¿Cuál es la ventaja de la composición (pasar un objeto a otro) versus la herencia?
> Composicion permite generar una estructura organizada y a su vez que las clases no 'hereden' logicas a las cuales no son del mismo tipo, pero si hacen uso de ellas. Un computador es un tipo de electrodomestico? Si/Herencia. Un computador es un tipo de automatizador autonomo? No/Composicion.

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 04: Orchestration & I/O
**Fecha de finalización:** 2026-07-09
**Métricas:**
- Tiempo de lectura: 3 min
- Tiempo en ejercicios: 10 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1

**Feynman Synthesis:**
1. ¿Qué es un Orquestador y qué lógica de negocio debería tener? (Pista: ninguna).
> El orquestador es el disparador de eventos, en un orden logico. Este no guarda ninguna logica en absoluto ya que su unica funcion es hacer el llamado a los distintos eventos, clases o metodos en una hoja de ruta establecida.

2. ¿Por qué aislar la lectura de archivos (I/O) en su propia clase facilita el testing con Mocks?
> Aislar la lectura de archivos permite manejar una estructura lofica mucho mas estable y menos propensa a errores que puedan ocurrir, aislandolo en su propia clase, permite que ejecute unicamente su accion de lectura y escritura unicamente cuando sea necesario y sea llamado por un orquestador. Esto a su vez permite que no se dependa de que archivos existan ya en maquina o en una conexion a una API, si no, que al usar Mocks, podemos verificar via test si dica clase esta haciendo correctamente su funcion de input o output.

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 05: Testing with Pytest
**Fecha de finalización:** 2026-07-10
**Métricas:**
- Tiempo de lectura: 5 min
- Tiempo en ejercicios: 15 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1
- ¿Completé el ejercicio de testing sin ver la solución?: Si

**Feynman Synthesis:**
1. Explica la estructura GIVEN / WHEN / THEN (Arrange / Act / Assert).
> Esta estructura hace funcion como un orquestador, pero con matices en los test. Dicha estructura permite, inicializar una clase/objeto/metodo, ejecutar una accion y verificar que la accion fue ejecutada de manera correcta.  

2. ¿Cuál es el propósito exacto de un `fixture` en pytest?
> Un fixture permite inicializar una clase una unica vez para poder usarla en distintos test sin la teria de tener que inicializarla de nuevo en cada test que se quiera hacer.

**Friction Log (Opcional):**
> [¿Qué te costó más trabajo entender?]

---

## Capítulo 06: Logging y Error Handling
**Fecha de finalización:** 2026-07-14
**Métricas:**
- Tiempo de lectura: 4 min
- Tiempo en ejercicios: 10 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1

**Feynman Synthesis:**
1. ¿Por qué es mejor usar Excepciones de Dominio personalizadas en lugar de un `ValueError` genérico?
> Al usar Domain Exceptions tenemos la posibilidad de saber exactamente en que parte del codigo y de la logica se esta presentando un fallo dentro del mismo. Si no fuera asi, no se tendria clariadad al momento de que se presentara dichos fallos 

2. ¿En qué se diferencia usar `logger.error` de usar un simple `print`?
> EL logger.error guarda el error que se haya presentado en un archivo externo, permitiendo que este pueda ser observado y analizado a posterior. Al usar un simple print, este mostraria el error en consola, pero si el sistema se reinicia por cualquier razon, la informacion de ese error se perderia y no podria ser corregida de manera oportuna, en dado caso. 

**Friction Log (Opcional):**
> 

---

## Capítulo 07: CLI and Production Assembly
**Fecha de finalización:** 2026-07-14
**Métricas:**
- Tiempo de lectura: 4 min
- Tiempo en ejercicios: 8 min
- Veces que recurrí al Tutor/DM: 0 (Objetivo: ≤ 2)
- Fricción (1-10): 1

**Feynman Synthesis:**
1. ¿Para qué sirve el bloque `if __name__ == "__main__":` en Python?
> Para que el script, o programa se ejecute unicamente cuando este es llamado explicitamente en consola, evitando asi que se ejecute sin necesidad en otros entornos donde el programa no es requerido en su totalidad.

2. Describe cómo el `cli.py` se convierte en el lugar donde ensamblas ("inyectas") todas las dependencias.
> El CLI es la parte visible del programa que tendra acceso el usuario final. Debajo de el esta toda la logica, el codigo de dicho programa, pero el usuario no necesita acceder a el de forma directa. El CLI se encarga de tomar las partes externas del programa y unificarlas en una sola interfas o un par de lineas de codigo, trayendo archivos, buscando las rutas de carga o guardado y ejecutando el orquestador del mismo programa.

**Friction Log (Opcional):**
> 
