# Ejercicio 07-02: CLI Orchestration (Tipo B)

**Objetivo:** Ensamblar piezas sueltas de OOP a través del archivo principal de consola.

## Tu Tarea
Observa el siguiente archivo de CLI incompleto. Tienes un `GameLoader` y un `PhysicsEngine`, y necesitas armar el orquestador final. Completa la sección de "Ensamblaje" para que el programa inicie correctamente el pipeline de videojuegos.

```python
import argparse
# from game import GameLoader, PhysicsEngine, GameOrchestrator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True)
    args = parser.parse_args()
    
    # --- TU ENSAMBLAJE AQUÍ ---
    # loader = ...
    # engine = ...
    # orchestrator = ...
    # --------------------------
    
    orchestrator.start_level(args.level)

if __name__ == "__main__":
    main()
```

---
<details>
<summary>👀 Ver Solución Esperada</summary>

```python
import argparse
from game import GameLoader, PhysicsEngine, GameOrchestrator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True)
    args = parser.parse_args()
    
    loader = GameLoader()
    engine = PhysicsEngine()
    orchestrator = GameOrchestrator(loader, engine)
    
    orchestrator.start_level(args.level)

if __name__ == "__main__":
    main()
```
</details>
