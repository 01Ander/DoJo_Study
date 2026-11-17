# Quest BI-05: Publicación, Refresh y Seguridad a Nivel de Fila (RLS)

> **Objetivo:** Configurar y validar un rol de seguridad a nivel de fila (**RLS** estático) sobre `dim_store`, publicar en Power BI Service y documentar el flujo de actualización (*Refresh*).
> **Requisitos Previos:** Lore de los Capítulos 00–05 y `BI-04` completada.
> **Presupuesto máximo:** 180 minutos.

---

## 🎯 Objetivo de Negocio
**Librería El Faro** requiere que el gerente regional de Bogotá solo visualice las ventas de las tiendas ubicadas en `"Bogotá"` dentro del mismo reporte publicado, sin duplicar el archivo `.pbix`, y con un flujo de actualización documentado.

---

## 📋 Instrucciones

1. **Crear el rol RLS estático en Power BI Desktop:**
   - Ve a **Modeling → Manage roles → New**.
   - Crea el rol `Bogota_Manager` sobre la tabla **`dim_store`** con la expresión DAX: `[city] = "Bogotá"`.
2. **Validar con *View as*:**
   - En **Modeling → View as**, selecciona `Bogota_Manager` y verifica el aislamiento de datos (toma captura de pantalla).
3. **Publicar y documentar Refresh (`my_deployment_notes.md`):**
   - Publica el `.pbix` en tu *Workspace* de Power BI Service (**Home → Publish**) — o documenta la captura de pantalla de la configuración de *Refresh* y *Security* en el Service.
   - En `my_deployment_notes.md`, documenta: (a) por qué Power BI Service no puede refrescar un PostgreSQL local (`localhost`) sin *On-Premises Data Gateway*, y (b) el método de refresh elegido (manual desde Desktop + republicación, o fuente en nube).

---

## 🧪 Validación (Andamiaje Nivel 5 — Ciclo AAA)

> *Nota: `BI-BASICO` se valida por artefacto + defensa oral (no usa `pytest`).*

1. **Arrange:** Sin roles activos y con `year = 2026`, registra el `[Total Revenue]` global (`480,000`) y el de `Bogotá` (`410,000`).
2. **Act:** Activa **View as → `Bogota_Manager`**.
3. **Assert:**
   - `[Total Revenue]` en 2026 muestra exactamente **`410,000`** (no `480,000`).
   - El *slicer* de `dim_store[city]` muestra únicamente `"Bogotá"` (desaparece `"Medellín"`).
   - `my_deployment_notes.md` documenta el rol RLS y la restricción de gateway para PostgreSQL local.

---

## 💡 Restricciones y Entrega
- Prohibido aplicar el filtro RLS sobre `fact_book_sales` en lugar de `dim_store` o duplicar el `.pbix` por ciudad.
- **Entregables:** `.pbix` final + `my_deployment_notes.md` + captura de **View as** + captura/evidencia de *Refresh*.
