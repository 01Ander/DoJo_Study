# Sistema de automatizacion de limpieza y agrupacion de registros web

## **Business Problem**

Esta automatizacion busca la reduccion de costos y tiempo manual en el procesamiento de logs que vienen de un servidor web.

## **Solution Overview**

La solucion propuesta implementa un sistema totalmente automatico que elimina registros corruptos, errores y datos invalidos. Entrega un resumen sencillo con informacion sobre la cantidad de solicitudes hechos a un punto de la web. De manera similar, presenta un registro de las peticiones que fueron rechazadas por el sistema, en caso que se quiera hacer una auditoria externa posterior.

## **Key Benefits**

Este sistema elimina posibles riesgos de errores humanos en la validacion de los registros. Permite tener trazabilidad de los errores y por que se rechazan. La clasificacion de datos presenta un formato estandar para su lectura y posible utilizacion posterior en distintos equipos de trabajo.
Siendo un sistema totalmente resiliente frente a errores y posibles cambios, permitiendo su validacion y posterior mejora si los registros de entrada difieren, o si se busca otro tipo de agrupacion de informacion o distintas validaciones.


## **How It Works (Simple)**

- Adquisicion de raw logs.
- Limpieza y validacion de: fecha, endpoint, status code y time response ms.
- Captacion de registros no validos.
- Captacion de registros validos.
- Agrupacion por status code.
- Entrega de informacion agrupada por archivo JSON.
- Entrega de registro de logs no validos.

## **Error Handling**

El sistema automatico presenta en sus distintas etapas la captacion de posibles errores y validaciones correspondientes, en caso de que exista un error persistente, este se registra y no bloquea el correcto funcionamiento del script.

## **Usage**

Para iniciar el sistema se ejecuta el comando: `python etl.py`

## **Tech Stack**

Este script hace uso unicamente de herramientas propias del lenguaje de programacion Python (stdlib).