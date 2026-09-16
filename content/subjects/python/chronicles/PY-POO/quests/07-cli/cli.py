import argparse


def main():
    parser = argparse.ArgumentParser(description="The pipeline")
    parser.add_argument("--savefile", required=True, help="Filepath")
    args = parser.parse_args()
    print(f"load file: {args.savefile}")


if __name__ == "__main__":
    main()
