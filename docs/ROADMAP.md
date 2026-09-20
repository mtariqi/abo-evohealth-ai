# Roadmap

## Stage 1 — Research foundation

- Preregister claims, outcomes, confounders, mediators, and subgroup analyses.
- Curate an evidence table linking each claim to cohort, population, effect estimate, and source.
- Add schema-controlled GWAS Catalog, GTEx, and Open Targets ingestion.

## Stage 2 — Population genomics

- Build reproducible 1000 Genomes/IGSR ingestion.
- Add haplotype-aware ABO and FUT2/FUT3 calling with confidence flags.
- Estimate ancestry-stratified frequencies and selection statistics.
- Add ancient-DNA analyses with coverage and ascertainment sensitivity checks.

## Stage 3 — Clinical phenotyping

- Map diagnoses, labs, procedures, and medications to OMOP concepts.
- Implement validated VTE and major-bleeding phenotypes.
- Separate pathogen acquisition, symptomatic infection, severity, and mortality.
- Validate genotype-derived ABO against serology and flag transfusion/transplant contexts.

## Stage 4 — Statistical and AI validation

- Add Cox and competing-risk models.
- Add bootstrap confidence intervals and multiple imputation.
- Add mediation and colocalization modules.
- Add site-held-out, temporal, geographic, and pathogen-strain validation.
- Add decision curves, subgroup calibration, and quantitative bias analysis.

## Stage 5 — Evidence graph and interface

- Store source-grounded gene–glycan–pathogen–phenotype relations.
- Require provenance and evidence grade for every trusted edge.
- Add retrieval that surfaces contradictory evidence and refuses personal medical advice.

## Stage 6 — Prospective research

- Proceed only after external replication and documented net benefit.
- Perform silent-mode evaluation before any clinician-facing prototype.
- Establish monitoring for drift, calibration, and subgroup harm.

