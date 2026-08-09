# RMDC26 Modeling Roadmap

This document describes the next scientific modeling layer after the completed Stage 1 PSPL/1S1L baseline. It is a roadmap only; it does not claim that Stage 2 has already been executed.

## Starting state

The completed Stage 1 pass produced:

```text
Experienced-tier targets: 2079
Model-bearing Stage 1 solutions: 2078
1S1L_candidate: 1148
anomalous_route: 930
data_quality_route: 1
```

The 930-event anomalous queue is the primary scientific worklist for higher-order model selection and fitting.

## Organizer references for the next phase

The next-phase design should be anchored to the official RGES-PIT workshop material rather than invented in isolation.

### Single-lens pipeline reference

https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20B:%20Single%20Lens%20%26%20Pipelines/Single_Lens_Pipeline.ipynb

Use this to compare Stage 1 assumptions, anomaly-finding strategy, priors, parallelization, and single-lens pipeline conventions.

### Binary-lens fitting reference

https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20C:%20Binary%20Lens/Fitting_Binary_Lenses.ipynb

The organizer workshop explicitly demonstrates multiple binary-lens initialization strategies and discusses grid searches, informed/uninformed starting points, degeneracies, stochastic likelihood structure, parallelization, and higher-order effects. That notebook should be reviewed before freezing a Stage 2 binary-lens implementation.

### Tooling survey reference

https://github.com/rges-pit/data-challenge-notebooks/blob/main/Extras/Microlensing_Tools.ipynb

Use this before adding new microlensing dependencies so the pipeline prefers mature open-source tools where appropriate.

## Proposed Stage 2 sequence

A conservative higher-order workflow is:

```text
Stage 1 anomalous_route
        |
        v
residual morphology / quality review
        |
        +--> likely binary-lens morphology
        |
        +--> possible finite-source / high-magnification structure
        |
        +--> long-timescale / asymmetry candidate
        |
        +--> ambiguous / low-information residual structure
        |
        v
model-family candidate set
        |
        v
coarse or grid search where required
        |
        v
local/stochastic refinement
        |
        v
compare against Stage 1 baseline
        |
        v
retain competing degeneracies when materially indistinguishable
        |
        v
submission-tool validation as a new versioned scientific artifact
```

## Model-family escalation rule

Do not infer a physical class solely from a Stage 1 residual threshold. Stage 1 identifies where 1S1L is inadequate; Stage 2 must establish whether a more expressive model is actually supported.

Candidate model families may include, where justified by the event and challenge specification:

- binary lens (`2L1S`);
- triple lens or other more complex lens configurations;
- binary source (`1L2S`) where supported;
- finite-source effects;
- parallax;
- lens/source orbital motion;
- combinations of higher-order effects.

The exact model vocabulary and parameter contract must be checked against the current `microlens-submit` specification before implementation.

## Prioritization strategy

The 930-event queue should not be treated as a flat batch. Prioritize using Stage 1 evidence already available:

1. strongest residual significance / longest coherent residual runs;
2. largest improvement opportunity relative to the Stage 1 baseline;
3. events with stable Stage 1 geometry but localized residual structure;
4. events with boundary-convergence or flux-quality flags requiring model-quality review;
5. ambiguous cases that may need morphology clustering or manual inspection before expensive fitting.

This order is intended to maximize scientific gain per CPU hour while preserving difficult/ambiguous events for later attention rather than discarding them.

## Compute controls

Higher-order modeling can be much more expensive than Stage 1. Before launching a bulk Stage 2 run:

- benchmark a small representative canary set;
- measure wall time and CPU time by model family;
- determine whether grid search, stochastic sampling, or deterministic local optimization dominates cost;
- explicitly cap parallelism to the Nexus allocation in use;
- checkpoint per event/model candidate;
- retain failed fits and optimizer diagnostics;
- avoid generating posterior samples for every candidate unless they materially improve the evaluation objective.

The RMDC26 evaluation rubric explicitly considers computational efficiency, including anomaly detection/categorization efficiency and the balance between finding solutions and collecting posteriors.

## Comparison contract

Every Stage 2 candidate should be compared against its locked Stage 1 baseline using a documented metric set. At minimum preserve:

- event ID;
- Stage 1 solution ID / baseline parameters;
- candidate model family;
- candidate parameters;
- log likelihood or equivalent fit statistic;
- change in fit statistic relative to Stage 1;
- parameter-boundary state;
- optimizer/sampler convergence state;
- runtime / CPU cost;
- degeneracy label or competing-solution relationship where applicable;
- evidence supporting model escalation.

A higher-order model should not replace the baseline merely because it is more flexible; the evidence for the additional complexity must be inspectable.

## Submission versioning

The already verified Stage 1 ZIP is a historical artifact and must remain immutable.

If Stage 2 produces scientifically improved solutions, create a **new** submission project/version and repeat the controlled validation chain rather than editing the locked Stage 1 export in place.

## Gate before execution

Before a full Stage 2 execution, the repository should contain:

- a reviewed model-family contract based on current organizer specifications;
- a small synthetic/known-case regression suite;
- a representative real-event canary plan;
- measured resource estimates;
- a failure/recovery policy;
- a submission mapping plan for every higher-order model family in scope.

Only after those controls are explicit should the 930-event anomalous queue be launched at scale.
