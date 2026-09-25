# Capítulo 00: AWS Identity & Access Management (IAM)

Bienvenido a la nube. Hasta ahora, todos tus scripts corrían en tu computadora local o en un servidor dedicado. Cuando trabajamos en la nube (específicamente en Amazon Web Services o AWS), necesitamos una forma centralizada de identificarnos y de restringir quién puede hacer qué. Aquí es donde entra **IAM**.

## 1. El Concepto Principal (Qué y Por qué)

**QUÉ es:** IAM (*Identity and Access Management*) es el servicio central de AWS que controla la autenticación (quién eres) y la autorización (qué puedes hacer). Es el guardia de seguridad insobornable de tu infraestructura en la nube.
**POR QUÉ importa:** Sin IAM, cualquiera con acceso a tu sistema podría borrar bases de datos enteras, exponer datos sensibles de clientes, o gastar miles de dólares en servidores minando criptomonedas. IAM evita desastres.

> **Densidad (Analogía del Gremio de Dragones):**
> - **IAM User:** Imagina el Gremio de Cuidadores de Dragones. IAM es el sistema de gafetes mágicos. El novato recién ingresado no debe tener llaves del depósito de dragones adultos inestables; su gafete (IAM User programático con Access Keys) solo le permite entrar a la sala de crías.
> - **IAM Role:** Es como un "Sombrero Mágico de Domador". El sombrero otorga los permisos para acercarse a dragones alfa. No se lo das a una persona permanentemente; simplemente, quien esté de turno se pone el sombrero, hace el trabajo y se lo quita (credenciales temporales rotativas).

Para otorgar estos permisos usamos las **IAM Policies** (documentos JSON que definen explícitamente qué acciones se permiten o deniegan basándose en el principio del mínimo privilegio).

### El formato JSON de una Policy

Aunque es configuración y no Python, es fundamental entender la estructura de estos permisos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::alimento-dragones-pantano/*"
      ]
    }
  ]
}
```

*Zero Surprise Syntax:*
- `"Effect": "Allow"`: Define si el bloque está permitiendo o bloqueando una acción (`Allow` o `Deny`).
- `"Action": ["s3:GetObject"]`: La acción específica que se permite. Sigue el formato `servicio:Accion`.
- `"Resource"`: A qué recurso exacto aplica la regla. El `arn` es el identificador único universal de AWS. El asterisco `/*` significa "cualquier archivo dentro del bucket".

## 2. Setup Inicial (Zero Assumption)

Si nunca has interactuado con AWS desde Python, necesitas instalar la librería oficial de AWS llamada `boto3`, y `python-dotenv` para poder cargar variables de entorno locales de forma segura.

```bash
pip install boto3 python-dotenv
```

Debes crear un archivo llamado `.env` en la raíz de tu proyecto (¡y asegurarte de que este archivo esté mencionado en tu `.gitignore`!):

```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1
```

## 3. Implementación (Cómo)

### El Camino Frágil (Si aplica por complejidad)
**🎯 Objetivo de Negocio:** Autenticarnos en AWS para verificar nuestra identidad en el Gremio programáticamente.

Si ignoramos las buenas prácticas de seguridad, podríamos vernos tentados a inyectar las credenciales directamente en el código de Python:

```python
import boto3

# ¡PELIGRO! Esto es "Hardcoding".
access_key = "AKIAIOSFODNN7EXAMPLE"
secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Si subes este código a GitHub (incluso privado), bots extraerán tus llaves en segundos
# y usarán tu cuenta para minar criptomonedas, dejándote deudas miles de dólares.
iam_client = boto3.client('iam', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
```

### El Camino Robusto (Zero Surprise Syntax)
**🎯 Objetivo de Negocio:** Autenticarnos en AWS asegurando que no queden rastros de las llaves secretas en nuestro código fuente, usando variables de entorno.

```python
import os
import boto3
from dotenv import load_dotenv

# 1. Cargamos las variables de entorno del archivo .env a la memoria del SO
load_dotenv()

# 2. boto3 buscará automáticamente las variables AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
# en el entorno operativo. No necesitamos pasárselas manualmente.
try:
    iam_client = boto3.client('iam')
    response = iam_client.get_user()
    usuario = response['User']['UserName']
    print(f"✅ Autenticación exitosa. Logueado como: {usuario}")

except Exception as e:
    print(f"❌ Error de autenticación: {e}")
```

*Zero Surprise Syntax:*
- `load_dotenv()`: Busca un archivo oculto llamado `.env` y carga cada línea como variable de entorno en `os.environ`.
- `boto3.client('iam')`: Crea una conexión activa (un cliente) específica hacia IAM. Por debajo llama a `os.environ.get('AWS_ACCESS_KEY_ID')` automáticamente.
- `iam_client.get_user()`: Realiza una petición de red a la API de AWS para obtener los metadatos del usuario asociado a las llaves. Retorna un diccionario.

## 4. Conexión con Testing (Test-Driven Lore)

Cuando construimos infraestructura Cloud, probarla ejecutando el código repetidamente contra la nube real es lento, peligroso y potencialmente costoso. Para resolverlo, en nuestros tests usamos **Mocks** (simuladores).

- **El decorador `@patch`:** Viene de `unittest.mock`. Permite interceptar una llamada a una librería (como `boto3`) y reemplazarla temporalmente por un "doble de riesgo" de mentira.
- **`MagicMock`:** Es el objeto de mentira que reemplaza a tu cliente de AWS.
- **`return_value`:** Le decimos al objeto de mentira: "Cuando mi código real llame a la API de AWS pidiendo el usuario, en vez de conectarte a internet, simplemente devuélveme este diccionario falso instantáneamente".

```python
from unittest.mock import patch, MagicMock

@patch('my_solution.boto3.client')
def test_ejemplo(mock_boto):
    mock_iam = MagicMock()
    # Forzamos la respuesta de la API
    mock_iam.get_user.return_value = {'User': {'UserName': 'cuidador-falso'}}
    mock_boto.return_value = mock_iam
    # Ahora cuando la función llame a boto3, usará nuestro objeto falso.
```

## 5. Mapa de Ejercicios

Dirígete a la carpeta `quests/00-aws-iam/` para poner a prueba tu conocimiento implementando tu primer pipeline de validación IAM seguro.
