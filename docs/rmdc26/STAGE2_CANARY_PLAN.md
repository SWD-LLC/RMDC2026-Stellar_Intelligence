# RMDC26 Stage 2 Canary Plan

## Purpose

Stage 2 begins from the 930 Stage 1 events routed as `anomalous_route`. The objective is to test higher-order modeling strategy on a small, representative set before committing significant Roman Nexus compute to the entire anomaly queue.

Stage 1 routing is evidence that the baseline `1S1L` model is inadequate or suspicious for an event; it is **not** itself a physical model classification.

## Canary size

Initial target:

```text
16 unique anomalous events
```

The selector is implemented in:

```text
scripts/select_rmdc26_stage2_canary_v010.py
```

It is deterministic and read-only with respect to Stage 1.

## Evidence strata

The canary intentionally spans several regimes instead of taking only the numerically worst fits.

Default 16-event allocation:

```text
strongest_chi2       4
coherent_run         3
high_p99             3
quality_boundary     2
moderate_ambiguous   4
```

### `strongest_chi2`

High reduced chi-square events test obvious baseline-model failure and give Stage 2 a high-signal regime in which a more expressive model should demonstrate measurable improvement.

### `coherent_run`

Events with long contiguous residual runs test whether temporally coherent departures are better explained by binary/higher-order structure rather than isolated noise excursions.

### `high_p99`

Events with extreme 99th-percentile absolute residuals test localized high-significance deviations.

### `quality_boundary`

Events carrying parameter-boundary or flux-quality flags test failure modes where Stage 1 geometry or flux decomposition may be unstable. These events must not be automatically promoted to a more complex physical interpretation; Stage 2 must determine whether the issue is modeling or data/optimization quality.

### `moderate_ambiguous`

Events near the middle of the anomaly-evidence distribution prevent the canary from being biased toward only extreme, easy-to-detect failures. This stratum is important for evaluating classification efficiency and false-positive behavior.

## Stage 2 modeling order

For each selected event:

1. reload the locked Stage 1 baseline and its diagnostics;
2. inspect residual morphology and data-quality flags;
3. define a justified candidate model-family set;
4. benchmark initialization strategy and runtime on the event;
5. fit candidate models using organizer-supported conventions/tools where appropriate;
6. compare every candidate against the locked Stage 1 baseline;
7. retain materially competitive degeneracies rather than forcing a single interpretation;
8. record wall time, CPU time, convergence state, and failure diagnostics;
9. make no changes to the locked Stage 1 export.

## Candidate model families

Candidate families may include, where justified and supported by the current submission specification:

- `1S2L` — one source, two lenses;
- `2S1L` — two sources, one lens;
- finite-source extensions;
- parallax;
- orbital-motion extensions;
- other higher-order combinations supported by the challenge contract.

The exact `model_type`, `model_tags`, required parameters, and units must be checked against the installed/current `microlens-submit` specification before any submission mapping is frozen.

## Comparison record

Every Stage 2 attempt must preserve at minimum:

```text
event_id
Stage 1 baseline identifier / parameters
candidate model family
candidate parameters
fit statistic / log likelihood
change relative to Stage 1
parameter-boundary state
optimizer or sampler convergence state
runtime seconds
CPU seconds / CPU hours where measurable
initialization strategy
degeneracy relationship
failure reason, if any
model-escalation rationale
```

A model should not replace Stage 1 merely because it has more degrees of freedom.

## Compute gates

Before full-scale Stage 2 execution:

- measure per-event wall and CPU time on the canary;
- record memory pressure and parallelism;
- determine whether grid search, local optimization, or stochastic sampling dominates cost;
- quantify success/failure rate by evidence stratum;
- identify model families that are too expensive for indiscriminate use;
- checkpoint per event and candidate model;
- preserve failed runs and diagnostics.

## Stop conditions

Do not proceed to bulk Stage 2 if any of the following occurs:

- Stage 1 baseline files or hashes change;
- the locked Stage 1 submission ZIP is modified or regenerated in place;
- selected canary IDs are not unique;
- a selected row is not `anomalous_route` + `fit_success`;
- model-family parameter mapping is not compliant with the current challenge submission specification;
- higher-order code cannot reproduce synthetic/known-case tests;
- runtime or memory behavior is uncontrolled;
- fit failures are being silently discarded;
- model escalation is based only on Stage 1 route labels without fit evidence.

## Success gate

A successful canary should produce:

1. deterministic event selection;
2. reproducible model-family initialization;
3. measured compute per candidate family;
4. inspectable fit-improvement evidence;
5. explicit degeneracy handling;
6. zero mutation of the locked Stage 1 scientific and submission artifacts;
7. a clear decision about which model families and search strategies are safe to scale to the 930-event queue.
