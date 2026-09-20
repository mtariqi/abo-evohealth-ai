"""Leakage-safe nested-model evaluation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CLINICAL = [
    "age", "sex", "bmi", "smoking", "cancer", "recent_surgery", "anticoagulant"
]
CONTEXT = ["site", "genetic_ancestry"]
MODEL_FEATURES = {
    "M0_clinical": CLINICAL,
    "M1_context": CLINICAL + CONTEXT,
    "M2_ABO": CLINICAL + CONTEXT + ["abo_phenotype"],
    "M3_mechanism": CLINICAL
    + CONTEXT
    + ["abo_phenotype", "fut2_status", "vwf", "factor_viii"],
}


@dataclass
class EvaluationResult:
    comparison: pd.DataFrame
    group_metrics: pd.DataFrame


def _make_pipeline(data: pd.DataFrame, features: list[str]) -> Pipeline:
    categorical = [f for f in features if data[f].dtype == "object"]
    numeric = [f for f in features if f not in categorical]
    prep = ColumnTransformer(
        [("numeric", StandardScaler(), numeric),
         ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical)]
    )
    return Pipeline([("preprocess", prep), ("model", LogisticRegression(max_iter=2_000))])


def _calibration(y: np.ndarray, probabilities: np.ndarray) -> tuple[float, float]:
    eps = np.finfo(float).eps
    bounded = np.clip(probabilities, eps, 1 - eps)
    logits = np.log(bounded / (1 - bounded)).reshape(-1, 1)
    recalibrator = LogisticRegression(C=1e6, max_iter=2_000)
    recalibrator.fit(logits, y)
    return float(recalibrator.intercept_[0]), float(recalibrator.coef_[0, 0])


def evaluate_nested_models(
    data: pd.DataFrame,
    outcome: str = "vte_1y",
    test_size: float = 0.25,
    seed: int = 42,
) -> EvaluationResult:
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_idx, test_idx = next(splitter.split(data, groups=data["patient_id"]))
    train, test = data.iloc[train_idx], data.iloc[test_idx]
    rows: list[dict[str, float | str]] = []
    final_probabilities: np.ndarray | None = None

    for name, features in MODEL_FEATURES.items():
        model = _make_pipeline(train, features)
        model.fit(train[features], train[outcome])
        probabilities = model.predict_proba(test[features])[:, 1]
        intercept, slope = _calibration(test[outcome].to_numpy(), probabilities)
        rows.append({
            "model": name,
            "auroc": roc_auc_score(test[outcome], probabilities),
            "auprc": average_precision_score(test[outcome], probabilities),
            "brier": brier_score_loss(test[outcome], probabilities),
            "calibration_intercept": intercept,
            "calibration_slope": slope,
            "n_train": len(train),
            "n_test": len(test),
        })
        final_probabilities = probabilities

    assert final_probabilities is not None
    group_rows = []
    for group, frame in test.assign(probability=final_probabilities).groupby("genetic_ancestry"):
        if frame[outcome].nunique() < 2:
            continue
        group_rows.append({
            "genetic_ancestry": group,
            "n": len(frame),
            "prevalence": frame[outcome].mean(),
            "auroc": roc_auc_score(frame[outcome], frame["probability"]),
            "brier": brier_score_loss(frame[outcome], frame["probability"]),
        })
    return EvaluationResult(pd.DataFrame(rows), pd.DataFrame(group_rows))
