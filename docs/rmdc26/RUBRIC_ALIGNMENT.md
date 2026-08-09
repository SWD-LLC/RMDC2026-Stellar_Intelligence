# RMDC26 Evaluation Rubric Alignment

This document maps the Stellar Intelligence RMDC26 Experienced-tier work to the organizer evaluation categories. It is an evidence index, not a self-assigned score.

## Challenge goals addressed

The organizer rubric asks participants to:

1. classify all targets;
2. fit appropriate microlensing models and tabulate derived parameters;
3. describe the modeling approach, software, hardware, and innovations;
4. optionally provide plotted model output and posterior samples.

The evaluation panel assigns up to five points in each of five categories:

1. accuracy of fitted-model parameters;
2. number of events modeled;
3. software/computational efficiency;
4. innovation;
5. broadening the field by bringing in new researchers.

The rubric also states that evaluators receive wall/CPU timing and hardware information and should consider anomaly detection/categorization efficiency and the fraction of compute spent finding solutions versus collecting posteriors.

## 1. Accuracy of fitted-model parameters

### Public evidence

- `scripts/fit_rmdc26_1s1l_baseline_v022.py`
- `tests/test_rmdc26_1s1l_baseline_v022.py`
- `docs/rmdc26/STAGE1_RUNBOOK.md`
- `docs/rmdc26/SUBMISSION_RECORD.md`

### Method controls

The Stage 1 fitter:

- fits a point-source/single-point-lens photometric baseline;
- solves source/blend flux independently per observed band;
- fits `t0`, `u0`, and `tE` under bounded optimization;
- uses multiple deterministic coarse starts;
- uses L-BFGS-B with a Powell fallback when the primary optimizer does not move or sufficiently improve;
- records optimizer state and fit-quality metadata;
- preserves negative fitted source flux as evidence rather than clipping it away;
- records parameter-boundary convergence as quality metadata;
- does not silently drop the one event with no valid unsaturated photometry.

Synthetic regression tests verify clean PSPL recovery, anomaly routing, and the data-quality route.

### Time-coordinate control

The source time axis and fitted Stage 1 `t0` values were audited before submission mapping. The RMDC26-specific organizer resolution was to retain the numeric BJD values unchanged. No hidden BJD-to-HJD transform was introduced.

## 2. Number of events modeled

### Production accounting

```text
RMDC26 Experienced events selected: 2079
Stage 1 failures:               0
Model-bearing solutions:        2078
Data-quality-only events:       1
Submitted solution records:     2078
Unique submitted solution IDs:  2078
```

The single data-quality-only event, `RMDC26_001563`, was preserved as an explicit coverage row rather than being silently omitted from the Stage 1 accounting.

### Route accounting

| Route | Count |
|---|---:|
| `1S1L_candidate` | 1,148 |
| `anomalous_route` | 930 |
| `data_quality_route` | 1 |

These route labels are triage classifications, not claims that every event is physically single-lens.

## 3. Software / computational efficiency

### Measured Stage 1 resource use

| Metric | Value |
|---|---:|
| wall time | 5,920.372 s / 1.644548 h |
| user CPU | 5,846.498 s |
| system CPU | 33.235 s |
| total measured CPU | 5,879.733 s / 1.633259 CPU-h |
| reported CPU utilization | 99.31% |
| configured threads | 4 |
| DuckDB memory limit | 4 GB |

### Hardware recorded in final submission metadata

```text
CPU: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
Memory: 15.34 GB
OS: Linux
Nexus image: 378083651696.dkr.ecr.us-east-1.amazonaws.com/roman:RomanNexus-2026.1
Python: 3.12.13
microlens-submit: 0.17.9
```

### Efficiency design choices

The Stage 1 implementation was built for high-throughput triage rather than posterior sampling:

- DuckDB reads only the selected event and required photometric columns from Parquet;
- fitting uses at most a configured deterministic subset of high-information epochs per event;
- source and blend fluxes are solved analytically for each trial geometry instead of included as nonlinear optimizer dimensions;
- coarse starts are evaluated cheaply before bounded local optimization;
- checkpoints allow long runs to resume without recomputing completed events;
- residual metrics route poor fits to later work instead of spending Stage 1 compute on every higher-order model.

The submission lifecycle itself was also performance-audited. A semantically correct serial deactivation implementation was retired after it was proven to impose repeated whole-project load/save overhead; the remaining lifecycle transition was completed in one package load and one save with integrity verification.

## 4. Innovation

Innovation is documented as process and system design rather than asserted from the existence of a new model family.

### Evidence-preserving triage

Instead of forcing every event directly through increasingly expensive models, Stage 1 separates:

- clean PSPL-like residual behavior;
- statistically anomalous residual structure;
- unusable Stage 1 photometry;
- model-quality conditions such as parameter-boundary convergence or negative source flux.

The system intentionally keeps these categories distinct so computational triage is not mislabeled as astrophysical truth.

### Provenance-first submission engineering

The workflow adds transaction-style scientific controls around the challenge submission process:

- source/derived time-axis audit before mapping `t0`;
- explicit organizer-resolution record for an ambiguous convention;
- synthetic contract probes against the installed submission toolkit version;
- persistent-state lifecycle testing before real bulk import;
- inactive-state and active-state cryptographic locks;
- before/after hashing of protected Stage 1 artifacts;
- exact solution-ID accounting across import, activation, and export;
- archive CRC, member-path safety, and identity reconciliation after export.

### Failure as evidence

Operational failures that changed the design are retained in the engineering record. Examples include default-active import behavior, serial deactivation performance, path-resolution failures, and terminal output flooding. Corrections are tied to evidence instead of being erased from the record.

## 5. Broadening the field

The public repository is being structured as a reproducible technical record rather than only a private competition artifact. The intent is to expose:

- runnable fitting code;
- synthetic tests that require no challenge data;
- clearly separated challenge-data and external-reference boundaries;
- explicit explanations of fitting, routing, compute usage, and validation;
- an engineering journal that records uncertainty and failures rather than presenting only polished success states.

This lowers the barrier for researchers and developers entering microlensing from adjacent technical fields to understand how a Roman-scale workflow is actually engineered.

## Evaluator navigation

Recommended review order:

1. repository `README.md`;
2. `docs/rmdc26/SUBMISSION_RECORD.md`;
3. `scripts/fit_rmdc26_1s1l_baseline_v022.py`;
4. `tests/test_rmdc26_1s1l_baseline_v022.py`;
5. `docs/rmdc26/STAGE1_RUNBOOK.md`;
6. `docs/rmdc26/ENGINEERING_JOURNAL_2026-08-05.md`;
7. `docs/rmdc26/REFERENCES.md`.

## Known boundary

The final challenge ZIP is a separate submission artifact and is not committed to this public repository. Its verified SHA-256 is:

```text
0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597
```
