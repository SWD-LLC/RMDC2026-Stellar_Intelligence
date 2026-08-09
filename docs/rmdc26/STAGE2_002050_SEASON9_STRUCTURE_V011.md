# RMDC26_002050 — Season 9 Structure v0.1.1 Corrected

This note records the corrected Season 9 temporal-structure decomposition for `RMDC26_002050`. It supersedes the v0.1.0 window-timing interpretation while preserving the valid cross-band statistics from that run.

## Evidence binding

- v0.1.0 structure report SHA-256: `8302c180b98353d1a5ef8c929211c2f5d41198a776aafacf7c68dc3e006ccb5f`
- following-season diagnostic SHA-256: `9f4aa4f6c57f448349e7e98d5b8e1dc6265d45e866bca2b1d5bb8059642ddd8a`
- corrected v0.1.1 report SHA-256: `d69a9652e868f96c5ff77ffd6f95c07ca467f1458435b9d0a74d1dcde7e35b29`

## Absolute-time repair

The corrected 0.5-day bin origin is BJD `2463093.5`. The six selected 5-day windows map to absolute BJD as follows:

1. `2463126.0–2463131.0`
2. `2463121.0–2463126.0`
3. `2463131.0–2463136.0`
4. `2463159.5–2463164.5`
5. `2463094.0–2463099.0`
6. `2463154.5–2463159.5`

The touching windows merge into three broader high-excess episodes:

- Episode 1: `2463094.0–2463099.0` (5 d), 7.61% of F146+F213 excess
- Episode 2: `2463121.0–2463136.0` (15 d), 53.09% of F146+F213 excess
- Episode 3: `2463154.5–2463164.5` (10 d), 16.19% of F146+F213 excess

All three exceed the 5% engineering threshold used by this diagnostic.

## Cross-band coherence

The valid v0.1.0 coherence statistics remain:

- Pearson F146/F213: `0.9997721485225378`
- Spearman F146/F213: `0.9995844318334152`
- same-sign fraction: `0.9928057553956835`
- high-excess same-sign fraction: `1.0`

The corrected episode-level signs are also consistent between F146 and F213:

- Episode 1: both strongly negative
- Episode 2: both strongly positive
- Episode 3: both strongly negative

F087 is sampled in every episode but remains near the noise floor, with only order-10 excess chi-square in each episode while F146/F213 contribute hundreds of thousands to millions.

## Corrected diagnostic gate

```text
CORRECTED_STRUCTURE_DECISION: MULTIPLE_COHERENT_HIGH_EXCESS_EPISODES
MERGED_EPISODE_COUNT: 3
MAJOR_EPISODE_COUNT_GE_5PCT: 3
```

This is a diagnostic label, not a physical classification. It establishes that Season 9 contains three broad, strongly coherent F146/F213 episodes with alternating sign (negative → positive → negative), while F087 remains effectively quiet at its cadence/SNR.

## Interpretation boundary

The pattern is inconsistent with treating Season 9 as one isolated short excursion. It also should not yet be labeled parallax, orbital motion, a second microlensing event, stellar variability, or detector/systematics.

The next diagnostic should test whether the F146/F213 variability is consistent with a single shared color vector and whether that color vector matches the source-flux color of the Season 8 1S2L solution. Cross-season recurrence should also be measured before fitting another physical model.

No new astrophysical model was fitted. Stage 1 products and the locked export remained byte-identical.