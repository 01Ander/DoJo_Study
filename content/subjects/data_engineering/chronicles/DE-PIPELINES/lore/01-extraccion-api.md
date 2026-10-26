# Capítulo 01: Extracción Automatizada (APIs REST)

> 🎯 **Objetivo de Negocio:** El Gremio de Alquimistas necesita saber qué ingredientes exóticos están disponibles en el Mercado Negro de la capital. Para ello, enviaremos mensajeros automatizados a solicitar el catálogo diario, autenticándonos con nuestra insignia del gremio.

Antes, si querías el catálogo del Mercado Negro, enviabas un cuervo. Hoy, los mercados modernos exponen **APIs REST**.

## 1. ¿Qué es una API REST?

**Analogía 1 (El Recepcionista Estricto):**
Imagina el Mercado Negro como un gran almacén cerrado. No puedes entrar y buscar tú mismo. En su lugar, hay un recepcionista en una ventanilla. Tú le entregas un formulario estandarizado pidiendo "3 colas de dragón" (Request), y él te devuelve una caja con las colas (Response) o un sello de "Rechazado" si no tienes permiso. Esa ventanilla es la API.

Para hablar con la API en Python, usamos la librería `requests`.
*Zero Assumption Setup:* Si no la tienes, instálala en tu entorno virtual:
```bash
pip install requests
```

## 2. Autenticación y Cabeceras (Headers)

El Mercado Negro no le da su catálogo a cualquiera. Necesitas demostrar que eres del Gremio. Para eso usamos un **Token** (tu placa de miembro) que enviamos en los **Headers** (el sobre cerrado donde va el formulario).

### Ejemplo Progresivo: Extracción de Datos

**El Mal Camino (Ingenuo y frágil):**
```python
import requests

# 🎯 Objetivo: Traer ingredientes del mercado.
def get_ingredients_bad():
    # Si la API cambia o se cae, esto explota horriblemente.
    response = requests.get("https://api.mercadonegro.com/ingredientes")
    return response.json()
```

**El Buen Camino (Robusto y autenticado):**
```python
import requests

def get_ingredients(api_url: str, guild_token: str) -> list:
    # 1. Preparamos nuestro sobre (Headers) con la insignia (Token)
    headers = {
        "Authorization": f"Bearer {guild_token}"
    }
    
    # 2. Hacemos la petición (El mensajero va a la ventanilla)
    # requests hará el trabajo sucio y usará nuestras cabeceras
    response = requests.get(api_url, headers=headers)
    
    # 3. Seguridad: Si el gremio nos da un error 401, 403, 404, o 500, explota rápido
    response.raise_for_status()
    
    # 4. Convertimos la respuesta de JSON a un diccionario nativo de Python
    data = response.json()
    
    return data.get("ingredients", [])
```

> **Explicación de Sintaxis:**
> - `headers=headers`: Le pasamos un diccionario con la llave "Authorization" obligatoria.
> - `response.raise_for_status()`: Si el status code es 200 (OK), no hace nada. Si es 4xx o 5xx, lanza una excepción `HTTPError` deteniendo el código inmediatamente.
> - `data.get("ingredients", [])`: Intentamos sacar la llave "ingredients" del diccionario. Si el mercado nos devolvió un diccionario vacío o sin esa llave, retorna una lista vacía `[]` como valor por defecto, evitando un error `KeyError`.

> **¿Por qué usar un Token (Bearer) es más seguro que enviar Usuario/Contraseña?**
> 1. **Es revocable:** Si alguien roba el token, puedes invalidarlo en el servidor sin tener que cambiar tus credenciales reales.
> 2. **Es temporal:** Los tokens suelen tener una fecha de expiración.
> 3. **Protege tu identidad:** No envías tu información sensible en cada petición HTTP, solo un permiso temporal.
> *Analogía:* El token es como una llave de hotel temporal. Si la pierdes, el hotel la desactiva. Tu identidad original nunca estuvo en riesgo.
## 3. Paginación: Cuando el catálogo es masivo

**Analogía 2 (Los Tomos del Catálogo y el Marcapáginas):**
Si el Mercado Negro tiene 50,000 ingredientes, el recepcionista no te entregará una carreta de 5 toneladas en un solo viaje. Te entregará el "Tomo 1" con 100 pergaminos y una nota al final diciendo: *"Si deseas continuar, solicita el Tomo 2"* o *"Usa este marcapáginas sellado (Cursor) para la siguiente entrega"*. Esto es la paginación.

En código, las APIs de producción **imponen** paginación por defecto. No es una opción: si tu script no itera por todas las páginas, **perderás el 99% de los datos silenciosamente**, ya que la primera petición responderá con código HTTP 200 sin emitir advertencia alguna.

---

### 3.1 Los Dos Estándares de la Industria: Offset vs Cursor

| Característica | Paginación por Página / Offset (`page=2`) | Paginación por Cursor (`cursor=tok_99x`) |
|---|---|---|
| **Mecanismo** | Salta $N$ registros en la base de datos (`OFFSET 100`). | Usa un puntero indexado hacia el último ID procesado. |
| **Ventaja** | Simple e intuitiva; permite saltar a páginas intermedias arbitrarias. | Extremadamente rápida ($O(1)$) y no degrada con millones de registros. |
| **Vulnerabilidad** | **Page Drift:** Si se insertan o eliminan filas mientras iteras, puedes leer duplicados o saltarte registros. | Inmune al Page Drift; el cursor apunta con exactitud al límite del lote. |
| **Casos de Uso** | Búsquedas en UI, catálogos pequeños o datos históricos inmutables. | Feeds en tiempo real, APIs de alto volumen (Stripe, GitHub, Slack, Shopify). |

---

### 3.2 Patrón de Producción 1: Paginación por Offset/Página con Salvaguarda

```python
import requests
from typing import Any

# 🎯 Objetivo de Negocio: Extraer catálogo paginado evitando bucles infinitos con un límite de seguridad.

def extract_all_pages_offset(
    api_url: str, 
    token: str, 
    page_size: int = 50, 
    max_pages: int = 100
) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    current_page = 1

    while current_page <= max_pages:
        # Pasamos parámetros query en un diccionario estructurado (requests los codifica en la URL)
        params = {"page": current_page, "limit": page_size}
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        payload = response.json()
        batch = payload.get("data", [])

        # Condición de salida 1: Página vacía (fin del catálogo)
        if not batch:
            break

        # Deduplicación defensiva en memoria
        for item in batch:
            item_id = item.get("id")
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                records.append(item)

        # Condición de salida 2: Si el lote trajo menos registros que el tamaño de página, era la última
        if len(batch) < page_size:
            break

        current_page += 1

    return records
```

---

### 3.3 Patrón de Producción 2: Paginación por Cursor y Resiliencia a Rate Limits (HTTP 429)

Cuando extraes miles de registros, la API puede responder con un código **HTTP 429 Too Many Requests**, indicando que sobrepasaste su cuota por segundo o minuto. Un pipeline resiliente no debe colapsar: debe leer la cabecera `Retry-After`, aplicar una pausa controlada (*backoff*) y reintentar.

```python
import time
import requests
from typing import Any

class RateLimitExceededError(Exception):
    """Excepción de dominio lanzada cuando se agotan los reintentos tras recibir HTTP 429."""
    pass

# 🎯 Objetivo de Negocio: Ingestar eventos mediante cursor continuo manejando rate limits y pausas de servidor.

def extract_feed_by_cursor(
    api_url: str,
    token: str,
    max_pages: int = 50,
    max_retries_per_page: int = 3
) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    all_events: list[dict[str, Any]] = []
    next_cursor: str | None = None
    pages_processed = 0

    while pages_processed < max_pages:
        params: dict[str, Any] = {"limit": 100}
        if next_cursor:
            params["cursor"] = next_cursor

        # Bucle de reintento para la página actual
        retries = 0
        response = None
        while retries <= max_retries_per_page:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 429:
                # El servidor nos pide esperar: leemos Retry-After o usamos fallback progresivo
                wait_seconds = float(response.headers.get("Retry-After", 1.5))
                time.sleep(wait_seconds)
                retries += 1
                continue
            
            response.raise_for_status()
            break
        else:
            raise RateLimitExceededError(
                f"Rate limit superado tras {max_retries_per_page} reintentos en cursor '{next_cursor}'."
            )

        payload = response.json()
        batch = payload.get("events", [])
        all_events.extend(batch)
        pages_processed += 1

        # El servidor nos entrega el cursor de la próxima página; si es None o vacío, terminamos
        next_cursor = payload.get("next_cursor")
        if not next_cursor:
            break

    return all_events
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): Paginación y Resiliencia
> * **`params={"page": page, "limit": page_size}`:** En `requests`, pasar un diccionario al argumento `params` codifica automáticamente los valores URL-encoded de forma segura (`?page=1&limit=50`), previniendo errores de concatenación de strings.
> * **`payload.get("next_cursor")`:** Extrae el token de continuación devuelto por la API. Si la API no lo incluye o devuelve `None`, indica de manera no ambigua que se ha alcanzado el final del dataset.
> * **`response.status_code == 429`:** Código de estado HTTP oficial para *Too Many Requests*.
> * **`response.headers.get("Retry-After", 1.5)`:** Inspecciona la cabecera enviada por la API indicando cuántos segundos debemos aguardar antes de reintentar.
> * **`while ... else:` en Python:** El bloque `else` de un bucle `while` se ejecuta únicamente si el bucle terminó normalmente sin alcanzar un `break`. Si agotamos todos los reintentos sin éxito, levantamos nuestra excepción de dominio `RateLimitExceededError`.
> * **`max_pages`:** Salvaguarda esencial de ingeniería para impedir bucles infinitos en caso de que la API devuelva cursores circulares por error.

---

### 🌐 Analogías del Mundo Real (Domain Shifting)

1. **Analogía 1 (Atención Bancaria — Turnero vs Ficha):**
   * *Offset:* Pedir "los clientes del 10 al 20". Si un cajero atiende a alguien y cancela una cuenta en medio del conteo, el turno 11 de la lista se corre, provocando que atiendas a alguien dos veces o saltes a un cliente.
   * *Cursor:* El cliente sostiene una ficha con un hash único (`F-489A`). El cajero dice: *"Quien tenga la ficha siguiente a F-489A, pase adelante"*. No importa si entra o sale gente de la sucursal: el orden relativo está fijado en la ficha.

2. **Analogía 2 (Control de Tráfico Portuario — Rate Limiting):**
   Un barco de carga no puede desembarcar contenedores a discreción si el muelle está saturado. La torre de control emite una bandera roja (*HTTP 429*) y le ordena fondear durante 15 minutos (*Retry-After*). El capitán espera disciplinadamente y vuelve a solicitar muelle cuando expira la orden, en lugar de embestir el puerto.

## 4. Testing de APIs sin golpear el Mercado (Mocking con `responses`)

El Gremio nos cobraría mucho dinero si probáramos nuestro código haciendo miles de peticiones reales al mercado. Para testear código que usa `requests`, usamos la librería **`responses`**.

*Zero Assumption Setup:* Instálala en tu entorno.
```bash
pip install responses
```

Esta herramienta intercepta (mockea) las peticiones que hace `requests` en nuestros tests y devuelve respuestas falsas que nosotros preconfiguramos.

> **Explicación de Sintaxis (Testing):**
> - `@responses.activate`: Decorador que enciende el interceptor mágicamente en tu test. Si no lo pones, el test hará peticiones reales.
> - `responses.add(responses.GET, url, json={"key": "value"}, status=200)`: Le enseña al interceptor: "Oye, cuando alguien haga un GET a esta `url`, devuélvele un objeto con este `json` y este `status` (200 OK)".

## 5. Calidad y Tipado Estático con `mypy` en Data Pipelines

En ingeniería de datos, un error de tipo en tiempo de ejecución (ej. pasar una tupla donde se esperaba un string) puede tumbar un pipeline después de horas de procesamiento.

Para evitar esto, los pipelines profesionales incorporan **anotaciones de tipo explícitas** (Type Hints) y verificación estática con **`mypy`**:

```python
from typing import Any

# Anotaciones claras en parámetros y valor de retorno:
def extract_catalog(endpoint: str, timeout: int = 10) -> list[dict[str, Any]]:
    # ...
    return []
```

### Ejecutar `mypy` en la Terminal
Antes de enviar tu código a producción (o someter tu Rite), ejecuta:
```bash
mypy src/
```
`mypy` analizará tu código sin ejecutarlo, detectando discrepancias de tipos, retornos inconsistentes y posibles referencias `None`. Un Definition of Done (DoD) profesional exige **0 errores de mypy**.

---

## Misión a seguir
Dirígete a `quests/01-extraccion-api/` y completa el laboratorio de extracción. ¡Asegúrate de llevar tu placa del Gremio!

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar conceptos de auth y extraccion REST` o `feat(quests): extraer ingredientes con requests`.
