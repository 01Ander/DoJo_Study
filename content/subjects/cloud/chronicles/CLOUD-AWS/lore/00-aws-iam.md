# Capítulo 00: AWS Identity & Access Management (IAM)

Bienvenido a la nube. Hasta ahora, todos tus scripts corrían en tu computadora local o en un servidor dedicado. Cuando trabajamos en la nube (específicamente en Amazon Web Services o AWS), necesitamos una forma centralizada de identificarnos y de restringir quién puede hacer qué. Aquí es donde entra **IAM**.

## 1. ¿Qué es AWS IAM?

**QUÉ es:** IAM (*Identity and Access Management*) es el servicio central de AWS que controla la autenticación (quién eres) y la autorización (qué puedes hacer). Es el guardia de seguridad insobornable de tu infraestructura en la nube.
**CÓMO se usa:** No requiere código de aplicación directo en la mayoría de los casos. Se configura mediante la consola web de AWS, infraestructura como código (ej. Terraform), o AWS CLI. Tu código escrito en Python luego hereda o utiliza estos permisos al conectarse mediante credenciales.
**POR QUÉ importa:** Sin IAM, cualquiera con acceso a tu sistema podría borrar bases de datos enteras, exponer datos sensibles de clientes, o gastar miles de dólares en servidores minando criptomonedas. IAM evita desastres.

*Analogía del Gremio de Dragones:* Imagina el Gremio de Cuidadores de Dragones de Pantano en Ankh-Morpork. No quieres que el novato recién ingresado tenga las llaves del depósito de dragones adultos, porque son altamente inestables y explosivos. IAM es el sistema de gafetes mágicos que asegura que el novato solo pueda entrar a la sala de alimentación de crías.

## 2. Usuarios de Servicio (IAM Users)

**QUÉ es:** Un *IAM User* es una entidad que creas en AWS para representar a la persona o aplicación que interactúa con la nube. Existen dos tipos principales: usuarios de consola (humanos con contraseña para la interfaz web) y usuarios programáticos (scripts o aplicaciones). En ingeniería de automatización y datos, usaremos constantemente **usuarios de servicio programáticos**.
**CÓMO se usa:** Para un usuario programático se genera un par de llaves criptográficas: un `AWS_ACCESS_KEY_ID` y un `AWS_SECRET_ACCESS_KEY`.
**POR QUÉ importa:** Tu script en Python necesita demostrarle a AWS que tiene derecho a existir y operar. Las aplicaciones no pueden tipear contraseñas en un formulario web, necesitan llaves alfanuméricas de sistema.

## 3. Políticas de Mínimo Privilegio (IAM Policies)

**QUÉ es:** Una *Policy* (Política) es un documento en formato JSON que define de manera explícita qué acciones están permitidas o denegadas. El principio de **Mínimo Privilegio (Least Privilege)** dicta que un usuario o servicio solo debe tener los permisos estrictamente necesarios para hacer su tarea específica y absolutamente nada más.
**CÓMO se usa:** Se crea el documento JSON de la política y luego se adjunta al IAM User o al IAM Role.
**POR QUÉ importa:** Si a un script encargado exclusivamente de leer datos le das permisos de "Administrador Total" por conveniencia, y alguien malintencionado logra robar las credenciales de ese script, tu cuenta entera de AWS está comprometida. Si solo le das permiso de lectura, el daño potencial es minúsculo.

### El formato JSON de una Policy

AWS usa JSON para declarar estos permisos. Aunque es configuración y no Python, es fundamental entender su estructura:

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
- `"Action": ["s3:GetObject"]`: La acción específica que se permite. En AWS las acciones siguen el formato `servicio:Accion`. En este caso, descargar (`GetObject`) usando el servicio de almacenamiento `s3`.
- `"Resource"`: A qué recurso exacto aplica la regla. El `arn` (*Amazon Resource Name*) es el identificador único universal de AWS. El asterisco `/*` significa "cualquier archivo dentro del bucket llamado alimento-dragones-pantano".

🎯 **Objetivo de Negocio:** Darle permiso a nuestro script para leer el inventario de la dieta de los dragones, pero bloqueando explícitamente que pueda alterar o borrar los registros.

## 4. Roles (IAM Roles)

**QUÉ es:** Un *Role* (Rol) es similar a un usuario porque define qué permisos se tienen, pero **no tiene credenciales a largo plazo** (no tiene contraseñas ni Access Keys fijas). En su lugar, un Rol es asumido temporalmente por alguien o *algo* (por ejemplo, un servidor EC2 o una función Lambda corriendo tu código).
**CÓMO se usa:** Le indicas a un servicio de AWS que se ejecute asumiendo un rol. AWS, por debajo, genera credenciales temporales que rotan automáticamente cada par de horas.
**POR QUÉ importa:** Elimina casi por completo el riesgo de que se filtren credenciales. Si tu código corre dentro de AWS asumiendo un rol, nunca hay claves estáticas guardadas en archivos de texto que puedan ser hackeadas.

*Analogía del Gremio:* Un Role es como un "Sombrero Mágico de Domador". El sombrero otorga los permisos para acercarse a los dragones alfa de forma segura. No le das esos permisos a una persona permanentemente; simplemente, quien sea que esté haciendo el turno de guardia se pone el sombrero, hace el trabajo, y luego se lo quita.

## 5. Cero Hardcoding: Variables de Entorno

**QUÉ es:** Hardcodear (escribir como un string directamente en el código de Python) tus credenciales de AWS es el peor pecado de seguridad en la nube. Para evitarlo, usamos siempre **Variables de Entorno**.
**CÓMO se usa:** Se inyectan de forma segura en la memoria del sistema operativo y tu código de Python las lee en tiempo de ejecución. El SDK de AWS lo hace automáticamente por nosotros.
**POR QUÉ importa:** Si subes código con tus claves hardcodeadas a GitHub (incluso si es un repositorio privado), existen bots automatizados que pueden encontrarlas en segundos y usar tu cuenta para iniciar ataques o minar criptomonedas, dejándote una factura de miles de dólares.

### Setup de Boto3 y Dotenv

> **Zero Assumption (Configuración Inicial):** Si nunca has interactuado con AWS desde Python, necesitas instalar la librería oficial de AWS para Python llamada `boto3`, y `python-dotenv` para poder simular variables de entorno localmente.
> ```bash
> pip install boto3 python-dotenv
> ```

Creamos un archivo llamado `.env` en la raíz de nuestro proyecto (¡y nos aseguramos inmediatamente de que este archivo esté mencionado en nuestro `.gitignore`!):

```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-east-1
```

Ahora, veamos cómo usar este entorno seguro en Python.

🎯 **Objetivo de Negocio:** Autenticarnos en AWS de manera programática para verificar nuestra identidad en el Gremio, asegurando que no queden rastros de las llaves secretas en nuestro código fuente.

```python
import os
import boto3
from dotenv import load_dotenv

# 1. Cargamos las variables de entorno del archivo .env a la memoria del SO
load_dotenv()

# 2. boto3 buscará automáticamente las variables AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
# en el entorno operativo. No necesitamos pasárselas manualmente como strings.
try:
    # Creamos un cliente de un servicio de AWS (IAM en este caso) solo para probar conexión
    iam_client = boto3.client('iam')
    
    # Intentamos obtener los detalles del usuario actual
    response = iam_client.get_user()
    
    usuario = response['User']['UserName']
    print(f"✅ Autenticación exitosa. Logueado como el usuario de servicio: {usuario}")

except Exception as e:
    print(f"❌ Error de autenticación: Verifica tus credenciales. Detalle: {e}")
```

*Zero Surprise Syntax:*
- `load_dotenv()`: Busca un archivo oculto llamado `.env` en el mismo directorio donde se ejecuta el script y carga cada línea como una variable de entorno en `os.environ`.
- `boto3.client('iam')`: Crea una conexión activa (un cliente) específica hacia el servicio IAM de AWS. `boto3` es inteligente y por debajo llama a `os.environ.get('AWS_ACCESS_KEY_ID')` para autenticarse.
- `iam_client.get_user()`: Realiza una petición de red a la API de AWS para obtener los metadatos del usuario asociado a las llaves criptográficas que estamos usando. Retorna un diccionario.
