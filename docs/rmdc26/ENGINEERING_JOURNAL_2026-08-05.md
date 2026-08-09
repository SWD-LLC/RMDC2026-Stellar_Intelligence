# RMDC26 Daily Engineering Journal — 2026-08-05

**Project owner:** Sierra Warren  
**Project:** Stellar Intelligence / RMDC26 Experienced tier  
**Execution environment:** Roman Nexus, `RomanNexus-2026.1`  
**Coverage window:** 2026-08-04 21:34 EDT through 2026-08-05 21:34 EDT

This public journal preserves the engineering decisions and measured evidence that governed the transition from the completed Stage 1 baseline into a controlled challenge-submission workflow. Where a measurement was not captured, it is identified as missing rather than reconstructed after the fact.

## Carry-in Stage 1 baseline

The full Stage 1 baseline completed immediately before this journal window.

```text
Script: scripts/fit_rmdc26_1s1l_baseline_v022.py
Pipeline version: 0.2.2
Source: /data/data-challenge/rges/RMDC26_Experienced_Data.parquet
Output directory: outputs/fits_v022_full
Events selected: 2079
Failures: 0
Threads: 4
Memory limit: 4GB
Checkpoint interval: 25
Run ID: rmdc26_stage1_v022_full_20260804T230001Z
Exit status: 0
```

Measured resources:

```text
Wall time: 5920.372 seconds = 1.644548 hours
User CPU: 5846.498 seconds = 1.624027 CPU-hours
System CPU: 33.235 seconds = 0.009232 CPU-hours
Total CPU: 5879.733 seconds = 1.633259 CPU-hours
CPU utilization: 99.31%
```

Verified routing state:

```text
1S1L_candidate: 1148
anomalous_route: 930
data_quality_route: 1
model-bearing rows: 2078
data-quality-only event: RMDC26_001563
```

Stage 1 evidence archive SHA-256:

```text
6b4cd9483f8d3c28d28917615d1ecb0edd0fcda00623ee4dbc3c9b088a2aa1ae
```

## Chronological engineering record

| Seq. | Area | Action | Result / decision |
|---:|---|---|---|
| 01 | submission contract | reviewed challenge and `microlens-submit` requirements | required CSV fields and 1S1L parameter contract identified |
| 02 | environment | inspected Python/package environment | Python `3.12.13`; `microlens-submit==0.17.9` |
| 03 | CLI | investigated missing direct executable | console script existed under user base; module invocation used without PATH mutation |
| 04 | CLI contract | inspected supported commands/help | specific init/import/activate/deactivate/validation commands confirmed |
| 05 | synthetic dry run | ran contract probe | invocation and parsing behavior passed without persistent RMDC26 import |
| 06 | persistence | ran isolated persistent import probe | imported solution persisted and defaulted to active |
| 07 | source inspection | inspected installed importer | CSV import path did not expose a reliable inactive-state mapping |
| 08 | lifecycle | tested import -> deactivate -> reload | supported deactivation persisted inactive state |
| 09 | time standard | audited source BJD and Stage 1 `t0` | numeric axis preserved; documentation ambiguity escalated |
| 10 | organizer resolution | requested challenge-specific BJD/HJD guidance | organizer instructed team to use BJD; no conversion applied |
| 11 | reference code | cloned official `rges-pit/data-challenge-notebooks` with Git | reference checkout separated from project repo |
| 12 | package hygiene | rejected a generated package with incorrect attribution/identifier contamination | corrected project-owned package rebuilt and rescanned |
| 13 | canary preparation | installed corrected real-data canary controls | corrected archive hash matched; unit tests passed |
| 14 | documentation | established exhaustive daily journal and state-capture requirement | future challenge work required files/processes/data/compute/evidence state tracking |

## Scientific decisions

### Stage 1 model

- baseline model: point-source/single-point-lens (`1S1L` / PSPL);
- fitted nonlinear core parameters: `t0`, `u0`, `tE`;
- source/blend flux solved per observed band;
- bands represented in Stage 1 provenance include F087, F146, and F213;
- positive/nonnegative baseline convention used for `u0`;
- residual route labels are computational triage, not final astrophysical classifications.

### Time-coordinate decision

The read-only time audit found the challenge input represented on a BJD coordinate while the submission documentation used HJD wording. The source BJD range and the Stage 1 fitted `t0` range were measured as numerically aligned:

```text
source BJD range: 2461447.75721162 to 2463164.49811815
Stage 1 t0 range: 2461447.75721162 to 2463164.49811815
t0_time_system: input_bjd
```

Locked RMDC26 policy after organizer clarification:

1. copy numeric Stage 1 `t0` unchanged;
2. preserve `t0_time_system=input_bjd` in internal provenance;
3. do not perform BJD-to-HJD conversion;
4. map the unchanged numeric value into the submission `t0` parameter;
5. treat this as a challenge-specific rule, not a general time-system equivalence.

## Submission-system engineering

The key lifecycle discovery was that imported solutions defaulted to active. Because the CSV importer did not provide a proven inactive-import mechanism, a direct bulk import was not treated as safe.

The controlled design became:

```text
isolated staging project
    -> import
    -> immediate supported deactivation
    -> reload JSON records
    -> verify every solution inactive
    -> verify t0/u0/tE against Stage 1
    -> run solution/event/submission validation
    -> no export until a separate authorization gate
```

This policy was established before the later full 2,078-solution execution.

## Dependencies and environment

Verified during the journal window:

| Item | State |
|---|---|
| environment | `RomanNexus-2026.1` |
| Python | `3.12.13` |
| Python executable | `/opt/conda/envs/RomanNexus-2026.1/bin/python` |
| `microlens-submit` | `0.17.9` |
| package location | `/home/swa417/.local/lib/python3.12/site-packages` |
| working invocation | `python -m microlens_submit.cli` |
| Git | available |
| `ripgrep` | available |
| `unzip` | available |
| `sha256sum` | available |

The Stage 1 code records NumPy, pandas, DuckDB, SciPy, Python/platform, thread count, and memory limit into its generated run manifest.

No package upgrade/downgrade, shell-profile change, credential rotation, or PATH mutation was required to resolve the submission-tool investigation.

## Data operations

The challenge data were treated as read-only inputs.

| Artifact | Operation | State |
|---|---|---|
| RMDC26 Experienced Parquet | Stage 1 fit and read-only audits | source not intentionally modified |
| Stage 1 Parquet | protected derived baseline | read-only during submission investigation |
| Stage 1 CSV | protected derived baseline | unchanged |
| Stage 1 manifest | protected run metadata | unchanged |
| BJD-to-HJD conversion | not performed | organizer-approved BJD policy |
| synthetic probe rows | isolated tooling probes | not RMDC26 event data |

## Tests and validation in this window

```text
Stage 1 synthetic clean PSPL recovery: PASS
Stage 1 injected anomaly routing: PASS
Stage 1 no-valid-photometry coverage row: PASS
Stage 1 full production run: PASS
Stage 1 accounting: PASS
microlens-submit contract probe: PASS
persistence probe: PASS
default active-state observation: True
synthetic supported deactivation: PASS
time-standard audit: PASS
organizer resolution: use BJD
corrected canary package identifier scan: PASS
corrected canary unit tests: PASS
```

The real full staging import and final export had not yet occurred during this journal's coverage window. Later records in `SUBMISSION_RECORD.md` document those subsequent transactions.

## Failures and corrective actions

| Failure / risk | Root cause | Correction |
|---|---|---|
| console command unavailable | user script directory absent from PATH | used `python -m microlens_submit.cli` |
| imported solutions active by default | package lifecycle semantics | proved deactivation and required inactive-state verification |
| CSV could not safely request inactive state | importer behavior | designed staging import followed by deterministic deactivation |
| BJD/HJD ambiguity | source/submission wording mismatch | audited and obtained organizer instruction instead of silently converting |
| GitHub CLI unavailable on Nexus | tool absent | used standard Git clone for reference repository |
| canary package path confusion | file browser / terminal location mismatch | restored explicit project paths and fresh corrected package |
| incorrect external identifier in generated package | attribution contamination | rejected package, rebuilt, hard-scanned and retested |
| Jupyter workspace/tabs appeared reset | workspace/session issue | verified files and running sessions rather than assuming file loss |

Failures are retained here because they explain why the final submission workflow contains specific safety gates.

## Challenge-ground-rule traceability

| Ground-rule concern | Recorded evidence |
|---|---|
| dependencies and CPU hours | Python/package environment, Stage 1 wall/CPU timing, generated runtime manifest |
| open-source documented code | production scripts, tests, runbooks, contracts, evidence and journal records retained for publication |
| format validation | submission-tool contract and later full validation evidence |
| designated project owner | Sierra Warren recorded as author/project owner |
| organizer communication | BJD/HJD clarification preserved as a project decision |

## Evidence hashes recorded in the engineering archive

```text
V3 control bundle
7916bfdf86cc55b83248bf2ab478826b8fca79d7ed11c8a9439da591e42508a9

Stage 1 verified evidence ZIP
6b4cd9483f8d3c28d28917615d1ecb0edd0fcda00623ee4dbc3c9b088a2aa1ae

contract probe v0.2.0
f5648fd6f26db20c8f4ffd23ce3ac36cb9808194313cdfdabdfeab343c6aec90

persistence probe v0.3.0
c7d9666aaec4b2ffb1160d0ac9c13227ecd47b2fb3bd84ecc5216ac507e3934e

importer semantics JSON
94da6f0b52f459911e3222f7dee8a8e24ce2efd851f16624ede69d705acdf034

importer semantics source
75536ee4dd199c358a79545eb77c5b47805e8828f49f69073d9127a66d5396b4

deactivation lifecycle package v0.4.0
042b3391ece79f21cd20a299c79ba343989e58b52055b064729c516bc9ee868a

time-standard audit v0.5.0
4dceb7981d3507eccd7e0f6df1a97b0c23c919153d3b5abe9e5c45c35997e3ba

corrected real-data canary v0.1.1
d415503f08fe0ad49ba0f07b150ea6c79180d7c029baec231c17c648af43b1b7
```

## Evidence policy

The project uses three rules throughout this record:

1. preserve measured values rather than replace them with retrospective estimates;
2. record missing measurements explicitly;
3. preserve failures and corrective actions when they materially changed the final architecture or submission controls.

Later submission lifecycle, validation, hardware-remediation, activation, and export evidence is summarized separately in `SUBMISSION_RECORD.md` so this dated journal remains historically faithful to its original coverage window.
