# **AUTOMATICACION DE REGISTROS FINANCIEROS**


## **Business Problem**

Esta automatizacion busca reducir costos y tiempo manual en la adquisicion de datos financiero, validaciones y un ligero analisis financiero. Actualmente el proceso manual de verificacion de registros consume + 8 horas de una persona por conjunto de datos.

## **Solution Overview**

Esta solucion ofrece una limpieza de registros, eliminando registros corruptos, dañados o inválidos. Presenta una capa de seguridad mediana financiera para movimientos incompletos en informacion o movimientos sospechosos. Entrega un analisis de agrupacion de registros por categoria (esta agrupacion es editable, se puede entregar en cualquier otra categoria presente en los registros) y ofrece un registro con las transacciones que no cumplieron los requerimientos de validacion y seguridad.

## **Key Benefits**

La solucion ofrece un ROI del 100% frente a proceso manual. Es un proceso totalmente automatico donde el analista solo debe cargar la base de datos y el sistema se encarga de todo lo demas. Este sistema es resiliente ante errores al poder comprobar los registros invalidos al finalizar el proceso automatico. De igual manera el sistema es auditable en cada una de sus etapas, por si los registros aumentan en complejidad o se requiere hacer distintos analisis financieron directamente con los datos verificados y limpios.

## **How It Works (Simple)**

- Adquisicion de raw data.
- Limpieza y validacion de datos, fecha, amount, currency.
- Captacion de registros no validos.
- Captacion de datos validados.
- analisis y agrupacion por categoria.
- Entrega de informacion por archivo de agrupacion jerarquica.
- Entrega de registro con transacciones no validas.


## **Error Handling**

El sistema automatico esta disenado para que en cada punto de validacion de informacion se capte y posteriormente se agrupe en un unico registro de informacion invalida, dando un flujo continuo al sistema, sin caer en crasheos innecesarios por erroes de datos.

## **Usage**

Para iniciar el sistema se ejecuta el comando: `python etl.py`

## **Tech Stack**

Este script hace uso unicamente de Python stdlib.
