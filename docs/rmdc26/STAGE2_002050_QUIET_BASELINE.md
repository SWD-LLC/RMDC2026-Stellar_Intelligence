# RMDC26_002050 — Quiet-Baseline Magnification Viability

This note records the quiet-season baseline reconstruction and same-source magnification-viability gate for the season following the primary event-season fit. It does not introduce a new astrophysical model and does not modify Stage 1 or the locked export.

## Evidence binding

- Color/recurrence report SHA-256: `022c53e7a437dcdcf7f7b5c8be3478f61c9386a32323e7472e667fbecfe1c76b`
- Corrected Season 9 structure SHA-256: `d69a9652e868f96c5ff77ffd6f95c07ca467f1458435b9d0a74d1dcde7e35b29`
- Local 1S2L refinement SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- Quiet-baseline report SHA-256: `119c05fd3c08d4b5f5b5ec717fa6a4917abc25cdc52bb14b109cf4f9e5649027`

## Quiet baseline

The high-cadence quiet seasons selected by the diagnostic are `0, 1, 2, 7`.

Adopted robust quiet baselines:

```text
F087   0.227312 uJy
F146  62.400176 uJy
F213 647.285921 uJy
```

The corresponding event-season 1S2L source fluxes are:

```text
F087   0.208010 uJy
F146  61.251068 uJy
F213 572.902655 uJy
```

## Season 9 magnification proxy

Using `A_proxy = 1 + (F - F_quiet)/F_source`, F146 and F213 remain above unity across all half-day bins under the 3-sigma gate:

```text
F146: min A_proxy = 1.047628, max A_proxy = 1.579352, fraction below A=1 at 3σ = 0
F213: min A_proxy = 1.045411, max A_proxy = 1.580310, fraction below A=1 at 3σ = 0
```

F087 is too weakly constrained to be useful for the same gate because its fitted source flux is very small relative to the photometric uncertainty; its extreme proxy range is therefore not used to reject the F146/F213 result.

The three broad corrected Season 9 episodes are all positive relative to the quiet baseline in F146 and F213, with matched magnification proxies:

```text
episode 1: A_proxy ~1.0674 (F146), ~1.0676 (F213)
episode 2: A_proxy ~1.5305 (F146), ~1.5301 (F213)
episode 3: A_proxy ~1.0697 (F146), ~1.0695 (F213)
```

## Gate

The diagnostic returned:

```text
QUIET_BASELINE_DECISION: SAME_SOURCE_NONNEGATIVE_MAGNIFICATION_PLAUSIBLE
```

This means the apparent negative-positive-negative Season 9 pattern seen after subtracting the Season 9 mean is compatible with one positive same-source magnification structure when the unlensed level is anchored to independent quiet seasons.

It does **not** yet establish a second microlensing event or identify the responsible lens. The next model-family test should compare a same-source achromatic PSPL/Paczynski-like transient against a non-microlensing smooth transient using the same quiet baselines and source color.

## Locked boundary

No new astrophysical model was fit in this gate. Stage 1 products and the verified export ZIP remained byte-identical. No submission or export state changed.