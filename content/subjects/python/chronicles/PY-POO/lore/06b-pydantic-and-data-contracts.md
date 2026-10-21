# Capítulo 06B: Contratos Fuertes y Validación de Datos con Pydantic V2

> **Prerrequisito conceptual:** Haber completado el Capítulo 02 (`@dataclass`) y el Capítulo 06 (§1 a §4: Excepciones Personalizadas y Logging).  
> **Área temática:** Frontera de Ingestión de Datos y Calidad de Esquemas.

---

## 1. La Evolución del Manejo de Datos en Python

A lo largo de tu trayectoria en Python, has modelado entidades y datos estructurados usando distintas herramientas del lenguaje. Cada una resolvió una limitación del nivel anterior:

```text
Evolución de Estructuras de Datos en Python:
1. Diccionarios planos (dict)       --> Flexibles, pero sin tipado, sin autocompletado y propensos a KeyError.
2. Clases tradicionales (__init__)  --> Permiten encapsulación y métodos, pero exigen excesivo código boilerplate.
3. @dataclass (Capítulo 02)         --> Sintaxis limpia y representaciones automáticas, pero CERO validación en runtime.
4. Pydantic BaseModel (Este Cap)    --> Validación en tiempo de ejecución, tipado estricto y coerción automática de tipos.
```

### Analogía 1: La Aduana de Frontera con Escáner Biométrico
Imagina el control migratorio de un país de alta seguridad:
* **El guardia pasivo (`@dataclass`):** Solo mira si tienes una hoja de papel en la mano. Si la hoja es una servilleta rayada con crayón que dice "Pasaporte", el guardia sonríe y te deja entrar. El desastre ocurre adentro cuando intentas registrarte en el hotel.
* **El escáner biométrico (`Pydantic`):** Comprueba el chip digital, valida que la firma criptográfica coincida, verifica que la fecha de expiración sea futura y que la foto corresponda a tus rasgos faciales. Si algo no coincide, activa una alarma inmediata (`ValidationError`) en el punto cero, impidiendo que el dato corrupto ponga un solo pie dentro del país.

### Analogía 2: El Plano de Arquitectura Visado
Imagina construir una torre de telecomunicaciones:
* Una `@dataclass` es el boceto preliminar que dibujas en una libreta. No hay ingenieros revisándolo; si anotaste que una viga de soporte resiste -500 kg de peso, el papel lo acepta.
* Un `BaseModel` de Pydantic es el plano visado por el colegio de ingenieros estructurales: cada cota tiene tolerancias mínimas y máximas (`Field(gt=0)`), los materiales deben pertenecer al catálogo aprobado (`@field_validator`) y si intentas ingresar un valor imposible, el visado se rechaza antes de comprar el primer gramo de acero.

---

## 2. Zero Assumption: Configuración del Entorno

Pydantic es una librería externa mantenida por la comunidad y altamente optimizada en Rust (`pydantic-core`). Para garantizar reproducibilidad en tu entorno virtual:

```bash
# Instalación de Pydantic V2 en el entorno virtual
pip install "pydantic>=2.8.0"

# Verificación de instalación y versión
python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')"
```

---

## 3. El Problema Crítico: La Ilusión de Seguridad de `@dataclass`

### ¿QUÉ es?
En el Capítulo 02 aprendiste a usar `@dataclass`. Permite definir atributos con anotaciones de tipo (`name: str`, `altitude_km: float`).

### ¿POR QUÉ falla en producción?
Las anotaciones de tipo de Python son **únicamente pistas de análisis estático (type hints)** para el editor o herramientas como `mypy`. **El intérprete de Python ignora por completo los tipos durante la ejecución del programa.**

### ¿CÓMO se evidencia el fallo?

```python
# 🎯 Objetivo de Negocio: Demostrar cómo una dataclass acepta datos corruptos sin emitir advertencias en tiempo de ejecución.

from dataclasses import dataclass

@dataclass
class VulnerableSensorReading:
    sensor_id: str
    temperature_celsius: float
    battery_percentage: int

# ❌ PELIGRO: Python NO valida tipos ni rangos en tiempo de ejecución
corrupted_packet = VulnerableSensorReading(
    sensor_id="",                  # Identificador vacío
    temperature_celsius="extreme", # String en vez de float
    battery_percentage=-150        # Porcentaje negativo imposible
)

print(corrupted_packet)
# Output: VulnerableSensorReading(sensor_id='', temperature_celsius='extreme', battery_percentage=-150)
```

**Consecuencia en el pipeline:** Si este objeto entra a tu motor de cálculo o base de datos, provocará fallos catastróficos (`TypeError` al multiplicar, balances alterados, o registros inválidos guardados silenciosamente).

---

## 4. Los Cuatro Pilares de Pydantic V2

### 4.1 `BaseModel` (Tipado y Coerción Automática)

#### QUÉ es:
Es la clase base provista por Pydantic de la cual heredan todos los esquemas de datos.

#### CÓMO funciona internamente:
Cuando instancias un `BaseModel`, Pydantic inspecciona los argumentos recibidos contra las anotaciones de tipo. Si un valor no coincide exactamente con el tipo anotado pero es **convertible sin ambigüedad** (por ejemplo, el string `"42.5"` para un campo `float`), Pydantic realiza una **coerción de tipos automática**. Si el dato no es convertible (por ejemplo, `"n/a"` para un `float`), frena la ejecución.

```python
# 🎯 Objetivo de Negocio: Validar automáticamente tipos y convertir strings compatibles a valores numéricos en la entrada de datos.

from pydantic import BaseModel, ValidationError

class TelemetryHeader(BaseModel):
    station_id: str
    frequency_mhz: float
    is_active: bool

# ✅ Coerción automática exitosa:
valid_header = TelemetryHeader(
    station_id="GS-ALPHA-01",
    frequency_mhz="437.45",  # Convertido de string a float
    is_active=1              # Convertido de int 1 a True
)

print(type(valid_header.frequency_mhz))  # <class 'float'>
print(valid_header.is_active)           # True

# 🛑 Rechazo inmediato de tipo incompatible:
try:
    invalid_header = TelemetryHeader(
        station_id="GS-ALPHA-01",
        frequency_mhz="uncalibrated",  # Imposible de convertir a float
        is_active=True
    )
except ValidationError as error:
    print("Rechazo de tipo detectado:")
    for err in error.errors():
        print(f"Campo: {err['loc']} -> Error: {err['msg']}")
```

---

### 4.2 `Field(...)` (Restricciones Declarativas de Negocio)

#### QUÉ es:
Es una función de Pydantic que permite declarar restricciones numéricas, de longitud y valores por defecto directamente en la definición del campo, sin escribir condicionales manuales.

#### Parámetros fundamentales:
* `gt` (*greater than*): Estrictamente mayor que (`gt=0`).
* `ge` (*greater than or equal*): Mayor o igual que (`ge=0`).
* `lt` (*less than*): Estrictamente menor que (`lt=100`).
* `le` (*less than or equal*): Menor o igual que (`le=100`).
* `min_length`: Longitud mínima para strings o secuencias (`min_length=3`).
* `max_length`: Longitud máxima para strings (`max_length=64`).
* `default`: Valor por defecto cuando la carga útil no incluye la llave.

```python
# 🎯 Objetivo de Negocio: Restringir rangos físicos de operación en sensores orbitales mediante restricciones declarativas.

from pydantic import BaseModel, Field, ValidationError

class OrbitParameters(BaseModel):
    satellite_code: str = Field(min_length=3, max_length=12)
    perigee_altitude_km: float = Field(ge=160.0, le=2000.0) # Órbita baja terrestre (LEO)
    inclination_degrees: float = Field(ge=0.0, le=180.0)
    encryption_enabled: bool = True # Valor por defecto

# ✅ Parámetros dentro de norma física:
orbit = OrbitParameters(
    satellite_code="SAT-ORION-9",
    perigee_altitude_km=420.5,
    inclination_degrees=51.6
)
print(orbit.encryption_enabled)  # True

# 🛑 Parámetros que violan las restricciones físicas:
try:
    bad_orbit = OrbitParameters(
        satellite_code="X",             # Error: min_length=3
        perigee_altitude_km=50.0,       # Error: ge=160.0 (peligro de reingreso atmosférico)
        inclination_degrees=210.0       # Error: le=180.0
    )
except ValidationError as error:
    print(f"Total de violaciones detectadas: {len(error.errors())}")
```

---

### 4.3 `@field_validator` (Reglas de Dominio Complejas)

#### QUÉ es:
Es un decorador utilizado para aplicar lógica de negocio personalizada sobre campos individuales que no pueden resolverse con simples operadores de rango (por ejemplo: comprobación contra listas maestras permitidas, normalización de formatos de texto o cálculos derivados).

#### ¿Por qué requiere `@classmethod`?
En Pydantic V2, el validador de campo se ejecuta **durante el proceso de instanciación del modelo**, antes de que la instancia final (`self`) haya terminado de construirse en memoria. Por ende, opera a nivel de clase recibiendo `(cls, value: Any)` y **debe retornar el valor transformado o validado**.

```python
# 🎯 Objetivo de Negocio: Normalizar a mayúsculas y validar que la banda de transmisión satelital pertenezca a un espectro internacional autorizado.

from pydantic import BaseModel, field_validator, ValidationError

class RadioTransmissionSpec(BaseModel):
    transmitter_id: str
    frequency_band: str

    @field_validator("frequency_band")
    @classmethod
    def validate_frequency_band(cls, value: str) -> str:
        cleaned_band = value.strip().upper()
        allowed_bands = {"UHF", "VHF", "S-BAND", "X-BAND", "KA-BAND"}

        if cleaned_band not in allowed_bands:
            raise ValueError(
                f"Transmission band '{value}' is not within authorized ITU spectrum "
                f"({sorted(list(allowed_bands))})"
            )
        return cleaned_band  # El valor retornado será el almacenado en el atributo
```

---

### 4.4 `ValidationError` (Anatomía del Error de Validación)

#### QUÉ es:
Es la excepción técnica que lanza Pydantic cuando cualquier regla de `BaseModel`, `Field` o `@field_validator` es quebrantada.

#### Estructura interna de `error.errors()`:
Cada entrada en la lista contiene:
* `loc`: Tupla con la ruta del campo problemático (ej. `('perigee_altitude_km',)`).
* `msg`: Mensaje descriptivo legible del fallo.
* `type`: Identificador formal de la regla violada (ej. `'greater_than_equal'`, `'string_too_short'`, `'value_error'`).
* `input`: El valor original exacto que causó el fallo.

---

## 5. Ubicación Arquitectónica: Pydantic en la Frontera de Ingestión

En ingeniería de software y datos profesional, **Pydantic no se utiliza en toda la aplicación; vive en el perímetro exterior (Boundary / Ingestion Layer)**:

```text
[API Externa / Archivo Telemetría / Evento de Red]
                        │
                        ▼ (Frontera del Sistema)
          ┌───────────────────────────┐
          │   Pydantic Ingestion Gate  │  <-- Valida, coerciona y limpia
          └─────────────┬─────────────┘
                        │
              ┌─────────┴─────────┐
              ▼ (Datos Válidos)   ▼ (Datos Corruptos: ValidationError)
        ┌───────────────┐   ┌────────────────────────────────────────┐
        │ Lógica Core / │   │ Logger Structured Error                │
        │ Base de Datos │   │ Traducción a Excepción de Dominio      │
        └───────────────┘   │ Dead-Letter Queue (DLQ / Archivo Cuarentena)
                            └────────────────────────────────────────┘
```

El núcleo analítico jamás debe recibir diccionarios crudos ni lidiar con `ValidationError`. La frontera captura el error técnico y lo transforma en una **Excepción de Dominio** estructurada.

---

## 6. Ejemplo Completo End-to-End: Ingestor de Paquetes Orbitales

Observa a continuación la integración completa de todos los conceptos: Excepción de dominio, Modelo Pydantic con restricciones y validador, función de ingestión perimetral y manejo estructurado.

```python
# 🎯 Objetivo de Negocio: Ingestar paquetes de telemetría de satélites orbitales, validar el payload crudo mediante un esquema estricto, rechazar anomalías antes de ingresar a la base de datos y transformar errores técnicos en eventos de dominio rastreables.

from typing import Any, Dict
from pydantic import BaseModel, Field, field_validator, ValidationError


# 1. Domain Exception (Luz del tablero propia de la aplicación)
class CorruptedTelemetryPacketError(Exception):
    """Raised when an incoming telemetry packet violates orbital contract schemas."""
    pass


# 2. Schema Model (Aduana de entrada con Pydantic)
class OrbitalTelemetryPayload(BaseModel):
    satellite_id: str = Field(min_length=4, max_length=16)
    battery_level_pct: float = Field(ge=0.0, le=100.0)
    solar_panel_voltage: float = Field(ge=0.0)
    transmission_band: str = "UHF"
    reboot_count: int = Field(default=0, ge=0)

    @field_validator("transmission_band")
    @classmethod
    def enforce_valid_radio_band(cls, value: str) -> str:
        clean_band = value.strip().upper()
        authorized_bands = {"UHF", "VHF", "S-BAND", "X-BAND"}
        if clean_band not in authorized_bands:
            raise ValueError(f"Unauthorized transmission band: '{value}'")
        return clean_band


# 3. Boundary Ingestion Function (Frontera de Ingestión)
def ingest_telemetry_packet(raw_payload: Dict[str, Any]) -> OrbitalTelemetryPayload:
    """
    Validates and ingests raw dictionary payload into a certified domain model.
    Catches technical ValidationError and translates it into a domain exception.
    """
    try:
        return OrbitalTelemetryPayload(**raw_payload)
    except ValidationError as validation_err:
        error_details = [
            f"Field '{err['loc'][0]}': {err['msg']} (received: {err.get('input')})"
            for err in validation_err.errors()
        ]
        summary_message = " | ".join(error_details)
        raise CorruptedTelemetryPacketError(
            f"Telemetry ingestion rejected due to schema violations: {summary_message}"
        ) from validation_err


# --- Demostración de Ejecución ---

# Caso A: Payload crudo válido proveniente de la red
raw_valid_data = {
    "satellite_id": "SAT-ORION-01",
    "battery_level_pct": "87.5",  # Se convertirá automáticamente a float 87.5
    "solar_panel_voltage": 28.4,
    "transmission_band": "s-band"  # Se normalizará a "S-BAND"
}

telemetry_record = ingest_telemetry_packet(raw_valid_data)
print(f"Record accepted: {telemetry_record.satellite_id} | Band: {telemetry_record.transmission_band}")
# Output: Record accepted: SAT-ORION-01 | Band: S-BAND

# Caso B: Payload corrupto (batería imposible y banda ilegal)
raw_corrupt_data = {
    "satellite_id": "SAT-ERR",
    "battery_level_pct": 145.0,     # Ilegal: le=100.0
    "solar_panel_voltage": -5.0,    # Ilegal: ge=0.0
    "transmission_band": "MICROWAVE" # Ilegal: no autorizada
}

try:
    ingest_telemetry_packet(raw_corrupt_data)
except CorruptedTelemetryPacketError as domain_err:
    print(f"Domain rejection captured:\n{domain_err}")
```

---

## 7. Conexión con Testing (Ciclo AAA con Pytest)

Para probar modelos y fronteras de Pydantic seguimos rigurosamente el patrón **Arrange-Act-Assert (AAA)** en `pytest`. Debemos verificar:
1. Instanciación válida y coerción exitosa.
2. Violaciones de rango en `Field` disparando `ValidationError`.
3. Validadores personalizados rechazando valores no admitidos.
4. Función de frontera envolviendo el error técnico en la excepción de dominio.

```python
# 🎯 Objetivo de Negocio: Probar exhaustivamente contratos de datos, validadores y traducción de excepciones en la suite de pruebas unitarias.

import pytest
from pydantic import ValidationError


def test_telemetry_payload_coercion_and_defaults():
    # Arrange: Preparar datos crudos convertibles y sin campo opcional
    raw_packet = {
        "satellite_id": "SAT-NOVA-44",
        "battery_level_pct": "95.0",
        "solar_panel_voltage": 32.1,
        "transmission_band": "uhf"
    }

    # Act: Construir el modelo
    payload = OrbitalTelemetryPayload(**raw_packet)

    # Assert: Verificar tipos convertidos, valores normalizados y defaults
    assert payload.satellite_id == "SAT-NOVA-44"
    assert payload.battery_level_pct == 95.0
    assert isinstance(payload.battery_level_pct, float)
    assert payload.transmission_band == "UHF"
    assert payload.reboot_count == 0  # Valor por defecto


def test_telemetry_payload_raises_on_out_of_bounds_battery():
    # Arrange: Carga con nivel de batería por encima del 100%
    invalid_packet = {
        "satellite_id": "SAT-NOVA-44",
        "battery_level_pct": 105.0,
        "solar_panel_voltage": 24.0
    }

    # Act & Assert: Verificar que Pydantic rechace la violación de Field(le=100.0)
    with pytest.raises(ValidationError) as exc_info:
        OrbitalTelemetryPayload(**invalid_packet)

    errors = exc_info.value.errors()
    assert any(err["loc"][0] == "battery_level_pct" for err in errors)


def test_telemetry_payload_rejects_unauthorized_band():
    # Arrange: Carga con banda no autorizada
    invalid_packet = {
        "satellite_id": "SAT-NOVA-44",
        "battery_level_pct": 80.0,
        "solar_panel_voltage": 24.0,
        "transmission_band": "LASER-BAND"
    }

    # Act & Assert: El @field_validator debe lanzar ValueError envuelto en ValidationError
    with pytest.raises(ValidationError) as exc_info:
        OrbitalTelemetryPayload(**invalid_packet)

    assert "Unauthorized transmission band" in str(exc_info.value)


def test_ingest_telemetry_packet_translates_into_domain_exception():
    # Arrange: Carga con identificador de satélite demasiado corto (< 4 chars)
    corrupted_data = {
        "satellite_id": "SAT",
        "battery_level_pct": 50.0,
        "solar_panel_voltage": 20.0
    }

    # Act & Assert: La función de frontera debe levantar CorruptedTelemetryPacketError
    with pytest.raises(CorruptedTelemetryPacketError) as exc_info:
        ingest_telemetry_packet(corrupted_data)

    assert "satellite_id" in str(exc_info.value)
    assert isinstance(exc_info.value, CorruptedTelemetryPacketError)
```

---

## 8. Mapa de Ejercicios Prácticos

Con esta base teórica completa, procede a resolver los dos ejercicios graduales en `quests/06-logging/`:

- [[03-dataclass-to-pydantic]]: Migrar una `@dataclass` a un `BaseModel` con `Field` (Paso 1).
- [[04-pydantic-domain-exceptions]]: Implementar `@field_validator` e integrar con excepciones de dominio en la frontera (Paso 2).
