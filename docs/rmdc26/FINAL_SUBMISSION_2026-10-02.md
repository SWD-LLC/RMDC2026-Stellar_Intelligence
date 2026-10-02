# RMDC26 Final Submission Record — October 2, 2026

**Project:** Stellar Intelligence  
**Team name:** Sierra Warren RMDC26  
**Project owner:** Sierra Warren  
**Organization:** Sierra Warren Developments, LLC  
**Challenge tier:** Experienced

This file records the final validated RMDC26 challenge artifact prepared on October 2, 2026. It supersedes older repository references when identifying the final October 2 export, while preserving the earlier Stage 1 and August export records as historical provenance.

## Final package identity

```text
archive: RMDC26_Sierra_Warren_Experienced_20261002.zip
size_bytes: 2600175
zip_members: 6235
sha256: 6f509d13444cc723622db27e04ce729da7f63dfe4d1c2bee33ae2e940427140e
```

The final ZIP is intentionally not committed to this public repository.

## Final submission state

```text
events: 2078
solution_jsons: 2078
solution_notes: 2078
active_solutions: 2078
inactive_solutions: 0
malformed_solution_jsons: 0
zip_integrity: PASS
submission_validation_issues: 0
official_validate_submission: ALL VALIDATIONS PASSED
```

Every active solution in the final archive is a `1S1L` Stage 1 baseline solution.

## Notes and dossier

The final project contained one non-empty Markdown note for every active solution:

```text
active_solutions: 2078
nonempty_notes: 2078
missing_note_files: 0
empty_note_files: 0
```

A comprehensive dossier was generated successfully before final export. The dossier is a human-review artifact and is not part of the exported challenge ZIP.

## Final packaging and validation environment

The final package was validated and exported on Roman Research Nexus with `microlens-submit==0.17.9`.

Embedded `submission.json` metadata in the frozen final ZIP:

```json
{
  "team_name": "Sierra Warren RMDC26",
  "tier": "experienced",
  "hardware_info": {
    "cpu_details": "2 online CPUs: 0,1",
    "memory_gb": 15.0,
    "platform": "Roman Nexus",
    "nexus_image": "RomanNexus-2026.2"
  },
  "repo_url": "https://github.com/SWD-LLC/RMDC2026-Stellar_Intelligence.git",
  "git_dir": null
}
```

The archived `submission.json` contains no separate `cpu` model field. Although a CPU model was observed during Nexus environment inspection, it is not claimed here as embedded final-submission metadata.

This is distinct from the historical Stage 1 production environment recorded elsewhere in the repository. The Stage 1 run remains documented as `RomanNexus-2026.1`; the final October 2 packaging and validation environment was `RomanNexus-2026.2`. The historical execution record is not rewritten.

## Stage 1 accounting boundary

The production Stage 1 run processed 2,079 Experienced-tier targets:

- 2,078 produced model-bearing 1S1L solutions;
- `RMDC26_001563` was documented as a data-quality-only Stage 1 record because no valid unsaturated Stage 1 photometry remained.

The final October 2 challenge archive contains 2,078 event records and 2,078 active solution records. This final package record does not alter the earlier 2,079-target Stage 1 accounting.

## Scientific interpretation boundary

Passing `microlens-submit` validation establishes package/schema validity. It does not establish that a 1S1L baseline is the most appropriate physical model for every Experienced-tier event.

The repository's existing `SCIENTIFIC_SCOPE.md` and `MODELING_ROADMAP.md` remain authoritative for the Stage 1 scientific limitation and higher-order modeling boundary.

## Submission destination

The RMDC26 Slack `Helpful Links` resource identifies the challenge submission destination as:

https://lsu.app.box.com/f/9c12c0e9d1c74bbc82f89bf9ebdf9f17

External challenge upload is not claimed by this record until an upload confirmation is preserved.
