# RMDC26 Experienced — Stage 1 v0.2.2 Runbook

## Objective

Run a reproducible, photometry-only 1S1L/PSPL baseline across RMDC26 Experienced-tier events, solve source and blend fluxes independently by observed filter, preserve data-quality failures, and route statistically poor fits for later binary/higher-order review.

This is computational triage infrastructure, not the final astrophysical classification layer.

## Production files

```text
scripts/fit_rmdc26_1s1l_baseline_v022.py
tests/test_rmdc26_1s1l_baseline_v022.py
```

The fitter reads the organizer-provided Roman Nexus dataset:

```text
/data/data-challenge/rges/RMDC26_Experienced_Data.parquet
```

Production output directory:

```text
outputs/fits_v022_full/
```

Primary generated artifacts:

```text
rmdc26_1s1l_baseline.parquet
rmdc26_1s1l_baseline.csv
rmdc26_1s1l_baseline_manifest.json
```

A failures JSON is written only if event-level exceptions occur.

## Environment

Recorded production environment:

```text
Roman Nexus environment: RomanNexus-2026.1
Python: 3.12.13
threads: 4
DuckDB memory limit: 4GB
```

Core Python dependencies used by the Stage 1 workflow:

- DuckDB
- NumPy
- pandas
- SciPy
- PyArrow (Parquet I/O environment)

The submission workflow later used `microlens-submit==0.17.9`.

## Synthetic verification

From the repository root:

```bash
python -m py_compile scripts/fit_rmdc26_1s1l_baseline_v022.py
PYTHONPATH=scripts python tests/test_rmdc26_1s1l_baseline_v022.py
```

The v0.2.2 synthetic tests cover:

- clean PSPL parameter recovery;
- injected residual anomaly routing;
- all-saturated / no-valid-photometry coverage handling.

## Stage 1 fitting behavior

For each event the pipeline:

1. removes saturated rows and rows with non-finite photometry or non-positive flux uncertainty;
2. sorts by BJD;
3. constructs deterministic per-band encodings;
4. estimates standardized excess flux relative to per-band robust baselines;
5. retains high-information epochs and a deterministic regular sample when an event exceeds the fit-point cap;
6. constructs coarse candidates for `t0`, `u0`, and `tE`;
7. analytically solves source/blend flux for each band at every trial geometry;
8. runs bounded L-BFGS-B optimization from the best coarse starts;
9. invokes a bounded Powell fallback when the primary optimizer fails, does not move, or does not sufficiently improve;
10. evaluates the final model on all valid unsaturated photometry;
11. computes fit and residual diagnostics;
12. emits explicit route and quality metadata.

## Fitted and derived quantities

Core fitted microlensing parameters:

```text
t0
u0
tE
```

Per-band linear parameters:

```text
source_flux_uJy
blend_flux_uJy
```

Key diagnostics:

```text
chi2
reduced_chi2
log_likelihood
constant_chi2
delta_chi2_vs_constant
max_abs_sigma
p99_abs_sigma
fraction_abs_gt5
max_run_gt4
runtime_seconds
```

Quality/provenance metadata include optimizer method, optimizer success/message, fit-point counts, parameter-boundary flags, negative-source-flux flags, timestamps, pipeline stage, and pipeline version.

## Residual-routing defaults

The v0.2.2 defaults are:

```text
anomaly_red_chi2       = 2.0
anomaly_p99_abs_sigma  = 5.0
anomaly_fraction_gt5   = 0.002
anomaly_max_run_gt4    = 8
```

An event routes to `anomalous_route` if one or more residual criteria trigger. Otherwise it routes to `1S1L_candidate`, subject to separate fit-quality metadata.

No valid unsaturated photometry produces a `data_quality_route` record rather than an omitted event.

## Quality semantics

Negative source flux in one or more bands is retained as evidence and recorded as a quality flag. It is not, by itself, treated as proof of higher-order microlensing structure.

Convergence near parameter bounds is likewise recorded as model-quality metadata, not automatically labeled as an anomaly.

An optimizer that remains effectively at its seed is routed to quality review.

## Time-coordinate policy

The fitter reads `bjd` and records:

```text
t0_time_system = input_bjd
```

No time-system conversion occurs inside Stage 1. The numeric values used in the final RMDC26 submission were preserved unchanged after explicit challenge-specific clarification; see `SUBMISSION_RECORD.md`.

## Full production execution

The completed full run used:

```text
script: scripts/fit_rmdc26_1s1l_baseline_v022.py
output: outputs/fits_v022_full
threads: 4
memory limit: 4GB
checkpoint interval: 25
run ID: rmdc26_stage1_v022_full_20260804T230001Z
```

The recorded production result was:

```text
Events selected: 2079
Failures: 0
1S1L_candidate: 1148
anomalous_route: 930
data_quality_route: 1
model-bearing rows: 2078
```

Resource accounting:

```text
Wall time: 5920.372 s
User CPU: 5846.498 s
System CPU: 33.235 s
Total measured CPU: 5879.733 s = 1.633259 CPU-h
Reported CPU utilization: 99.31%
```

## Output contract

Important submission-oriented columns include:

- `event_id`
- `solution_alias`
- `model_tags`
- `model_type`
- `t0`
- `t0_time_system`
- `u0`
- `tE`
- per-band `F*_S` / `F*_B` values

The outputs also preserve routing, residual diagnostics, optimizer state, data-quality counts, and runtime provenance.

## Scientific guardrail

`1S1L_candidate` means only that the event passed the current Stage 1 photometric residual thresholds. `anomalous_route` means the baseline residuals justify more expressive modeling or review. `data_quality_route` means Stage 1 could not construct a valid photometric fit.

None of these labels alone constitutes a final astrophysical determination.
