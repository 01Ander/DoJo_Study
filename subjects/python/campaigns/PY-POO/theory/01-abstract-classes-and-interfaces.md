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

Ahora creamos clases concretas que "heredan" de este contrato. Si olvidamos implementar el método `.send()`, Python lanzará un error *antes* de que el código corra, salvándonos de bugs en producción.

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

## 5. Setup y Ejecución

El módulo `abc` viene incluido (built-in) en la librería estándar de Python. No necesitas instalar nada.

## 6. Mapa de Ejercicios

Dirígete a `exercises/01-abstractions/` y completa los ejercicios:

```text
PY-POO/exercises/01-abstractions/
├── 01-interface-segregation.md   (Tipo A: Implementación ABC)
└── 02-test-structure.md          (Tipo B: Testing Nivel 2)
```
