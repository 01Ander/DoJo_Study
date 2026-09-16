Friction Level: 4

## Identification

**Problematica:** Mocks logs de un servidor web que contienen datos corruptos, erroneos, tiempos irregulares de entrega y campos faltantes. No se indica el tiempo usado actualmente.

**Requerimientos:** Uso de un script totalmente automatico que sustituya el trabajo manual para la limpieza de datos.

**Objetivos tecnicos:** Crear un script capaz de obtener datos de un documento CSV que contiene informacion de timestamp, endpoint, status code y response time ms. Se debe normalizar fechas, validar datos completos y sobrellevar logs corruptos a un estdo aparte para posterior verificacion. Agrupacion de informacion por: total requests, requests per endpoint, HTTP status breakdown. Se entrega un registro final en JSON con logs validados.

---

## Propuesta

**Posible solucion:** Pipeline que extraiga los registos, valide errores y vacios de inforamcion, y carge y agrege los registros validos a un sumary report para su entrega. Manejo de errores sin romper el script.

### **Arquitectura:**

  - **Informacion en data:** timestamp, endpoint, status_code, response_time_ms.

  - **Solucion:**
    1. Lectura de archivo.
    2. Verificacion de datos:
       1. timestamp:str / ISO-8601 / Captacion interna de erroes.
       2. endpoint:str / Captacion interna de errores.
       3. status_code:int / Captacion interna de errores.
       4. reponse_time_ms:float / Internal captation errors.
    3. Agrupacion de informacion.
       1. Total requests:int
       2. Requests per endpoint:int
       3. HTTP status breakdown:str
    4. Validacion de log erroneo.
       1. Captacion de 'ERROR: CONNECTION RESET BY PEER at... '
    5. Carga de datos invalidos a log de errores.
    6. Creation and save sumary_report.JSON.
  
  - **Necesidades especificas:**
    - Se formatea la fecha para mejor lectura y se parchea las inconsistencia.
    - Solucion primaria para deteccion de ERROR en logs.
    - Captacion de logs con campos vacios, se registran como errores y se mandan a errors_log
    - Captacion de demas campos erroneos se envian a errors_log
  
### Definicion de contratos/test

**Se establece esta jerarquia de funciones; si una transaccion es marcada como erronea pasara al registro de errores**

* def read_file(path: str) -> list[str]
  1. Recibe raw data.
  2. Entrega lista de raw data.
* def normalize_transation_date(str) - str
  1. Recibe el campo 'timestamp'
  2. Entrega la fecha normalizada a YYY-MM-DD HH:MM:SS
* def cleanse_record(list[str]) ->list[dict[TypedDict]]
  1. Recibe raw data.
  2. Entregas lista de diccionarios con logs verificados.
* def agreggate_logs(list(dict[str, Any])) -> list[dict[str, Any]]
  1. Recibe la lista de registros limpios.
  2. Entrega la lista de diccionarios con la informacion agrupada.
* def error_log(str) -> None
  1. Recibe 'ERROR: CONNECTION RESET BY PEER at...'.
  2. Genera y guarda el registro en error_log.
* def process_records(list[dict[str, Any]]) -> path:str
  1. Recibe la lista de registros agrupada.
  2. Entrega sumary_report.json

## **Requerimientos tecnicos:**

- Uso exclusivo de logica de python. Sin uso de librerias externas.
- Datacion correcta para el dict de logs:
  - class LogRecord(TypedDict):
    timestamp: str
    endpoint: str
    status_code: int
    response_time_ms: int