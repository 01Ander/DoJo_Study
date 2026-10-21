# Capítulo 01: Abstract Classes and Interfaces

El problema de las clases normales es que cualquiera puede instanciarlas, y Python, por defecto, es un lenguaje "relajado" donde cualquiera puede crear un método con cualquier nombre.

En Ingeniería de Software formal, necesitamos **Contratos Estrictos**. Si estás programando un pipeline y requieres extraer datos, no te importa si vienen de un CSV o una base de datos; solo te importa que el objeto que los extrae tenga un método `.extract()`.

Para forzar esto, usamos **Clases Abstractas (ABC)**.

## 1. El Módulo `abc`

Una Clase Abstracta es un molde *para hacer otros moldes*. **No se puede instanciar directamente**. Solo sirve para obligar a las clases "hijas" a implementar ciertos métodos.

```python
from abc import ABC, abstractmethod

# 1. Definimos el Contrato
class NotificationSender(ABC):
    
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        """Envia un mensaje y retorna True si fue exitoso."""
        pass # La clase abstracta NO implementa el comportamiento

# ❌ Esto fallará con TypeError:
# sender = NotificationSender() 
```

## 2. Implementando el Contrato (Polimorfismo Básico)

Ahora creamos clases concretas que "heredan" de este contrato. Si olvidamos implementar el método `.send()`, la clase se definirá sin problemas, pero Python lanzará un `TypeError` en tiempo de ejecución al momento de intentar instanciarla (`email_service = EmailSender()`), previniendo la creación de objetos incompletos.

```python
# 2. Clase concreta (Hija)
class EmailSender(NotificationSender):
    
    def send(self, message: str, recipient: str) -> bool:
        print(f"Enviando Email a {recipient}: {message}")
        # Lógica real de SMTP aquí...
        return True

class SMSSender(NotificationSender):
    
    def send(self, message: str, recipient: str) -> bool:
        print(f"Enviando SMS a {recipient}: {message}")
        # Lógica real de Twilio API aquí...
        return True

# ✅ Esto funciona:
email_service = EmailSender()
email_service.send("Hola", "test@test.com")
```

## 3. ¿Por qué esto es poderoso? (Inyección de Dependencias)

Imagina una función que orquesta notificaciones. Gracias al contrato `NotificationSender`, esta función no necesita saber *cómo* se envía el mensaje. Puede recibir un `EmailSender` hoy, y un `SlackSender` mañana, sin cambiar una sola línea de código.

```python
def notify_user(sender: NotificationSender, message: str):
    # Confiamos ciegamente en que el método .send() existe
    # porque la clase abstracta lo garantiza.
    sender.send(message, "user123")
```

## 4. Conexión con Testing (Nivel 2: Comprobar el Contrato)

El test más básico para una clase abstracta es validar que su instanciación está prohibida, y que sus hijas cumplen el contrato.

```python
import pytest

def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        # Intentar instanciar la clase abstracta debe fallar
        sender = NotificationSender()

def test_email_sender_obeys_contract():
    # Arrange
    sender = EmailSender()
    # Act
    result = sender.send("Test", "admin")
    # Assert
    assert result is True
```

---

## 5. Extracción Polimórfica Desacoplada (Caso de Estudio: Extractores Multiformato)

### ¿QUÉ es?
En arquitectura de software e ingeniería de datos, desacoplar la extracción significa definir una interfaz abstracta (`AbstractDataExtractor`) que estipule un método común: `.extract(file_path: str) -> list[dict]`. De este modo, los consumidores del pipeline leen registros sin importar si la fuente física es un archivo `.csv` con delimitadores por comas o un archivo `.json` jerárquico.

### Analogía del Mundo Real: El Adaptador Universal de Viaje
Cuando viajas por el mundo, cada país tiene enchufes físicos distintos (tipo A en América, tipo C en Europa, tipo G en Reino Unido). Tu laptop no sabe ni le interesa qué forma física tiene la pared; solo le interesa recibir energía a 220V/110V. El adaptador universal (la clase abstracta) convierte cualquier enchufe físico en la interfaz estándar que tu laptop espera.

### ¿CÓMO se implementa? (Domain Shifting: Red de Observación Meteorológica)

```python
# 🎯 Objetivo de Negocio: Ingestar observaciones climáticas multiformato (CSV y JSON) bajo un contrato polimórfico común.

from abc import ABC, abstractmethod
import csv
import json
from typing import Any, Dict, List


class AbstractClimateExtractor(ABC):
    """Abstract contract enforcing uniform data extraction across formats."""

    @abstractmethod
    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extracts records from file_path and returns a normalized list of dictionaries.
        """
        pass


class CSVClimateExtractor(AbstractClimateExtractor):
    """Concrete extractor parsing comma-separated meteorological logs."""

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, mode="r", encoding="utf-8") as file_handle:
            reader = csv.DictReader(file_handle)
            return [dict(row) for row in reader]


class JSONClimateExtractor(AbstractClimateExtractor):
    """Concrete extractor parsing JSON observation arrays."""

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, mode="r", encoding="utf-8") as file_handle:
            content = json.load(file_handle)
            if isinstance(content, list):
                return content
            return [content]
```

### Conexión con Testing (Ciclo AAA y Polimorfismo)

```python
# 🎯 Objetivo de Negocio: Validar que ambos extractores cumplan el contrato y retornen listas de diccionarios equivalentes.

def test_extractors_obey_polymorphic_contract(tmp_path):
    # Arrange: Preparar datos idénticos en ambos formatos
    json_path = tmp_path / "readings.json"
    json_path.write_text('[{"station": "EST-01", "temp": 21.5}]', encoding="utf-8")

    # Act: Extraer con el extractor JSON
    extractor: AbstractClimateExtractor = JSONClimateExtractor()
    records = extractor.extract(str(json_path))

    # Assert: Validar estructura del contrato
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0]["station"] == "EST-01"
```

---

## 6. Setup y Ejecución

Los módulos `abc`, `csv` y `json` forman parte de la librería estándar de Python (`built-in`). No requieren instalación adicional.

---

## 7. Mapa de Ejercicios

Dirígete a `quests/01-abstractions/` y completa los ejercicios:

- [[01-interface-segregation]]
- [[02-test-structure]]
- [[03-decoupled-json-extractor]]

```text
PY-POO/quests/01-abstractions/
├── [[01-interface-segregation]].md     (Tipo A: Implementación ABC)
├── [[02-test-structure]].md            (Tipo B: Testing Nivel 2)
└── [[03-decoupled-json-extractor]].md   (Tipo A: Extractor Desacoplado CSV y JSON)
```

