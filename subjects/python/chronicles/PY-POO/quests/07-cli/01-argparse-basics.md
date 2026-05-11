# Ejercicio 07-01: Argparse Basics (Tipo A)

**Objetivo:** Crear una interfaz de consola que reciba un argumento obligatorio.

## Contexto (Domain Shifting: Videojuegos)
Quieres hacer un script que salude al jugador cargando su "Save File".

## Tu Tarea
En `quests/07-cli/`, crea `cli.py`:
1. Importa `argparse`.
2. Crea el `ArgumentParser`.
3. Añade un argumento obligatorio `--savefile`.
4. Añade el Entry Point para ejecutar el script que imprima "Cargando archivo: [tu_archivo]".

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Game Loader")
    parser.add_argument("--savefile", required=True, help="Path to your save file")
    
    args = parser.parse_args()
    print(f"Cargando archivo: {args.savefile}")

if __name__ == "__main__":
    main()
```
</details>
