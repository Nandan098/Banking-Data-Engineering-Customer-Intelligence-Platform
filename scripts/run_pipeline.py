"""Run the project pipeline from the repository root."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pipeline import run  # noqa: E402

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--load-db", action="store_true", help="Load into PostgreSQL after validation")
    args = parser.parse_args()
    run(skip_db=not args.load_db)
