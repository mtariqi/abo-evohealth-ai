# Model Card: Synthetic VTE Demonstrator

## Intended use

Software validation, teaching, and pipeline development using synthetic data.

## Prohibited use

Diagnosis, transfusion decisions, anticoagulation decisions, personalized risk prediction, insurance, employment, or ancestry inference.

## Inputs

Synthetic demographic, clinical, site, ancestry, ABO, FUT2, VWF, and factor VIII fields.

## Output

One-year synthetic VTE probability and aggregate performance tables.

## Limitations

The data-generating process is designed by the repository author. Performance therefore measures recovery of simulated structure, not clinical validity. Genetic ancestry categories are coarse software-test labels and must not be interpreted as race.

## Required validation before research use

Phenotype validation, genotype/serology concordance, missing-data assessment, external validation, calibration analysis, subgroup uncertainty, negative controls, privacy review, and REB/IRB approval.

