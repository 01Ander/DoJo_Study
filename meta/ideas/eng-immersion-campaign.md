# 💡 Idea: ENG-IMMERSION — Inglés como Campaign Intercalada

> **Estado:** Idea — Pendiente de RFC formal
> **Fecha:** 2026-04-29
> **Conecta con:** RFC v3 (Campaign as Course), Syllabus Maestro (ENG-INT)

---

## El Principio

El inglés no compite por un "espacio libre" en el calendario — se le asigna
territorio propio con el mismo estatus estructural que Python, SQL o Cloud.
Es una habilidad técnica paralela a la programación, no un suplemento.

---

## Modelo de Calendario Macro (Interleaving Estructurado)

```
PY-POO             (6-8 semanas)  ← campaign técnica
        ↓
ENG-IMMERSION-1    (2-3 semanas)  ← pausa activa / comprensión auditiva
        ↓
SQL-FUNDAMENTALS   (6-8 semanas)
        ↓
ENG-IMMERSION-2    (2-3 semanas)  ← registro técnico y vocabulario DE
        ↓
DE-ETL-BATCH       (6-8 semanas)
        ↓
ENG-IMMERSION-3    (2-3 semanas)  ← producción escrita formal
        ↓
...
```

Cada ENG-IMMERSION-N avanza en nivel. No repite. Tiene progresión interna
propia aunque viva fraccionada entre campaigns técnicas.

**Por qué intercalada y no un día fijo semanal:**
Un día fijo compite con deuda técnica de la misma semana — el inglés pierde
siempre. Una campaign intercalada tiene inicio y fin claros: cuando empieza
ENG-IMMERSION el código está cerrado y el contexto mental está limpio.

---

## Arquitectura de la Campaign (compatible con v5.0)

```
ENG-IMMERSION-N/
├── campaign.md
├── grimoire.md      ← escrito 100% en inglés desde la primera entrada
├── lore/            ← fonética, patrones de reducción, registro formal/informal
├── quests/          ← shadowing, dictado, episode log, phrase bank
└── boss/            ← Boss: análisis escrito o resumen oral grabado
```

### Input primario: herramientas externas

| Herramienta | Rol |
|---|---|
| Netflix / HBO | Comprensión auditiva — registro informal y dramático |
| YouTube | Input técnico (talks, tutoriales DE/Python en inglés) |
| Busuu | Gramática estructurada — se mantiene como en el Syllabus |
| NotebookLM | Tutor de lore/ sin costo de API |

### Protocolo de episodio (ritual central)

```
1. WATCH     (25 min) — subtítulos en inglés, nunca en español. Flow completo.
2. REWATCH   (10 min) — escena difícil, sin subtítulos. Pausa + shadowing.
3. LOG       ( 5 min) — en grimoire.md:
                        · 3 frases nuevas con contexto
                        · 1 patrón fonético identificado
                        · Auto-evaluación de comprensión (0-10)
```

El DM solo entra vía `/dojo-ask` para dudas puntuales de contexto.
Costo de API casi cero — NotebookLM absorbe el tutor de gramática.

---

## Progresión por Etapa

| Etapa | Foco | Boss |
|---|---|---|
| ENG-IMMERSION-1 | Comprensión auditiva + fonética | Dictado de escena sin subtítulos |
| ENG-IMMERSION-2 | Vocabulario técnico DE en inglés | Glosario contextualizado de 50 términos |
| ENG-IMMERSION-3 | Producción escrita formal | Análisis de episodio (500 palabras, registro B2) |
| ENG-IMMERSION-4 | Producción oral | Grabación de 3-5 min resumiendo contenido técnico |

---

## Por qué funciona como pausa cognitiva real

El cerebro procesa lenguaje natural y código en modos distintos. Pasar de
TDD a comprensión auditiva activa es un cambio de modo genuino — no es
descanso pasivo, pero tampoco es la misma tensión cognitiva que un Boss
de Data Engineering. Recarga sin desconectar.

---

## Pendiente para RFC formal

- [ ] Definir duración exacta de cada ENG-IMMERSION según campaign técnica anterior
- [ ] Establecer criterios del DM para auditar el Boss de producción escrita
- [ ] Evaluar si YouTube técnico (en inglés) puede ser input simultáneo
      durante campaigns técnicas sin romper el interleaving
- [ ] Decidir si ENG-IMMERSION aparece en el Skills Tracker con el mismo
      peso que una campaign técnica
