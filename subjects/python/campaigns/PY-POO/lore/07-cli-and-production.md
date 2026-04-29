# Capítulo 07: CLI and Production Assembly

Tu código Orientado a Objetos es hermoso y está 100% cubierto por tests. Pero un usuario no sabe abrir Python e importar tus clases. Necesitan una interfaz de consola (CLI).

## 1. Construyendo la CLI

Usaremos `argparse` (nativo) o librerías modernas como `Click` o `Typer` (si están disponibles en el proyecto).

Ejemplo básico con `argparse`:

```python
# cli.py
import argparse
from pipeline import MiOrquestador
from extractors import CSVExtractor
from engines import MiEngine

def main():
    parser = argparse.ArgumentParser(description="Mi super pipeline")
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV")
    args = parser.parse_args()
    
    # 1. Ensamblaje en Producción (Dependency Injection manual)
    extractor = CSVExtractor()
    engine = MiEngine()
    orquestador = MiOrquestador(extractor, engine)
    
    # 2. Ejecución
    orquestador.run(args.input)

# 3. El Entry Point
if __name__ == "__main__":
    main()
```

## 2. El Entry Point (`if __name__ == "__main__":`)

Este bloque asegura que `main()` **solo corra** si alguien ejecuta el archivo desde la consola (`python cli.py --input datos.csv`), pero **NO** si importas el archivo en un test. Si esto no existiera, cada vez que pytest importara tu CLI, se ejecutaría el programa entero.

## 3. Finalizando la Campaña

Este es el último eslabón de tu entrenamiento. Con esto, sabes cómo abstraer I/O, crear entidades, procesar sin estado, orquestar, loggear errores y exponer el programa al mundo empaquetado en una CLI.

**¡Estás listo para el Boss!**
Dirígete a `boss/requirements.md` para iniciar.

## 4. Mapa de Ejercicios

Dirígete a `quests/07-cli/`:

```text
PY-POO/quests/07-cli/
├── 01-argparse-basics.md        (Tipo A: Parsing Básico)
└── 02-cli-orchestration.md      (Tipo B: Ensamblaje Completo)
```
