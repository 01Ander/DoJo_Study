# Capítulo 06: Logging y Error Handling

Un pipeline fallará en producción. Archivos corruptos, APIs caídas, datos faltantes. Si usas `print()`, esa información se pierde al cerrar la consola o al rotar los contenedores en la nube. 

## 1. El Módulo Logging

El módulo `logging` es la forma profesional de registrar eventos en un sistema. 

### Analogía: La Caja Negra del Avión
Imagina que vas en un avión y hay turbulencia. 
- **Usar `print()`:** Es como si el piloto abriera la ventana y gritara "¡Hay turbulencia!". Si nadie lo escuchó en ese exacto milisegundo, la información se pierde para siempre.
- **Usar `logging`:** Es la Caja Negra del avión. Registra exactamente la hora, la severidad del problema (INFO, WARNING, ERROR, CRITICAL) y el mensaje. Si el avión aterriza (o se estrella), los ingenieros pueden abrir la caja negra y ver todo el historial de vuelo.

### Ejemplo de Código
```python
# ❌ MAL: print no tiene contexto ni niveles
print("Empezando a procesar el archivo")
print("Error: archivo no encontrado")

# ✅ BIEN: logging
import logging

# Configuración básica (generalmente en el Orquestador o en cli.py)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FileProcessor:
    def process(self, filepath: str):
        logger.info(f"Empezando a procesar: {filepath}")
        # ...
        logger.warning("Campo edad vacío, usando default.")
        # ...
        logger.error("Archivo no encontrado. Abortando operación.")
```

## 2. Excepciones Personalizadas (Domain Exceptions)

En Python existen errores como `ValueError` o `TypeError`. Pero en código empresarial, necesitamos atrapar errores específicos del negocio para saber exactamente qué falló.

### Analogía: Las Luces del Tablero del Auto
Imagina que tu auto se descompone.
- **Sin Excepciones Custom:** Solo se enciende una luz roja gigante que dice "ERROR". Podría ser que no tienes gasolina, o podría ser que el motor explotó. No tienes idea de cómo solucionarlo.
- **Con Excepciones Custom:** El tablero tiene luces específicas: "Presión de Aceite Baja", "Puerta Abierta", "Sin Gasolina". Sabes exactamente cuál es el problema y cómo reaccionar.

### Ejemplo de Código
```python
# Creamos nuestras "luces del tablero" personalizadas
class InvalidTransactionError(Exception):
    pass

class ExpiredCardError(Exception):
    pass

class Engine:
    def process(self, amount, card_year):
        if amount < 0:
            # Encendemos la luz específica
            raise InvalidTransactionError(f"El monto no puede ser negativo: {amount}")
        if card_year < 2024:
            raise ExpiredCardError("La tarjeta está vencida")
```

## 3. Manejo en el Orquestador

El orquestador es quien atrapa estas excepciones de dominio, loggea el error crítico, y decide si el pipeline aborta de forma segura o continúa con el siguiente registro (por ejemplo, ignorar la transacción mala y seguir con la siguiente).

```python
    def run(self):
        try:
            self.engine.process(-5, 2025)
        except InvalidTransactionError as e:
            # Atrapamos la luz de advertencia y la guardamos en la caja negra
            logger.error(f"Falla en el pipeline: {e}")
```

## 4. Conexión con Testing (Nivel 2)

Podemos testear que nuestra clase levante (raise) la excepción correcta cuando debe hacerlo usando `pytest.raises`.

```python
import pytest

def test_raises_invalid_transaction():
    engine = Engine()
    # "Esperamos que este bloque de código arroje un InvalidTransactionError"
    with pytest.raises(InvalidTransactionError):
        engine.process(-5, 2025)
```

## 5. Validación de Datos con Pydantic (Modelos y Contratos Fuertes)

En pipelines modernos de ingeniería de datos, los registros provienen de orígenes no confiables: APIs externas, archivos CSV con columnas corruptas, o JSONs con tipos inesperados (`"100"` en vez de `100`, campos nulos donde se requería un entero, o montos negativos).

Si validáramos cada campo manualmente usando cascadas de `if isinstance(...)` y `if amount < 0`, el código se volvería inmanejable y frágil. Aquí es donde entra **Pydantic**.

### Analogía: La Aduana Aeroportuaria
Imagina la entrada a un país de alta seguridad:
- **Validación manual básica:** Un guardia le pregunta al viajero: "¿Trae algo ilegal?". Si el viajero miente o no sabe responder, pasa sin revisión profunda.
- **Pydantic:** Es el escáner biométrico de rayos X. Analiza el equipaje completo contra un manifiesto estricto: tipo de datos, límites, formatos de texto y reglas especiales. Si algo viola las leyes, emite una alarma inmediata (`ValidationError`) indicando con precisión quirúrgica qué maleta (campo) y qué norma falló.

### Componentes Clave de Pydantic V2

1. **`BaseModel`:** Clase base de la que heredan todos los esquemas. Convierte tipos automáticamente si es posible (e.g. `"42"` a `42`) y valida tipos estrictos.
2. **`Field`:** Permite definir restricciones declarativas como `gt` (mayor que), `ge` (mayor o igual), `min_length`, valores por defecto o descripciones.
3. **`@field_validator`:** Decorador para reglas de negocio personalizadas sobre campos específicos.
4. **`ValidationError`:** Excepción nativa que lanza Pydantic al encontrar inconsistencias. Contiene la lista detallada de errores (`e.errors()`).

### Ejemplo Didáctico (Dominio Alquímico / Laboratorio Mágico)

```python
from pydantic import BaseModel, Field, field_validator, ValidationError

class PotionRecipe(BaseModel):
    name: str = Field(min_length=3)
    potency: int = Field(gt=0, le=100)
    element: str = "Neutral"

    @field_validator("element")
    @classmethod
    def validate_element(cls, value: str) -> str:
        allowed = {"Fire", "Water", "Earth", "Air", "Neutral"}
        if value.capitalize() not in allowed:
            raise ValueError(f"Elemento '{value}' no reconocido en el grimorio.")
        return value.capitalize()

# Uso exitoso:
recipe = PotionRecipe(name="Elixir de Fénix", potency=85, element="fire")
print(recipe.element)  # Output: "Fire" (normalizado por el validador)

# Falla de validación:
try:
    bad_recipe = PotionRecipe(name="Veneno", potency=150, element="Void")
except ValidationError as e:
    # Pydantic nos dice exactamente qué campos fallaron:
    # 1. potency: Input should be less than or equal to 100
    # 2. element: Elemento 'Void' no reconocido en el grimorio.
    print(f"Alquimia rechazada: {e}")
```

### Integración con Excepciones de Dominio y Logging
En la capa de servicio o ingesta, un buen patrón consiste en capturar `ValidationError` y transformar la falla técnica en una **Excepción de Dominio** contextualizada (como `InvalidRecordError`) o registrar el incidente en el logger antes de descartar el registro.

---

## 6. Mapa de Ejercicios

Dirígete a `quests/06-logging/`:

- [[01-custom-exceptions]]
- [[02-test-exceptions]]
- [[03-pydantic-validation]]

```text
PY-POO/quests/06-logging/
├── [[01-custom-exceptions]].md      (Tipo A: Lanzar Errores)
├── [[02-test-exceptions]].md        (Tipo B: Testing Nivel 2)
└── [[03-pydantic-validation]].md     (Tipo A: Validación de Esquemas con Pydantic)
```

