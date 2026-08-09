# RMDC26_002050 — Signed Δχ² Localization

This note records the signed residual-localization follow-up for the first real Stage 2 point-source 1S2L pilot. It is an engineering/scientific screening result, not a final astrophysical classification.

## Bound pilot

- Event: `RMDC26_002050`
- Pilot report SHA-256: `7fc2ff76071fae780947501a71f172f757111429beabd83715909114cc276f4f`
- Signed-localization report SHA-256: `46f36c7dd290e1fb7ee41e1f052d02f35930deb9156507763d321dcddf5d515e`
- Point-source 1S2L topology from pilot: `close`
- Pilot parameters: `s=0.36141352452960657`, `q=0.03432673400925643`, `alpha_deg=75.43518533181198`, `t0=2462939.0129455496`, `u0=0.30676625190204293`, `tE=15.411904053229344`

## Signed global accounting

```text
net Δχ²                    +6795.568679433338
positive contributions     +48591.73392726974
negative contributions     -41796.16524783641
positive/net ratio         7.150502955599834
```

The global improvement is therefore strongly cancelling: substantial regions improve while others degrade. This prevents interpreting the global Δχ² in isolation.

## Localization around the binary-event epoch

The improvement is strongly concentrated around the fitted binary event epoch despite the long-baseline cancellation:

```text
± 2 d:   Δχ² =  2431.527311
± 5 d:   Δχ² =  5907.791205   (0.8694 × global net)
±10 d:   Δχ² =  7604.424402   (1.1190 × global net)
±20 d:   Δχ² = 13018.338206   (1.9157 × global net)
```

Outside ±20 d the binary solution loses `6222.769526` χ², explaining much of the cancellation.

## Band-local event behavior

Within ±5 d:

```text
F146: Δχ² = +5576.674391
F213: Δχ² =  +331.172993
F087: Δχ² =    -0.056179
```

Within ±10 d:

```text
F146: Δχ² = +7167.319697
F213: Δχ² =  +437.191792
F087: Δχ² =    -0.087087
```

The independent F213 improvement supports a multi-band event-local signal. F087 is effectively neutral at the available cadence/count and does not drive the binary preference.

## Peak-region residual behavior

Within ±5 d the point-source binary model reduces the RMS standardized residual from approximately `2.47 → 1.04` in F146 and `3.39 → 1.43` in F213. Within ±2 d the reductions are `2.49 → 1.00` and `3.00 → 1.10`, respectively.

This is a substantial local improvement and is much more diagnostically useful than the full-baseline reduced χ², which is dominated by later-season residual structure.

## Observing-season decomposition

The observing season containing the fitted binary `t0` contributes:

```text
Δχ² = +7868.317180
```

The following season contributes:

```text
Δχ² = -35457.184667
```

The latter season dominates the global cancellation and also contains extremely large absolute χ² in both models. It is therefore treated as a separate long-baseline/systematics or additional-model-family diagnostic rather than evidence against the event-local binary structure by itself.

## Promotion decision

The signed-localization engineering gate returned:

```text
WINDOW_20D_FRACTION_OF_NET: 1.9157099015419752
EVENT_SEASON_FRACTION_OF_NET: 1.1578600042366183
ENGINEERING_DECISION: PROMOTE_TO_LOCAL_BINARY_REFINEMENT
```

This promotes `RMDC26_002050` to a higher-resolution local binary-lens refinement stage.

## Scientific boundary

This result does **not** establish a final physical classification. The next stage must:

1. refine close/resonant/wide point-source minima on the event-local data;
2. preserve multiple degeneracies rather than only the current close minimum;
3. compare local and event-season likelihoods/BIC against the Stage 1 baseline;
4. only then test finite-source `rho`/VBBL where warranted by residual morphology or caustic proximity;
5. separately diagnose the severe later-season residual structure before any submission-facing replacement is considered.

Stage 1 products and the previously verified submission archive remain unchanged.