# RMDC26_002050 — Finite-Source Necessity Screen

This note records the finite-source necessity screen for the current event-season point-source 1S2L solution. It is a model-complexity gate, not a final physical classification.

## Bound solution

Event: `RMDC26_002050`

Current event-season point-source 1S2L solution:

```text
s = 0.2182345358679645
q = 0.2582835206857784
alpha_deg = 68.96961512110634
t0 = 2462938.997642504
u0 = 0.25250741716172986
tE = 17.94720009730105 d
chi2 = 8521.260530246143
```

The prior model-family gate preferred 1S2L over the tested 2S1L competitor by `ΔBIC = +263.12046879029367` in the 1S2L direction.

## Caustic geometry

The closest approach of the fitted source trajectory to the sampled close-binary caustic is:

```text
minimum observed distance = 0.23510233381419782 theta_E
minimum dense distance    = 0.23510229829420293 theta_E
closest dense epoch       = 2462938.877642504
closest epoch - t0        = -0.12000000011175871 d
```

The trajectory is therefore not close to a caustic on the scale explored by the finite-source grid.

## Fixed-geometry rho scan

The point-source solution reproduced exactly before the scan.

```text
point-source chi2 = 8521.260530246143
```

The tested source-radius grid was:

```text
1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1
```

Results were effectively identical to the point-source fit through `rho=3e-3`. The best tested finite-source value was:

```text
rho = 0.01
t_star = 0.1794720009730105 d
chi2 = 8519.442857706568
Delta chi2 vs point source = +1.8176725395751419
rho / minimum caustic distance = 0.04253467563930904
```

Larger radii worsened the fit strongly:

```text
rho=0.03  Delta chi2 = -44.85084329450001
rho=0.10  Delta chi2 = -6846.558359870276
```

## Gate decision

```text
FINITE_SOURCE_GATE = FINITE_SOURCE_NOT_REQUIRED_AT_FIXED_GEOMETRY
```

The fixed-geometry scan does not justify adding `rho` to the current model. The small `Delta chi2` gain at `rho=0.01` is far below the engineering promotion threshold used for a full joint finite-source refit.

This does not prove `rho=0`; it means the current data and geometry do not provide sufficient evidence to spend model complexity on a finite-source parameter at this stage.

## Next scientific task

The current provisional event-season winner remains a static point-source close 1S2L model. Before any submission-facing replacement is considered, the severe later-season residual structure must be diagnosed independently. In particular, the next step should determine whether the following observing season is explained by per-season photometric offsets/systematics, a second coherent transient, or a higher-order model family requiring separate treatment.

## Provenance and immutability

Finite-source necessity report SHA-256:

`5fb226900cda5bd7bcb106e49de01a787b4369c90ac1774fd0d761e430e34231`

Protected Stage 1 outputs and the verified Stage 1 submission ZIP remained unchanged. No submission mutation or export occurred during this screen.
