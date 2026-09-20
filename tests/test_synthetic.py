import pandas as pd
import pytest

from abo_evohealth.synthetic import generate_synthetic_cohort
from abo_evohealth.validation import validate_cohort


def test_generator_is_deterministic():
    first = generate_synthetic_cohort(300, seed=7)
    second = generate_synthetic_cohort(300, seed=7)
    pd.testing.assert_frame_equal(first, second)


def test_generated_data_passes_contract():
    validate_cohort(generate_synthetic_cohort(300))


def test_duplicate_patient_is_rejected():
    data = generate_synthetic_cohort(300)
    data.loc[1, "patient_id"] = data.loc[0, "patient_id"]
    with pytest.raises(ValueError, match="unique"):
        validate_cohort(data)

