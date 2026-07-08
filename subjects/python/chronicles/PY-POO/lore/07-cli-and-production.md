# Capítulo 07: CLI and Production Assembly

Tu código Orientado a Objetos es hermoso, modular y está 100% cubierto por tests. Pero un usuario final no sabe abrir Python e importar tus clases. Necesitan una interfaz para interactuar con tu programa desde la consola (CLI - Command Line Interface).

## 1. La Interfaz de Consola y el Ensamblaje

Usaremos `argparse` (nativo en Python) para crear esta interfaz. El archivo `cli.py` no solo define los comandos, sino que actúa como el lugar de "Ensamblaje Final".

### Analogía 1: El Tablero del Auto (La CLI)
Tu `PhysicsEngine` y tu `CSVExtractor` son como los pistones y las bujías de un motor. Son muy potentes, pero un conductor normal no abre el capó para acelerar tirando de un cable de metal. El conductor usa un volante y un pedal (la CLI). La CLI oculta la complejidad interna y expone solo lo necesario (ej: "ingrese el archivo a procesar").

### Analogía 2: La Fábrica de Ensamblaje (Inyección)
El `cli.py` es la planta de ensamblaje de tu aplicación. 
Aquí es donde sacas el Extractor de su caja, sacas el Engine de su caja, y los conectas (Inyección de Dependencias) dentro del Orquestador para crear el producto final listo para usar.

### Ejemplo de Código con `argparse`

```python
# cli.py
import argparse
from pipeline import MiOrquestador
from extractors import CSVExtractor
from engines import MiEngine

def main():
    # 1. Definimos el volante y los pedales (Argumentos de Consola)
    parser = argparse.ArgumentParser(description="Mi super pipeline")
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV")
    args = parser.parse_args()
    
    # 2. Ensamblaje en Producción (Dependency Injection manual)
    extractor = CSVExtractor()
    engine = MiEngine()
    orquestador = MiOrquestador(extractor=extractor, engine=engine)
    
    # 3. Ejecución del programa
    orquestador.run(args.input)

# 4. El Entry Point
if __name__ == "__main__":
    main()
```

## 2. El Entry Point (`if __name__ == "__main__":`)

¿Por qué ponemos la ejecución de `main()` dentro de ese extraño bloque `if`?

### Analogía: Mirar vs Arrancar
Imagina que vas a un concesionario de autos. Quieres **mirar** el auto, abrir las puertas y ver el motor. No quieres que, por el simple hecho de mirarlo, el auto se encienda y salga a 100 km/h por la ventana del concesionario.
- Si no pones ese `if`, cualquiera que importe tu código (por ejemplo, `pytest` para hacer pruebas unitarias) ejecutará todo el programa automáticamente.
- Al poner ese `if` (El "Entry Point"), le dices a Python: "Solo enciende el auto si el usuario lo ejecuta explícitamente desde la consola. Si alguien solo lo está importando para mirarlo, mantén el motor apagado".

## 3. Finalizando la Campaña

Este es el último eslabón de tu entrenamiento. Con esto, sabes cómo:
1. Aislar lectura de datos (Cap 01)
2. Crear entidades de dominio protegidas (Cap 02)
3. Procesar datos sin estado impredecible (Cap 03)
4. Orquestar e Inyectar dependencias (Cap 04)
5. Testear con Mocks y Fixtures (Cap 05)
6. Loggear y manejar errores (Cap 06)
7. Exponer tu programa empaquetado en una CLI (Cap 07)

**¡Estás listo para el Rite!**
Dirígete a `rite/requirements.md` para iniciar tu proyecto monolítico.

## 4. Mapa de Ejercicios

Dirígete a `quests/07-cli/`:

- [[01-argparse-basics]]
- [[02-cli-orchestration]]

```text
PY-POO/quests/07-cli/
├── [[01-argparse-basics]].md        (Tipo A: Parsing Básico)
└── [[02-cli-orchestration]].md      (Tipo B: Ensamblaje Completo)
```
