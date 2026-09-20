"""Data-contract checks for analysis-ready cohorts."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {
    "patient_id", "age", "sex", "bmi", "smoking", "cancer",
    "recent_surgery", "anticoagulant", "site", "genetic_ancestry",
    "abo_phenotype", "fut2_status", "vwf", "factor_viii", "vte_1y",
}


def validate_cohort(data: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if data["patient_id"].duplicated().any():
        raise ValueError("patient_id must be unique")
    if not set(data["abo_phenotype"].dropna()).issubset({"O", "A", "B", "AB"}):
        raise ValueError("abo_phenotype contains an unsupported category")
    if not set(data["vte_1y"].dropna()).issubset({0, 1}):
        raise ValueError("vte_1y must be binary")
    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("The demonstration cohort must not contain missing values")

