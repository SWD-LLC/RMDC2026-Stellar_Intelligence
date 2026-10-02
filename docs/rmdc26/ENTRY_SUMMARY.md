# RMDC26 Experienced-Tier Entry Summary

## Entry identity

**Project:** Stellar Intelligence  
**Principal architect / project owner:** Sierra Warren  
**Organization:** Sierra Warren Developments, LLC  
**Challenge tier:** Experienced  

This repository documents the computational and scientific workflow used to produce a verified local RMDC26 submission package on the Roman Research Nexus.

## Scientific approach

The production Stage 1 pipeline performs a fast photometry-only point-source/point-lens (`1S1L` / PSPL) baseline fit across the Experienced-tier event set. It solves source and blend fluxes analytically per band while optimizing the nonlinear lens parameters and then computes residual diagnostics used for deterministic routing.

The route labels are computational triage, not final astrophysical classifications.

```text
Experienced events processed: 2079
Model-bearing Stage 1 solutions: 2078
1S1L_candidate: 1148
anomalous_route: 930
data_quality_route: 1
Stage 1 failures: 0
```

The one data-quality-only event is `RMDC26_001563`, for which no valid unsaturated photometry remained after the documented quality filter.

## Stage 1 model and routing

The baseline model uses the standard PSPL magnification relation. For each filter, source and blend fluxes are solved by weighted linear least squares at each nonlinear trial.

Residual routing uses several complementary diagnostics rather than a single goodness-of-fit threshold:

- reduced chi-square;
- 99th-percentile absolute standardized residual;
- fraction of residuals above 5 sigma;
- longest coherent run above 4 sigma.

Events that exceed the documented thresholds are routed to `anomalous_route` for more expressive modeling or review.

## Compute and efficiency

Recorded Stage 1 production compute:

```text
Roman Nexus environment: RomanNexus-2026.1
Python: 3.12.13
threads: 4
DuckDB memory limit: 4GB
wall time: 5920.372 s = 1.644548 h
user CPU: 5846.498 s
system CPU: 33.235 s
total measured CPU: 5879.733 s = 1.633259 CPU-h
reported CPU utilization: 99.31%
```

Historical Stage 1/staging environment metadata:

```text
RomanNexus-2026.1
Python 3.12.13
```

Final October 2 packaging metadata embedded in the frozen archive:

```text
cpu_details: 2 online CPUs: 0,1
memory_gb: 15.0
platform: Roman Nexus
nexus_image: RomanNexus-2026.2
```

The Stage 1 design intentionally limits expensive nonlinear optimization by preserving high-information epochs and filling the remaining fit subset deterministically.

## Submission lifecycle and validation

The workflow used `microlens-submit==0.17.9` and treated submission-state transitions as auditable operations.

Key controls included:

1. contract and persistence probes before real-data import;
2. organizer-resolved `t0` time-coordinate policy;
3. a ten-event real-data canary;
4. isolated full staging import;
5. explicit inactive-state verification;
6. accelerated deactivation recovery after the supported per-solution CLI path proved prohibitively slow;
7. solution, event, and submission validation;
8. hardware metadata remediation;
9. controlled activation;
10. active-state cryptographic lock;
11. one separately authorized export;
12. archive integrity and identity reconciliation.

Final active-state validation before export:

```text
solutions: 2078
active: 2078
inactive: 0
solution validation messages: 0
solution validation exceptions: 0
event validation messages: 0
event validation exceptions: 0
submission validation messages: 0
submission validation exception: None
```

## Verified export

The final October 2 submission artifact is not committed to GitHub.

```text
archive: RMDC26_Sierra_Warren_Experienced_20261002.zip
size_bytes: 2600175
members: 6235
sha256: 6f509d13444cc723622db27e04ce729da7f63dfe4d1c2bee33ae2e940427140e
```

Final archive verification established:

- 2,078 event JSON records;
- 2,078 solution JSON records;
- 2,078 Markdown solution notes;
- 2,078 unique active solutions;
- 0 inactive solutions;
- embedded hardware metadata present;
- ZIP integrity clean;
- official `microlens-submit validate-submission` passed;
- submission validation issues: 0.

Final packaging and validation were performed in `RomanNexus-2026.2` with `microlens-submit==0.17.9`.

The earlier August export hashes remain preserved in `SUBMISSION_RECORD.md` and `EVIDENCE_INDEX.md` as historical provenance; they are not the October 2 final artifact.

## Time-coordinate provenance

Stage 1 records:

```text
t0_time_system = input_bjd
```

For this RMDC26 submission, the Stage 1 numeric `t0` values were copied unchanged into the submission parameter after organizer clarification resolved the challenge-specific BJD/HJD ambiguity. No BJD-to-HJD transform was applied.

## Scientific limitation and next phase

The verified Stage 1 export is a baseline package, not a claim that all Experienced-tier events have received final higher-order physical modeling.

The 930-event `anomalous_route` queue is the next scientific target. Stage 2 is designed to use representative canaries, model-family escalation, measured compute controls, and comparison against the locked Stage 1 baseline before any bulk higher-order run.

## Primary repository documents

- `SCIENTIFIC_SCOPE.md` — interpretation limits;
- `STAGE1_RUNBOOK.md` — Stage 1 execution contract;
- `ENVIRONMENT.md` — exact runtime and compute record;
- `SUBMISSION_RECORD.md` — lifecycle and export provenance;
- `RUBRIC_ALIGNMENT.md` — evaluation traceability;
- `OFFICIAL_CHALLENGE_RESOURCES.md` — organizer source-of-truth links;
- `SUBMISSION_SPEC_ALIGNMENT.md` — submission-format mapping;
- `SOURCE_INTEGRITY.md` — archived/public source attestation;
- `MODELING_ROADMAP.md` — higher-order modeling plan;
- `EVIDENCE_INDEX.md` — cryptographic and evidence map.
