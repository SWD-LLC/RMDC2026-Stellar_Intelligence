# RMDC26 Experienced — Submission Record

This document is the evaluator-facing provenance summary for the Stellar Intelligence RMDC26 Experienced-tier submission workflow.

## Final local submission state

The final controlled export completed successfully on Roman Research Nexus.

```text
STATUS: PASS_EXPORTED_ARCHIVE_VERIFIED
EXPORT_RETURN_CODE: 0
EXPORTED_SOLUTION_JSONS: 2078
EXPORTED_UNIQUE_SOLUTION_IDS: 2078
EXPORTED_IDS_MATCH_LIVE: True
EXPORTED_HARDWARE_PRESENT: True
ZIP_CRC_CLEAN: True
ZIP_PATHS_SAFE: True
LIVE_PROJECT_UNCHANGED: True
STAGE1_UNCHANGED: True
ACTIVE_LOCK_UNCHANGED: True
ACTIVE_AFTER_EXPORT: 2078
INACTIVE_AFTER_EXPORT: 0
UPLOAD_PERFORMED=NO
EXTERNAL_SUBMISSION_PERFORMED=NO
```

Export artifact:

```text
RMDC26_Experienced_Stellar_Intelligence_20260809T002925Z.zip
SHA256 0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597
SIZE   2600508 bytes
MEMBERS 6235
```

The ZIP is intentionally not stored in this public repository. This repository contains the code, methods, documentation, and provenance needed to understand how it was produced.

## Stage 1 production pass

- Script: `scripts/fit_rmdc26_1s1l_baseline_v022.py`
- Pipeline version: `0.2.2`
- Source: `/data/data-challenge/rges/RMDC26_Experienced_Data.parquet`
- Output directory: `outputs/fits_v022_full`
- Events selected: `2,079`
- Failures: `0`
- Run ID: `rmdc26_stage1_v022_full_20260804T230001Z`

Verified route accounting:

| Route | Count | Meaning |
|---|---:|---|
| `1S1L_candidate` | 1,148 | photometric residuals passed Stage 1 thresholds |
| `anomalous_route` | 930 | residual structure requires more expressive modeling/review |
| `data_quality_route` | 1 | no valid unsaturated photometry for Stage 1 fitting |
| model-bearing solutions | 2,078 | Stage 1 1S1L solutions eligible for controlled staging |

The data-quality-only event was `RMDC26_001563`.

## Stage 1 model and routing

Stage 1 is a point-source/single-point-lens photometric baseline. It fits the core parameters:

- `t0`
- `u0`
- `tE`

Source and blend fluxes are solved independently for each observed band. Stage 1 uses deterministic fit-point selection, a coarse parameter search, bounded optimization, and a Powell fallback when the primary L-BFGS-B optimization does not move or improve sufficiently.

Residual diagnostics include:

- reduced chi-square;
- 99th percentile absolute residual significance;
- fraction of residuals above 5 sigma;
- maximum consecutive run above 4 sigma.

Negative fitted source flux and parameter-boundary convergence are retained as explicit quality metadata instead of being silently suppressed. A Stage 1 route is computational triage, not a final astrophysical classification.

## Compute and efficiency

Full Stage 1 resource accounting:

| Quantity | Recorded value |
|---|---:|
| wall time | 5,920.372 s (1.644548 h) |
| user CPU | 5,846.498 s |
| system CPU | 33.235 s |
| total measured CPU | 5,879.733 s (1.633259 CPU-h) |
| reported CPU utilization | 99.31% |
| configured threads | 4 |
| configured DuckDB memory limit | 4 GB |

Environment:

- Roman Nexus environment: `RomanNexus-2026.1`
- Python: `3.12.13`
- submission toolkit: `microlens-submit==0.17.9`
- principal numerical/data stack: DuckDB, NumPy, pandas, SciPy, PyArrow

Final submission hardware metadata:

```text
platform: Linux-6.12.94-123.190.amzn2023.x86_64-x86_64-with-glibc2.39
os: Linux
cpu_details: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
memory_gb: 15.34
nexus_image: 378083651696.dkr.ecr.us-east-1.amazonaws.com/roman:RomanNexus-2026.1
```

The challenge's Roman Nexus documentation lists the standard server configurations separately; the values above are the hardware metadata detected and persisted in this submission project at validation time.

## Time-coordinate provenance

Stage 1 preserved the source dataset's numeric time coordinate and recorded:

```text
t0_time_system = input_bjd
```

The source BJD range and Stage 1 fitted `t0` range were audited as numerically aligned. Because challenge documentation used HJD wording for the submission field, the team requested organizer clarification instead of applying an undocumented conversion.

The resulting RMDC26-specific policy was:

1. keep Stage 1 numeric `t0` unchanged;
2. preserve `t0_time_system=input_bjd` in internal provenance;
3. do not apply a BJD-to-HJD conversion;
4. map the unchanged value into the challenge submission `t0` field.

This decision is challenge-specific and should not be read as a general equivalence between BJD and HJD.

## Controlled submission lifecycle

The submission workflow was deliberately staged because `microlens-submit==0.17.9` imports solutions as active by default and the CSV importer does not provide a reliable inactive-import field.

The controlled lifecycle was therefore:

```text
Stage 1 artifacts
    -> CSV staging map
    -> isolated microlens-submit project
    -> import
    -> verify imported solution count
    -> deactivate all staged solutions
    -> verify inactive persisted state
    -> validate each preserved solution
    -> validate events
    -> validate submission structure
    -> add/verify hardware metadata
    -> lock inactive state
    -> controlled activation
    -> validate active state
    -> lock active state
    -> one authorized export
    -> ZIP integrity and identity audit
```

The initial serial deactivation implementation proved semantically correct but operationally inefficient because it repeatedly loaded and saved the whole project once per solution. That process was safely retired after the persisted state was audited. The remaining solutions were deactivated in one package load / one save using the same model-level `Solution.deactivate()` semantics, with before/after checks proving parameters, IDs, and Stage 1 artifacts were unchanged.

## Validation chain

Final chain:

```text
Stage 1                       PASS
Full import                    PASS 2078/2078
Deactivation                   PASS 0 active / 2078 inactive
Solution validation            PASS 2078/2078, 0 messages
Event validation (inactive)    PASS expected inactive-state notices only
Hardware metadata              PASS
Inactive state lock            PASS
Controlled activation          PASS 2078 active / 0 inactive
Solution validation (active)   PASS 0 messages / 0 exceptions
Event validation (active)      PASS 0 messages / 0 exceptions
Submission validation (active) PASS 0 messages / no exception
Active state lock              PASS
Export                         PASS_EXPORTED_ARCHIVE_VERIFIED
External upload                NOT PERFORMED in recorded transaction
```

## Integrity anchors

Key SHA-256 values:

```text
Stage 1 verified artifact ZIP
6b4cd9483f8d3c28d28917615d1ecb0edd0fcda00623ee4dbc3c9b088a2aa1ae

Validated inactive-state manifest
debde39c12331a04b504778860b2275098c6366649d41c359d76d7a1abb4f0d9

Controlled activation report
84c278318f73e85806c8838b94917244b8bf6f5ddbbd086e85d691678af6404e

Active solution tree
97bbfaff5ee0b42cb13b2b4a67a3a309088cf8de6b52814c693b3e588b382434

Active validated manifest
dd404b9832d8e77b7c7325c773fcd72ef82b851bc32251f090f146d838c412b9

Exported submission ZIP
0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597

Controlled export report
259e6d374c409f10734ac9d9aeec5783251110926ff00d5cd799e85d62e61248
```

## What the public repository does not contain

This repository does not redistribute the RMDC26 challenge dataset. It also does not treat external reference catalogs as challenge measurements. External sources such as OGLE are documented as scientific context/reference resources and remain outside the blind-fit input unless an artifact explicitly states otherwise.

## Ownership and accountability

Project owner and principal architect: **Sierra Warren**  
Organization: **Sierra Warren Developments, LLC**

The evidence policy is to document missing measurements as missing rather than estimate them after the fact, preserve failed attempts when they explain a design correction, and maintain explicit boundaries between challenge data, external references, scientific inference, and submission tooling.
