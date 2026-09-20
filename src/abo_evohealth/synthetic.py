"""Generate synthetic, non-clinical data for software demonstrations."""

from __future__ import annotations

import numpy as np
import pandas as pd

ANCESTRIES = np.array(["AFR", "AMR", "EAS", "EUR", "SAS"])
SITES = np.array(["Toronto", "Little Rock", "Boston", "Vancouver"])
ABO_TYPES = np.array(["O", "A", "B", "AB"])


def _sigmoid(value: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-value))


def generate_synthetic_cohort(n_samples: int = 5_000, seed: int = 42) -> pd.DataFrame:
    """Return a deterministic synthetic cohort.

    The generator contains an intentionally modest non-O/VWF signal so the
    evaluation pipeline can detect incremental value. It must not be used to
    estimate real-world effects.
    """
    if n_samples < 200:
        raise ValueError("n_samples must be at least 200 for a stable demonstration")

    rng = np.random.default_rng(seed)
    ancestry = rng.choice(ANCESTRIES, size=n_samples, p=[0.16, 0.12, 0.22, 0.32, 0.18])
    site = rng.choice(SITES, size=n_samples)
    abo = rng.choice(ABO_TYPES, size=n_samples, p=[0.44, 0.34, 0.17, 0.05])
    non_o = (abo != "O").astype(int)
    age = np.clip(rng.normal(52, 16, n_samples), 18, 90)
    sex = rng.choice(["female", "male"], size=n_samples)
    bmi = np.clip(rng.normal(27.2, 5.3, n_samples), 15, 55)
    smoking = rng.binomial(1, _sigmoid(-1.5 + 0.012 * (age - 50)))
    cancer = rng.binomial(1, _sigmoid(-4.2 + 0.045 * (age - 50)))
    recent_surgery = rng.binomial(1, 0.08, n_samples)
    anticoagulant = rng.binomial(1, _sigmoid(-3.0 + 0.8 * cancer + 0.02 * (age - 50)))
    fut2_secretor = rng.choice(["secretor", "non_secretor"], size=n_samples, p=[0.78, 0.22])

    vwf = rng.normal(90 + 22 * non_o + 0.35 * (age - 50), 20, n_samples)
    factor_viii = rng.normal(95 + 16 * non_o + 0.25 * (age - 50), 18, n_samples)
    linear = (
        -3.8
        + 0.036 * (age - 50)
        + 0.035 * (bmi - 25)
        + 0.42 * smoking
        + 1.05 * cancer
        + 1.15 * recent_surgery
        - 0.55 * anticoagulant
        + 0.22 * non_o
        + 0.006 * (vwf - 100)
    )
    vte_1y = rng.binomial(1, _sigmoid(linear))

    return pd.DataFrame(
        {
            "patient_id": [f"SYN-{i:06d}" for i in range(n_samples)],
            "age": age.round(1),
            "sex": sex,
            "bmi": bmi.round(1),
            "smoking": smoking,
            "cancer": cancer,
            "recent_surgery": recent_surgery,
            "anticoagulant": anticoagulant,
            "site": site,
            "genetic_ancestry": ancestry,
            "abo_phenotype": abo,
            "fut2_status": fut2_secretor,
            "vwf": vwf.round(2),
            "factor_viii": factor_viii.round(2),
            "vte_1y": vte_1y,
        }
    )
