# Capítulo 06B: Contratos Fuertes y Validación de Datos con Pydantic V2

> **Prerrequisito conceptual:** Haber completado el Capítulo 02 (`@dataclass`) y el Capítulo 06 (§1 a §4: Excepciones Personalizadas y Logging).

---

## 1. La Evolución del Manejo de Datos en Python

A lo largo de tu aprendizaje en Python, has modelado entidades con diferentes niveles de sofisticación:

```text
Evolución de Estructuras de Datos en Python:
1. Diccionarios planos (dict)  --> Flexibles, pero sin tipado estricto, sin autocompletado y propensos a KeyError.
2. Clases tradicionales (__init__) --> Permiten encapsulación y métodos, pero exigen excesivo código boilerplate.
3. @dataclass (Capítulo 02)    --> Sintaxis limpia y representaciones automáticas, pero CERO validación en runtime.
4. Pydantic BaseModel (Este Cap) --> Validación en tiempo de ejecución, tipado estricto y coerción automática de tipos.
```

---

## 2. El Problema Crítico: La Ilusión de Seguridad de `@dataclass`

En el Capítulo 02 aprendiste a usar `@dataclass`. Son extraordinarias para estructurar datos internos y limpios generados por tu propio código. Sin embargo, **las anotaciones de tipo de Python son solo pistas (type hints); el intérprete de Python nunca las valida en tiempo de ejecución**.

Observa este experimento real:

```python
from dataclasses import dataclass

@dataclass
class TransactionDataclass:
    account_id: int
    amount: float

# ❌ Esto NO falla en Python:
bad_tx = TransactionDataclass(account_id="cuenta_fantasma", amount=-9999.0)
print(bad_tx)
# Imprime: TransactionDataclass(account_id='cuenta_fantasma', amount=-9999.0)
```

`TransactionDataclass` aceptó un texto donde iba un entero y un monto negativo absurdo. Si este objeto llega a tu motor contable o a la base de datos, corromperá el balance silenciosamente.

Para evitar esto con `@dataclass`, tendrías que escribir un método `__post_init__` con decenas de líneas de `if not isinstance(...)` e `if amount < 0: raise ValueError(...)`.

---

## 3. La Solución Industrial: Pydantic `BaseModel`

Pydantic convierte tus clases en **aduanas de datos activas**. Si los datos son válidos o convertibles, crea el objeto; si los datos violan las reglas, levanta una alarma inmediata (`ValidationError`) detallando con precisión quirúrgica qué falló.

```python
from pydantic import BaseModel, Field, ValidationError

class TransactionPydantic(BaseModel):
    account_id: int = Field(gt=0)
    amount: float = Field(gt=0.0)

# ✅ Coerción inteligente: convierte el string "1500.50" en float 1500.50
ok_tx = TransactionPydantic(account_id=101, amount="1500.50")
print(ok_tx.amount)  # 1500.5 (número real, no string)

# 🛑 Rechazo inmediato de datos corruptos:
try:
    bad_tx = TransactionPydantic(account_id="no_es_numero", amount=-50.0)
except ValidationError as e:
    print("Datos rechazados en la entrada:")
    for err in e.errors():
        print(f" - Campo: {err['loc'][0]} -> {err['msg']}")
```

---

## 4. Los Cuatro Pilares de Pydantic V2

### 1. `BaseModel`
Es la clase base de Pydantic. Todo modelo hereda de ella.
* **Inspección de tipos:** Analiza las anotaciones `int`, `str`, `float`, `bool`.
* **Coerción de tipos:** Si un campo es `int` y recibe `"42"`, lo convierte a `42`. Si recibe `"cuarenta y dos"`, falla.
* **Serialización integrada:** Convierte el modelo a diccionario con `.model_dump()` o a JSON con `.model_dump_json()`.

### 2. `Field(...)`
Permite declarar **restricciones de negocio declarativas** sin escribir código procedimental:
* `gt` (*greater than*): Estrictamente mayor que (`Field(gt=0)`).
* `ge` (*greater or equal*): Mayor o igual que (`Field(ge=18)`).
* `lt` / `le` (*less than / less or equal*): Menor / Menor o igual.
* `min_length` / `max_length`: Longitud mínima y máxima de strings o listas (`Field(min_length=3)`).
* `default`: Valor por defecto (`currency: str = "USD"`).

### 3. `@field_validator`
Se utiliza cuando una restricción no puede resolverse con una simple comparación numérica (por ejemplo: validar que una moneda pertenezca a una lista aprobada, o forzar que un código esté en mayúsculas).

> **¿Por qué `@classmethod`?**  
> En Pydantic V2, los validadores de campo operan con `@classmethod` porque se ejecutan **durante el proceso de instanciación**, antes de que el objeto final (`self`) haya sido completamente ensamblado en memoria.

```python
from pydantic import BaseModel, field_validator

class CurrencySchema(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def must_be_valid_iso(cls, value: str) -> str:
        clean_value = value.strip().upper()
        allowed = {"USD", "EUR", "COP", "GBP"}
        if clean_value not in allowed:
            raise ValueError(f"Moneda '{value}' no soportada por el sistema.")
        return clean_value  # El retorno es el valor que finalmente se guarda
```

### 4. `ValidationError`
Es la excepción que lanza Pydantic al encontrar inconsistencias. Contiene:
* `.errors()`: Lista de diccionarios con cada error encontrado, su ubicación (`loc`), tipo de error (`type`) y mensaje legible (`msg`).
* Permite acumular **todos los errores de un registro a la vez**, en vez de fallar de uno en uno.

---

## 5. Ubicación Arquitectónica: ¿Dónde se usa Pydantic en un Pipeline?

En arquitecturas limpias y pipelines de datos, **Pydantic vive exclusivamente en la frontera de entrada (Boundary / Ingestion Layer)**:

```text
[API Externa / Archivo CSV / Payload JSON]
                   │
                   ▼ (Frontera del Sistema)
     ┌───────────────────────────┐
     │  Pydantic Schema Parser   │  <-- Valida, coerciona y limpia
     └─────────────┬─────────────┘
                   │
         ┌─────────┴─────────┐
         ▼ (Datos Válidos)   ▼ (Datos Corruptos: ValidationError)
   ┌───────────────┐   ┌────────────────────────────────────────┐
   │ Entidades del │   │ Logging (logger.error)                 │
   │ Dominio / ETL │   │ Traducción a Excepción de Dominio      │
   └───────────────┘   │ Descarte a archivo de rechazos (DLQ)   │
                       └────────────────────────────────────────┘
```

El núcleo de tu negocio (motores analíticos, agregaciones, modelos ML) no debe preocuparse por si un monto viene en string o si la fecha viene mal formateada. La aduana de Pydantic garantiza que al núcleo solo ingresen datos 100% íntegros.

---

## 6. Progresión de Quests

Para dominar esta herramienta paso a paso, abordaremos dos ejercicios graduales:

1. **Quest 06-03 (`03-dataclass-to-pydantic`):** Migrar una `@dataclass` vulnerable a un `BaseModel` con `Field` (tipos, coerción y restricciones numéricas).
2. **Quest 06-04 (`04-pydantic-domain-exceptions`):** Validadores de negocio con `@field_validator` y traducción de `ValidationError` a excepciones de dominio con logging.
