import argparse


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
