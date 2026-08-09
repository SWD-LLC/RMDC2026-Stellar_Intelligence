# RMDC26_002050 — Stage 2 Point-Source 1S2L Pilot

Status: **strong binary-lens screening signal; not a final astrophysical classification**.

This record captures the first real Stage 2 higher-order execution after the deterministic 16-event canary selection and model-backend preflight. The pilot used the `strongest_chi2` canary event `RMDC26_002050` and compared the locked Stage 1 1S1L/PSPL baseline against a point-source 1S2L search with MulensModel.

## Input / execution state

- Event: `RMDC26_002050`
- Canary stratum: `strongest_chi2`
- Valid photometric rows: `49,488`
- Fit-screen subset: `1,200`
- MulensModel backend smoke test: `PASS`
- Close coarse models: `324` valid
- Resonant coarse models: `324` valid
- Wide coarse models: `324` valid
- Local refinements retained: `6`
- Stage 1 protected artifacts changed: `NO`
- Submission state changed: `NO`
- Submission exported/regenerated: `NO`

## Baseline reproducibility

The Stage 1 stored chi-square reproduced exactly on the full photometric data:

```text
Stage 1 stored chi2:     24663650.52746036
Stage 1 recomputed chi2: 24663650.52746036
relative difference:     0.0
```

This exact equality is an important control: the Stage 2 comparison is being made against the same Stage 1 photometric baseline rather than against a re-fitted or altered reference model.

## Best point-source 1S2L screen

```text
topology: close
s:        0.36141352452960657
q:        0.03432673400925643
alpha:    75.43518533181198 deg
alpha:    1.3165923558922503 rad (submission-facing conversion)
t0:       2462939.0129455496
u0:       0.30676625190204293
tE:       15.411904053229344 d
```

Model comparison:

```text
chi2 1S1L: 24663650.52746036
chi2 1S2L: 24656854.958780933
delta chi2: 6795.568679425865

BIC 1S1L: 24663747.812829815
BIC 1S2L: 24656984.67260687
delta BIC: 6763.140222944319

screen label: STRONG_1S2L_SCREEN
```

Runtime record:

```text
wall_seconds: 13.419444647966884
cpu_seconds:   8.308651621000001
cpu_hours:     0.0023079587836111115
```

Evidence report SHA-256:

```text
7fc2ff76071fae780947501a71f172f757111429beabd83715909114cc276f4f
```

## Scientific interpretation boundary

The large positive `delta chi2` and `delta BIC` establish that a close-topology point-source binary-lens model captures statistically significant structure that the locked 1S1L baseline does not. This is sufficient to advance `RMDC26_002050` to deeper binary-lens analysis.

It is **not** sufficient to declare the event a final 1S2L classification. The absolute chi-square remains extremely large relative to the number of photometric points, and the point-source 1S2L improvement is only a small fraction of the total baseline chi-square. The next analysis must determine whether the improvement is temporally/band localized in a physically coherent anomaly and whether finite-source treatment (`rho` with VBM/VBBL) materially changes the retained minimum.

The close solution (`s < 1`) must also be treated as a candidate minimum, not a unique topology. Close/resonant/wide degeneracies and alternative model families remain open until explicitly tested.

No physical companion label (planet, brown dwarf, stellar binary, etc.) is assigned from `q` alone at this stage.
