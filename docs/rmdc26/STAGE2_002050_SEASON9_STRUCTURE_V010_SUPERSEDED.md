# RMDC26_002050 — Season 9 Structure v0.1.0 Superseded

The first Season 9 structure-decomposition run completed mechanically (`STRUCTURE_RC=0`) but contains a coordinate-origin bug in the reporting of selected non-overlapping windows.

## Valid outputs from v0.1.0

The following quantities are unaffected by the bug and remain valid:

- `N_COMMON_BINS = 139`
- Pearson correlation F146/F213: `0.9997721485225378`
- Spearman correlation F146/F213: `0.9995844318334152`
- same-sign fraction: `0.9928057553956835`
- high-excess same-sign fraction: `1.0`
- total F146+F213 excess chi-square: `9208740.501016585`
- top-three selected 5-day windows account for `0.5308817981354176` of the F146+F213 excess

These values are computed from common bin identifiers and excess statistics and do not depend on the faulty absolute-time reconstruction.

## Invalid / incomplete outputs

`select_nonoverlapping_windows()` reconstructed `t_start`, `t_stop`, and `t_center` as `bin_id * BIN_DAYS` without restoring the absolute BJD origin used by `make_bins()`.

Consequences:

1. reported window times such as `START=32.5` are relative offsets, not BJD;
2. `WINDOW × BAND STRUCTURE` was empty because relative window times were compared against absolute BJD bin centers;
3. F087 coverage was falsely reported as zero for every selected window;
4. the label `MULTIPLE_COHERENT_TEMPORAL_STRUCTURES` is not yet accepted as a scientific/engineering gate because the three highest windows are adjacent and may represent one broader episode rather than three distinct structures.

## Required correction

A v0.1.1 rerun must preserve the absolute bin origin, recover per-band window summaries, recover F087 coverage, and merge touching/adjacent 5-day windows into broader temporal episodes before deciding whether Season 9 contains multiple distinct coherent structures.

The v0.1.0 evidence directory is retained for forensic provenance and is not deleted. Stage 1 products and the locked submission export were unchanged.