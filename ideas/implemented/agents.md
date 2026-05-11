============================================================
  PROPUESTA: ARQUITECTURA MULTI-AGENTE PARA DOJO STUDY
  + SELECCION DE LLMs POR CAPA (COSTO-OPTIMIZADO)
============================================================


PARTE 1: FRACCIONAMIENTO EN 4 CAPAS
------------------------------------------------------------

Actualmente tu DojoAgent es un monolito de 564 lineas
donde UNA sola clase hace todo: tutoria, revision, logging,
RAG, journaling, auditing. Las 5 personalidades (GLOBAL,
MAIN, WORK, EXERCISES, THINK) son solo cambios de prompt
pero comparten el mismo cerebro, la misma memoria, y la
misma cadena.

Propongo 4 agentes especializados:


AGENTE 1: EL TUTOR (Reemplaza MAIN + EXERCISES)
  Responsabilidad:
    - Explicar teoria con Domain Shifting
    - Generar ejemplos de codigo en dominios analogos
    - Definir Criterios de Aceptacion y casos borde
    - Responder dudas conceptuales

  Necesita:
    - Conocimiento tecnico amplio y profundo
    - Capacidad de generar codigo funcional y correcto
    - Creatividad para analogias (Domain Shifting)
    - Ventana de contexto grande (leer requirements + teoria)

  Complejidad cognitiva: ALTA
  Frecuencia de uso: MEDIA (solo durante Fase A y muros)

  Modelo: Qwen3.5 122B (0.4/3.20)
  Alternativa: Gemma 4 31B (0.128/0.398)

AGENTE 2: EL REVIEWER (Reemplaza WORK)
  Responsabilidad:
    - Pair Programming Socratico (preguntas, no respuestas)
    - Code Review (SOLID, Clean Code, Type Safety)
    - Validar Business Context / ROI antes de codear
    - Dar luz verde MVP o bloquear
    - Evaluar Mini-RFCs

  Necesita:
    - Razonamiento critico fuerte
    - Capacidad de "contenerse" (no dar la solucion)
    - Leer codigo y encontrar code smells
    - Seguir reglas estrictas (Socratico, Guardian)

  Complejidad cognitiva: ALTA (razonamiento, no generacion)
  Frecuencia de uso: ALTA (es el companero constante)

  Modelo: Qwen3.5 122B
  Alternativa: Gemma4 32B

AGENTE 3: EL SCRIBE (Nuevo - reemplaza auto-logging)
  Responsabilidad:
    - Actualizar journal.md automaticamente
    - Sincronizar estado de misiones (Pendiente -> Ejecucion
      -> Completado) -- la feature de ideas-in-live.md
    - Generar resumenes de sesion
    - Mantener el historial.md limpio
    - Actualizar metadata en requirements.md
    - Detectar inconsistencias entre docs

  Necesita:
    - Seguir instrucciones de formato estrictas
    - Leer/escribir archivos con precision
    - Resumir sin perder informacion critica
    - NO necesita creatividad ni razonamiento profundo

  Complejidad cognitiva: BAJA-MEDIA
  Frecuencia de uso: MUY ALTA (cada interaccion)

  Modelo: Gemma 4 31B (0.128/0.398)
  Alternativa: Qwen3.5 122B (0.4/3.20)

AGENTE 4: EL ARQUITECTO (Reemplaza GLOBAL + THINK)
  Responsabilidad:
    - Auditar coherencia del sistema DoJo completo
    - Analizar progreso macro (campanas, syllabus)
    - Proponer refactorizaciones del propio framework
    - Debate filosofico sobre arquitectura y patrones
    - Supervisar que los otros agentes cumplan las reglas
    - Conciencia temporal (Rest Days, Burnout Alerts)

  Necesita:
    - Vision sistemica amplia
    - Razonamiento a largo plazo
    - Capacidad de leer TODO el repo y sintetizar
    - Ventana de contexto MUY grande

  Complejidad cognitiva: MUY ALTA
  Frecuencia de uso: BAJA (ventanas de Arquitecto, sabados)

  Modelo: Gemini3.1pro
  Alternativa: Opus 4.6 +caro