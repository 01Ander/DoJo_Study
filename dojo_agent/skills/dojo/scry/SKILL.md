---
name: scry
description: El Dungeon Master escudriña tu grimoire y decide si el Rite se desbloquea
version: 1.0.0
metadata:
  hermes:
    tags: [dojo, audit, dm, gatekeeper, discworld]
    category: dojo
    requires_toolsets: [file]
---

# Scry (Dungeon Master Audit)

## When to Use
Cuando el Operador quiere verificar su progreso en una chronicle o solicitar acceso al Rite.

## Usage
```
/scry [chronicle]
```
Ejemplo: `/scry PY-POO`

Sin argumentos, intenta detectar la chronicle desde el directorio de trabajo.

Para auditoría cualitativa profunda:
```
/scry PY-POO --deep
```

## Procedure

**IMPORTANTE: El directorio raíz del proyecto es `~/Documents/DoJo/DoJo_Study/`. NO busques archivos fuera de este directorio.**

### Paso 1: Localizar la chronicle

1. Construir la ruta: `~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/{CHRONICLE}/`
2. Verificar que existan: `grimoire.md`, `lore/`, `quests/`, `rite/`
3. Si falta algo, reportar error y detener.

### Paso 2: Auditar el Grimoire

Leer `grimoire.md` de la chronicle. Para CADA capítulo:

**Checklist Estructural (verificación binaria):**
- [ ] ¿La "Fecha de finalización" tiene una fecha real (no YYYY-MM-DD)?
- [ ] ¿Las métricas están completas (no contienen `__` ni placeholders)?
- [ ] ¿Las respuestas Feynman tienen contenido escrito (no contienen `[Tu respuesta aquí...]`)?

**Resultado por capítulo:** `✅ PASS` o `❌ FAIL (razón)`

### Paso 3: Auditar las Quests

Para cada carpeta en `quests/`:
- Listar archivos `.py` que NO sean parte del enunciado (los `.md` son enunciados).
- Verificar que cada `.py` tenga más de 5 líneas (no es un archivo vacío o stub).
- **Resultado por quest:** `✅ PASS` o `❌ FAIL (faltan archivos o están vacíos)`

### Paso 4: Generar Reporte

```
[DM] 🔮 Scry — Chronicle: {CHRONICLE}
═══════════════════════════════════════

Capítulo 00: {PASS/FAIL}  |  Quest 00: {PASS/FAIL}
Capítulo 01: {PASS/FAIL}  |  Quest 01: {PASS/FAIL}
...
Capítulo 07: {PASS/FAIL}  |  Quest 07: {PASS/FAIL}

═══════════════════════════════════════
Resultado: {X}/8 capítulos completados

{Si todos PASS:}
🏰 RITE DESBLOQUEADO. Puedes iniciar el Rite en rite/.
Recomendación: Activa /personality witch para pair programming.

{Si alguno FAIL:}
🔒 Rite bloqueado. Capítulos pendientes:
- Cap {N}: {razón del FAIL}
```

### Paso 5 (Opcional): Auditoría Cualitativa (`--deep`)

Si el Operador solicita `/scry PY-POO --deep`:

Leer las respuestas Feynman del grimoire y evaluar:
- ¿La respuesta demuestra comprensión propia o es copy-paste del lore?
- ¿Usa terminología correcta?
- ¿Podría explicar el concepto a alguien más con esta respuesta?

Reportar observaciones por capítulo. Se sugiere usar un modelo con capacidades de razonamiento amplias para esta evaluación.

## Pitfalls
- **NO modifiques el grimoire.** Solo léelo y reporta.
- **NO ejecutes scripts Python ni búsquedas globales.** Usa `read_file` y `list_dir`.
- Si la chronicle no existe, lista las disponibles en `subjects/python/campaigns/`.
- La auditoría cualitativa (`--deep`) es opcional y explícita. No la ejecutes por defecto.
