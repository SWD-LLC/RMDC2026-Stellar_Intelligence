# RMDC26 Stage 2 Execution Boundary

Stage 2 begins only after the deterministic 16-event canary selection and runtime/backend preflight have passed on Roman Research Nexus.

Current canary selection accounting:

- `16` unique events total
- `4` strongest-chi-square
- `3` coherent-run
- `3` high-p99
- `2` quality-boundary
- `4` moderate-ambiguous

Runtime/backend preflight established the production Nexus environment as Python `3.12.13` with `MulensModel==3.9.0`, `VBMicrolensing==5.5`, NumPy, pandas, SciPy, and Astropy available. The organizer binary-lens notebook was found locally and hashed before any Stage 2 higher-order model execution.

## First executable Stage 2 layer

The first higher-order execution is intentionally limited to a single real canary event selected from the `strongest_chi2` stratum. It is a **point-source 1S2L screening pilot**, not a final astrophysical classification.

The pilot must:

1. bind to the locked Stage 1 result table and deterministic canary CSV;
2. preserve the Stage 1 `t0`, `u0`, and `tE` solution as the comparison baseline;
3. use `MulensModel` for binary-lens magnification;
4. search close, resonant, and wide binary-lens topology regions in `s`;
5. search mass ratio `q` and trajectory angle `alpha` while retaining multiple local minima;
6. solve source/blend flux coefficients analytically per photometric band;
7. report `chi2`, `BIC`, delta-chi-square, delta-BIC, runtime, CPU time, and backend versions;
8. record `alpha` in MulensModel degrees internally and radians for submission-facing compatibility;
9. leave finite-source, parallax, orbital motion, binary-source, and astrometric terms disabled in this first screening layer;
10. mutate neither Stage 1 products nor any `microlens-submit` staging/submission artifact.

A strong point-source 1S2L improvement is evidence that the event warrants deeper binary-lens analysis; it is not by itself a final classification. Caustic-adjacent or otherwise unresolved fits must advance to finite-source/VBM analysis before scientific closure.

## Locked submission boundary

The previously verified Stage 1 submission ZIP remains immutable during Stage 2 research. Stage 2 results are developed as new evidence and do not silently rewrite or regenerate the locked Stage 1 package.
