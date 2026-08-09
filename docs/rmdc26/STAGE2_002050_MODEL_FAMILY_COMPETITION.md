# RMDC26_002050 — 1S2L vs 2S1L model-family competition

This note records the event-season point-source model-family competition for `RMDC26_002050`. It is a Stage 2 scientific screening result, not yet a final physical classification.

## Bound inputs

- Local 1S2L refinement report SHA-256: `377430ebfd720ab75f3995734db073ff92a534143d3f0f4c3299042e51c28047`
- 2S1L competition report SHA-256: `04ed59dfca5a4a34b08bc1fa6d9ca5978c2e59aa14212eae7d7157e860e63aa2`
- Event season: 8,185 valid points in F087/F146/F213
- Prior reproduction: PASS for both 1S1L and 1S2L

## Model comparison

```text
1S1L chi2 = 20526.65658494264
1S2L chi2 =  8521.260530246143
2S1L chi2 =  8766.360882056826

1S1L BIC = 20607.747111350887
1S2L BIC =  8629.381232123806
2S1L BIC =  8892.5017009141

2S1L - 1S2L chi2 = +245.1003518106827
2S1L - 1S2L BIC  = +263.12046879029367
```

The point-source `1S2L` model is therefore strongly preferred over the tested `2S1L` binary-source model family on the same event season.

## Best 2S1L competitor

```text
t01 = 2462938.753572969
u01 = 0.2323014297692422
t02 = 2462940.352954616
u02 = 0.3401097797217103
tE  = 17.949663343589403 d
```

The secondary source remained positive in all three bands. The fitted source-flux ratios were:

```text
F087 Fs2/Fs1 = 1.3485762219953505
F146 Fs2/Fs1 = 0.36380827249613573
F213 Fs2/Fs1 = 0.36294137876978516
```

Thus the 2S1L family did not fail by collapsing to a single-source solution; it produced a viable binary-source competitor that was nevertheless substantially worse than 1S2L under both chi-square and BIC.

## Current scientific interpretation

The current evidence hierarchy is:

1. Stage 1 1S1L fit routes `RMDC26_002050` as anomalous.
2. Event-local point-source 1S2L strongly improves the fit.
3. Close topology is strongly preferred over resonant and wide alternatives.
4. A flexible 2S1L binary-source model improves over 1S1L but remains disfavored relative to 1S2L by `Delta BIC = +263.12` in the `2S1L - 1S2L` direction.

This establishes `1S2L` as the current provisional model-family winner. It does **not** yet establish a final physical binary-lens solution, because finite-source necessity, caustic proximity, higher-order effects, and long-baseline residual structure have not been fully closed.

## Next gate

Before adding `rho`, run a caustic-proximity / finite-source-necessity diagnostic on the close 1S2L solution. Only if the source trajectory approaches or crosses a caustic closely enough to make finite-source effects physically or statistically relevant should the workflow promote to VBM/VBBL finite-source refinement.

## Protected-state boundary

The Stage 1 parquet/CSV/manifest and the verified submission ZIP remained byte-identical before and after the 2S1L competition. No submission artifact was regenerated or modified.
