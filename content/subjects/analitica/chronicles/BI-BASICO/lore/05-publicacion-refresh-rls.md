# Capítulo 05: Publicación, Refresh y Seguridad a Nivel de Fila (RLS)

Un tablero que solo vive en tu computador local no aporta valor a la empresa: los gerentes de **Tostadora El Roble** necesitan consultarlo en la web con datos actualizados, y el gerente regional de Bogotá no debería ver los costos internos ni el detalle operativo de las sucursales de Medellín. La **publicación en Power BI Service**, la **gestión de actualización (*Refresh*)** y la **seguridad a nivel de fila (*Row-Level Security — RLS*)** cierran el ciclo productivo de un reporte de BI.

---

## 1. Publicación en Power BI Service (Qué y Por qué)

**Qué es:** Es el proceso de subir tu archivo `.pbix` (que contiene tanto el **Modelo Semántico** como el **Reporte** visual) desde Power BI Desktop hacia un área de trabajo (*Workspace*) en **Power BI Service** (la plataforma en la nube de Microsoft).

**Por qué importa:** Enviar archivos `.pbix` adjuntos por correo crea múltiples versiones desactualizadas ("`ventas_final_v3_ahora_si.pbix`"). Publicar en Power BI Service centraliza una única fuente de verdad accesible por enlace web, donde se administran permisos, actualizaciones y seguridad.

---

## 2. Refresh Manual vs. Programado y Restricción de PostgreSQL Local (Qué y Por qué)

**Qué es:**
- **Refresh (Actualización):** Proceso mediante el cual Power BI Service vuelve a ejecutar tus pasos de Power Query (`query.pq`) contra la fuente de datos para traer registros nuevos al modelo semántico.
- **On-Premises Data Gateway:** Un agente de software (exclusivo de Windows) que actúa como puente seguro entre la nube de Power BI Service y una base de datos privada en tu red local (como tu PostgreSQL local en Docker).

**Por qué importa (Restricción crítica de arquitectura):** Power BI Service vive en la nube de Microsoft; **no puede conectarse directamente a `localhost:5432` en tu computador** sin un *On-Premises Data Gateway* instalado y encendido en Windows. Si trabajas en macOS o sin gateway permanente, debes documentar esta restricción arquitectónica y operar con una de dos estrategias:
1. **Refresh manual desde Power BI Desktop:** Refrescar localmente contra PostgreSQL/CSV en tu VM Windows y republicar el `.pbix` al Service.
2. **Fuente en la nube o archivo sincronizado (OneDrive/SharePoint):** Permitir *Scheduled Refresh* (actualización programada) en Power BI Service sin depender de un gateway local.

> **Analogías (*Tostadora El Roble*):**
> 1. **La vitrina de la tienda vs. el horno:** Power BI Service es la vitrina web donde los clientes miran el menú; Power BI Desktop es el obrador donde horneas. Si el proveedor de café (*PostgreSQL local*) solo entrega en la puerta trasera de tu casa, la vitrina en el centro comercial (*la nube*) no puede ir a recoger los sacos por sí sola sin un mensajero (*On-Premises Data Gateway*).
> 2. **Las llaves por sucursal (*RLS*):** Todos los gerentes entran al mismo edificio (*el mismo reporte `.pbix`*), pero la tarjeta magnética de cada gerente solo abre la puerta de su propia sucursal. No duplicas el edificio para cada persona; restringes la vista dentro del mismo modelo.

---

## 3. Seguridad a Nivel de Fila (RLS Estático) y Prueba *View as* (Qué y Por qué)

**Qué es:** **RLS (*Row-Level Security*)** es una regla de filtrado definida sobre una tabla de dimensión del modelo semántico (por ejemplo, `dim_branch`) que restringe qué filas puede ver un usuario o grupo al consultar el reporte. En **RLS estático**, defines una regla fija por rol (ej. rol `Bogota_Manager` donde `dim_branch[city] = "Bogotá"`).

**Por qué importa:** Evita el antipatrón de mantener 10 copias distintas del mismo archivo `.pbix` ("reporte_bogota.pbix", "reporte_medellin.pbix"). Mantienes **un solo modelo semántico y un solo reporte**, y el motor de Power BI aplica el filtro de seguridad automáticamente antes de calcular cualquier medida DAX.

*(Nota de alcance: El RLS dinámico basado en `USERPRINCIPALNAME()` y tablas puente corporativas pertenece a la Fase 2 / BI empresarial; en `BI-BASICO` dominamos el RLS estático y su verificación).*

---

## 4. Implementación de RLS y Publicación (Cómo)

### Setup Inicial (Power BI Desktop → Manage Roles)

1. Abre tu `.pbix` en Power BI Desktop.
2. Ve a la pestaña **Modeling** en la cinta superior.
3. Haz clic en **Manage roles**.

### El Camino Frágil (Duplicar reportes o filtrar solo en el lienzo)

**🎯 Objetivo de Negocio:** Asegurar que el gerente de Bogotá en *Tostadora El Roble* solo vea las ventas de su ciudad sin acceder a las cifras de Medellín.

Un enfoque frágil consiste en ocultar la ciudad de Medellín usando un filtro visual del panel **Filters** o un *slicer* bloqueado, o peor, filtrar en la tabla de hechos en lugar de la dimensión. Un usuario con acceso al modelo o a exportar datos puede evadir filtros visuales, y filtrar la tabla de hechos no escala a otras métricas.

### El Camino Robusto (Rol RLS estático sobre `dim_branch` + *View as*)

**🎯 Objetivo de Negocio:** Crear un rol `Bogota_Manager` en `dim_branch` que restrinja el modelo completo vía relación `1:N` hacia `fact_coffee_sales`, validarlo con *View as* y publicarlo en Power BI Service.

1. En **Manage roles** → clic en **New** (o **Create**).
2. Nombra el rol: `Bogota_Manager`.
3. Selecciona la tabla de dimensión **`dim_branch`** (aprovechando que la relación `1:N` unidireccional propagará este filtro de seguridad hacia `fact_coffee_sales`).
4. Escribe la expresión DAX de filtro de tabla:

```dax
-- ROBUST: Static RLS filter applied on dimension table dim_branch
[city] = "Bogotá"
```

#### Desglose de Sintaxis (Zero Surprise Syntax)

| Elemento | Qué hace | Por qué se eligió | Cómo funciona internamente |
|---|---|---|---|
| `[city] = "Bogotá"` | Expresión booleana que evalúa cada fila de `dim_branch` y conserva solo aquellas donde la columna `city` es exactamente `"Bogotá"`. | Aplicarlo sobre `dim_branch` (lado `1` de la relación) filtra automáticamente todas las filas relacionadas en `fact_coffee_sales` (lado `*`). | Antes de ejecutar cualquier visual o medida DAX, el motor tabular inyecta esta condición como filtro obligatorio en `dim_branch`. |

5. **Probar localmente con *View as*:**
   - En la pestaña **Modeling**, haz clic en **View as**.
   - Marca la casilla **`Bogota_Manager`** → **OK**.
   - Verás un banner amarillo arriba: *"Now viewing as: Bogota_Manager"*. Todos los KPIs, gráficos y *slicers* mostrarán únicamente las sucursales de Bogotá.
   - Haz clic en **Stop viewing** cuando termines la prueba.
6. **Publicar y documentar Refresh:**
   - Pestaña **Home** → **Publish** → selecciona tu *Workspace* en Power BI Service.
   - En Power BI Service (navegador web), abre el *Semantic model* → **Security** para asignar usuarios al rol `Bogota_Manager`, y abre **Settings → Refresh** para verificar el estado de actualización manual o programada (documentando si requiere *On-Premises Data Gateway* cuando la fuente es PostgreSQL local).

---

## 5. Conexión con Testing y Validación (Regla Crítica)

Validamos el RLS y el flujo de Refresh aplicando el ciclo **AAA**:

1. **Arrange (Preparar baseline sin RLS):** Anota el valor de `[Total Revenue]` global (todas las ciudades) y el valor filtrado manualmente para `"Bogotá"` en el reporte sin roles activos.
2. **Act (Activar el rol de seguridad):** En **Modeling → View as**, activa el rol `Bogota_Manager` (y toma captura de pantalla como evidencia).
3. **Assert (Verificar aislamiento y paridad):**
   - El `[Total Revenue]` visible bajo `Bogota_Manager` coincide **exactamente** con el total de `"Bogotá"` anotado en Arrange (y es estrictamente menor que el total global).
   - En el *slicer* de ciudades ya no aparecen opciones de otras ciudades (como `"Medellín"` o `"Cali"`).
   - La captura de *Refresh* (o documentación del flujo manual/gateway) confirma cuándo y cómo se actualizaron los datos sin errores de credenciales.

---

## 6. Mapa de Ejercicios

Dirígete a `quests/05-publicacion-refresh-rls/` y completa la práctica deliberada **BI-05**:

```text
quests/05-publicacion-refresh-rls/
└── quest.md          (Instrucciones, criterios de aceptación y evidencia requerida)
```
