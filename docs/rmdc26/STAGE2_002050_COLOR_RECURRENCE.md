# RMDC26_002050 — Color and Cross-Season Recurrence

This note records the achromaticity and recurrence diagnostic for the season following the primary event-season fit. It does not introduce a new astrophysical model and does not modify Stage 1 or the locked export.

## Evidence binding

- Local 1S2L refinement SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- Corrected Season 9 structure SHA-256: `d69a9652e868f96c5ff77ffd6f95c07ca467f1458435b9d0a74d1dcde7e35b29`
- Color/recurrence report SHA-256: `022c53e7a437dcdcf7f7b5c8be3478f61c9386a32323e7472e667fbecfe1c76b`

## Season 8 fitted source color

The event-season point-source close 1S2L fit yields source fluxes:

```text
F087   0.208010
F146  61.251068
F213 572.902655
```

Therefore the fitted source color ratio is:

```text
F213/F146 = 9.3533496081
```

## Season 9 variation color

Using half-day flux bins and subtracting each season-9 band baseline, F146 and F213 vary with:

```text
Pearson r                 0.9998451582
Spearman r                0.9995576210
slope through origin      9.3429077407
slope with intercept      9.3213314775
fractional scatter        0.0174633813
```

The ratio of the season-9 variation color to the season-8 fitted source color is `0.9988836227`, a fractional difference of only `0.0011163773` (~0.11%).

The three corrected broad season-9 episodes independently give F213/F146 variation ratios of approximately `9.14`, `9.46`, and `9.16`.

## Cross-season behavior

Seasons 0–7 are statistically quiet in F146/F213 (standardized RMS near unity) and do not show strong coherent F146/F213 recurrence. The event season (8) and following season (9) are the only high-amplitude, highly correlated seasons in this event's light curve under the current diagnostic.

The diagnostic gate returned:

```text
COLOR_DECISION: SEASON9_COLOR_COMPATIBLE_WITH_SEASON8_EVENT_SOURCE
RECURRENCE_DECISION: SEASON9_DOMINANT_COHERENT_STRUCTURE
```

## Interpretation boundary

The color match is strong evidence that the season-9 varying component has the same spectral scaling as the source flux inferred from the successful season-8 1S2L model. It is not, by itself, proof of a second lensing event or of a specific higher-order effect.

A useful next test is to determine whether season 9 can be represented as an additional non-negative magnification of that same source relative to a baseline estimated from quiet seasons, rather than from the season-9 mean. This avoids misreading the observed negative-positive-negative mean-subtracted pattern: a single broad positive magnification can appear negative at the season edges when the season mean includes the central excess.

Before invoking parallax, lens orbital motion, xallarap, intrinsic source variability, or a second lensing event, the next model-family gate should compare a same-source achromatic Paczynski-like transient against a flexible non-microlensing smooth model on season 9.

Stage 1 products and the locked submission export remain unchanged.