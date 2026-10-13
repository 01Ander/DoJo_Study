class GameLoader:
    def load(self, level: str):
        return f"Level {level} loaded"


class PhysicsEngine:
    def initialize(self):
        return "Physics engine initialized"


class GameOrchestrator:
    def __init__(self, loader: GameLoader, engine: PhysicsEngine):
        self.loader = loader
        self.engine = engine

    def start_level(self, level: str):
        print(f"Starting level {level} with physics engine ready")
