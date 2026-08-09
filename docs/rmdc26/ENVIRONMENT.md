# RMDC26 Compute Environment and Reproducibility Record

This page separates **exactly recorded runtime facts** from dependency names that were present in the Stage 1 workflow but whose exact package version was not copied into this public document.

## Exact recorded environment

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

The exact runtime versions of NumPy, pandas, DuckDB, and SciPy were written by the Stage 1 script into its generated run manifest. They are not guessed here where an exact version has not been copied into the public record yet.

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

## Reproducibility policy

1. Do not invent missing package versions.
2. Prefer generated runtime manifests over retrospective environment guesses.
3. Preserve the challenge dataset path as a reference rather than redistributing challenge data.
4. Keep scientific fit code and submission-tool lifecycle code conceptually separate.
5. Record exact package/tool versions whenever behavior depends on implementation semantics.
6. Treat the measured CPU/wall-time record as part of the scientific submission evidence.
