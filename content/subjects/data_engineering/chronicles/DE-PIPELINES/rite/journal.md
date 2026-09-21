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
Se solicita la conexion a una API (dummi) // o catalogo de servidor local. La desicion se tomara con Witch para verificar mejor uso y correcta asimilacion de conceptos. 
Se debe manejar datos en zona Bronze, carga de datos tal cual vienen del exterior. Manejo de estados. 
Se disenara un ELT con el uso de requests. No se hace mencion a paginacion por lo que se tomara como no necesario. Los datos dummi seran suficientes para no requerir paginacion en este caso. 

## [Fecha] - Fase 2: Transformación Inicial
...

## [Fecha] - Fase 3: Los Portones de Calidad y la Zona Silver
...

## [Fecha] - Fase 4: La Zona Gold y el Gran Archivo
...

## [Fecha] - Fase 5: El Gran Maestro Orquestador
...
