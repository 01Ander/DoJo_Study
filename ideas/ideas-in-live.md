## ⏳ Pendiente (Features Futuras)
- **[INBOX | 2026-04-29] ENG-IMMERSION — Inglés como Chronicle Intercalada:** Modelo de interleaving estructurado donde chronicles de inglés (2-3 semanas) se intercalan entre chronicles técnicas, con arquitectura v5.1 completa (lore, quests, rite, grimoire). Ver documento completo: [`ideas/eng-immersion-campaign.md`](eng-immersion-campaign.md).
- **[INBOX | 2026-04-15] Feature para el Agente: Integración WakaTime API standalone** — Al ejecutar el cierre del Rite, el agente consulta automáticamente la API de WakaTime usando la API key de `~/.wakatime.cfg`, extrae el tiempo de coding/testing/docs del proyecto activo, y lo inyecta formateado en la entrada del journal. **Requisito:** API key ya existe en `~/.wakatime.cfg`. Usar autenticación Basic Auth (base64 de la api_key).
- **[INBOX | 2026-04-21] Protocolo de Bloques de 90 Minutos (Context Reset Strategy):** Formalizar la estrategia de sesión óptima. Incluye: estructura de sesión `[Bloque 90 min] → descanso 10 min → [Bloque 90 min]`, regla de decisión de pausas, y la regla de una chronicle por día.
- **[INBOX | 2026-04-27] Memoria Contextual y Adaptabilidad (Journals):** Buscar la manera de extraer y mantener el contexto emocional/cognitivo de journals o métricas de fricción para que el sistema module automáticamente su comportamiento.

## ✅ Resuelto en v5.1.0 (2026-05-11)
- ~~Feature para el Agente (Sugerencia de Próxima Misión)~~ → Absorbida por `/scry` que muestra progreso por capítulo.
- ~~Refactorización de recarga de personalidad~~ → Simplificado a 2 personalidades. Menos relevante.
- ~~Feature `/dojo-test`~~ → Parcialmente cubierta por `/scry` que verifica existencia de archivos .py.
- ~~Bug de Parseo Hermes (Errno 63)~~ → Eliminadas las skills que causaban mensajes largos.
- ~~Banner de confirmación para skills~~ → Con solo 2 skills atómicas, ya no es necesario.
- ~~Bug underscores~~ → Documentado en Regla 8 de `.hermes.md`, workaround aplicado.
- ~~Rol dual del Tutor en temas nuevos~~ → Resuelto por diseño: Wizard enseña, Witch revisa. Sin zona gris.

## 🔍 Evaluación Pendiente
- (Vacía — todas las evaluaciones anteriores fueron resueltas o absorbidas por v5.1)
