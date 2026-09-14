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

## 3. Paginación: Cuando el catálogo es muy grande

**Analogía 2 (Los Tomos del Catálogo):**
Si el Mercado Negro tiene 10,000 ingredientes, el recepcionista no te dará una caja de una tonelada. Te dará el "Tomo 1" y te dirá: *"Si quieres más, pídeme la página 2"*. Esto es la paginación.

En código, solemos enviar un parámetro extra (query param) para pedir la siguiente página, y repetimos hasta que la página venga vacía.

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

---

## Misión a seguir
Dirígete a `quests/01-extraccion-api/` y completa el laboratorio de extracción. ¡Asegúrate de llevar tu placa del Gremio!

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar conceptos de auth y extraccion REST` o `feat(quests): extraer ingredientes con requests`.
