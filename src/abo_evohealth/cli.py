"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import pandas as pd
import sklearn
import yaml

from abo_evohealth.modeling import evaluate_nested_models
from abo_evohealth.synthetic import generate_synthetic_cohort
from abo_evohealth.validation import validate_cohort


def run_demo(config_path: Path) -> None:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    cohort = generate_synthetic_cohort(config["n_samples"], config["seed"])
    validate_cohort(cohort)
    result = evaluate_nested_models(
        cohort, outcome=config["outcome"], test_size=config["test_size"], seed=config["seed"]
    )
    cohort.to_csv(output_dir / "synthetic_cohort.csv", index=False)
    result.comparison.to_csv(output_dir / "model_comparison.csv", index=False)
    result.group_metrics.to_csv(output_dir / "group_metrics.csv", index=False)
    metadata = {
        "config": config,
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "warning": "Synthetic demonstration only; not clinical evidence.",
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(result.comparison.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(prog="abo-evohealth")
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser("demo", help="run the synthetic VTE demonstration")
    demo.add_argument("--config", type=Path, default=Path("configs/demo.yaml"))
    args = parser.parse_args()
    if args.command == "demo":
        run_demo(args.config)


if __name__ == "__main__":
    main()

