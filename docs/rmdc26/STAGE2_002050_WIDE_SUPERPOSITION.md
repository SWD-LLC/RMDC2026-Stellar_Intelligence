# RMDC26_002050 — Wide-Superposition Feasibility

This note records the full-light-curve feasibility test for a hierarchical wide third-lens interpretation. The executed model is an approximation,

```text
A_total = A_close_1S2L + A_tertiary_1S1L - 1
```

and is **not** an exact 1S3L magnification calculation.

## Evidence binding

- Local close-1S2L refinement SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- Quiet-baseline viability SHA-256: `119c05fd3c08d4b5f5b5ec717fa6a4917abc25cdc52bb14b109cf4f9e5649027`
- Season-9 transient competition SHA-256: `ed93423cc1205b8158ff1ce4825c14ba6a515a150d821e3ac55d7ae88c01f04f`
- Wide-superposition feasibility report SHA-256: `8ef302661b29babc7115e3f7b0dc5d81f353ae36159f3433831bae24ff9c525a`

## Global result

The test used all `49,488` prepared data points in F087/F146/F213. The close 1S2L geometry was held fixed at the validated Season-8 solution while the tertiary PSPL parameters were optimized globally with one shared source-color template and one baseline per band.

```text
chi2 null                 184,779,952.7604
chi2 close only            24,857,073.5118
chi2 tertiary only        168,221,766.7242
chi2 wide composite            51,078.8003
composite chi2/dof                  1.03242
```

The composite is favored over the close-only approximation by `ΔBIC = 24,805,962.28` and over the tertiary-only model by `ΔBIC = 168,170,623.07`.

The fitted global source-template scale is `1.001079`, leaving the effective source fluxes essentially unchanged from the independently inferred Season-8 source template.

## Residual quality

Every observing season is near the expected noise floor. Season RMS values range from approximately `0.937` to `1.095`; the maximum is `1.09513`. The two event-bearing seasons are:

```text
Season 8 RMS = 1.03909
Season 9 RMS = 1.03977
```

Global per-band residual RMS:

```text
F087 = 0.98158
F146 = 1.01684
F213 = 1.02198
```

This means the same composite approximation simultaneously explains the two distinct magnification episodes while preserving noise-like residuals in the quiet seasons.

## Wide-component parameters and geometry proxies

The globally refit tertiary PSPL is:

```text
t0 = 2463128.381712115
u0 = 0.7658093691
tE = 17.6638512520 d
```

Relative to the fixed close 1S2L solution:

```text
Δt = 189.3840696 d
tE_tertiary / tE_close = 0.9842121
(tE ratio)^2 = 0.9686734
longitudinal trajectory offset = 10.55229 close-pair Einstein radii
wide-separation proxy = 10.56419 or 10.60016 close-pair Einstein radii
```

The `(tE ratio)^2` quantity is only a mass-ratio proxy under the additional assumption that the wide component and close pair share lens distance and relative proper motion. It is not yet a measured physical mass ratio.

## Gate

The engineering/scientific gate returned:

```text
DECISION: PROMOTE_HIERARCHICAL_WIDE_THIRD_LENS_CANDIDATE
```

This is strong evidence that the full light curve is consistent with a repeating same-source microlensing configuration in which a close binary lens is accompanied by a much wider lensing component. It is not yet a final 1S3L classification because the calculation superposes binary- and single-lens excess magnifications rather than evaluating the exact three-lens equation.

The next step is an exact triple-lens backend preflight and a seeded exact 1S3L fit centered on this validated wide-limit solution. No parallax, orbital motion, xallarap, Stage-1 mutation, or submission mutation has been performed here.

## Locked boundary

Stage-1 Parquet/CSV/manifest and the verified export ZIP remained byte-identical. No submission or export state changed.