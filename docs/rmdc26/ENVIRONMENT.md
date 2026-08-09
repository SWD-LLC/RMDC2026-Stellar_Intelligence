# RMDC26 Compute Environment and Reproducibility Record

This page separates **exactly recorded runtime facts** from the organizer-maintained challenge environment. They are related, but they are not interchangeable.

## Exact recorded production environment

```text
Execution platform: Roman Research Nexus
Conda/environment label: RomanNexus-2026.1
Python: 3.12.13
Python executable: /opt/conda/envs/RomanNexus-2026.1/bin/python
microlens-submit: 0.17.9
microlens-submit module location: /home/swa417/.local/lib/python3.12/site-packages
working CLI invocation: python -m microlens_submit.cli
```

Final submission hardware metadata:

```text
platform: Linux-6.12.94-123.190.amzn2023.x86_64-x86_64-with-glibc2.39
os: Linux
cpu_details: Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
memory_gb: 15.34
nexus_image: 378083651696.dkr.ecr.us-east-1.amazonaws.com/roman:RomanNexus-2026.1
```

Stage 1 execution controls:

```text
threads: 4
DuckDB memory limit: 4GB
checkpoint interval: 25
run ID: rmdc26_stage1_v022_full_20260804T230001Z
```

## Measured compute

```text
Wall time: 5920.372 seconds = 1.644548 hours
User CPU: 5846.498 seconds = 1.624027 CPU-hours
System CPU: 33.235 seconds = 0.009232 CPU-hours
Total measured CPU: 5879.733 seconds = 1.633259 CPU-hours
Reported CPU utilization: 99.31%
```

These are measured values from the production Stage 1 run, not reconstructed estimates.

## Stage 1 Python dependencies

The production fitter imports:

```text
duckdb
numpy
pandas
scipy
```

Parquet I/O in the documented environment also used PyArrow support.

The exact runtime versions of NumPy, pandas, DuckDB, and SciPy were written by the Stage 1 script into its generated run manifest. They are not guessed here where an exact version has not yet been copied into the public record.

## Official organizer environment reference

The official `rges-pit/data-challenge-notebooks` repository currently publishes an `env.yml` named `rges-pit-dc`. Its pinned/declared scientific stack includes:

```text
python=3.11
numpy==1.26.0
scipy==1.11.3
pandas==2.1.3
matplotlib==3.8.0
emcee==3.1.4
corner==2.2.2
astropy==5.3.4
astroquery==0.4.6
ipykernel==6.25.2
ipython==8.16.1
ipywidgets==8.1.1
jupyter_client==8.3.1
jupyter_core==5.3.2
microlens-submit>=0.17.8
```

The same environment also includes or installs challenge-relevant packages such as:

```text
BAGLE
VBMicrolensing
MulensModel==3.4.0
pyLIMA
RTModel
eesunhong
scikit-optimize
scikit-learn
nbi
joblib
numba
pathos
s3fs
```

The official `requirements.txt` likewise lists the core numerical stack plus microlensing packages including MulensModel, VBMicrolensing, RTModel, BAGLE, and pyLIMA.

Authoritative files:

- https://github.com/rges-pit/data-challenge-notebooks/blob/main/env.yml
- https://github.com/rges-pit/data-challenge-notebooks/blob/main/requirements.txt

## Why the two environments are not collapsed

The completed Stage 1 production run used the recorded `RomanNexus-2026.1` / Python 3.12.13 environment. The organizer reference environment currently specifies Python 3.11 and a different explicit dependency set. Rewriting the historical execution record to match the organizer file would therefore be false provenance.

Use the distinction this way:

- **recorded production environment** = what actually executed the locked Stage 1 and submission transaction;
- **official organizer environment** = compatibility/reference environment for reproducing workshop notebooks and designing future challenge work;
- **public CI environment** = lightweight synthetic verification environment defined by `requirements-rmdc26.txt` and GitHub Actions.

## Higher-order modeling dependency policy

The official environment confirms that the challenge ecosystem anticipates several mature microlensing packages. Before Stage 2 chooses a modeling backend, the official binary-lens and tools notebooks should be reviewed and a representative canary should compare candidate packages for:

- model coverage;
- parameter conventions;
- numerical stability;
- binary-lens magnification performance;
- higher-order-effect support;
- parallelization characteristics;
- licensing and reproducibility;
- compatibility with the active Nexus environment.

A package being present in the organizer environment does not automatically make it the project backend. The backend decision must be explicit and benchmarked.

## Submission-tool dependency boundary

`microlens-submit==0.17.9` was the version actually tested for:

- CLI discovery;
- persistent CSV import behavior;
- default activation behavior;
- deactivation lifecycle;
- solution validation;
- event validation;
- submission validation;
- hardware metadata persistence;
- final export.

The submission workflow should therefore be interpreted against that version, rather than against an unspecified future version of the package.

## Nexus context

The RMDC26 Nexus documentation lists standard server profiles with combinations including small (2 vCPU / 16 GB), medium (8 vCPU / 16 GB), large CPU-optimized (32 vCPU / 64 GB), and large memory-optimized (16 vCPU / 128 GB). The hardware values recorded above are the values detected from the actual submission environment and persisted into the submission metadata; they should not be replaced by a generic profile label after the fact.

The organizer also states that the `RGES PIT Nexus` image includes the challenge kernel, so recreating the environment from `env.yml` is generally unnecessary when using that image.

## Reproducibility policy

1. Do not invent missing package versions.
2. Prefer generated runtime manifests over retrospective environment guesses.
3. Preserve the challenge dataset path as a reference rather than redistributing challenge data.
4. Keep scientific fit code and submission-tool lifecycle code conceptually separate.
5. Record exact package/tool versions whenever behavior depends on implementation semantics.
6. Treat measured CPU/wall-time as part of the scientific submission evidence.
7. Keep historical runtime facts distinct from organizer-maintained reference environments.
8. Recheck the official environment and submission package versions before any future higher-order bulk run or export.
