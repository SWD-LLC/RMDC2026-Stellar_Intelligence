# RMDC26 Scientific Scope and Interpretation Boundary

This document states exactly what the currently exported RMDC26 package represents scientifically, and equally importantly, what it does **not** represent.

## What was completed

A full Stage 1 photometric 1S1L/PSPL baseline was fit across all 2,079 Experienced-tier targets.

- 2,078 events produced model-bearing 1S1L solutions.
- 1 event (`RMDC26_001563`) was preserved as a data-quality-only record because no valid unsaturated Stage 1 photometry remained.
- 1,148 model-bearing events passed the Stage 1 residual thresholds and were routed as `1S1L_candidate`.
- 930 model-bearing events showed residual evidence sufficient to route them as `anomalous_route`.

All 2,078 model-bearing Stage 1 solutions were later placed through the controlled submission lifecycle and were present in the verified local export archive.

## What `anomalous_route` means

`anomalous_route` does **not** mean the event has been physically classified as a binary lens, planetary lens, triple lens, binary source, parallax event, orbital-motion event, finite-source event, or another higher-order class.

It means that the Stage 1 PSPL baseline leaves residual structure that crosses one or more documented routing thresholds and therefore warrants more expressive modeling or expert review.

## Experienced-tier model complexity

The organizer's Experienced-tier specification includes substantially more complexity than a pure 1S1L population. The challenge design includes single-, binary-, and triple-lens cases and multiple higher-order effects. Therefore a Stage 1 PSPL fit to an event routed as anomalous should be interpreted as a **baseline solution and triage result**, not as evidence that the correct generative model is 1S1L.

## Current exported ZIP boundary

The locally verified export contains 2,078 active Stage 1 1S1L solution records. It passed the submission-tool schema and integrity checks, but schema validity is not the same thing as demonstrating that the most appropriate physical model has been fit for every complex Experienced-tier event.

This distinction is intentionally public because the evaluation rubric scores parameter accuracy and modeling complexity, not merely file-format validity.

## Downstream modeling status

Stage 2 higher-order fitting was not part of the completed Stage 1 execution documented here. The 930-event anomalous queue was identified specifically so higher-order work could be prioritized rather than hidden behind an apparently successful PSPL optimizer result.

Accordingly:

- the current export is a technically valid, fully audited **Stage 1 baseline submission package**;
- it is not represented here as a completed higher-order physical classification of all Experienced-tier events;
- external submission should be treated as a separate scientific decision from technical package validity.

## Why preserve the baseline package

The Stage 1 package remains valuable even if additional modeling is performed later because it provides:

- complete baseline coverage;
- deterministic reference solutions;
- anomaly-routing evidence;
- per-event runtime and fit diagnostics;
- a reproducible point against which more expressive models can be compared;
- a cryptographically locked submission artifact that should not be silently mutated after validation.

Any later higher-order submission should be versioned as a new scientific artifact rather than rewriting the historical Stage 1 record.

## Interpretation rule

Throughout this repository:

> **Format-valid** means the submission artifact satisfies the tested `microlens-submit` contract. **Scientifically complete** would require the appropriate physical modeling/classification demanded by the Experienced-tier event complexity. These are different claims and are not conflated.
