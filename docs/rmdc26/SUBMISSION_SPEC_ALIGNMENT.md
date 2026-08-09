# RMDC26 Submission Specification Alignment

This document maps the recorded Stellar Intelligence submission workflow to the organizer-maintained `microlens-submit` contract. It is intended to prevent a technically valid local artifact from drifting away from the format and metadata rules used by automated evaluation.

## Authoritative references

- Submission documentation: https://microlens-submit.readthedocs.io/en/latest/
- CLI tutorial: https://microlens-submit.readthedocs.io/en/latest/cli_tutorial.html
- Python API: https://microlens-submit.readthedocs.io/en/latest/api.html
- Usage examples: https://microlens-submit.readthedocs.io/en/latest/usage_examples.html
- Manual submission format: https://microlens-submit.readthedocs.io/en/latest/submission_manual.html
- Tool repository: https://github.com/rges-pit/microlens-submit

The recorded workflow was executed against `microlens-submit==0.17.9`.

## Organizer workflow contract

The official tutorial describes the submission lifecycle as:

```text
project initialization
    -> add or bulk-import solutions
    -> validate
    -> document / optionally generate dossier
    -> export
```

The manual strongly recommends using the official tool instead of hand-building a submission because it provides validation and automated metadata handling.

## Project metadata

The official tutorial expects repository and hardware information to be recorded before final validation/export.

Recorded final project metadata included:

```text
Tier: experienced
Repository: this public project repository
CPU: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
Memory: 15.34 GB
OS: Linux
Nexus image: 378083651696.dkr.ecr.us-east-1.amazonaws.com/roman:RomanNexus-2026.1
Python: 3.12.13
microlens-submit: 0.17.9
```

The exact repository URL stored in the historical project should be checked before any future export if the GitHub repository has since been renamed.

## CSV import contract

The official manual requires the following core CSV fields for bulk import:

```text
event_id
solution_alias
model_tags
```

The Stage 1 conversion additionally supplied the required 1S1L parameters:

```text
t0
u0
tE
```

The manual defines `model_tags` as a JSON array containing the model type and any higher-order-effect tags.

The Stage 1 mapping used:

```text
model_tags = ["1S1L"]
```

for each of the 2,078 model-bearing solutions.

## Model vocabulary

Submission-facing model names must follow the official source-count / lens-count notation used by `microlens-submit`.

Current documented active model types include:

| `model_type` / primary tag | Meaning | Required core parameters |
|---|---|---|
| `1S1L` | 1 source, 1 lens | `t0`, `u0`, `tE` |
| `1S2L` | 1 source, 2 lenses | `t0`, `u0`, `tE`, `s`, `q`, `alpha` |
| `2S1L` | 2 sources, 1 lens | `t0`, `u0`, `tE`, second-source timing/impact parameters, flux ratio |
| `other` | custom model | model-specific |

Additional multiplicities may appear in the documentation with planned rather than active status. Their availability must be rechecked against the installed challenge version before use.

Important notation rule:

```text
scientific shorthand "2L1S"  -> submission tag "1S2L"
scientific shorthand "1L2S"  -> submission tag "2S1L"
```

Do not put reversed lens/source shorthand into submission-facing model fields.

## Higher-order effects

The official usage examples document higher-order tags including:

- `parallax`
- `finite-source`
- `lens-orbital-motion`
- `xallarap`
- `gaussian-process`
- `stellar-rotation`
- `fitted-limb-darkening`

Any future Stage 2 mapping must use the exact tag spelling supported by the installed package version.

## Validation semantics

The official tutorial directs users to validate at three levels:

```text
validate-solution <solution_id>
validate-event <event_id>
validate-submission
```

The installed `0.17.9` package was source-inspected during this project because inactive staging has a special consequence: event validation operates on active solutions. The project therefore validated each preserved inactive Solution object independently before activating the final set.

Final active-state validation completed with:

```text
solutions: 2078 / 2078 valid
solution validation messages: 0
event validation messages: 0
submission validation messages: 0
submission validation exception: none
```

This final active-state result is the relevant pre-export validation state.

## Active solutions and export

The official tutorial states that export packages active solutions. It also documents that an event with one active solution should have relative probability `1.0` or `None`, while multiple active solutions must satisfy the event probability-sum rules.

The recorded Stage 1 export contained one active 1S1L solution for each model-bearing event:

```text
active: 2078
inactive: 0
unique solution IDs: 2078
```

The one data-quality-only Stage 1 event did not have a model-bearing solution.

## Compute accounting

The official tutorial recommends recording CPU and wall time and dependency versions.

Recorded Stage 1 totals:

```text
wall time: 5920.372 s = 1.644548 h
user CPU: 5846.498 s
system CPU: 33.235 s
total measured CPU: 5879.733 s = 1.633259 CPU-h
reported CPU utilization: 99.31%
```

Per-event `runtime_seconds` is also preserved in the Stage 1 result table.

## Repository publication rule

The RMDC26 challenge ground rules require developed code to be documented and open source. This repository publishes the fitting code, synthetic tests, methods, compute record, submission controls, and provenance documentation while excluding protected/raw challenge data and the final submission ZIP.

## Nexus reference-directory rule

Organizer-provided notebooks in the Nexus reference directory are read-only and regularly replaced from their source repository. They are used as references, not as a durable project workspace. Project-owned code and evidence are versioned here instead.

## Final export record

The locally exported ZIP was audited after export:

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
```

Archive SHA-256:

```text
0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597
```

No external upload is claimed by this record.

## Future-export gate

Before any new higher-order export:

1. recheck current `microlens-submit` version and official docs;
2. recheck model names and required parameters;
3. verify exact higher-order tag spelling;
4. verify repo URL and hardware metadata;
5. validate each candidate solution;
6. validate each event's active solution set and probabilities;
7. validate the complete submission;
8. generate/review a dossier if useful;
9. lock the pre-export state;
10. export once and audit the archive independently.
