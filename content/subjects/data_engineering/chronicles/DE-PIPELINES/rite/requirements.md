# Rito de Paso: El Gran Pipeline del Gremio de Alquimistas

## Contexto del Proyecto (Domain Shifting: Alquimia)
El Gremio de Alquimistas de Ankh-Morpork te ha ascendido a Ingeniero Arcano de Datos. El mercado de ingredientes es caótico y los maestros alquimistas necesitan un inventario centralizado y purificado para planificar la producción de pociones del mes. 

Tu misión es construir un pipeline de datos automatizado y orquestado que conecte el catálogo clandestino del Mercado Negro con la Gran Bóveda Relacional del Gremio.

Este Rito se divide en Fases Desbloqueables. No puedes avanzar a la siguiente sin dominar la anterior.

---

## Fases del Proyecto

### Fase 0: Architecture First
Antes de escribir cualquier línea de código, debes diseñar la solución.
- **Requisito 1:** Documentar tu propuesta de arquitectura y flujo de datos en el `journal.md`.
- **Requisito 2:** Validar esta arquitectura con tu mentor (Witch/Tutor) antes de proceder a la implementación.

### Fase 1: La Zona Bronze y la Extracción (Capítulo 00 y 01)
Debes conectarte a la API del Mercado Negro y almacenar los datos crudos en la Zona Bronze.

- **Requisito 1:** Usar la librería `requests` para extraer el catálogo de ingredientes desde una API REST simulada (o servidor local provisto por tu mentor).
- **Requisito 2:** Debes autenticarte enviando tu Token del Gremio en los `Headers` de la petición.
- **Requisito 3:** Manejar correctamente los códigos de estado HTTP (usar `raise_for_status()`).
- **Requisito 4:** Guardar esta respuesta cruda. Esta es tu **Zona Bronze**. Es inmutable.
- **Requisito 5:** Al finalizar esta fase, realiza un Semantic Commit evidenciando tu progreso.

### Fase 2: Transformación Inicial (Capítulo 02)
Los datos que vienen del Mercado Negro están sucios, tienen nulos y los precios están como texto.

- **Requisito 1:** Usar `pandas` para transformar la Zona Bronze.
- **Requisito 2:** Aplicar transformaciones vectorizadas para eliminar todas las filas que contengan algún valor nulo.
- **Requisito 3:** Normalizar la columna de nombres de los ingredientes (quitar espacios en los bordes y pasar todo a minúsculas).
- **Requisito 4:** Castear la columna del precio para que sea estrictamente de tipo entero.
- **Requisito 5:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 3: Los Portones de Calidad y la Zona Silver (Capítulo 03)
El Gremio te demandará si les das datos erróneos o duplicados.

- **Requisito 1:** Implementar un Quality Gate de reconciliación usando aserciones nativas. Comprobar que tras la limpieza (Fase 2), la pérdida de registros no sea mayor al 10% respecto al tamaño original (Bronze).
- **Requisito 2:** Eliminar registros exactamente duplicados (filas idénticas en todas sus columnas, como recibos pasados dos veces por el mensajero).
- **Requisito 3:** Implementar un Gate que valide que ya no existe absolutamente ningún nulo en las columnas críticas.
- **Requisito 4:** Esta data validada será tu **Zona Silver**.
- **Requisito 5:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 4: La Zona Gold y el Gran Archivo (Capítulo 04)
Los datos limpios y auditados deben guardarse para consulta.

- **Requisito 1:** Usar Pandas para agregar los datos de la Zona Silver (por ejemplo, calcular el stock total por ingrediente). Esta información agregada para negocio será tu **Zona Gold**.
- **Requisito 2:** Usar `SQLAlchemy` para crear un engine de conexión (puedes usar SQLite en memoria o un archivo local para efectos de este Rito: `sqlite:///guild.db`).
- **Requisito 3:** Utilizar Pandas para cargar tu DataFrame Gold a una tabla llamada `clean_inventory`.
- **Requisito 4:** La inserción debe anexar datos sin destruir la tabla y no debe incluir el índice de Pandas.
- **Requisito 5:** Ejecutar una consulta SQL cruda para verificar por consola que los datos se insertaron correctamente.
- **Requisito 6:** Al finalizar esta fase, realiza un Semantic Commit.

### Fase 5: El Gran Maestro Orquestador (Capítulo 05)
El pipeline completo debe ejecutarse por sí solo. 

- **Requisito 1:** Refactorizar tu código aislando la lógica en distintas funciones, y decorándolas con `@task` de `prefect`.
- **Requisito 2:** Agregar a tu tarea de Extracción (Fase 1) la capacidad de reintento, simulando que la conexión al Mercado Negro es inestable.
- **Requisito 3:** Crear una función principal decorada con `@flow` que orqueste secuencialmente todas las tareas.
- **Requisito 4:** Ejecutar el Flow completo y evidenciar los logs de Prefect en tu terminal.
- **Requisito 5:** Al finalizar esta fase, realiza un Semantic Commit.

---

## Criterios de Éxito y Evaluación
- **Independencia Funcional:** El pipeline entero debe poder ejecutarse con un solo comando o corriendo un solo script.
- **Testing y Validaciones (DoD #3):** Todo el desarrollo debe haber sido construido guiado por pruebas (TDD con `pytest`), debes validar estrictamente los tipos (`mypy`), e incluir un logging forense adecuado (evitando el uso de simples `print`).
- **Manejo de Errores:** Si el Quality Gate falla, el pipeline debe detenerse abruptamente con un mensaje claro, evitando cargar basura en la base de datos.
- **Transparencia:** Durante el desarrollo del Rito, todo bloqueo mental, bug encontrado y decisión técnica DEBE estar documentada en tu `journal.md`.

¡Que la alquimia de datos te sea favorable, Operador!
