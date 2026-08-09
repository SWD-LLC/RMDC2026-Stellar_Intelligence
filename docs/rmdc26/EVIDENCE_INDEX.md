# RMDC26 Evidence Index

This index maps the public repository record to the locked Nexus evidence chain. Raw challenge data, generated staging trees, and the final submission ZIP are intentionally not committed here.

## Stage 1 production

| Evidence | Status / anchor |
|---|---|
| Stage 1 pipeline | `scripts/fit_rmdc26_1s1l_baseline_v022.py` |
| Pipeline version | `0.2.2` |
| Full run ID | `rmdc26_stage1_v022_full_20260804T230001Z` |
| Events processed | `2079` |
| Model-bearing results | `2078` |
| Stage 1 failures | `0` |
| `1S1L_candidate` | `1148` |
| `anomalous_route` | `930` |
| `data_quality_route` | `1` |
| DQ-only event | `RMDC26_001563` |
| Verified Stage 1 evidence ZIP SHA-256 | `6b4cd9483f8d3c28d28917615d1ecb0edd0fcda00623ee4dbc3c9b088a2aa1ae` |
| Archived validated fitter SHA-256 | `ac8eed11ca16d9787d3042ecef2f42666359b90ac1075a8eca2d1f5f9150e64a` |

## Public source integrity

| Evidence | Anchor |
|---|---|
| Public fitter Git blob SHA-1 at attestation | `6091774d0d6b4bd8d3e42e2f003c0ec4cb8d7628` |
| Public fitter SHA-256 | `917566cbd60acc366bcc082892a167651d5ce9a6b4b3e2685978a28d273665f6` |
| Archived fitter Git blob SHA-1 | `4264a9c8508c65f5392e4e2f9c4306316d4cefff` |
| Exact discrepancy | `two blank-line placement differences only` |
| Semantic identity | `PASS` |
| Public-source CI byte lock | `PASS gate at 917566cbd60...` |
| Byte identity with archive | `NO` |

See `SOURCE_INTEGRITY.md` for the exact discrepancy and source-lock contract.

## Submission-tool qualification

The submission workflow was qualified against `microlens-submit==0.17.9` before full real-data execution.

Evidence classes preserved on Nexus include:

- CLI contract probe;
- persistence/import behavior probe;
- importer source inspection;
- supported deactivation lifecycle probe;
- `t0` time-standard audit;
- organizer-resolution record;
- ten-event real-data canary;
- full staging preflight;
- execution reauthorization.

The public repository documents these controls without publishing raw challenge-event submission trees.

## Full staging import

| Evidence | Status |
|---|---|
| Imported solutions | `2078 / 2078` |
| Import return code | `0` |
| Original serial deactivation | `48` completed before retirement |
| Accelerated recovery deactivation | `2030` |
| Final inactive after recovery | `2078` |
| Final active after recovery | `0` |
| Duplicate solution IDs | `0` |
| Unreadable solutions | `0` |
| Stage 1 artifacts unchanged | `YES` |
| Parameters preserved | `YES` |
| Solution IDs preserved | `YES` |

The serial per-solution deactivation implementation was retired for performance after source inspection established that it repeatedly loaded and saved the complete submission state. Recovery used one package load, in-memory lifecycle transitions, and one save while preserving solution semantics.

## Validation chain

### Solution validation

```text
validated: 2078
exceptions: 0
solutions with messages: 0
total validation messages: 0
project mutation: none
Stage 1 mutation: none
```

### Event validation while deliberately inactive

```text
events validated: 2078
expected no-active-solution notices: 2078
unexpected event messages: 0
event exceptions: 0
```

### Submission validation before hardware remediation

```text
submission messages: 2079
expected inactive-state messages: 2078
hardware warning: 1
other unexpected messages: 0
```

### Hardware remediation

```text
status: PASS
hardware present: true
hardware validation messages: 0
submission messages: 2078
expected inactive-state messages: 2078
unexpected messages: 0
solution semantics unchanged: true
Stage 1 unchanged: true
```

## Locked staging state

Validated inactive staging manifest:

```text
status: PASS_VALIDATED_INACTIVE_STAGING
manifest SHA-256:
debde39c12331a04b504778860b2275098c6366649d41c359d76d7a1abb4f0d9
```

Controlled activation report:

```text
status: PASS_ACTIVE_VALIDATED_NO_EXPORT
report SHA-256:
84c278318f73e85806c8838b94917244b8bf6f5ddbbd086e85d691678af6404e
```

Active validated solution-tree SHA-256:

```text
97bbfaff5ee0b42cb13b2b4a67a3a309088cf8de6b52814c693b3e588b382434
```

Active validated state manifest SHA-256:

```text
dd404b9832d8e77b7c7325c773fcd72ef82b851bc32251f090f146d838c412b9
```

Final active-state validation:

```text
active: 2078
inactive: 0
solution validation messages: 0
solution validation exceptions: 0
event validation messages: 0
event validation exceptions: 0
submission validation messages: 0
submission validation exception: None
```

## Controlled export

Verified local submission ZIP:

```text
RMDC26_Experienced_Stellar_Intelligence_20260809T002925Z.zip
SHA-256:
0bb982805fe62eded6d43dd99252c02e853733356c49a8637573a7b577740597
size_bytes: 2600508
```

Controlled export report SHA-256:

```text
259e6d374c409f10734ac9d9aeec5783251110926ff00d5cd799e85d62e61248
```

Archive audit:

```text
ZIP members: 6235
corrupt member: none
unsafe paths: 0
event JSONs: 2078
solution JSONs: 2078
unique solution IDs: 2078
active exported solutions: 2078
inactive exported solutions: 0
unknown active state: 0
unreadable exported solutions: 0
submission.json members: 1
hardware metadata: present
exported IDs exactly match live project: true
live project unchanged after export: true
Stage 1 unchanged after export: true
```

## Scope boundaries

The evidence chain distinguishes three separate claims:

1. **Stage 1 computational validity** — the 1S1L baseline fit/routing pipeline completed and its outputs are locked;
2. **submission-package validity** — the 2078-solution active package passed the controlled validation/export chain;
3. **scientific completeness** — not claimed for the 930 anomalous events, which remain candidates for higher-order modeling.

No challenge-data Parquet, generated event submission tree, or final challenge ZIP should be committed to this repository.
