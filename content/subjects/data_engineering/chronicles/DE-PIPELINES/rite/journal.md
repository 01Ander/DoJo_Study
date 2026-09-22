# Bitácora del Rito (Journal)

Este documento es tu diario técnico durante el desarrollo del Rito. 
Usa este espacio para registrar:
1. **Errores Encontrados:** El traceback del error y por qué crees que ocurrió.
2. **Decisiones Técnicas:** Por ejemplo, ¿cómo estructuraste tus tests (TDD)? ¿Cómo manejaste los duplicados en Pandas?
3. **Bloqueos:** Si te trabas, escribe aquí tu proceso de pensamiento (Duck Debugging).
4. **Diseño (Architecture First):** Documenta aquí tu propuesta de flujo antes de programar la Fase 1.

---

## 2026-09-21 - Inicio del Proyecto


## 2026-09-21 - Fase 0: Architecture First
1. Patrón arquitectónico
   - ELT con arquitectura Medallion (zonas Bronze / Silver / Gold).
   - La "L" del ELT es Bronze: el crudo se guarda tal cual llega desde la API.
   - La escritura a la base en Fase 4 no es la L: se nombra save/publish del Gold.

2. Responsabilidades y dónde viven (una responsabilidad = un archivo)
   - Comunicación con la API, incluyendo persistir el crudo en Bronze → Fase 1
   - Limpieza y transformación → Fase 2
   - Validación de calidad → Fase 3
   - Agregación (Gold) → Fase 4
   - Escritura en base (save) → Fase 4
   - Coordinación → el flow, en Fase 5

3. Jerarquía de ejecución
   - Las tareas son las unidades de trabajo; el flow es quien las llama.
   - El flow vive en su propio archivo e importa las tareas de los demás módulos.

4. Regla de parada
   - Si una etapa falla, el pipeline se detiene ahí. No se avanza con un proceso fallido. [excepción acotada: los reintentos de la Fase 5 aplican solo a fallos transitorios, se define en esa fase].

5. Flujo de datos
	1.  extract — trae el catálogo desde la API. No produce zona todavía, produce datos en memoria.
	2. load — guarda el crudo tal cual llegó. Produce Bronze (archivo inmutable).
	3. transform — limpia, normaliza nombres, castea el precio. Produce Silver.
	4. verify — los portones de calidad. No produce zona: produce una decisión (pasa o se aborta).
	5. aggregate — agrupa el Silver y calcula los totales por ingrediente. Produce Gold.
	6. save — escribe el Gold en la tabla clean_inventory.

6. Zonas
    - Bronze = archivo. Silver y Gold: forma pendiente, se decide en su fase.
    - Decisión: Bronze = un archivo por corrida, con marca de tiempo. Append-only.
	- Justificación: honra el Requisito 4 literal + reconciliación de Fase 3 + patrón de industria.
	- Consecuencia arquitectónica: la ruta del archivo viaja como valor entre etapas; no se descubre buscando en el disco.



## 2026-09-21 - Fase 1: La Zona Bronze y la Extracción
1. Se solicita la conexion a una API (dummi) // o catalogo de servidor local. La desicion se tomara con Witch para verificar mejor uso y correcta asimilacion de conceptos.  Se debe manejar datos en zona Bronze, carga de datos tal cual vienen del exterior. Manejo de estados. 
2. Se disenara un ELT con el uso de requests. No se hace mencion a paginacion por lo que se tomara como no necesario. Los datos dummi seran suficientes para no requerir paginacion en este caso. 
### 2026-09-22 
3. Al realizar el planteamiento de la fase 0 se designa una carga LOAD en zona bronze; esta fase implementa el extract y load. 
	- Desicion: API simulada con responses.
	- Justificación: estándar de industria para testear clientes HTTP + hermético + criterio de "un solo comando" + los reintentos de Fase 5 se disparan con excepciones reales de la pila requests.
	- Consecuencia: extract recibe api_url y token por parámetro.
4. Archivo Bronze — dónde vive y cómo se llama
	   - Directorio: data/, en la raíz de rite/. Los artefactos de datos no viven junto al código (src/).
	   - El pipeline crea el árbol de carpetas si no existe, y no falla si ya existe. La carpeta no depende de venir en el repositorio: git no versiona directorios vacíos.
	   - Nombre: solo la marca de tiempo, sin texto. Precisión de segundos con milésimas y ancho fijo, para que el orden alfabético coincida con el cronológico.
	   - Zona horaria: UTC. Decisión tomada para que el pipeline no dependa de la zona horaria de la máquina o del servidor donde corra.
	   - Extensión .json. Contenido: la respuesta cruda de la API, tal cual, sin reformatear.
	   - Criterio de nombres por zona: el crudo no lleva texto, solo la fecha. Los datos procesados (Silver/Gold) llevarán un prefijo de texto antes de la fecha. El nombre del archivo es el marcador de zona.
	   - Descartado: dejar la carpeta creada en el repositorio. Obligaría a un archivo fantasma para que git la conserve, y el pipeline no debe depender de eso.
5. Configuración de la API (URL y token)
   - Decisión: constantes escritas directamente en el código.
   - Justificación: el Rite consolida los conceptos del lore, y la gestión de secretos (variables de entorno, config externa) no forma parte de esta chronicle. Se implementa el manejo de credenciales tal como lo enseña el Capítulo 01.
   - Deuda declarada: hardcodear un token es mala práctica en producción. Se revisa cuando el syllabus cubra configuración y secretos.
   - Forma: URL y token viven en un único módulo, no repartidos entre archivos, para que una futura migración a entorno sea un solo punto de cambio.

6. Token vacío o inválido
   - Decisión: no se valida antes de la petición. Se deja que la API responda con error de estado y que raise_for_status() levante la excepción.
   - Justificación: coherente con el Capítulo 01 y con la regla de parada de la Fase 0 — el pipeline se detiene en el punto donde falla, sin avanzar con datos que no llegaron.

7. Propagación del error y observabilidad de la etapa
   - Decisión: la excepción de raise_for_status() se propaga sin capturarse. Ninguna etapa de la Fase 1 la intercepta.
   - Justificación: coherente con la regla de parada de la Fase 0. Quien decide qué hacer con el fallo es el flow, en la Fase 5.
   - Decisión: la etapa registra ambas cosas — la cantidad de registros obtenidos y la ruta donde quedó el archivo crudo.
   - Justificación: DoD #3 exige logging forense. Sin registro, la Fase 3 no tiene testigo con qué reconciliar.

8. Header de autenticación
   - El token viaja en el header Authorization, con formato Bearer <token>.

##2026-09-22 - Fase 1: Cierre técnico (Zona Bronze y Extracción)

Estado: 5 tests en verde y mypy src sin observaciones (3 módulos). Requisitos 1 a 4
cubiertos. Pendiente: Requisito 5 (commit semántico).

Estructura creada
- src/config.py: MARKET_URL, MARKET_TOKEN, BRONZE_DIR = "data". Único hogar de los ajustes.
- src/extract.py: fetch_market(catalog_url, market_token) y load_raw(payload, target_dir).
- tests/test_pipeline.py: un solo archivo de tests, consistente con la decisión de la Fase 0.
- tests/fixtures/market_catalog.json: los datos de prueba.
- pyproject.toml: pythonpath = ["."] (resuelve los imports de src) y mypy apuntando a src.

Decisiones de esta fase
- Nombres: la cadena de la Fase 0 dice extract y load; en código son fetch_market y
  load_raw. Mapeo directo, para que no parezcan dos proyectos distintos.
- Guardar el crudo: re-serializado. load_raw escribe el payload con json.dump, no los
  bytes literales de la respuesta. Costo declarado: el contenido se preserva, la representación
  se regenera. La Fase 2 parsea el archivo igual, así que la fidelidad de bytes no aporta nada aquí.
- Ruta de Bronze: relativa ("data"). Se resuelve contra el directorio de ejecución, así que
  el pipeline se corre desde la raíz de rite/. Se descartó anclar la ruta al proyecto.
- Datos de prueba: archivo externo y sucio a propósito. 10 registros con un nulo (para el
  dropna de la Fase 2), precios como texto (para el casteo), espacios y mayúsculas
  inconsistentes (para la normalización) y dos duplicados que solo se detectan después de
  normalizar (para la deduplicación de la Fase 3). El cálculo no es casual: 10 registros con un
  nulo dan exactamente 10% de pérdida, justo en el borde del portón de la Fase 3.

Guía nueva: lo que el lore no tenía resuelto
El Capítulo 01 enseña a devolver la lista (data.get("ingredients", [])). El Requisito 4
obliga a conservar la respuesta completa, y esa diferencia arrastró trabajo que el lore no
cubría:
- La extracción devuelve el cuerpo entero, así que los asserts atraviesan un nivel más
  (result["results"][0]["name"]) en lugar de contar el valor recibido.
- El payload de prueba se carga desde un archivo, no escrito en línea en el test.
- El Requisito 2 (token en headers) se prueba inspeccionando la petición interceptada por
  responses (responses.calls[0].request.headers), algo que el lore no menciona.
- El guardado se prueba con tmp_path (directorio recibido por parámetro) y con una comprobación
  de ida y vuelta: se lee el archivo y se compara contra el payload original.
- Se agregó un quinto test derivado de la Fase 0: dos guardados consecutivos dejan dos archivos,
  con nombres distintos y en orden alfabético creciente. Prueba el append-only y que el orden
  alfabético coincide con el cronológico.
- El logging forense no se testea (caplog no está en el lore); se verifica en la corrida.

Errores encontrados
1. src/init.py en lugar de src/init.py: el marcador de paquete lleva doble guion bajo.
   Los imports igual resolvían (namespace packages de Python 3), pero el archivo no cumplía
   ninguna función.
2. ImportError: cannot import name 'fetch_market' from 'src.extract': el módulo se encontró en
   la ruta correcta y estaba vacío. Rojo por la razón correcta (TDD), no un problema de entorno —
   y de paso confirmó que pyproject.toml, pythonpath y los imports estaban bien.
3. no tests ran: pytest recolecta por patrón de nombre (test_*.py o *_test.py), no por
   carpeta. tests.py y tests_pipeline.py no coinciden con el patrón. La carpeta se llama
   tests/ (plural) y el prefijo del archivo es test_ (singular).

Pendiente
- Requisito 5: commit semántico de la fase.

## [Fecha] - Fase 2: Transformación Inicial
...

## [Fecha] - Fase 3: Los Portones de Calidad y la Zona Silver
...

## [Fecha] - Fase 4: La Zona Gold y el Gran Archivo
...

## [Fecha] - Fase 5: El Gran Maestro Orquestador
...
