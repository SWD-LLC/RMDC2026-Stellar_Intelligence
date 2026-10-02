# RMDC26 Final Submission Record — October 2, 2026

**Project:** Stellar Intelligence  
**Challenge:** Roman Microlensing Data Challenge 2026 (RMDC26)  
**Challenge tier:** Experienced  
**Repository:** https://github.com/SWD-LLC/RMDC2026-Stellar_Intelligence

This file records the final audited artifact prepared and submitted through the RMDC26 alternative Box submission path on October 2, 2026. It supersedes older October 2 artifact references in this repository while preserving earlier Stage 1 and August records as historical provenance.

## Final submitted package identity

The corrected submission-facing artifact supersedes the earlier October 2 package:

```text
Stellar_Intelligence_RMDC26_Experienced_20261002_CORRECTED_1S3L.zip
SHA256 8e0568f457635bbdcdf304f46535bff5002540b85feda5bdf2c2763b2db18e04
SIZE   16537040 bytes
```

The earlier artifact is retained as historical provenance:

```text
Stellar_Intelligence_RMDC26_Experienced_20261002_FINAL.zip
SHA256 f9fdb62dbf9a75f7bd2a5f68e17a25c27f9d990a606c47c2d42a30e2388d41dd
```

The challenge ZIP itself is intentionally not committed to this public repository.

The corrected artifact was prepared for submission through the RMDC26 alternative Box file request on October 2, 2026. See `1S3L_CORRECTION_2026-10-02.md` for the exact correction record.

## Final exported state

```text
events: 2078
solutions: 2078
active_solutions: 2078
inactive_solutions: 0
zip_integrity: PASS
final_archive_audit: PASS
model_mix:
  1S1L: 2076
  1S3L: 1
  2S1L: 1
```

The two higher-complexity recovered solutions are:

- `RMDC26_002050`: `1S3L`
- `RMDC26_000249`: `2S1L`

`RMDC26_000435` remains a `1S1L` solution in the final archive.

## Notes and evaluator-facing documentation

RMDC26 organizer guidance states that written notes included through the submission object's Markdown note hooks are rendered into the evaluator dossier. The final workflow therefore treats the submission object's notes and requested metadata as the evaluator-facing record rather than relying on an external notebook or supplemental dossier.

The repository may contain broader engineering and provenance documentation, but those files are not represented as substitutes for the challenge submission notes.

## Validation and schema boundary

The original October 2 package completed the recorded submission validation/export workflow with `microlens-submit==0.17.9` and passed its archive audit.

Before the final corrected submission, the `RMDC26_002050` `1S3L` geometry was remapped from the fit-native fields `s_21/q_21/s_31/q_31/alpha/psi` into the pairwise fields defined by `microlens-submit/spec/parameter_spec.yaml`:

```text
s01/q01/alpha01
s02/q02/alpha02
s12/q12/alpha12
```

The fitted `t0`, `u0`, and `tE` values were preserved unchanged. Direct checking against the canonical YAML specification returned no missing required fields and no unknown `1S3L` fields:

```text
SPEC_CONFORMANT = True
```

The local generated validator was stale relative to the same checkout's canonical specification and did not include `1S3L` in its active `MODEL_DEFINITIONS`. The scientific parameters were therefore not altered to satisfy the stale generated validator. See `1S3L_CORRECTION_2026-10-02.md` for the full correction record.

Exporter warnings that set equal `relative_probability` values when likelihood information is absent are retained as toolkit warnings rather than represented as validation failures. Each event in the final export has one active solution.

Passing package validation establishes submission/package validity. It does not establish that every Experienced-tier event has received an exhaustive final astrophysical classification.

## Final packaging and hardware metadata

The final package was validated and exported on Roman Research Nexus in `RomanNexus-2026.2`.

Final embedded hardware metadata includes:

```text
cpu: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
cpu_details: 2 online CPUs: 0,1
memory_gb: 15
platform: Roman Nexus
nexus_image: RomanNexus-2026.2
repo_url: https://github.com/SWD-LLC/RMDC2026-Stellar_Intelligence.git
```

The historical Stage 1 execution record remains separate and is not rewritten by this final packaging record.

## Stage 1 accounting boundary

The production Stage 1 run processed 2,079 Experienced-tier targets:

- 2,078 produced model-bearing 1S1L solutions;
- `RMDC26_001563` was preserved as a data-quality-only Stage 1 record because no valid unsaturated Stage 1 photometry remained.

The final challenge archive contains 2,078 event records and 2,078 active solution records. The final higher-complexity recovery work changed the model type for two exported events without changing the Stage 1 target accounting.

## Scientific interpretation boundary

The final archive is not presented as an exhaustive higher-order solution of all Experienced-tier events. Most exported solutions remain Stage 1 `1S1L` baselines. The repository's scientific-scope and modeling-roadmap documents remain relevant when interpreting those solutions.

## Submission destination

The alternative RMDC26 submission was made through the organizer-provided Box file request. The submission-facing artifact is the Stellar Intelligence-named ZIP identified above.


## Authorship

**Author and project owner:** Sierra Warren  
**Organization:** Sierra Warren Developments, LLC
