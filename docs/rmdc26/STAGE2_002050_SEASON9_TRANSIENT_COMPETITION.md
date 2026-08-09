# RMDC26_002050 — Season 9 Transient Model Competition

This note records the same-source Season 9 transient model-family competition. It does not modify Stage 1 or the locked export.

## Evidence binding

- Quiet-baseline viability SHA-256: `119c05fd3c08d4b5f5b5ec717fa6a4917abc25cdc52bb14b109cf4f9e5649027`
- Local 1S2L refinement SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- Season 9 transient-competition report SHA-256: `ed93423cc1205b8158ff1ce4825c14ba6a515a150d821e3ac55d7ae88c01f04f`

## Result

The primary comparison used 7,942 F146/F213 points with the quiet-season baseline and the Season-8 fitted source flux held as the shared achromatic scaling.

```text
quiet-baseline null chi2         27,778,589.4108
same-source PSPL chi2                 8,650.8422
Gaussian chi2                        223,561.5648
asymmetric Gaussian chi2             223,488.9147
PSPL chi2 / dof                            1.08966
```

The best smooth competitor was the asymmetric Gaussian. Its BIC exceeds the PSPL BIC by `214,847.0524`.

Best Season-9 PSPL parameters:

```text
t0 = 2463128.379373279
u0 = 0.765321396220055
tE = 17.676525361186524 d
Amax = 1.577732935155485
```

Per-band residual quality for the PSPL is near the noise floor:

```text
F087 RMS 1.0176
F146 RMS 1.0405
F213 RMS 1.1410
```

The engineering gate returned:

```text
TRANSIENT_MODEL_DECISION: PROMOTE_SECOND_PSPL_LIKE_TRANSIENT
```

## Interpretation boundary

This establishes that Season 9 is extraordinarily well represented by an achromatic Paczynski-like transient acting on the same source flux identified in Season 8. It does not yet establish that the Season-9 lens is a physically separate foreground object or that the complete event should be classified as two independent microlensing events.

The timing and timescale are notable: the Season-9 peak occurs about `189.38 d` after the Season-8 close-1S2L peak, and the fitted timescales are nearly equal (`17.68 d` versus `17.95 d`). This makes a hierarchical wide third-lens / repeating-microlensing interpretation a high-priority hypothesis, but a full triple-lens calculation has not yet been executed.

MulensModel's production magnification machinery used here supports point and binary lenses; therefore an exact 1S3L fit requires a separate validated triple-lens backend or an explicitly documented approximation. The next gate should first test a wide-separation composite (close 1S2L + tertiary PSPL) with one shared source and shared band fluxes over Seasons 8+9, while retaining the distinction between that approximation and an exact 1S3L solution.

Stage 1 products and the verified export ZIP remained byte-identical. No submission or export state changed.