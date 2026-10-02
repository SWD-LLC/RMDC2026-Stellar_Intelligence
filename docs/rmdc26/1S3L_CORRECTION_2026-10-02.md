# RMDC26 1S3L Correction Record — October 2, 2026

**Author:** Sierra Warren  
**Project:** Stellar Intelligence  
**Challenge:** Roman Microlensing Data Challenge 2026 (RMDC26)  
**Tier:** Experienced  
**Event:** `RMDC26_002050`

This record documents the final correction applied to the active `1S3L` solution for `RMDC26_002050` before submission through the organizer-provided alternative Box file request.

## Corrected submitted artifact

```text
Stellar_Intelligence_RMDC26_Experienced_20261002_CORRECTED_1S3L.zip
SHA256 8e0568f457635bbdcdf304f46535bff5002540b85feda5bdf2c2763b2db18e04
SIZE   16537040 bytes
```

The challenge ZIP itself is intentionally not committed to this public repository.

## 1S3L mapping correction

The fitted trajectory core was preserved exactly:

```text
t0 = 2462937.4494308094
u0 = 0.1740851251464745
tE = 24.9891751751578
```

The fit-native triple-lens geometry

```text
s_21
q_21
s_31
q_31
alpha
psi
```

was remapped into the pairwise `1S3L` fields defined in `microlens-submit/spec/parameter_spec.yaml`:

```text
s01      = 0.12301369727721631
q01      = 0.32016267221703165
alpha01  = 1.204586116633564

s02      = 7.699994419344329
q02      = 1.266453926332858
alpha02  = -3.099209493544448

s12      = 7.749692324409099
q12      = 3.9556576585366425
alpha12  = -3.0846422987749182
```

The remapped representation passed the direct canonical-spec check:

```text
MISSING_REQUIRED = []
UNKNOWN_TO_1S3L_SPEC = []
SPEC_CONFORMANT = True
```

## Validator/specification boundary

The local generated validator in the working environment did not include `1S3L` in its active `MODEL_DEFINITIONS`, while the same checkout's `parameter_spec.yaml` defined `1S3L`, its required `t0/u0/tE` core, and the pairwise optional fields used above.

The scientific parameters were not altered to satisfy that stale generated validator. The corrected representation was checked directly against the canonical YAML specification instead.

## Provenance

The pre-remap solution and earlier submission artifact are retained as historical provenance. This correction record supersedes the earlier statement that the native `1S3L` geometry field names were intentionally left unmapped.

**Project owner and author:** Sierra Warren  
**Organization:** Sierra Warren Developments, LLC
