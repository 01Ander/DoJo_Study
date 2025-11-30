# Subjects – Estructura de Materias del DoJo Study

Este directorio organiza todas las materias técnicas y lingüísticas del DoJo Study.  
La finalidad es mantener un orden claro entre campañas, misiones y proyectos reales, sin mezclar teoría, práctica ni documentación conceptual.


---

## 1. Objetivo de este directorio

`subjects/` sirve como:

- Contenedor de todas las materias del DoJo.
- Punto de acceso para campañas técnicas.
- Estructura para registrar misiones principales, secundarias y boss missions.
- Base para conectar el estudio diario con los proyectos del repositorio.

Este espacio solo contiene contenido aplicado (campañas, misiones), nunca teoría abstracta.

---

## 2. Estructura general

Cada materia tendrá su propio directorio y su propio estándar interno:

```text
subjects/
├─ python/
│ ├─ campaigns/
│ │ ├─ PY-BASICO/
│ │ ├─ PY-POO/
│ │ └─ PY-INTERMEDIO/
│ ├─ missions/
│ └─ README.md
├─ sql/
│ ├─ campaigns/
│ ├─ missions/
│ └─ README.md
├─ qa/
├─ cloud/
├─ automation/
├─ data/
└─ eng-int/
```


Las carpetas se añadirán a medida que avances.

---

## 3. Contenido interno de cada materia

Cada materia usa el mismo formato:

### 3.1 `campaigns/`
Contendrá subcarpetas para cada campaña técnica, por ejemplo:

subjects/python/campaigns/PY-BASICO/
subjects/python/campaigns/PY-POO/
subjects/python/campaigns/PY-INTERMEDIO/


Cada campaña tendrá:

- `campaign.md` (explicación de la campaña en español)
- `missions/` (misiones principales, secundarias y boss)
- Archivos derivados necesarios

Ejemplo:
```text
├─ campaign.md
└─ missions/
├─ M01.md
├─ M02.md
├─ S01.md
└─ B01.md
```

---

### 3.2 `missions/`
Este directorio contendrá misiones generales (no asociadas a una campaña específica) que nacen de proyectos o descubrimientos durante estudio.

Es opcional, pero útil.

---

### 3.3 `README.md`
Cada materia tendrá su propio README interno que explica:

- La finalidad de esa materia
- La estructura particular de sus campañas
- Cómo se relaciona con tu camino Data & Automation Engineer
- Notas específicas (por ejemplo, Python tiene más campañas que QA)

Ejemplo básico para un futuro README:

Python – Materia General del DoJo

Este directorio contiene las campañas de aprendizaje técnico en Python, desde lo básico hasta construcción de proyectos reales...


---

## 4. Convenciones del DoJo en Subjects

### 4.1 Explicación en español
Todo lo conceptual, contextual y organizativo.

### 4.2 Identificadores en inglés
- nombres de carpetas  
- nombres de archivos  
- códigos de campañas (ej. `PY-BASICO`)  
- códigos de misiones (`M01`, `S02`, `B01`)  

### 4.3 Plantillas
Toda misión y campaña debe usar las plantillas de:

- `templates/mission-template.md`
- `templates/campaign-template.md`

Esto garantiza consistencia en todo el sistema.

---

## 5. Cómo crear una campaña nueva

1. Crear una carpeta dentro de `campaigns/` usando su código:

mkdir -p subjects/python/campaigns/PY-BASICO

2. Copiar `campaign-template.md` dentro de esa carpeta como `campaign.md`.
3. Definir:
- objetivo técnico
- misiones principales
- side missions
- boss mission
4. Crear carpeta `missions/`.
5. Para cada misión, crear un archivo usando `mission-template.md`.

---

## 6. Relación con los chats XX-MAIN / XX-EXERCISES / XX-WORK

El directorio `subjects/` funciona como la base física del progreso del DoJo.

Los chats con IA:

- generan teoría mínima (MAIN)
- proponen misiones (EXERCISES)
- ayudan a resolver misiones (WORK)

Y todo lo completado se registra aquí.

---

Este archivo define el estándar para todas las materias del DoJo Study.
