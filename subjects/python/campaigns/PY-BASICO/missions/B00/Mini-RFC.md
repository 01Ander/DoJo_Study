Friction Level: 2

Problematica; Datos en bruto se reciben de manera inconsistente y corrupta. Consumo de horas manuales +8.

Requerimientos; reduccion de costos en un 100% bajo el uso de un script **automatico**. Proporcionar informes claros de resgistros, reduciendo los riesgos financierons por discrepacias.

Posible solucion proporcionada: un pipeline (inconsistencia tecnica sobre el significado claro de pipline) que extraiga, limpie/transforme, agrege y carge los datos. Uso exclusivo de librerias de python basicas o standard. Uso de loops y condicionales. Registro de fallos inmediato sin romper el sistema.

Objetivos tecnicos: Crear un script o sistema ligero, ETL, capas de leer archivos en formato CSV/JSON que contengan transacciones bancarias. Se debe formalizar formatos (fechas, monedas), uso de reglas financieras (deteccion de anomalias como datos negativos - posibles incosistencias en fechas- o datos vacios o corruptos), calcular las adiciones financiaras por clasificaciones. y un manejo 'elegante' de los errores donde no detengan operaciones.

## **Arquitectura propuesta:**

- Antes de poder efectuar una arquitectura, quisiera ver las datos en RAW para saber con que informacion se va a trabajar y con que operaciones se deben contar.

### ***Informacion de data***:
  - se cuenta con; id, fecha y hora de la transaccion, amount, divisa, categoria, descripcion y status.

### **Solucion propuesta:**

Al indicar los datos se presenta;
  1. Lectura de archivo
  2. Verificacion de datos:
     - Validacion de existencia de dato
     - Validacion de dato correcto en formato:
       - id:string
       - fecha:YYYY-MM-DD HH:MM:SS - string?
         - captacion interna de error si falta dato
       - amount:float
         - captacion interna de error si falta dato
       - currency:string
         - captacion interna de error si falta dato
       - category:string
       - description:string
     - Validacion de dato correcto:
       - amount: datos > 0
       - corrency: moneda existente, validacion por diccionario
       - category: categoria existente, validacion por diccionario.
       - status: status existente; completed, pending, failed.
     - Validaciones de seguridad financiera:
       - fecha fuera de limites, fecha posterior a la fecha actual.
       - descripcion sospechosa
  3. Carga de datos individuales a necesidad de consulta;
      - Fecha
      - Categoria
      - Currency
      - Amout > o < a ...
      - Status
  4. Calculos acumulativos por clasificacion
  5. Manejo de posibles errores.
  6. Salida de solicitudes por formarto .json.

#### **soluciones especificas:**

**Soluciones dadas ya que el `requirements` no indica que se debe hacer en estos casos.**
- Inconsistencias en fechas se formatearan en el formato especificado.
- Si se detecta un amount negativo, se transformara a positivo.
- Las transacciones que no pasen validaciones, seran registradas en un log.


### **Definicion de contratos/Test**

**Se establece esta jerarquia de funciones; si una transaccion es marcada como erronea pasara al registro de errores**

- def read_file(path: str) -> list[str]
  1. Recibe los datos en crudo
  2. Entrega una lista de datos raw
- def cleanse_record(list[str]) -> dict[str, any]/list[str]
  1. Formatea y Valida que exista un dato en la lista y fecha anterior a fecha actual.
  2. Entrega un diccionario de datos formateados {'id':str,'timestamp':date,'amount':float,'currency':str,'category':string,'description':str,'status':str} y una lista de erroneos marcando el dato erroneo [id,timestamp,amount,currency,category,description,status].
- def validation_record( dict[str, any]) -> dict[str, any]/list[str]
  1. Valida amount > 0, y concordancia en courrent, category, status.
  2. Entrega un diccionario de datos correctos validados y una lista de erroneos marcando el dato erroneo [id,timestamp,amount,currency,category,description,status].
- def security_validation(dict[str, any]) -> dict[str, any]/list[str]
  1. Descripcion sospechosa
  2. Entrega un diccionario de datos aprobados por security y una lista de erroneos marcando el dato erroneo [id,timestamp,amount,currency,category,description,status].
- def errors(list[str]) -> path:str
  1. Agrupa la lista con los errores
  2. Genera el reporte de datos no validados, no seguros.
- def load_data(dict[str, any]) -> list[str]
  1. Carga en variables los datos de la consulta
  2. Entrega una lista
- def save_data(dic[str]) -> path:str
  1. Genera el archico .json con la consulta
  2. Entrega un archivo .json con la solicitud hecha



### **Informacion tecnica para codificacion**

Se recuerda:
  - Uso de diccionarios para la toma de datos por ID.
  - Uso de listas
  - Clases y definiciones para ejecutar funciones


## **Posibles carencias tecnicas**

Se observa carencias tecnicas en:
  - Lectura de datos. Se recuerda que se vio en un momento, pero no se recuerda estructura de codigo; se sugiere buscar ejemplos hechos anteriormente.
  - Validacion de formatos. No se recuerda como cargarlos y/o transformarlos a un solo estado.
  - Salida de solucitudes  por formato .json
  - Manejo de errores, se recuerda el try/catch, mas no la salida a un log.
  - No se recuerda si las 'collections'

