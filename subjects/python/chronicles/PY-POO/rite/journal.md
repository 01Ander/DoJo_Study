**[2026-07-21]** : Primer acercamiento al rite. Se lee los requerimientos y se plantea el posible camino a seguir para la primera fase. Se hace uso del agent para aclarar ideas y bajar la friccion de un 5 a un 2. Se plantea: 
	- La implementacion de una clase abstracta para la extraccion de datos para cualquier tipo de archivo que pueda llegar al sistema, de esta manera, se pueden crear subclases para un tipo de archivo especifico, permitiendo no romper logica original y mantener una guia de que debe extraer el Extractor de manera general y que herede dicha funcion para cualquier archivo. Se considera, con lo que se vio en PY-BASICO el uso del csv.DictReader para la extraccion de la informacion en el csv. Se usaria la funcion que existe en la mision boss 1 de py-basico, como metodo con la herencia de la clase abstracta.
	- Se solicita tambien un manejo de errores, a partir de Domain Exceptions, para la carga del archivo especificamente. Se puede considerar tambien, quizas, para posibles fallas de carga o que el archivo venga sin datos. 
	- Por ultimo, se requiere un testing basico que se vio en el capitulo 06, muy similar, para poder validar que la clase abstracta no se instacie sola y que el extractor obtenga los datos correctos.
Como primera entrada, se deja por el momento aqui, ya que el dia estuvo cortado por eventos externos que no permitieron el avance a codigo, pero se validara el planteamiento aqui descrito por el DM para el dia de manana llegar directo a codear esta primera fase. 
Igualmente, por requerimiento personal, se va a manejar este journal como un mini rfc para poder aclarar las ideas y poder tener claro que se va a hacer.

<details>
<summary>Uso del agent:</summary> 
╭⚕ Hermes ╮
    Adelante, Operador. El papel está en blanco y el Boss te mira desde lo alto de la mazmorra. Cuéntame qué tienes en la cabeza para la Fase 1, y vamos puliendo la
    idea entre los dos antes de que toques el teclado.

    — "Un buen plano ahorra más sudor que veinte martillazos ciegos."
╰─╯
────────────────────────────────────────
● La fase uno me pide crear una interfaz para la lectura y extraccion de datos, a partir de una clase abstracta que permita leer cualquier tipo de archivo en general. Y a
su vez manejar posibles errores con la ruta y el archivo. Lo que no recuerdo bien es como implementar esa lectura de archivo, cualqueira que sea. En py-basico en las
misiones boss algo hice sobre eso, que tanto puedo usar de ahi?
────────────────────────────────────────

╭─ ⚕ Hermes ─╮
    Buena pregunta. Vamos a ver qué tienes en tu arsenal de PY-BASICO — puede que ya hayas escrito algo parecido antes
╰╯
  ┊ 💻 preparing terminal…
  ┊ 💻 $         find /Users/ander/Documents/DoJo/DoJo_Study/subjects/python/chronicles/PY-BASICO -type f -name "*.py"  0.1s
  ┊ 📖 preparing read_file…
  ┊ 🔎 preparing search_files…
  ┊ 📖 read      test_etl.py  0.1s
  ┊ 🔎 find      *.py  0.1s
  ┊ 📖 preparing read_file…
  ┊ 📖 read      etl.py  0.1s

╭─ ⚕ Hermes ─╮
    Ahora sí tengo el mapa completo. Esto es lo que encontré en tu misión B01 de PY-BASICO:

    python
    load_logs — leía CSV línea por línea con csv.reader
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)          # saltaba el header
        for row in reader:
            lines.append(",".join(row))


    Ahora, la Fase 1 del Rite te pide algo conceptualmente diferente: no es una función suelta, sino una jerarquía de clases con herencia y contrato abstracto.

    Tres preguntas para que tú mismo encuentres los límites de lo reusable:

    1. En PY-BASICO, load_logs() retornaba list[str] — cadenas crudas. La Fase 1 pide que extract() retorne list[dict]. ¿Qué cambiaría en la lectura del
    CSV para que cada fila sea un diccionario en lugar de un string?

    2. El DataSourceNotFoundError es una excepción de dominio. ¿Qué crees que la diferencia de un FileNotFoundError genérico de Python? (Pista: ya viste esto
    en el lore del Cap 06.)

    3. La interfaz AbstractExtractor con el módulo abc — ¿recuerdas cómo se declara un método abstracto? Lo viste en el lore del Cap 01 y lo practicaste en la
    quest correspondiente.

    Cuéntame qué piezas crees que puedes tomar prestadas de PY-BASICO y cuáles tienes que construir desde cero, y vamos refinando la idea.

    — "El mago sabio no aprende nuevos hechizos; aprende cuándo reciclar los viejos."
╰─╯
────────────────────────────────────────
● Si, entiendo que se declara una clase abstracta que es la encargada de mantener el metodo para definir cualquier tipo de archivo a posterior, en ese caso puedo declarar
una clase heredada que sea para csv, otra para json y dejar abierto para cualquier otro tipo de archivo que pueda entrar luego, sin romper el codigo como se haria con una
funcion simple. por otra parte, si recuerdo que es mejor manejar el error directamente con el logging para evitar salidas en consola y posterior poder tener un registro
aparte de como va el funcionamiento del programa y capturar los posibles errores, de carga y lectura
────────────────────────────────────────

╭─ ⚕ Hermes ─╮
    Vas bien encaminado. El Principio de Abierto/Cerrado se asoma: una interfaz abstracta que permite añadir nuevos formatos sin tocar el código existente. Eso es
    exactamente lo que busca la Fase 1.

    Dos matices para afinar antes de que escribas una línea:

    1. Error Handling: excepción vs logging.
    Mencionaste logging, y es cierto que en el Cap 06 viste que logger.error() es mejor que print(). Sin embargo, el requirements.md de la Fase 1 dice textual:

    > "Si el archivo no existe o la ruta es inválida, lanzar una excepción de dominio DataSourceNotFoundError (no usar FileNotFoundError genérico)."

    Ojo: no dice "loguear el error y continuar". Dice lanzar una excepción. El logging viene después en la Fase 4 cuando el orquestador atrape esa excepción. Aquí,
    en la capa de extracción, la responsabilidad es avisar que los datos no existen, no gestionar qué hacer con ese aviso.

    2. El retorno del método extract() es list[dict].
    Si tienes un CSV con columnas date,amount,category,description, ¿cómo convertirías cada fila del CSV a un diccionario con esas llaves? ¿Hay alguna herramienta
    del módulo csv que te evite hacer el mapeo a mano?

    Tirita de ese hilo y dime si te queda claro el diseño antes de pasar a código.

    — "Un hechizo mal preparado no falla en el lanzamiento; falla en el momento en que el mago confunde sus ingredientes."
╰──╯
────────────────────────────────────────
● 1. si, perdon, es con doamin exceptions, en ese caso deberia generar las clases para los errores de lectura y carga de archivo, con 'excpetion' y posterior validar el
archivo y los datos dentro para poder lezar la excepcion. 2. Pensaria en utilizar el mismo metodo que se utilizo en etl.py, con el csv.DictReader, para que haga el mapeo
completo y me regrese la lista de dics
────────────────────────────────────────

╭─ ⚕ Hermes ─╮
    Ahí está. Has conectado los puntos correctamente:

    Punto 1 — Excepción de dominio: Exacto. Creas tu propia clase que herede de Exception, la nombras DataSourceNotFoundError, y en el
    CSVExtractor.extract()Validarla existencia del archivo (con os.path.exists() o atrapando el error al abrir) y lanzas esa excepción personalizada.

    Punto 2 — csv.DictReader: Justo esa es la pieza. En PY-BASICO usaste csv.reader que te daba listas de strings. DictReader hace el mapeo automático usando
    la primera fila como cabecera — te devuelve cada fila como dict sin tener que escribir el mapeo a mano. Perfecto para el list[dict] que pide la interfaz.



    Resumen de tu plan para Fase 1:


    src/
    ├── extractors.py        → AbstractExtractor (ABC)
    │                           └── CSVExtractor (hereda, usa DictReader)
    ├── exceptions.py        → DataSourceNotFoundError (custom Exception)
    └── tests/
        └── test_extractors.py → TDD: falla → código → pasa


    ¿Te parece completo el mapa o ves alguna otra pieza que incluir en el diseño antes de abrir el editor?

    — "El arquitecto que dibuja antes de entender el suelo construye castillos que el primer viento derriba."
</details>


**[2026-07-22]** : Primera seccion de codigo realizada. Apriximadamente una hora de codigo y preguntas al agent para afinar. Se realiza la clase abstracta para la extraccion de los datos desde un csv, y se prueba con los test correspondientes, dando paso a las siguientes funciones que se piden en la fase 1. La friccion para iniciar fue casi minima, se busco el codigo que se habia visto en la version anterior del poo, para refrescar como se hacia la lectura y tambien los tests. Se hace uso de fixture para los test y la creacion de un csv temporal con tmp_path. 
<details>
<summary>Uso del agent:</summary> 

╭─ ⚕ Hermes ╮
    El test pasa perfecto. Buen trabajo con la estructura del abc.

    Ahora, revisando extractors.py línea por línea, veo algo curioso:

    Clase abstracta — contrato:
    python
    def extract(self, filepath: str) -> list[dict]:


    Clase concreta — implementación:
    python
    def load_data(self, filepath: str) -> list[dict]:


    Dos preguntas:

    1. El contrato de AbstractExtractor dice extract(filepath). CSVExtractor implementa load_data(filepath). Si alguien
    escribe:

    python
    extractor: AbstractExtractor = CSVExtractor()
    extractor.extract("data.csv")


    ¿Qué crees que pasaría en esa llamada? ¿Se ejecutaría load_data o se toparía con un muro?

    2. Bonus: sabiendo eso, ¿crees que CSVExtractor() se puede instanciar en este momento, o también lanzaría TypeError?

    — "Un contrato firmado con sangre exige que ambas partes usen el mismo nombre, aunque el conjuro sepa distinto."
╰────╯

────────────────────────────────────────
● ah ok, si, perdon, el metodo debe tener el mismo nombre para que funcione o no tendria logica y saltaria un error, no se ejecutaria. Ya
esta corregido
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 📖 read      extractors.py  0.1s

╭─ ⚕ Hermes ──╮
    Perfecto. Ahora sí, el contrato está alineado. Déjame verificar que todo sigue en verde:

╰───╯
  ┊ 💻 preparing terminal…
  ┊ 💻 $         .venv/bin/python -m pytest tests/test_extractors.py -v  0.2s

╭─ ⚕ Hermes ─╮
    Verde. Ahora tienes:


    rite/
    ├── src/
    │   ├── init.py
    │   └── extractors.py      → AbstractExtractor + CSVExtractor.extract() ✅
    │   ...
    ├── tests/
    │   └── test_extractors.py  → 1 test ✅


    La Fase 1 del requirements aún pide dos cosas que veo pendientes:

    - DataSourceNotFoundError — la excepción de dominio para rutas inválidas
    - Que CSVExtractor la lance si el archivo no existe (no dejar que open() suelte un FileNotFoundError genérico)
    - Test para CSVExtractor — validar que retorna datos correctos con un CSV real (o un fixture con tmp_path)

    ¿Quieres seguir con eso o prefieres que hablemos de cómo estructurar la excepción primero?

    — "Un conjuro a medias es solo una chispa que no enciende la hoguera."
╰──╯

────────────────────────────────────────
● como tengo el codigo ahi, quiero hacer el test para validar si el extract funciona correctamente. Mi pregunta es, como para test no
puedo depender de que exista el archivo real por el momento, debo utilizar mocks?
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Buena pregunta. Vamos a ver qué dice exactamente el requirements:

    > Testing Mínimo: Validar que AbstractExtractor no se puede instanciar y que CSVExtractor retorna los datos correctos.

    Fíjate que no dice "usa mocks" para esta fase. Eso aparece después en la Fase 4 para el orquestador. Para el extractor, lo que
    importa es que los datos se lean y se devuelvan correctamente.

    Ahora, piensa en esto:

    Si usas un mock para csv.DictReader, en realidad no estás probando que tu extractor sepa leer un CSV. Estás probando que el
    mock fue llamado — no que dict(row) funcione, ni que el encoding sea el correcto, ni que las cabeceras se mapeen bien.

    Pero si dependes de data/transactions.csv real para el test, tu test depende de **un archivo que puede moverse, borrarse, o que
    otro desarrollador no tenga en su máquina**.

    Dicho esto: en tu misión B01 de PY-BASICO ya usaste un patrón que resuelve exactamente este dilema sin mocks. ¿Recuerdas cómo
    creaste datos temporales para test_load_logs_returns_list_of_dicts?

    — "El mago sabio no necesita fingir que existe un dragón; puede invocar uno diminuto para practicar."
╰──╯
  💾 Self-improvement review: Memory updated

────────────────────────────────────────
● ok si, algo recuerdo de harcodear los datos creadon un dict y meterlos en un csv "falso", pero debo mirarlo porque no recuerdo bien como
se hace
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    En PY-BASICO usaste un fixture que se llama tmp_path — viene incluido con pytest, no hay que importarlo de ningún lado. Es un
    directorio temporal que pytest crea antes del test y lo destruye al terminar.

    El patrón era más o menos así:

    1. Creas un archivo con tmp_path / "nombre.csv"
    2. Le escribes contenido CSV con write_text()
    3. Le pasas la ruta a tu extractor

    Dos pistas finas para que lo reconstruyas:

    Pista 1: ¿Qué método usaste en B01 para escribir el CSV directamente como texto sin tener que abrir un archivo con open()?
    (Pista: el archivo del test de B01 lo tienes arriba en la conversación, en test_etl.py línea 87-98.)

    Pista 2: Una vez creado el archivo temporal, ¿qué necesitas pasarle a CSVExtractor.extract()? ¿Un Path object o un str?

    — "Recordar es el primer paso de todo conjuro. El segundo es saber qué parte del recuerdo es útil ahora."
╰──╯

────────────────────────────────────────
● ya, lo estoy viendo, con un fixture. creo un sample_csv, le cargo los datos ahi, y despues genero el test para verificarlo, si?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    Exacto. Ese es el camino. El fixture se encarga de:

    1. Crear el archivo temporal antes del test
    2. Cargar los datos de ejemplo
    3. Destruirlo automáticamente al terminar, sin dejar basura

    En tu PY-BASICO era así (para que lo tengas de referencia visual):

    python
    @pytest.fixture
    def sample_csv(tmp_path):
        filepath = tmp_path / "test_manifest.csv"
        filepath.write_text("cabeceras...\ndatos...")
        return filepath


    Para tu caso, necesitas que el CSV tenga las columnas que va a leer DictReader — date,amount,category,description o como hayas
    definido los datos de transacción — y al menos un par de filas para verificar.

    ¿Qué columnas crees que debería llevar ese CSV de prueba? Tíralas por aquí y las validamos antes de que escribas el test.

    — "Un buen aprendiz no solo recuerda el hechizo; recuerda que lo practicó, y eso es lo que cuenta."
╰───╯

────────────────────────────────────────
● voy a usar las mismas que se usaron en v4; id, date, amount, currency, type, description, category.
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Esos son 7 campos sólidos para el CSV — id, date, amount, currency, type, description, category. Justo lo que necesita
    DictReader para mapear cabeceras a llaves del diccionario.

    Adelante, escríbelo. Cuando tengas el fixture + el test, me llamas y lo revisamos.

    — "La pluma del test es más afilada que la espada del código."
╰──╯

────────────────────────────────────────
● duda, como estamos evaluando todo lo de extractors, puedo escribir el test en el mismo archivo que valida la instacia verdad?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    Claro. Es el mismo archivo de test para la misma unidad (extractors.py): un test para la clase abstracta, otro test para el
    extractor concreto. No necesitas un archivo separado.

    Al final quedaría algo así:


    tests/
    └── test_extractors.py   → Aquí están todos los tests de extractors
        ├── test_cannot_instantiate_abstract_class  ✅
        └── test_csv_extractor_returns_data         ⬜ (el que estás por escribir)


    Adelante, cuando lo tengas me dices.

    — "Un grimorio no tiene capítulos separados para cada conjuro; solo páginas, y todas cuentan."
╰───╯
  💾 Self-improvement review: Skill 'dojo-rite-workflow' created.

────────────────────────────────────────
● puedes ver el archivo del test y decirme en que me estoy equivocando?
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 📖 read      test_extractors.py  0.1s

╭─ ⚕ Hermes ─╮
    Buen intento, pero hay varios agujeros en el conjuro. Vamos por partes:

    🔴 Problema 1 — El fixture no se está inyectando.

    Mira el test:

    python
    def test_csv_extractor_returns_data():          # ← sample_csv no está como parámetro
        result = CSVExtractor()
        result.extract(str(sample_csv))              # ← ¿De dónde sale sample_csv?


    En pytest, un fixture se inyecta como parámetro de la función. Si no lo pones como argumento, no existe dentro del test.
    sample_csv está definido pero nunca se usa.

    🔴 Problema 2 — El resultado de extract() se está perdiendo.

    python
    result = CSVExtractor()           # ← result es un objeto CSVExtractor
    result.extract(str(sample_csv))   # ← el list[dict] que devuelve extract() se pierde
    assert isinstance(result, list)   # ← result sigue siendo CSVExtractor, no una lista


    🔴 Problema 3 — DictReader devuelve strings, siempre.

    Un CSV se lee como texto. Aunque escribiste 5000.00 y 1, DictReader los devuelve como "5000.00" y "1". Tu assert espera
    == 1 (entero) pero recibirá "1" (string).



    ¿Cuál de estos tres crees que debes atacar primero para que el test pase? ¿O ves alguno que no esperabas?

    *— "Un conjuro que se lanza sin verificar sus componentes rara vez termina bien. Pero todos hemos incendiado un par de
    matorrales."*
╰───╯

────────────────────────────────────────
● corregido todo y pasado los 2 test
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 💻 preparing terminal…
  ┊ 📖 read      test_extractors.py  0.1s
  ┊ 💻 $         .venv/bin/python -m pytest tests/test_extractors.py -v  0.2s

╭─ ⚕ Hermes ─╮
    2 verdes, 0 rojos. Fase 1 de la Extraction Layer, prendiendo:


    tests/test_extractors.py ✓✓


    Estado actual de Fase 1:

    | Elemento                                             | Estado       |
    |------------------------------------------------------|--------------|
    | AbstractExtractor con extract()                      | ✅           |
    | CSVExtractor con DictReader                          | ✅           |
    | Test: no instanciar abstracta                        | ✅           |
    | Test: CSVExtractor retorna datos                     | ✅           |
    | DataSourceNotFoundError                              | ⬜ Pendiente |
    | Error handling (ruta inválida)                       | ⬜ Pendiente |
    | Test: archivo inexistente lanza excepción de dominio | ⬜ Pendiente |

    ¿Vas a por la excepción? ¿O quieres parar aquí y retomar después?

    — "Dos velas encendidas en la mazmorra. La tercera espera su mecha."


</details>

**[2026-07-22]** : Segunda seccion del dia realizada. Al rededor de dos horas mas. Se termina la fase 1 y la fase 2 del rite. Ambas fases se completan de manera rapida, sobre todo la fase dos, la cual era casi una calca de lo visto en el lore de esa seccion, pero se vio fluides, tanto para hacer los test como para el codigo, aunque se busco fuentes anteriores y preguntas socraticas con el agent.
<details>
<summary>Uso del agent:</summary> 

────────────────────────────────────────
● Voy a contunuar con las excepciones, en este caso lo que haria seria la clase DataSourceNotFoundError(Exception), y ya. Mi pregunta
seria, dentro de extractors, manejaria un try catch para verificar el error, o mas adelante, que justo lo estoy viendo, en la fase 4 es
dodne se alzaria. por lo que para esto solo crearia el archivo con esa clase y listo, tendria que probar con los test nada mas, verdad?
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Casi, casi. Vamos a leer el requirements otra vez, finito:

    > Error Handling (Ref: Cap 06): Si el archivo no existe o la ruta es inválida, lanzar una excepción de dominio
    DataSourceNotFoundError (no usar FileNotFoundError genérico).

    Ahora, pregúntate:

    ¿Quién es el responsable de lanzar esa excepción?

    - Si el archivo no existe y le dices a open() que lo abra... open() va a lanzar su propio FileNotFoundError. No el tuyo.
    - Para que el error sea de dominio (DataSourceNotFoundError) y no genérico, alguien tiene que validar el archivo antes de
    abrirlo y lanzar tu excepción personalizada.

    Ese "alguien" no puede ser la Fase 4, porque la Fase 4 recibe lo que ya extrajiste. El extractor es el que está tocando el archivo.
    Si falla el archivo, el extractor es el primero en saberlo.

    Tu intuición sobre "crear la clase y listo" está bien para empezar, pero te falta una pieza: ¿dónde pones la guarda que decide
    "esto no existe, lanzo mi excepción en vez de dejar que open() la lance por mí"?

    — "La diferencia entre un mago y un aprendiz es que el mago sabe que la advertencia debe llegar antes del desastre, no después."
╰──╯

────────────────────────────────────────
● es que ahi tengo la duda. Dentro del metodo extract puedo poner el try/except, pero lo manejaria con el logger para capturar el error.
Pero leyendo la fase 4 dice que ahi es cuando se maneja con el logger.
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Ahí está el matiz fino. Vamos a separar dos responsabilidades distintas:

    Lanzar la excepción ≠ Capturar y loguear la excepción

    - Lanzar (Fase 1): CSVExtractor.extract() ve que el archivo no existe → salta la alarma → raise DataSourceNotFoundError. No
    necesita try/except para capturarlo. Solo una guarda: "si no existe, lanza esto en vez de lo otro".

    - Capturar y loguear (Fase 4): El orquestador envuelve la ejecución en un try/except DataSourceNotFoundError y ahí sí usa
    logger.error().

    Dicho de otra forma, en extract() no necesitas un bloque try — necesitas un bloque if:


    if el archivo no existe:
        raise DataSourceNotFoundError  ← esto es Fase 1
                                         el try/except con logger es Fase 4


    ¿Tiene más sentido así? La excepción atraviesa el extractor sin ser atrapada — el extractor solo la crea y la lanza. Quien la
    atrape más arriba decide qué hacer con ella (loguearla, mostrar un mensaje, salir del programa, etc.).

    — "El centinela no juzga al ladrón; solo da la alarma. El juez viene después."
╰───╯

────────────────────────────────────────
● Si, perdon, no lo habia visto y esta en el cap 6 claro. el raise es el que me levanta el error, y despues si el orquestador lo registra
como tal. Mi duda ahora es, como valido ese if o cual seria el codigo que me permita validar que el archivo exista
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Buena pregunta. En Python hay varios caminos para saber si un archivo existe antes de abrirlo. Dos comunes:

    1. Con os.path:
    python
    import os
    os.path.exists(filepath)  # True/False


    2. Con pathlib.Path:
    python
    from pathlib import Path
    Path(filepath).exists()  # True/False


    Ambos te devuelven un booleano. Ahora, la pregunta brujeril es:

    ¿Dónde pones esa guarda dentro de extract()?

    - ¿Antes del with open(...) para evitar que open() siquiera se ejecute si el archivo no existe?
    - ¿O envuelves el open() en un try/except FileNotFoundError y relanzas como DataSourceNotFoundError?

    ¿Cuál crees que es más limpio y por qué?

    — "Hay más de una llave para cada puerta. El mago elige la que no se atasca."
╰──╯

────────────────────────────────────────
● lo pondia justo antes que siquiera intente abrir el arcivho el metodo. Puedes ver el archivo de extractors y ver como lo solucione
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 📖 read      extractors.py  0.1s
  ┊ 📖 preparing read_file…
  ┊ 📖 read      exceptions.py  0.1s

╭─ ⚕ Hermes ─╮
    Bien estructurado. La guarda está justo donde debe — antes del open(). Y el exceptions.py está limpio y claro.

    Dos detalles finos de pulido:

    1. La condición. Esto funciona:
    python
    if os.path.exists(filepath) == False:

    Pero en Python es más natural:
    python
    if not os.path.exists(filepath):


    2. El mensaje de error. El requirements pide inglés profesional (DoD #4):
    - "not founded" → "not found"

    Estos no rompen la funcionalidad, pero son detalles de calidad que saltan en una code review seria.

    Ahora: ¿creaste el test para el caso "archivo no existe → DataSourceNotFoundError"?

    — "El diablo no está en los detalles, está en los detalles que dejas sin probar."
╰──╯
  💾 Self-improvement review: User profile updated

────────────────────────────────────────
● estoy en eso, se que debo probarlo con with pytest.raises, pero no se que poner en el assert o el codigo para que salte el error
correcto
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Es más simple de lo que crees. El patrón para pytest.raises es:

    python
    with pytest.raises(LaExcepcionQueEsperas):
        codigo_que_deberia_lanzarla()


    No necesitas un assert explícito — pytest.raises es la aserción. Si el código dentro del bloque lanza
    DataSourceNotFoundError, el test pasa. Si no lanza nada o lanza otra cosa, el test falla.

    O sea, para tu caso:

    - Instancias un CSVExtractor
    - Llamas extract() con una ruta que no existe — algo como "rutafalsa.csv"
    - Todo eso dentro de with pytest.raises(DataSourceNotFoundError):

    ¿Qué te falta para armarlo? ¿Importar DataSourceNotFoundError en el test? ¿O crees que ya lo tienes claro?

    — "Un test que no prueba el fracaso es un test que solo prueba la mitad del hechizo."
╰───╯

────────────────────────────────────────
● revisa los archivos y dime en que estoy fallando
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 📖 read      test_extractors.py  0.1s

╭─ ⚕ Hermes ──╮
    La estructura se ve correcta. Déjame ejecutarlo para ver qué pasa:

╰───╯
  ┊ 💻 preparing terminal…
  ┊ 💻 $         .venv/bin/python -m pytest tests/test_extractors.py -v  0.2s [exit 2]

╭─ ⚕ Hermes ─╮
    Ahí está el error. Mira la traza:


    src/extractors.py:2: in <module>
        from exceptions import DataSourceNotFoundError
    E   ModuleNotFoundError: No module named 'exceptions'


    El archivo exceptions.py está en src/exceptions.py, pero en extractors.py lo importas como si estuviera en la raíz:

    python
    from exceptions import DataSourceNotFoundError  # ← busca en raíz, no en src/


    Como pyproject.toml apunta pythonpath = ["."] (la raíz rite/), el import debería incluir el paquete:

    python
    from src.exceptions import DataSourceNotFoundError


    O también podrías usar un import relativo ya que ambos archivos viven dentro de src/:

    python
    from .exceptions import DataSourceNotFoundError


    ¿Cuál de los dos crees que es más claro y por qué?

    — "Hasta el mejor hechizo falla si el mago grita el nombre equivocado del ingrediente."
╰──╯
  💾 Self-improvement review: Patched SKILL.md in skill 'dojo-rite-workflow' (1 replacement).

────────────────────────────────────────
● ok, quedo corregido, y lo mejor es dejaro con scr. para que sea mas claro de donde viene el import y no tener que adivinar o mirar
directamente la carpeta raiz. Corri los test y todos en verde
────────────────────────────────────────

  ┊ 💻 preparing terminal…
  ┊ 💻 $         .venv/bin/python -m pytest tests/ -v  0.2s

╭─ ⚕ Hermes ──╮
    3 de 3. Fase 1 completada:


    rite/
    ├── src/
    │   ├── init.py
    │   ├── extractors.py      → AbstractExtractor + CSVExtractor con guarda
    │   └── exceptions.py      → DataSourceNotFoundError
    ├── tests/
    │   └── test_extractors.py → 3 tests ✅✅✅
    ├── data/                  → (aún vacío, el CSV real)
    ├── pyproject.toml
    └── requirements.md


    Resumen de Fase 1 — Extraction Layer: COMPLETA

    | Requisito                                             | Estado |
    |-------------------------------------------------------|--------|
    | AbstractExtractor con extract(filepath) -> list[dict] | ✅     |
    | CSVExtractor que hereda y usa DictReader              | ✅     |
    | DataSourceNotFoundError como excepción de dominio     | ✅     |
    | Guarda de archivo inexistente antes de open()         | ✅     |
    | Test: no se puede instanciar AbstractExtractor        | ✅     |
    | Test: CSVExtractor retorna datos correctos            | ✅     |
    | Test: ruta inválida lanza DataSourceNotFoundError     | ✅     |

    ¿Descansas aquí o te animas con la Fase 2 — Domain Entities (Transaction, Income, Expense)?

    — "Tres velas encendidas, tres sombras derrotadas. El boss respira, pero no cae solo."
╰──╯

────────────────────────────────────────
● Ok, voy a dejar escrito que lo que haria en la fase 2. Esta fase pide crear objetos de las transacciones en vez de simples diccionarios.
Para ello se debe crear una clase padre que sera Transaction con propiedades de amount y date. Como indica el requeriment, seria una clase
abstracta tambien, donde, si no estoy mal, se inicializa con self tambine. Aqui no entiendo exactamente a que se refiere con sobreescribir
el mentodo de representacion. Seria un metodo exclusivo para ver unicamente los incomes o expenses con la fecha y ya? El testting tambien
seria rapido porque solo se valida que sean instacias correctas y que los metodos retornen los valores con el signo correcto
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    Buena reflexión. Vamos a desglosar tu duda clave:

    "Sobrescribir el método de representación"

    En Python, los objetos tienen métodos "mágicos" (dunder) que controlan cómo se ven cuando los imprimes. Los dos principales son:

    - str() → lo que ve el humano cuando haces print(objeto)
    - repr() → la representación "oficial" del objeto (ideal para debugging)

    El requirements pide "formatos limpios" para imprimir. Así que cuando hagas:

    python
    income = Income(amount=5000, date="2024-01-15")
    print(income)


    Debería salir algo legible, no <main.Income object at 0x...>.

    Ahora, lo otro que mencionaste: "clase abstracta con self". Una abstracta puede tener init perfectamente — de hecho, si
    Transaction tiene amount y date como atributos comunes, el constructor puede vivir en la clase padre y las hijas llamarlo con
    super().init(). Lo único que hace a una clase abstracta es tener al menos un @abstractmethod.

    Pregunta brujeril: ¿Qué método crees que debería ser abstracto en Transaction para forzar que Income y Expense devuelvan
    el amount con su signo correcto? ¿O crees que el init es suficiente y el signo se resuelve solo en las subclases?

    — "El molde define la forma, pero el material decide cómo brilla."
╰──╯

────────────────────────────────────────
● como la clase padre solo recibe el amount y el date, creeria yo que el signo se resuelve en la subclase especifica. La clase abstracta
tecnicamente no tendria esa logica guardada ahi, solo el metodo de exposicion, no? Y ahi esta otra duda entonces, esa nueva exposicion,
seria tecnicamente hardcodeada directamente en un print para que no sea automatica, si?
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Buenas preguntas. Vamos por partes.

    Sobre el signo: Estás en lo correcto. La clase padre sabe que existe amount, pero no sabe qué tipo de transacción es. La
    lógica del signo vive en cada subclase — Income devuelve amount positivo, Expense devuelve amount negativo.

    Sobre la representación y "hardcodeada en un print":

    Aquí hay un matiz importante. No es que la clase tenga un print() dentro. Es que Python tiene métodos dunder que print()
    llama automáticamente.

    Cuando escribes:

    python
    print(income)


    Python internamente hace: print(income.str()) o print(str(income)).

    El método str retorna un string — no imprime nada él mismo. La clase construye el string, y quien lo recibe decide si lo
    imprime, lo guarda en un archivo, o lo envía por un tubo mágico.

    La pregunta clave: ¿Qué necesitas retornar en str para que Income y Expense se vean diferente? ¿Debería cada subclase
    tener su propio str o puedes poner uno genérico en Transaction y que el polimorfismo haga el trabajo sucio?

    — "El espejo no grita tu reflejo; solo lo muestra. El mago decide qué hacer con lo que ve."
╰──╯

────────────────────────────────────────
● A ver, regresemos una capa tecnica atras. Lo que estoy entendiendo es que en esta fase me estan pidiendo que cree un metodo especifico
que me imprima los datos de esa transaccion en un formato limpio, no se, se me ocurre un .show. En ese caso, el metodo show seria el
encargado de mostrar los datos, pero dentro de cada subclase, se tendria la logica para que se maneje el signo correcto de cada
trasaccion.
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Entiendo por dónde vas. Un método .show() funcionaría, claro. Pero el requirements dice textual:

    > "Sobrescribir el método de representación"

    No dice "crear un método nuevo". Dice sobrescribir, que en POO significa reemplazar un método que ya existe heredado de una
    clase superior.

    Todo objeto en Python ya viene con métodos de representación heredados de object (la clase más base de todas). Por ejemplo,
    cuando haces print(objeto), Python busca un método específico que todo objeto tiene por defecto. El problema es que la versión
    heredada muestra algo como <main.Income object at 0x10a3b2...> — que no es precisamente un "formato limpio".

    Pregunta: ¿Qué método crees que busca print() automáticamente cuando le pasas un objeto? Uno que todo objeto ya tiene y que
    puedes sobrescribir sin necesidad de crear un .show() desde cero.

    Pista: es un método dunder, como los que viste en el Cap 02.

    — "Un mago no inventa un nuevo idioma para hablar con su dragón; le enseña las palabras que el dragón ya entiende."
╰──╯

────────────────────────────────────────
● Seria con poliformismo, pero no se cual seria el metodo para modificar entonces ese print
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Vamos a Cap 02 del lore — 02-domain-entities-and-dataclasses.md. Ahí cubren exactamente esto. Los dunder methods para
    representación.

    Pista más clara: el método que print() llama automáticamente se llama como  + algo + . En el lore del Cap 02 hay dos: uno
    para humanos y otro para debugging. El que necesitas para print() es el que busca una salida legible.

    Si quieres, ábrelo tú:

    lore/02-domain-entities-and-dataclasses.md

    O dime si prefieres que lo lea yo y te resuelva esa pieza concreta.

    — "La respuesta ya la estudiaste, solo está esperando que la recuerdes desde el estante correcto de tu memoria."
╰──╯

────────────────────────────────────────
● lee el lore de ese capitulo porque yo no lo veo ahi
────────────────────────────────────────

  ┊ 📖 preparing read_file…
  ┊ 📖 read      02-domain-entities-and-dataclasses.md  0.1s

╭─ ⚕ Hermes ─╮
    Tienes razón, el lore del Cap 02 no habla explícitamente de cómo sobrescribir la representación. Vamos a las quests de ese capítulo
    a ver si allí aparece:

╰───╯
  ┊ 💻 preparing terminal…
  ┊ 💻 $         ls /Users/ander/Documents/DoJo/DoJo_Study/subjects/python/chronicles/PY-POO/quests/02-entities/  0.1s
  ┊ 📖 preparing read_file…
  ┊ 📖 preparing read_file…
  ┊ 📖 read      01-dataclass-creation.md  0.1s
  ┊ 📖 read      02-polymorphism-test.md  0.1s
  ┊ 📖 preparing read_file…
  ┊ 📖 read      07-cli-and-production.md  0.1s

╭─ ⚕ Hermes ─╮
    Tienes razón, el lore del Cap 02 no lo cubre. str no aparece explícitamente en los materiales de PY-POO. Vamos directo al
    grano entonces:

    str es el método que Python busca automáticamente cuando haces print(objeto) o str(objeto). Todo objeto lo hereda de
    object, pero la versión por defecto muestra algo como <src.entities.Income object at 0x10a3b2...>.

    Para sobrescribirlo, simplemente lo defines en tu clase retornando un string:

    python
    def str(self) -> str:
        return f"Algo legible aquí"


    Importante: str retorna un string, no hace print(). Es la función print() quien recibe ese string y lo muestra en
    pantalla.

    Ahora, para tu caso concreto — Transaction, Income, Expense:

    - Transaction puede definir str con un formato base
    - Income y Expense pueden sobrescribirlo para incluir su signo (positivo/negativo)
    - Cada subclase retorna un string con la información que quieras mostrar

    ¿Qué te gustaría que muestre el str de un Income o Expense? Por ejemplo, ¿algo como Income: +$5000.00 on 2024-01-15? ¿O
    prefieres otro formato?

    — "El hechizo que faltaba no estaba en el grimorio; estaba en la memoria colectiva de todo mago que usó Python."
╰───╯

────────────────────────────────────────
● Ok no, estoy verificando con el DM este error en la concepcion del rite, ya que el rite deberia justificar unicamente lo que se vio en
el lore de los capitulos, por lo que se elimino ese requerimiento como otro ambiguo en la fase 3.
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Entendido. Tiene toda la lógica del mundo — el Rite solo debe evaluar lo que el lore enseñó, y str no apareció en ningún
    lado. Bien tirado del hilo por parte del DM.

    Entonces la Fase 2 queda ajustada:

    Fase 2 — Domain Entities (post-auditoría del DM)

    | Requisito                                     | Estado       |
    |-----------------------------------------------|--------------|
    | Clase abstracta Transaction con amount y date | ⬜ Pendiente |
    | Income que hereda de Transaction              | ⬜ Pendiente |
    | Expense que hereda de Transaction             | ⬜ Pendiente |
    | Income devuelve amount positivo               | ⬜ Pendiente |
    | Expense devuelve amount negativo              | ⬜ Pendiente |
    | Test: instancias correctas                    | ⬜ Pendiente |
    | Test: ambas son subclases de Transaction      | ⬜ Pendiente |
    | Test: signo correcto                          | ⬜ Pendiente |
    | Sobrescribir método de representación         | ❌ Eliminado |

    ¿Quieres que revisemos el diseño antes de que escribas código, o prefieres lanzarte directamente?

    — "Un Rite no mide lo que el mago no aprendió. Mide lo que el grimorio realmente enseñó."
╰──╯

────────────────────────────────────────
● No, entonces regresemos a lo que ya habia comentado, no habria mas que hacer, verdad?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    No, tienes razón. Una vez quitado str, la Fase 2 es muy directa:

    1. Transaction (abstracta) con amount y date en el init
    2. Income(Transaction) — amount positivo
    3. Expense(Transaction) — amount negativo
    4. Tests de instanciación, isinstance y signo

    Es prácticamente el mismo patrón que ya hiciste en la quest 02-polymorphism-test.md con Employee → Developer, Manager, pero
    adaptado a transacciones.

    ¿Arrancas tú con el código y cuando tengas algo me llamas para revisar?

    — "A veces el conjuro más poderoso es el que sabes que puedes lanzar sin pensarlo dos veces."
╰───╯
  💾 Self-improvement review: Memory updated · User profile updated

────────────────────────────────────────
● OK, en ese caso lo puedo hacer relativamente rapido y ya. Mi duda, creeria que va todo en un nuevo archivo, pensaria yo quizas llamado
transactions.py, no?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    transactions.py me parece perfecto. Está dentro de src/ y es claro de lo que trata.


    rite/src/
    ├── init.py
    ├── exceptions.py
    ├── extractors.py
    └── transactions.py    ← nueva


    Adelante, cuando lo tengas lo reviso.

    — "Un archivo, un propósito. La biblioteca crece un libro a la vez."
╰──╯

────────────────────────────────────────
● aca mi duda es, que metodo van a manejar estas clases? seria como un save?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    Buena pregunta. A ver, voltéalo al revés: ¿qué crees que va a validar el test?

    El requirements dice:

    > Validar que cada una retorna su amount con el signo esperado (positivo para Income, negativo para Expense).

    Es decir, en el test alguien va a preguntarle a un Income o Expense: "¿cuánto vales?" y esperar una respuesta con signo.

    Pregunta: Si Transaction recibe amount en el init, y tanto Income como Expense lo heredan... ¿cómo sabe Expense
    que debe devolver su amount con signo negativo? ¿Dónde se define esa diferencia?

    Pista: el mismo patrón que usaste en la quest del Cap 02, donde Employee tenía un método abstracto calculate_bonus() y
    Developer vs Manager calculaban distinto.

    — "El molde sabe que tendrá una forma, pero no cuál. Eso lo deciden quienes heredan el molde."
╰───╯

────────────────────────────────────────
● Que seria, una correcion de signo? En ese caso, no?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    Exacto, una corrección de signo. Pero la pregunta es: ¿dónde vives esa corrección?

    Piénsalo así:

    - Income recibe amount=5000 → debe devolver +5000
    - Expense recibe amount=120.50 → debe devolver -120.50

    Si metes esa lógica en Transaction, la clase padre tendría que saber si es Income o Expense... y eso no es buena idea (la clase
    padre no debería conocer a sus hijas).

    Entonces: ¿dónde crees que debe vivir esa "corrección de signo"? ¿En un método específico? ¿En una propiedad? ¿Directo en el
    atributo?

    Pista: en la quest de Employee tenías un método calculate_bonus() que era abstracto y cada subclase lo implementaba diferente.
    Aquí el patrón sería el mismo, pero para el signo del amount.

    — "El padre da la herencia. Los hijos deciden cómo gastarla."
╰───╯

────────────────────────────────────────
● en cada clase, pero la clase padre va a tener el metodo abstracto y la inicializacion de los paramentros.
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Esa es la idea. La estructura queda:


    Transaction (ABC)
    ├── init(self, amount, date)    ← atributos comunes
    ├── @abstractmethod
    │   firma_que_retorna_el_monto()    ← cada hija lo implementa
    │
    ├── Income                          ← amount positivo
    └── Expense                         ← amount negativo


    ¿Qué nombre le pondrías al método abstracto? Algo que lea natural cuando en el test escribas:

    python
    income = Income(amount=5000, date="2024-01-15")
    assert income.tu_metodo() == 5000


    — "Nombrar un conjuro es casi tan importante como lanzarlo. Un mal nombre confunde hasta al mago que lo creó."
╰───╯

────────────────────────────────────────
● nombres explicitos, no? como seria en ingles; correction_sign?
────────────────────────────────────────


╭─ ⚕ Hermes ──╮
    correction_sign no es inglés natural. Piénsalo como si hablaras con otro ingeniero:

    "Give me the amount, but with the correct sign".

    En inglés financiero, quedaría natural como:

    - signed_amount → "el monto con su signo"
    - get_signed_amount → "obtén el monto firmado"

    De las dos, ¿cuál sientes más "pythonica"?

    — "El inglés técnico es como un conjuro: pocas palabras, mucho significado."
╰────╯

────────────────────────────────────────
● la opcion dos. Pero para poner el positivo en income, lo pensaria con un abs(), pero para el negativo, seria return -self.amount,
funcionaria? Porque en ese caso estaria asumiendo que los numeros vienen sin signo
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Funcionaría perfectamente. Asumiendo que el monto llega siempre positivo desde el CSV, el Income lo deja positivo y el Expense
    lo invierte con -self.amount.

    Lo que estás diseñando es:

    python
    class Income(Transaction):
        def get_signed_amount(self) -> float:
            return abs(self.amount)        # blindaje anti-negativos

    class Expense(Transaction):
        def get_signed_amount(self) -> float:
            return -self.amount            # siempre negativo


    El abs() en Income es un guardia extra: aunque alguien pase un amount negativo por error, Income lo fuerza a positivo. Buen
    detalle defensivo.

    ¿Te animas a escribirlo y cuando tengas los tests los revisamos?

    — "Un buen guardián no solo vigila la puerta; se asegura de que quien entre lo haga por el lado correcto."
╰────╯

────────────────────────────────────────
● esta escrito el codigo, y voy a verificarlo con los test, pero tengo la duda, para verificar las instancias, creo un objeto raw?
────────────────────────────────────────


╭─ ⚕ Hermes ─╮
    Exacto. No necesitas fixture para esto — las entidades de dominio son objetos simples. Creas la instancia directamente con los
    parámetros y validas:

    python
    income = Income(amount=5000.0, date="2024-01-15")
    expense = Expense(amount=120.50, date="2024-01-20")

    ¿Income es una Transaction? → True
    ¿Expense es una Transaction? → True
    ¿Income.get_signed_amount() es positivo? → True
    ¿Expense.get_signed_amount() es negativo? → True


    Sin mocks, sin archivos temporales, sin fixtures — solo datos puros. Escribe el test, lo corres, y si algo falla lo revisamos.

    *— "Las entidades de dominio son como los golems de barro: los creas, les das datos, y responden sin necesidad de rituales
    adicionales."*
╰───╯

────────────────────────────────────────
● hecho todo, codigo y test. Y test en verde
────────────────────────────────────────

  ┊ 💻 preparing terminal…
  ┊ 💻 $         .venv/bin/python -m pytest tests/ -v  0.2s
  ┊ 📖 preparing read_file…
  ┊ 📖 preparing read_file…
  ┊ 📖 read      transactions.py  0.1s
  ┊ 📖 read      test_transactions.py  0.1s

╭─ ⚕ Hermes ──╮
    Limpio y directo. 4 verdes en total:


    Phase 1 — Extraction Layer ✅
    ├── test_cannot_instantiate_abstract_class  ✅
    ├── test_csv_extractor_returns_data         ✅
    └── test_data_source_not_found_error        ✅

    Phase 2 — Domain Entities ✅
    └── test_isinstance_of_transactions         ✅


    Estado del proyecto:


    rite/
    ├── src/
    │   ├── init.py
    │   ├── exceptions.py         → DataSourceNotFoundError
    │   ├── extractors.py         → AbstractExtractor + CSVExtractor
    │   └── transactions.py       → Transaction, Income, Expense
    ├── tests/
    │   ├── test_extractors.py    → 3 tests
    │   └── test_transactions.py  → 1 test
    ├── pyproject.toml
    └── requirements.md


    ¿Pasamos a Fase 3 — Transformation Engine con AnalyticsEngine y sus @pytest.fixture?

    — "Dos jefes de zona caídos. El corazón del dungeon late más fuerte."

</details>