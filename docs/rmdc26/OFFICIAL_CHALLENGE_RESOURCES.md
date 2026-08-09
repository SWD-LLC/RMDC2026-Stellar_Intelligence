# Official RMDC26 Challenge Resources

This page defines the organizer-maintained resources used as the source of truth for challenge mechanics, submission format, Nexus usage, and reference modeling workflows.

## Source hierarchy

For RMDC26 challenge-specific behavior, use the following precedence:

1. **Current organizer instructions / direct clarification**
2. **`microlens-submit` submission documentation and the installed package behavior actually used for the recorded submission transaction**
3. **RGES-PIT RMDC26 challenge and Nexus documentation**
4. **Official `rges-pit` notebook repositories**
5. **This repository's derived runbooks and implementation notes**

This project does not silently override an organizer-defined submission contract with a local convention.

## Official repositories

### Notebook and informational repository

https://github.com/rges-pit/data-challenge-notebooks

The Roman Nexus preloads duplicates of most challenge notebooks. The organizer documentation warns that the preloaded reference notebooks are read-only and that the reference directory is regularly replaced from its source repository. They may be executed, but project work should not be saved into that directory.

### Submission tool repository

https://github.com/rges-pit/microlens-submit

The recorded submission lifecycle in this project was contract-tested against `microlens-submit==0.17.9`.

### Submission documentation

https://microlens-submit.readthedocs.io/en/latest/

The challenge documentation explicitly states that strict adherence to the submission criteria is required because much of the evaluation process is automated.

## Submission guides

- CLI tutorial: https://microlens-submit.readthedocs.io/en/latest/cli_tutorial.html
- Python API: https://microlens-submit.readthedocs.io/en/latest/api.html
- Usage examples: https://microlens-submit.readthedocs.io/en/latest/usage_examples.html
- Manual submission format: https://microlens-submit.readthedocs.io/en/latest/submission_manual.html

The official tool is the preferred submission interface. The manual format is retained as an exact specification/reference, not as justification to bypass validation.

## Nexus-specific challenge notebooks

### Challenge workflow and submission creation

Public notebook:

https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20A:%20Nexus/Nexus_Workflow.ipynb

Nexus/RGES-PIT page:

https://rges-pit.org/data-challenge/aas-workshop/notebooks/workflow/

Use this as the primary organizer reference for the end-to-end challenge workflow and submission construction.

### Single-lens fitting and full-season pipeline demonstration

Public notebook:

https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20B:%20Single%20Lens%20%26%20Pipelines/Single_Lens_Pipeline.ipynb

Nexus/RGES-PIT page:

https://rges-pit.org/data-challenge/aas-workshop/notebooks/pipeline/

This is the closest official notebook analogue to the high-throughput Stage 1 PSPL/1S1L baseline layer in this repository. It is a reference workflow, not the source code of the Stellar Intelligence fitter.

### Binary-lens fitting approaches

Public notebook:

https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20C:%20Binary%20Lens/Fitting_Binary_Lenses.ipynb

Nexus/RGES-PIT page:

https://rges-pit.org/data-challenge/aas-workshop/notebooks/binary/

The organizer workshop demonstrates three common binary-lens starting strategies: uninformed initialization, grid search, and informed initialization, and discusses degeneracies, stochastic likelihood structure, parallelization, and higher-order effects. This is a required methodological reference for planning the next modeling layer for Stage 1 anomalous events.

### Microlensing open-source tools

Public notebook:

https://github.com/rges-pit/data-challenge-notebooks/blob/main/Extras/Microlensing_Tools.ipynb

Nexus/RGES-PIT page:

https://rges-pit.org/data-challenge/aas-workshop/notebooks/microlensing_tools/

Use this to survey organizer-supported/open-source modeling tools before introducing a new dependency into the higher-order pipeline.

## Nexus reference-directory rule

Organizer guidance for the preloaded reference content is operationally important:

- reference notebooks can execute;
- the notebooks are read-only;
- do not save project notebooks into the reference directory;
- the reference content is regularly replaced from its source repository, so local changes there are not durable.

Accordingly, reproducible project artifacts belong in the project repository/workspace, while organizer reference notebooks remain external references.

## Environment files

The official notebook repository includes environment/dependency files such as `env.yml` and `requirements.txt`. On the organizer-provided `RGES PIT Nexus` image, the expected challenge kernel is already available, so recreating the environment is normally unnecessary.

For this repository, historical execution facts are not retroactively rewritten to match a generic environment file. The completed Stage 1 and submission transaction retain the exact runtime facts recorded at execution time; official environment files are used as compatibility/reference material.

## Challenge ground rules relevant to repository publication

The RMDC26 challenge page requires teams to document dependencies and CPU hours, publish developed code as documented open source, pass format validation with the submission tool, and designate a team lead/contact. It also asks participants to classify targets, fit appropriate microlensing models, describe their modeling/software/hardware approach, and document innovations.

These requirements are why this repository separately exposes:

- production fitting code;
- synthetic tests;
- measured compute and hardware metadata;
- scientific-scope boundaries;
- submission lifecycle evidence;
- source/provenance rules;
- rubric alignment.

## Local-reference rule

A local clone or Nexus-preloaded copy of an official notebook is treated as a **reference dependency**, not as project-owned source. If organizer code is adapted into project code later, the adapted file must carry explicit attribution and a clear statement of what changed.
