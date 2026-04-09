# 09 - The DoJo Agent & Operator CLI

## ¿Qué es el DoJo Agent?

Es el componente "vivo" e interactivo del ecosistema DoJo. Inicialmente un vigía pasivo, ha evolucionado a un **Middleware Operator** (CLI) y un *Pair Programmer* que tiene lectura instantánea a toda la base de datos de tu estudio (RAG) para acompañar la redacción de código, documentar sesiones e inspeccionar requerimientos.

El objetivo del Agente es reducir la carga cognitiva (*Protocol Yellow*), actuando como múltiples *Personas* dependiendo de tus necesidades de estudio y blindando el flujo técnico sin alucinaciones de internet.

---

## Arquitectura (Engine & Operator)

El sistema opera mediante tres barreras técnicas en tiempo real:

1. **La Mente (Local LLM & RAG Vectorial):** Corre `gemma4:latest` (Ollama) con embeddings espaciales (`ChromaDB`). Tiene memoria conversacional de corto plazo (Rolling Window) para seguir hilos de Pair Programming sin consumir toda tu memoria RAM.
2. **El Operador (Hybrid RAG & Episodic Memory):** Actúa como un Middleware que intercepta NLP y Slash Commands. No depende solo de vectores; si hay una misión activa, **inyecta físicamente** el contenido de `requirements.md` y las últimas 10 líneas de tu `journal.md` actual para garantizar una memoria inter-sesión inquebrantable.

3. **The Watcher (Watchdog Atómico):** Indexa cambios en tiempo real ("tatuando" la ruta del archivo en el contenido para máxima precisión de búsqueda semántica) e ignora ruidos de sistema.

> *(Nota Arquitectónica: La base de datos `dojo_agent/chroma_db` y el entorno `.venv` residen estrictamente en local y están excluidos en `.gitignore`).*

---

## Modos Dinámicos de Operación (`/mode`)

Con el comando `/mode [MODO]`, puedes resetear la memoria de corto plazo de la terminal e instruir a la base lingüística de `gemma` para que asuma las reglas estipuladas en el documento `05-estructura-chats`:

*   **`/mode main` (El Instructor):** Explicará la teoría arquitectónica general. Tiene prohibido darte código fuente directo. Flexibilidad bilingüe permitida.
*   **`/mode exercises` (El PM):** Se convertirá en un Product Manager hiper-conciso para generar Criterios de Aceptación y designar los *Edge Cases* a testear en la misión actual. (Inglés prioritario).
*   **`/mode work` (El Revisor):** Revisa el Clean Code y las arquitecturas complejas actuando como un Senior exigente. Evalúa TDD y Profiling de datos.
*   **`/mode think` (El Analista Fellow):** Un modo de razonamiento libre. Ofrece opiniones, perspectivas subjetivas y debate sobre la filosofía del sistema y tu progreso.

---

## Flujo Operativo y Context Binding (NLP)

Tu flujo de ejecución diario obedece a anclar el "Contexto" de la CLI para que sus extracciones RAG (`k=6`) no choquen matemáticamente con otras carpetas. 

### 1. Despliegue de Terminal
Abre tu consola en la raíz de `DoJo_Study` y arranca:
```bash
./dojo_agent/.venv/bin/python dojo_agent/main.py
```

### 2. Anclaje de Contexto (Context Binding)
Con esto, le avisas al Operator qué partes del RAG debe priorizar:
*   **Vía NLP:** Escribiendo directamente: *"Vamos a iniciar en PY-BASICO la mision B00"*. (Detecta dinámicamente las rutas y asume la carga física de documentos).
*   **Vía Slash:** `/start [Campaña] [Misión]`

### 3. Ejecución y Bitácoras
Habiendo fijado el contexto, toda respuesta extensa que el Agente RAG genere por consola, será **silenciosamente guardada en el archivo `journal.md` de tu misión actual** a modo de bitácora cronológica pasiva. 

Si requieres emitir tus propios pensamientos de aprendizaje, puedes forzar el guardado ejecutando:
*   `/log No logro entender cómo funciona la herencia aquí. Voy a detener el flujo y reiniciar mañana.`

### 4. Zero-Cost Auditing (Offline Payload)
Si localmente no logras descifrar un problema y requieres enviar tu duda a Gemini Web (Cloud), no necesitas copiar y pegar archivos a mano. Ejecuta:
*   `/audit ¿Por qué falla inyección de dependencias en esta línea?`

El operador compilará tu duda, escaneará la base RAG extrayendo los trozos de código y requerimientos locales *involucrados matemáticamente* en la pregunta, y te devolverá un formato de Prompt gigantesco perfectamente pre-generado. Lo copias, lo pegas en el navegador, y evitas gastos por llamados API.
