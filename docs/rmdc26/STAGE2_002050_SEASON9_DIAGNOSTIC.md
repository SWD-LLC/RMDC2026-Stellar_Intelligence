# RMDC26_002050 — Following-Season Diagnostic

This note records the read-only diagnostic of the observing season immediately following the event season for `RMDC26_002050`. It does not introduce a new astrophysical model and does not modify the locked Stage 1 submission state.

## Evidence chain

- Local 1S2L refinement SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- 2S1L model-family competition SHA-256: `04ed59dfca5a4a34b08bc1fa6d9ca5978c2e59aa14212eae7d7157e860e63aa2`
- Finite-source necessity SHA-256: `5fb226900cda5bd7bcb106e49de01a787b4369c90ac1774fd0d761e430e34231`
- Following-season diagnostic SHA-256: `9f4aa4f6c57f448349e7e98d5b8e1dc6265d45e866bca2b1d5bb8059642ddd8a`

## Season 9 accounting

Season 9 spans BJD `2463093.755269539`–`2463164.49811815` (`70.74285` d) with `8182` valid points in F087, F146, and F213.

```text
constant chi2             9,216,932.3436
linear chi2               9,178,485.1031
linear improvement          38,447.2405
fixed event 1S1L chi2     9,059,240.5006
fixed event 1S2L chi2     9,035,927.4670
1S2L vs fixed 1S1L        +23,313.0336 chi2
```

A per-band linear baseline changes the total chi-square by only about `0.417%`, so a simple monotonic baseline trend is not an adequate explanation for the season.

## Band structure

F087 is statistically quiet at the available sparse cadence (`240` points, chi2 `250.76`, RMS `1.02`). In contrast, F146 and F213 contain very large structured residuals:

```text
F146: 7701 points, constant-model RMS 33.56, max |residual| 63.66
F213:  241 points, constant-model RMS 47.45, max |residual| 86.69
```

The strongest 5-day windows in F146 and F213 are temporally aligned to within `0.1349 d`, centered near BJD `2463128.755`. This establishes coherent multi-band structure in at least one portion of the season, but that window explains only about `21.9%` of the season's total excess chi-square.

## Interpretation boundary

The current static season-8 1S2L geometry has only a `1.96%` fractional effect relative to the season-9 constant model. The season is therefore not adequately described by simply extending the previously fitted event geometry.

The diagnostic gate returned:

```text
DIAGNOSTIC_DECISION: DISTRIBUTED_LATER_SEASON_STRUCTURE
```

This label is diagnostic, not astrophysical. It means the later season contains broad and/or multiple structures rather than one dominant isolated five-day excursion under the current metrics.

The observed combination is important:

1. F146/F213 share a strongly aligned high-excess interval;
2. F087 is near the noise floor at its sparse sampling;
3. the strongest five-day interval accounts for only a minority of the full-season excess;
4. a linear baseline trend explains very little;
5. the season-8 static 1S2L geometry explains only a small fraction of the season-9 structure.

Therefore no parallax, lens orbital motion, second transient, source variability, or simulator/systematics interpretation is asserted yet. The next gate should decompose season 9 into multiple non-overlapping temporal structures and test their cross-band coherence before fitting another physical model.

## Locked boundary

The Stage 1 Parquet/CSV/manifest and verified export ZIP remained byte-identical after the diagnostic. No submission or export state changed.