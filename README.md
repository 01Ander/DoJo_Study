# DoJo Study – High Performance Engineering System v3.2

**DoJo Study** es un marco operativo de aprendizaje inmersivo, diseñado para la formación rigurosa y acelerada hacia el perfil de **Data & Automation Engineer**, operando bajo altos estándares de ingeniería de software (Arquitectura Limpia, TDD y Módulos Desacoplados).

Esta versión (v3.2) fue diseñada en Colombia asumiendo una disponibilidad inmersiva de 8+ horas diarias. Sustituye la mentalidad de "ahorro de energía" de versiones anteriores por el concepto de **Deep Work** y **English-Only Zone**.

---

## 1. Propósito del DoJo Study v3.2

- Escalar hacia un nivel Profesional/Senior en Data Engineering, Automatización y Cloud.
- Forzar la adopción de buenas prácticas corporativas: Tests Unitarios (Pytest), Documentación de Arquitectura (Mini-RFCs) y Naming Strict desde el minuto cero.
- Construir herramientas y pipelines funcionales, abandonando permanentemente las tareas abstractas o ejercicios sin conexión real.
- Adoptar una inmersión completa al **Inglés** como interfaz principal de tecnología (para misiones, código, diagramas y revisión de la IA).

---

## 2. Arquitectura del Sistema (El Modelo Binario)

El DoJo ahora separa brutalmente al estudiante en dos modalidades vitales:

### Deep Work (La Inmersión)
El estado base de operación. Bloques de 90 minutos de codificación intensiva, precedidos obligatoriamente por el **English Commando** (rutina de seteo de lenguaje en Busuu/Duolingo) y ejecutando estrictamente TDD (Primero falla el test, luego se escribe el código).

### Rest Day (El Vacío)
El protocolo obligatorio para gestionar la disipación cognitiva. Días de *Zero-Code Policy*. No hay misiones débiles; solo descanso real para asentar redes neuronales.

---

## 3. Estructura de Campañas e Ingeniería

Todo aprendizaje técnico se enmarca en la creación de pipelines dentro de la carpeta `/subjects`. Cada campaña utiliza:
- **Mini-RFCs:** Documentos de diseño antes que el código.
- **Main Missions (M):** Múltiples PRs simulados para completar el software base.
- **Scaling Refactors (S):** Escalado técnico (añadir automatización, migraciones a SQL, CI/CD).
- **Boss Missions (B):** La integración final del proyecto mediante Endpoints API o Serverless CLI.

---

## 4. Estructura del repositorio

```text
dojo-study/
├─ README.md
├─ docs/                 <- (DoJo Core, Riesgos, Flujos y Protocolos)
├─ archive/              <- (Histórico de v2.0 - Canadá)
├─ templates/            <- (Plantillas v3.2 con Deep Work / TDD tracking)
└─ subjects/
   └─ python/            <- (Core técnico y Campañas)
```

## 5. English-Only Zone

El español se ha preservado de manera exclusiva para reflexiones psicológicas personales o entendimiento de conceptos abstractos iniciales. **Todos los commits de Git, Readmes, Nombres de Clases y Métodos en este repositorio ESTÁN OBLIGADOS a escribirse en Inglés Técnico fluido**, sirviendo como escudo contra la *Interferencia del Francés* de tus fundamentos pasados.