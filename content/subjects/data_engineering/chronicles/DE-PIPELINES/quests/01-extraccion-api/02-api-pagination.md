# Quest 01-02: Consumo Resiliente de APIs con Paginación y Rate Limiting (Nivel 3)

**Objetivo:** Implementar extractores de datos para APIs REST que dominen la paginación por Offset y por Cursor, manejen códigos HTTP 429 (*Too Many Requests*) mediante reintentos con *backoff*, y protejan el pipeline contra bucles infinitos y duplicados (Lore 01 §3).

---

## Contexto de Negocio (Domain Shifting: Telemetría de Vuelo AeroFleet)

La plataforma de monitoreo aeroespacial **AeroFleet Global** ingesta eventos de telemetría de miles de aeronaves en ruta (`telemetry_events`). Debido al volumen masivo de datos:
1. Las consultas históricas se sirven mediante paginación por página/offset (`page` y `limit`).
2. El stream de telemetría continua se entrega mediante cursores opacos (`next_cursor`).
3. Si un script consulta demasiado rápido, el gateway de la API responde con **HTTP 429** y una cabecera `Retry-After`.

---

## Archivo de Trabajo

Edita el archivo [`api_paginator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py).

Debes implementar dos funciones extractoras profesionales dentro de dicho archivo:

### 1. `extract_paginated_offset(api_url: str, token: str, page_size: int = 20, max_pages: int = 50) -> list[dict[str, Any]]`

* **Headers:** Incluye `"Authorization": f"Bearer {token}"`.
* **Parámetros Query:** Envía `params={"page": page, "limit": page_size}`, comenzando en `page = 1`.
* **Estructura de Respuesta Esperada:** El JSON de respuesta contiene la llave `"data"`, que es una lista de diccionarios (cada uno con su `"id"` único).
* **Reglas de Parada:**
  1. Si `batch` viene vacío (`len(batch) == 0`), termina el bucle.
  2. Si `len(batch) < page_size`, se ha procesado la última página: termina el bucle.
  3. Si se alcanza `max_pages`, detiene la extracción para evitar bucles infinitos.
* **Deduplicación:** Si la API devuelve un registro cuyo `"id"` ya fue procesado en una página previa (efecto *Page Drift*), ignóralo para evitar duplicaciones.
* **Retorno:** Retorna la lista acumulada de diccionarios únicos.

---

### 2. `extract_paginated_cursor(api_url: str, token: str, max_pages: int = 50, max_retries: int = 3) -> list[dict[str, Any]]`

* **Headers:** Incluye `"Authorization": f"Bearer {token}"`.
* **Parámetros Query:**
  - Inicialmente envía `params={"limit": 50}`.
  - En iteraciones posteriores, si `next_cursor` no es `None`, añade `"cursor": next_cursor` al diccionario `params`.
* **Estructura de Respuesta Esperada:**
  - `"items"`: Lista de registros extraídos.
  - `"next_cursor"`: String con el cursor para la siguiente petición, o `None`/ausente si es el final.
* **Resiliencia ante Rate Limits (HTTP 429):**
  - Si la respuesta tiene `response.status_code == 429`:
    - Extrae los segundos de espera de `response.headers.get("Retry-After", 1.0)`.
    - Ejecuta `time.sleep(wait_time)`.
    - Reintenta la misma petición hasta un máximo de `max_retries` veces.
    - Si se superan los `max_retries` sin éxito, lanza la excepción `RateLimitExceededError`.
  - Para cualquier otro error (4xx/5xx), invoca `response.raise_for_status()`.
* **Reglas de Parada:**
  - Si `"next_cursor"` es `None`, string vacío, o no viene en la respuesta, termina el bucle.
  - Si se alcanza `max_pages`, termina el bucle.
* **Retorno:** Retorna la lista total de registros acumulados.

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas unitarias automatizada:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/pytest content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/test_api_pagination.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```python
import time
import requests
from typing import Any

class RateLimitExceededError(Exception):
    pass

def extract_paginated_offset(
    api_url: str, token: str, page_size: int = 20, max_pages: int = 50
) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    seen_ids = set()
    page = 1

    while page <= max_pages:
        params = {"page": page, "limit": page_size}
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        batch = response.json().get("data", [])

        if not batch:
            break

        for item in batch:
            item_id = item.get("id")
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                results.append(item)

        if len(batch) < page_size:
            break

        page += 1

    return results

def extract_paginated_cursor(
    api_url: str, token: str, max_pages: int = 50, max_retries: int = 3
) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    all_items = []
    next_cursor = None
    pages = 0

    while pages < max_pages:
        params = {"limit": 50}
        if next_cursor:
            params["cursor"] = next_cursor

        retries = 0
        while retries <= max_retries:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            if response.status_code == 429:
                wait_time = float(response.headers.get("Retry-After", 1.0))
                time.sleep(wait_time)
                retries += 1
                continue
            response.raise_for_status()
            break
        else:
            raise RateLimitExceededError("Rate limit exceeded")

        payload = response.json()
        all_items.extend(payload.get("items", []))
        pages += 1

        next_cursor = payload.get("next_cursor")
        if not next_cursor:
            break

    return all_items
```
</details>
