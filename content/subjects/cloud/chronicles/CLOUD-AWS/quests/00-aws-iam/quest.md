# Quest 00: AWS Identity & Access Management (IAM)

Bienvenido a tu primer Quest en la nube. Antes de poder construir infraestructura o procesar datos, necesitamos asegurarnos de que sabes cómo autenticar tus scripts de Python de manera segura, sin dejar contraseñas hardcodeadas.

## 🎯 Objetivo de Negocio
El Gremio de Cuidadores de Dragones ha emitido un gafete mágico (IAM User programático) para tu script. Debes crear una función que compruebe la validez de ese gafete y nos diga quién eres, utilizando variables de entorno.

## 📝 Instrucciones

1. **Carga Segura de Entorno:** Debes utilizar la librería `dotenv` para cargar las variables de entorno locales (asumiendo que existe un archivo `.env` configurado).
2. **Crear la función `verificar_identidad()`:**
   - **Propósito:** Conectarse al servicio IAM de AWS y obtener el nombre del usuario actual.
   - **Entrada (Parámetros):** Ninguno.
   - **Salida (Retorno):** Debe retornar un **String** con el nombre de usuario (`UserName`) extraído del diccionario de respuesta de `boto3`.
   - **Manejo de Errores:** Si la autenticación falla (ej. llaves inválidas) y `boto3` lanza una excepción, la función debe atraparla con un bloque `try/except` y retornar exactamente el string `"Error de autenticación"`.

> **Scaffolding Nivel 1 (Guía Activa):** Implementa tu código en `my_solution.py` guiándote por los comentarios. Luego, completa las aserciones (`assert`) en `test_my_solution.py` y ejecuta `pytest test_my_solution.py` para validar. `solution.py` y `reference_test.py` son las respuestas correctas de referencia; no las abras hasta haberlo intentado.
