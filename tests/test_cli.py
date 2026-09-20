from pathlib import Path

import yaml

from abo_evohealth.cli import run_demo


def test_demo_writes_expected_artifacts(tmp_path: Path):
    config = {
        "seed": 2,
        "n_samples": 500,
        "test_size": 0.25,
        "outcome": "vte_1y",
        "output_dir": str(tmp_path / "outputs"),
        "bootstrap_iterations": 10,
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    run_demo(config_path)
    expected = {
        "synthetic_cohort.csv",
        "model_comparison.csv",
        "group_metrics.csv",
        "run_metadata.json",
    }
    assert expected == {path.name for path in (tmp_path / "outputs").iterdir()}
