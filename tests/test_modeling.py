from abo_evohealth.modeling import MODEL_FEATURES, evaluate_nested_models
from abo_evohealth.synthetic import generate_synthetic_cohort


def test_outcome_and_identifier_are_not_features():
    for features in MODEL_FEATURES.values():
        assert "vte_1y" not in features
        assert "patient_id" not in features


def test_nested_evaluation_returns_bounded_metrics():
    data = generate_synthetic_cohort(1000, seed=11)
    result = evaluate_nested_models(data, seed=11)
    assert len(result.comparison) == 4
    assert result.comparison["auroc"].between(0, 1).all()
    assert result.comparison["auprc"].between(0, 1).all()
    assert result.comparison["brier"].between(0, 1).all()
    assert not result.group_metrics.empty

