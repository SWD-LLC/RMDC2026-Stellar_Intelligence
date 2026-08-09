# RMDC26 Stage 1 Source-Integrity Attestation

This document closes the provenance question around the public Stage 1 fitter without rewriting the already-validated scientific workflow.

## Files compared

Validated Nexus/archive source:

```text
scripts/fit_rmdc26_1s1l_baseline_v022.py
size_bytes: 29435
sha256: ac8eed11ca16d9787d3042ecef2f42666359b90ac1075a8eca2d1f5f9150e64a
git_blob_sha1: 4264a9c8508c65f5392e4e2f9c4306316d4cefff
```

Public `main` source at the time of this attestation:

```text
scripts/fit_rmdc26_1s1l_baseline_v022.py
size_bytes: 29435
sha256: 917566cbd60acc366bcc082892a167651d5ce9a6b4b3e2685978a28d273665f6
git_blob_sha1: 6091774d0d6b4bd8d3e42e2f003c0ec4cb8d7628
```

## Exact difference

The two files are not byte-identical. The difference is whitespace only and consists of moving one blank line across two adjacent function boundaries:

1. the archived source has one additional blank line between `objective()` and `centered_objective()`;
2. the public source has one additional blank line between `centered_objective()` and `max_consecutive_threshold()`.

Removing the first extra blank line and adding the second to the archived bytes reproduces the public Git blob SHA exactly:

```text
6091774d0d6b4bd8d3e42e2f003c0ec4cb8d7628
```

No executable statement, literal, identifier, parameter, threshold, algorithm, import, return value, or control-flow element differs.

## AST equivalence

Both files were parsed with Python `ast.parse()` and normalized with:

```python
ast.dump(tree, include_attributes=False)
```

The normalized AST SHA-256 is identical for both sources:

```text
0272069719865c4745c265e6ba7981fbd417d6c4d67f3a17aa5061a4cb4684b7
```

Therefore the public Stage 1 fitter is **semantically identical** to the archived validated source despite the two whitespace-placement differences.

## Provenance conclusion

Status:

```text
BYTE_IDENTITY: NO
SEMANTIC_IDENTITY: PASS
AST_IDENTITY: PASS
SCIENTIFIC_LOGIC_CHANGED: NO
VALIDATED_STAGE1_OUTPUTS_REGENERATED: NO
SUBMISSION_ZIP_REGENERATED: NO
```

The validated Stage 1 output and verified submission archive remain immutable. This attestation records the exact discrepancy rather than silently rewriting history to force a matching byte hash.
