# Stellar Intelligence — RMDC26 Experienced-Tier Work

This repository contains the public, reproducible technical record for the Stellar Intelligence Roman Microlensing Data Challenge 2026 (RMDC26) Experienced-tier workflow.

## RMDC26 status

The current RMDC26 pipeline reached a verified local export state on Roman Research Nexus.

- Challenge tier: **Experienced**
- Source dataset: `/data/data-challenge/rges/RMDC26_Experienced_Data.parquet`
- Stage 1 pipeline: `scripts/fit_rmdc26_1s1l_baseline_v022.py`
- Stage 1 version: `0.2.2`
- Events processed: **2,079**
- Model-bearing solutions: **2,078**
- Data-quality-only event: `RMDC26_001563`
- Stage 1 failures: **0**
- Submission solutions validated: **2,078 / 2,078**
- Active solutions at export: **2,078**
- Local export status: `PASS_EXPORTED_ARCHIVE_VERIFIED`
- External upload/submission: **not performed as of the recorded export transaction**

The exported submission archive itself is not committed here. Its verified SHA-256 is:

```text
0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597
```

### Scientific-scope warning

The verified ZIP is a **Stage 1 baseline package**, not a claim that every Experienced-tier event has received its final higher-order physical classification. Of the 2,078 model-bearing Stage 1 events, 930 were explicitly routed as anomalous and therefore warrant more expressive modeling or review. See `docs/rmdc26/SCIENTIFIC_SCOPE.md` and `docs/rmdc26/MODELING_ROADMAP.md` before interpreting technical package validity as scientific completeness.

## Official challenge source of truth

Challenge mechanics, submission criteria, Nexus instructions, and reference modeling workflows are anchored to organizer-maintained resources:

- RMDC26 challenge: https://rges-pit.org/data-challenge/
- Nexus / AAS workshop documentation: https://rges-pit.org/data-challenge/aas-workshop/1-nexus/
- official notebooks: https://github.com/rges-pit/data-challenge-notebooks
- official submission tool: https://github.com/rges-pit/microlens-submit
- submission documentation: https://microlens-submit.readthedocs.io/en/latest/

The organizer documentation states that strict adherence to submission criteria is required because much of the evaluation is automated. This repository therefore treats the official submission contract as authoritative and documents local implementation decisions separately.

See `docs/rmdc26/OFFICIAL_CHALLENGE_RESOURCES.md` for exact notebook links, submission guides, Nexus reference-directory rules, and source precedence. See `docs/rmdc26/SUBMISSION_SPEC_ALIGNMENT.md` for the direct mapping between the recorded local package and the official `microlens-submit` contract.

## What is public here

The RMDC26 portion of this repository is being organized so evaluators and researchers can inspect:

- the production Stage 1 fitting code;
- synthetic regression tests;
- the Stage 1 runbook;
- compute and hardware documentation;
- time-coordinate provenance and the challenge-specific `t0` decision;
- submission lifecycle and validation controls;
- engineering journals and evidence summaries;
- challenge-rubric traceability;
- scientific-scope limits;
- higher-order modeling roadmap;
- organizer-maintained challenge references;
- external scientific references used for background and comparison.

Challenge data are **not** redistributed by this repository.

## RMDC26 architecture

The Stage 1 production pass is a fast photometry-only point-source/point-lens baseline used as computational triage infrastructure.

```text
Roman RMDC26 Experienced photometry
        |
        v
quality filtering / saturation handling
        |
        v
1S1L / PSPL baseline fitting
        |
        +--> 1S1L_candidate
        |
        +--> anomalous_route
        |
        +--> data_quality_route
        |
        v
controlled microlens-submit staging
        |
        v
validation -> activation -> verified local export
```

A Stage 1 route label is **not** a final astrophysical classification. Residual anomaly evidence routes an event toward more expressive modeling; data-quality failures are preserved explicitly instead of being silently dropped.

For the anomalous queue, the next modeling layer is being designed against the official RGES-PIT binary-lens and microlensing-tools notebooks before any bulk Stage 2 execution.

## Provenance boundary

The challenge photometry is the fitted data source. Official organizer notebooks are treated as challenge-method references. External catalogs and literature resources, including OGLE, are treated as scientific references and comparison material unless an artifact explicitly states otherwise. None are silently injected into the blind challenge inference.

The Nexus preloaded reference directory is also treated as external reference content: organizer guidance states that it is read-only and regularly replaced, so project-owned code and evidence belong in a durable project workspace/repository instead.

## Compute record

The completed full Stage 1 run used:

- Roman Nexus environment: `RomanNexus-2026.1`
- Python: `3.12.13`
- threads: `4`
- configured DuckDB memory limit: `4GB`
- Stage 1 wall time: `5,920.372 s` (`1.644548 h`)
- Stage 1 user CPU: `5,846.498 s`
- Stage 1 system CPU: `33.235 s`
- Stage 1 total measured CPU: `5,879.733 s` (`1.633259 CPU-h`)
- reported CPU utilization: `99.31%`

Submission hardware metadata recorded in the final staging project:

- CPU: `Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz`
- memory: `15.34 GB`
- OS: Linux
- Nexus image: `378083651696.dkr.ecr.us-east-1.amazonaws.com/roman:RomanNexus-2026.1`

## Time-coordinate policy

Stage 1 retained the challenge input time coordinate numerically unchanged and records:

```text
t0_time_system = input_bjd
```

For this RMDC26 submission, the numeric Stage 1 `t0` values were copied unchanged into the submission parameter after the team explicitly resolved the BJD/HJD ambiguity with challenge organizers. No BJD-to-HJD transform was applied. This is an RMDC26-specific submission decision, not a general astronomical time-conversion rule.

## Repository map

```text
scripts/
  fit_rmdc26_1s1l_baseline_v022.py

tests/
  test_rmdc26_1s1l_baseline_v022.py

docs/rmdc26/
  OFFICIAL_CHALLENGE_RESOURCES.md
  SUBMISSION_SPEC_ALIGNMENT.md
  SUBMISSION_RECORD.md
  SCIENTIFIC_SCOPE.md
  MODELING_ROADMAP.md
  RUBRIC_ALIGNMENT.md
  ENVIRONMENT.md
  REFERENCES.md
  STAGE1_RUNBOOK.md
  ENGINEERING_JOURNAL_2026-08-05.md

requirements-rmdc26.txt
.github/workflows/rmdc26-stage1-synthetic.yml
```

Additional control/evidence files will be added from the Roman Nexus working tree without rewriting the already-validated scientific outputs.

## Public synthetic verification

The repository includes a lightweight test that does **not** require the challenge dataset. It checks clean PSPL recovery, injected-anomaly routing, and data-quality coverage behavior.

```bash
python -m pip install -r requirements-rmdc26.txt
python -m py_compile scripts/fit_rmdc26_1s1l_baseline_v022.py
PYTHONPATH=scripts python tests/test_rmdc26_1s1l_baseline_v022.py
```

A GitHub Actions workflow runs the same synthetic verification for relevant pull requests and changes to `main`.

## Official challenge tooling

RMDC26 uses the `microlens-submit` toolkit for challenge submission management, validation, dossier generation, and export. The recorded submission workflow used `microlens-submit==0.17.9` through:

```bash
python -m microlens_submit.cli
```

The official documentation provides the CLI tutorial, Python API, usage examples, and manual submission format. Those resources remain the authoritative contract for challenge packaging; local lifecycle controls in this repository exist to make adherence auditable.

## Ownership

**Principal architect and project owner:** Sierra Warren  
**Organization:** Sierra Warren Developments, LLC

The repository preserves execution history, uncertainty, failure modes, and provenance as part of the scientific product rather than treating those records as disposable implementation detail.
