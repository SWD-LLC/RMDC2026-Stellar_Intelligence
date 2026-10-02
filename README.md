# Stellar Intelligence — RMDC26 Experienced-Tier Work

This repository contains the public, reproducible technical record for the Stellar Intelligence Roman Microlensing Data Challenge 2026 (RMDC26) Experienced-tier workflow.

## RMDC26 status

The October 2, 2026 Stellar Intelligence RMDC26 Experienced-tier artifact has been validated, exported, archive-audited, cryptographically identified, and submitted through the organizer-provided alternative Box path.

- Project: **Stellar Intelligence**
- Challenge tier: **Experienced**
- Historical Stage 1 targets processed: **2,079**
- Historical Stage 1 model-bearing solutions: **2,078**
- Historical data-quality-only event: `RMDC26_001563`
- Final exported event records: **2,078**
- Final exported solution records: **2,078**
- Final active solutions: **2,078**
- Final inactive solutions: **0**
- Final model mix: **2,076 × 1S1L, 1 × 1S3L, 1 × 2S1L**
- Final archive audit: **PASS**
- Final export status: **PASS**
- External challenge upload: **submitted through the alternative Box file request**

Final submitted archive:

```text
Stellar_Intelligence_RMDC26_Experienced_20261002_FINAL.zip
sha256: f9fdb62dbf9a75f7bd2a5f68e17a25c27f9d990a606c47c2d42a30e2388d41dd
```

The challenge ZIP itself is intentionally not committed here. See `docs/rmdc26/FINAL_SUBMISSION_2026-10-02.md` for the final artifact record and `docs/rmdc26/SUBMISSION_RECORD.md` for the preserved submission history.

### Scientific-scope warning

The final archive is not a claim that every Experienced-tier event has received an exhaustive higher-order physical classification. Most exported solutions remain Stage 1 `1S1L` baselines. Two events contain recovered higher-complexity solutions in the submitted archive: `RMDC26_002050` as `1S3L` and `RMDC26_000249` as `2S1L`.

The current submission toolkit emits six schema warnings for the fit-native 1S3L geometry field names retained for `RMDC26_002050`. Those names were not remapped without proof of semantic equivalence. The corresponding submission note records this boundary.

Organizer guidance also establishes that evaluator-facing written notes are loaded from the Markdown note hooks referenced by the submission object. Repository notebooks and broader technical documents are supporting provenance, not substitutes for those submission notes.

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
- deterministic code-generated regression fixtures;
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

### Historical Stage 1 production run

The completed Stage 1 production run remains recorded exactly as executed:

- Roman Nexus environment: `RomanNexus-2026.1`
- Python: `3.12.13`
- threads: `4`
- configured DuckDB memory limit: `4GB`
- Stage 1 wall time: `5,920.372 s` (`1.644548 h`)
- Stage 1 user CPU: `5,846.498 s`
- Stage 1 system CPU: `33.235 s`
- Stage 1 total measured CPU: `5,879.733 s` (`1.633259 CPU-h`)
- reported CPU utilization: `99.31%`

Those values are historical execution facts and are not retroactively changed.

### Final October 2 packaging and validation environment

The final submission package was validated and exported on Roman Research Nexus using `microlens-submit==0.17.9` in `RomanNexus-2026.2`.

The final submitted artifact embeds:

```text
cpu: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
cpu_details: 2 online CPUs: 0,1
memory_gb: 15
platform: Roman Nexus
nexus_image: RomanNexus-2026.2
repo_url: https://github.com/SWD-LLC/RMDC2026-Stellar_Intelligence.git
```

The final packaging environment and the historical Stage 1 execution environment are intentionally documented separately.

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
  FINAL_SUBMISSION_2026-10-02.md
  SCIENTIFIC_SCOPE.md
  MODELING_ROADMAP.md
  RUBRIC_ALIGNMENT.md
  ENVIRONMENT.md
  REFERENCES.md
  STAGE1_RUNBOOK.md
  ENGINEERING_JOURNAL_2026-08-05.md

requirements-rmdc26.txt
.github/workflows/rmdc26-stage1-fixtures.yml
```

Additional control/evidence files will be added from the Roman Nexus working tree without rewriting the already-validated scientific outputs.

## Public fixture-based verification

The repository includes lightweight code-generated regression fixtures that do **not** use or reproduce the challenge dataset. They exercise clean PSPL recovery, injected-anomaly routing logic, and data-quality coverage handling. They are software test fixtures only and are not RMDC26 event products.

```bash
python -m pip install -r requirements-rmdc26.txt
python -m py_compile scripts/fit_rmdc26_1s1l_baseline_v022.py
PYTHONPATH=scripts python tests/test_rmdc26_1s1l_baseline_v022.py
```

A GitHub Actions workflow runs the same fixture-based verification for relevant pull requests and changes to `main`.

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
